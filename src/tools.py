import json
import os
import base64
import requests
from langchain.tools import tool
from PIL import Image
from io import BytesIO
from typing import List, Optional
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

# Configure Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

# Helper function to get the best available model
def get_best_vision_model():
    """Find and return the best available Gemini vision model"""
    # Try to list available models and find one that supports generateContent
    try:
        available_models = genai.list_models()
        for model in available_models:
            # Check if model supports generateContent
            if 'generateContent' in model.supported_generation_methods:
                model_name = model.name.replace('models/', '')
                logger.info(f"✓ Found available model: {model_name}")
                return genai.GenerativeModel(model_name)
    except Exception as e:
        logger.warning(f"Could not list models: {str(e)}")
    
    # Fallback to hardcoded list if listing fails
    model_priority = [
        'gemini-2.0-flash',
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-pro',
        'gemini-pro-vision',
    ]
    
    for model_name in model_priority:
        try:
            model = genai.GenerativeModel(model_name)
            logger.info(f"✓ Using model: {model_name}")
            return model
        except Exception as e:
            logger.debug(f"Model {model_name} not available: {str(e)}")
            continue
    
    raise Exception("No compatible Gemini vision models available. Check your API key and enabled APIs.")


class ExtractIngredientsTool():
    @staticmethod
    def extract_ingredient_direct(image_input: str):
        """
        Direct function to extract ingredients (without LangChain tool wrapper)
        
        :param image_input: The image file path (local) or URL (remote).
        :return: A list of ingredients extracted from the image.
        """
        try:
            logger.info(f"Loading image from: {image_input}")
            
            # Load image
            if image_input.startswith("http"):
                response = requests.get(image_input)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
            else:
                if not os.path.isfile(image_input):
                    raise FileNotFoundError(f"No file found at path: {image_input}")
                img = Image.open(image_input)

            logger.info("Image loaded successfully")
            
            # Get the best available model
            model = get_best_vision_model()
            
            # Create prompt
            prompt = """Analyze this image and extract all the ingredients or food items you can see.
            List each ingredient on a new line. Be specific and detailed.
            Only list the ingredients, nothing else."""
            
            logger.info("Sending request to Gemini API...")
            
            # Generate response
            response = model.generate_content([prompt, img])
            
            logger.info(f"✓ Gemini response received: {response.text[:100]}...")
            return response.text
            
        except Exception as e:
            logger.error(f"Error in extract_ingredient: {str(e)}")
            raise Exception(f"Failed to extract ingredients: {str(e)}")

    @tool("Extract ingredients")
    def extract_ingredient(image_input: str):
        """
        Extract ingredients from a food item image using Google Gemini Vision.
        
        :param image_input: The image file path (local) or URL (remote).
        :return: A list of ingredients extracted from the image.
        """
        return ExtractIngredientsTool.extract_ingredient_direct(image_input)


class FilterIngredientsTool:
    @staticmethod
    def filter_ingredients_direct(raw_ingredients: str) -> List[str]:
        """
        Direct function to filter ingredients (without LangChain tool wrapper)
        
        :param raw_ingredients: Raw ingredients as a string.
        :return: A list of cleaned and relevant ingredients.
        """
        try:
            logger.info(f"Filtering ingredients from: {raw_ingredients[:100]}...")
            
            # Split by newlines and commas, clean up
            ingredients = []
            for line in raw_ingredients.split('\n'):
                # Remove numbering, bullets, and extra whitespace
                cleaned = line.strip().lstrip('0123456789.-*• ').strip()
                if cleaned and len(cleaned) > 2:  # Ignore very short items
                    ingredients.append(cleaned.lower())
            
            # Remove duplicates while preserving order
            seen = set()
            unique_ingredients = []
            for item in ingredients:
                if item not in seen:
                    seen.add(item)
                    unique_ingredients.append(item)
            
            logger.info(f"✓ Filtered to {len(unique_ingredients)} ingredients: {unique_ingredients}")
            return unique_ingredients
            
        except Exception as e:
            logger.error(f"Error in filter_ingredients: {str(e)}")
            return []

    @tool("Filter ingredients")
    def filter_ingredients(raw_ingredients: str) -> List[str]:
        """
        Processes the raw ingredient data and filters out non-food items or noise.
        
        :param raw_ingredients: Raw ingredients as a string.
        :return: A list of cleaned and relevant ingredients.
        """
        return FilterIngredientsTool.filter_ingredients_direct(raw_ingredients)


class DietaryFilterTool:
    @staticmethod
    def filter_based_on_restrictions_direct(ingredients: List[str], dietary_restrictions: Optional[str] = None) -> List[str]:
        """
        Direct function to filter by dietary restrictions (without LangChain tool wrapper)

        :param ingredients: List of ingredients.
        :param dietary_restrictions: Dietary restrictions (e.g., vegan, gluten-free). Defaults to None.
        :return: Filtered list of ingredients that comply with the dietary restrictions.
        """
        try:
            # If no dietary restrictions are provided, return the original ingredients
            if not dietary_restrictions or dietary_restrictions.strip() == "":
                logger.info("No dietary restrictions provided, returning all ingredients")
                return ingredients

            logger.info(f"Filtering {len(ingredients)} ingredients for: {dietary_restrictions}")
            
            # Get the best available model
            model = get_best_vision_model()

            # Create a prompt for filtering
            prompt = f"""You are an AI nutritionist specialized in dietary restrictions.

Given the following list of ingredients:
{', '.join(ingredients)}

And the dietary restriction: {dietary_restrictions}

Please remove any ingredient that does NOT comply with this dietary restriction.
Return ONLY the compliant ingredients as a comma-separated list with no additional text, commentary, or explanation.
If an ingredient is uncertain, include it.

Compliant ingredients:"""

            # Generate response
            response = model.generate_content(prompt)
            filtered_text = response.text.strip()
            
            # Parse the response
            filtered_list = [item.strip().lower() for item in filtered_text.split(',') if item.strip()]
            
            logger.info(f"✓ Filtered to {len(filtered_list)} compliant ingredients: {filtered_list}")
            return filtered_list if filtered_list else ingredients
            
        except Exception as e:
            logger.error(f"Error in filter_based_on_restrictions: {str(e)}")
            return ingredients  # Return original if filtering fails

    @tool("Filter based on dietary restrictions")
    def filter_based_on_restrictions(ingredients: List[str], dietary_restrictions: Optional[str] = None) -> List[str]:
        """
        Uses Google Gemini to filter ingredients based on dietary restrictions.

        :param ingredients: List of ingredients.
        :param dietary_restrictions: Dietary restrictions (e.g., vegan, gluten-free). Defaults to None.
        :return: Filtered list of ingredients that comply with the dietary restrictions.
        """
        return DietaryFilterTool.filter_based_on_restrictions_direct(ingredients, dietary_restrictions)

    
class NutrientAnalysisTool():
    @staticmethod
    def analyze_image_direct(image_input: str):
        """
        Direct function to analyze nutrition (without LangChain tool wrapper)
        
        :param image_input: The image file path (local) or URL (remote).
        :return: A string with nutrient breakdown and estimated calorie information.
        """
        try:
            logger.info(f"Analyzing nutrition from image: {image_input}")
            
            # Load image
            if image_input.startswith("http"):
                response = requests.get(image_input)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
            else:
                if not os.path.isfile(image_input):
                    raise FileNotFoundError(f"No file found at path: {image_input}")
                img = Image.open(image_input)

            logger.info("Image loaded, getting model...")
            
            # Get the best available model
            model = get_best_vision_model()
            
            # Detailed nutritionist prompt
            prompt = """You are an expert nutritionist. Analyze the food in this image and provide a detailed nutritional assessment using the following format:

1. **Identification**: List each identified food item clearly, one per line.

2. **Portion Size & Calorie Estimation**: For each identified food item, specify the portion size and provide an estimated number of calories. Use bullet points:
   - **[Food Item]**: [Portion Size], [Number of Calories] calories

3. **Total Calories**: Provide the total number of calories for all food items.
   Total Calories: [Number]

4. **Nutrient Breakdown**: Include key nutrients:
   - **Protein**: [Food contributions] = [Total]
   - **Carbohydrates**: [Food contributions] = [Total]
   - **Fats**: [Food contributions] = [Total]
   - **Vitamins**: List key vitamins with %DV
   - **Minerals**: List key minerals with amounts

5. **Health Evaluation**: Evaluate the healthiness of the meal in one paragraph.

6. **Disclaimer**: 
The nutritional information and calorie estimates provided are approximate and are based on general food data. 
Actual values may vary depending on factors such as portion size, specific ingredients, preparation methods, and individual variations. 
For precise dietary advice or medical guidance, consult a qualified nutritionist or healthcare provider."""

            logger.info("Sending nutrition analysis request to Gemini...")
            
            # Generate response
            response = model.generate_content([prompt, img])
            
            logger.info("✓ Nutrition analysis completed")
            return response.text
            
        except Exception as e:
            logger.error(f"Error in analyze_image: {str(e)}")
            raise Exception(f"Failed to analyze nutrition: {str(e)}")

    @tool("Analyze nutritional values and calories of the dish from uploaded image")
    def analyze_image(image_input: str):
        """
        Provide a detailed nutrient breakdown and estimate the total calories using Google Gemini Vision.
        
        :param image_input: The image file path (local) or URL (remote).
        :return: A string with nutrient breakdown and estimated calorie information.
        """
        return NutrientAnalysisTool.analyze_image_direct(image_input)