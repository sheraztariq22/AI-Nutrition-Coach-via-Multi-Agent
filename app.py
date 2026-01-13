import gradio as gr
import base64
import time
import os
import logging
from dotenv import load_dotenv
from src.crew import NourishBotRecipeCrew, NourishBotAnalysisCrew
from src.tools import ExtractIngredientsTool, FilterIngredientsTool, DietaryFilterTool, NutrientAnalysisTool

# Load environment variables
load_dotenv()

# Verify Google API key is set
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env file. Please add your Google API key.")


def format_recipe_output(final_output):
    """
    Formats the recipe output into a table-based Markdown format.
    
    :param final_output: The output from the NourishBotRecipe workflow.
    :return: Formatted output as a Markdown string.
    """
    output = "## 🍽 Recipe Ideas\n\n"
    recipes = []

    # Check if final_output directly contains recipes
    if "recipes" in final_output:
        recipes = final_output["recipes"]
    else:
        # Fallback: try to extract from nested task output
        recipe_task_output = final_output.get("recipe_suggestion_task")
        if recipe_task_output and hasattr(recipe_task_output, "json_dict") and recipe_task_output.json_dict:
            recipes = recipe_task_output.json_dict.get("recipes", [])
    
    if recipes:
        for idx, recipe in enumerate(recipes, 1):
            output += f"### {idx}. {recipe['title']}\n\n"
            
            # Create a table for ingredients
            output += "**Ingredients:**\n"
            output += "| Ingredient |\n"
            output += "|------------|\n"
            for ingredient in recipe['ingredients']:
                output += f"| {ingredient} |\n"
            output += "\n"
            
            # Display instructions and calorie estimate
            output += f"**Instructions:**\n{recipe['instructions']}\n\n"
            output += f"**Calorie Estimate:** {recipe['calorie_estimate']} kcal\n\n"
            output += "---\n\n"
    else:
        output += "No recipes could be generated. Please try with a different image."
    
    return output


def format_analysis_output(final_output):
    """
    Formats nutritional analysis output into a table-based Markdown format,
    including health evaluation at the end.
    
    :param final_output: The JSON output from the NourishBotAnalysis workflow.
    :return: Formatted output as a Markdown string.
    """
    output = "## 🥗 Nutritional Analysis\n\n"
    
    # Basic dish information
    if dish := final_output.get('dish'):
        output += f"**Dish:** {dish}\n\n"
    if portion := final_output.get('portion_size'):
        output += f"**Portion Size:** {portion}\n\n"
    if est_cal := final_output.get('estimated_calories'):
        output += f"**Estimated Calories:** {est_cal} calories\n\n"
    if total_cal := final_output.get('total_calories'):
        output += f"**Total Calories:** {total_cal} calories\n\n"

    # Nutrient breakdown table
    output += "**Nutrient Breakdown:**\n\n"
    output += "| **Nutrient**       | **Amount** |\n"
    output += "|--------------------|------------|\n"
    
    nutrients = final_output.get('nutrients', {})
    # Display macronutrients
    for macro in ['protein', 'carbohydrates', 'fats']:
        if value := nutrients.get(macro):
            output += f"| **{macro.capitalize()}** | {value} |\n"
    
    # Display vitamins table if available
    vitamins = nutrients.get('vitamins', [])
    if vitamins:
        output += "\n**Vitamins:**\n\n"
        output += "| **Vitamin** | **%DV** |\n"
        output += "|-------------|--------|\n"
        for v in vitamins:
            name = v.get('name', 'N/A')
            dv = v.get('percentage_dv', 'N/A')
            output += f"| {name} | {dv} |\n"
    
    # Display minerals table if available
    minerals = nutrients.get('minerals', [])
    if minerals:
        output += "\n**Minerals:**\n\n"
        output += "| **Mineral** | **Amount** |\n"
        output += "|-------------|-----------|\n"
        for m in minerals:
            name = m.get('name', 'N/A')
            amount = m.get('amount', 'N/A')
            output += f"| {name} | {amount} |\n"
    
    # Append health evaluation at the end
    if health_eval := final_output.get('health_evaluation'):
        output += "\n**Health Evaluation:**\n\n"
        output += health_eval + "\n"
    
    return output


def analyze_food(image, dietary_restrictions, workflow_type, progress=gr.Progress(track_tqdm=True)):
    """
    Wrapper function for the Gradio interface with error handling.
    
    :param image: Uploaded image (PIL format)
    :param dietary_restrictions: Dietary restriction as a string (e.g., "vegan")
    :param workflow_type: Workflow type ("recipe" or "analysis")
    :return: Result from the NourishBot workflow.
    """
    
    try:
        # Validate inputs
        if image is None:
            return "❌ **Error:** Please upload an image."
        
        if not workflow_type:
            return "❌ **Error:** Please select a workflow type (recipe or analysis)."
        
        # Save the uploaded image temporarily
        image.save("uploaded_image.jpg")
        image_path = "uploaded_image.jpg"

        inputs = {
            'uploaded_image': image_path,
            'dietary_restrictions': dietary_restrictions if dietary_restrictions else "",
            'workflow_type': workflow_type
        }
        
        # Use direct tools instead of CrewAI pipeline to avoid LiteLLM issues
        progress(0.3, desc="Processing your request...")
        
        try:
            if workflow_type == "recipe":
                progress(0.6, desc="Extracting ingredients...")
                raw_ingredients = ExtractIngredientsTool.extract_ingredient_direct(image_path)
                filtered = FilterIngredientsTool.filter_ingredients_direct(raw_ingredients)
                
                if dietary_restrictions:
                    progress(0.7, desc="Filtering by dietary restrictions...")
                    filtered = DietaryFilterTool.filter_based_on_restrictions_direct(filtered, dietary_restrictions)
                
                # Format simple ingredient list
                result = "## 🍽 Recipe Ingredients\n\n"
                if filtered:
                    result += "**Detected Ingredients:**\n\n"
                    for i, item in enumerate(filtered, 1):
                        result += f"{i}. {item}\n"
                    result += "\n**Note:** For full recipes with instructions and detailed calorie estimates, you can extend this with a recipe generation service.\n"
                else:
                    result += "No ingredients could be detected. Please try with a clearer image of food items.\n"
                
                progress(1.0, desc="Complete!")
                return result
            
            elif workflow_type == "analysis":
                progress(0.6, desc="Analyzing nutritional content...")
                analysis_text = NutrientAnalysisTool.analyze_image_direct(image_path)
                result = "## 🥗 Nutritional Analysis\n\n" + analysis_text
                progress(1.0, desc="Complete!")
                return result
                
        except Exception as e:
            logging.exception("Direct tools pipeline failed: %s", str(e))
            error_msg = f"❌ **Error:** Failed to process image.\n\n"
            error_msg += f"**Error Details:** {str(e)[:300]}\n\n"
            error_msg += "**Troubleshooting:**\n"
            error_msg += "- Ensure your Google API key is correctly set in the .env file\n"
            error_msg += "- Check that you have enabled the Generative Language API\n"
            error_msg += "- Verify the image is a valid food image\n"
            error_msg += "- Try uploading a different image\n"
            return error_msg
    
    except FileNotFoundError as e:
        return f"❌ **File Error:** {str(e)}"
    except KeyError as e:
        return f"❌ **Configuration Error:** Missing key {str(e)}. Please check your config files."
    except Exception as e:
        error_msg = f"❌ **Error:** {str(e)}\n\n"
        error_msg += "**Troubleshooting:**\n"
        error_msg += "- Ensure your Google API key is correctly set in the .env file\n"
        error_msg += "- Check that the image is a valid food image\n"
        error_msg += "- Try a different image or workflow type\n"
        return error_msg

    
# Define custom CSS for styling
css = """
.title {
    font-size: 1.5em !important; 
    text-align: center !important;
    color: #FFD700; 
}

.text {
    text-align: center;
}
"""

js = """
function createGradioAnimation() {
    var container = document.createElement('div');
    container.id = 'gradio-animation';
    container.style.fontSize = '2em';
    container.style.fontWeight = 'bold';
    container.style.textAlign = 'center';
    container.style.marginBottom = '20px';
    container.style.color = '#eba93f';

    var text = 'Welcome to your AI NourishBot!';
    for (var i = 0; i < text.length; i++) {
        (function(i){
            setTimeout(function(){
                var letter = document.createElement('span');
                letter.style.opacity = '0';
                letter.style.transition = 'opacity 0.1s';
                letter.innerText = text[i];

                container.appendChild(letter);

                setTimeout(function() {
                    letter.style.opacity = '0.9';
                }, 50);
            }, i * 250);
        })(i);
    }

    var gradioContainer = document.querySelector('.gradio-container');
    gradioContainer.insertBefore(container, gradioContainer.firstChild);

    return 'Animation created';
}
"""

# Use a theme and custom CSS with Blocks
with gr.Blocks(theme=gr.themes.Citrus(), css=css, js=js) as demo:
    gr.Markdown("# How it works", elem_classes="title")
    gr.Markdown("Upload an image of your fridge content, enter your dietary restriction (if you have any!) and select a workflow type 'recipe' then click 'Analyze' to get recipe ideas.", elem_classes="text")
    gr.Markdown("Upload an image of a complete dish, leave dietary restriction blank and select a workflow type 'analysis' then click 'Analyze' to get nutritional insights.", elem_classes="text")
    gr.Markdown("You can also select one of the examples provided to autofill the input sections and click 'Analyze' right away!", elem_classes="text")

    with gr.Row():
        with gr.Column(scale=1, min_width=400):
            gr.Markdown("## Inputs", elem_classes="title")
            image_input = gr.Image(type="pil", label="Upload Image")
            dietary_input = gr.Textbox(label="Dietary Restrictions (optional)", placeholder="e.g., vegan, keto, gluten-free")
            workflow_radio = gr.Radio(["recipe", "analysis"], label="Workflow Type", value="recipe")
            submit_btn = gr.Button("Analyze", variant="primary")
        
        with gr.Column(scale=2, min_width=600):
            # Place Examples directly under the Analyze button
            gr.Examples(
                examples=[
                    ["examples/food-1.jpg", "vegan", "recipe"],
                    ["examples/food-2.jpg", "", "analysis"],
                    ["examples/food-3.jpg", "keto", "recipe"],
                    ["examples/food-4.jpg", "", "analysis"],
                ],
                inputs=[image_input, dietary_input, workflow_radio],
                label="Try an Example: Select one of the examples below to autofill the input section then click Analyze"
            )
            gr.Markdown("## Results will appear here...", elem_classes="title")
            result_display = gr.Markdown(
                "<div style='border: 1px solid #ccc; "
                "padding: 1rem; text-align: center; "
                "color: #666;'>No results yet. Upload an image and click Analyze!</div>",
                height=500
            )

    submit_btn.click(
        fn=analyze_food,
        inputs=[image_input, dietary_input, workflow_radio],
        outputs=result_display
    )

# Launch the Gradio interface
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=True)