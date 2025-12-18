import os
import yaml
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.tools import (
    ExtractIngredientsTool, 
    FilterIngredientsTool, 
    DietaryFilterTool,
    NutrientAnalysisTool
)
from src.models import RecipeSuggestionOutput, NutrientAnalysisOutput
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the absolute path to the config directory
CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")

# Initialize Google Gemini LLM for agents
def get_gemini_llm(temperature: float = 0.7):
    """Initialize Google Gemini LLM with proper model name for CrewAI"""
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=temperature,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        convert_system_message_to_human=True  # Required for Gemini
    )


@CrewBase
class BaseNourishBotCrew:
    agents_config_path = os.path.join(CONFIG_DIR, 'agents.yaml')
    tasks_config_path = os.path.join(CONFIG_DIR, 'tasks.yaml')
    
    def __init__(self, image_data, dietary_restrictions: str = None):
        self.image_data = image_data
        self.dietary_restrictions = dietary_restrictions if dietary_restrictions else ""

        with open(self.agents_config_path, 'r') as f:
            self.agents_config = yaml.safe_load(f)
        
        with open(self.tasks_config_path, 'r') as f:
            self.tasks_config = yaml.safe_load(f)

    @agent
    def ingredient_detection_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['ingredient_detection_agent'],
            tools=[
                ExtractIngredientsTool.extract_ingredient, 
                FilterIngredientsTool.filter_ingredients
            ],
            llm=get_gemini_llm(temperature=0.5),
            allow_delegation=False,
            max_iter=5,
            verbose=True
        )

    @agent
    def dietary_filtering_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['dietary_filtering_agent'],
            tools=[DietaryFilterTool.filter_based_on_restrictions],
            llm=get_gemini_llm(temperature=0.3),
            allow_delegation=False,
            max_iter=3,
            verbose=True
        )

    @agent
    def nutrient_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['nutrient_analysis_agent'],
            tools=[NutrientAnalysisTool.analyze_image],
            llm=get_gemini_llm(temperature=0.5),
            allow_delegation=False,
            max_iter=4,
            verbose=True
        )

    @agent
    def recipe_suggestion_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['recipe_suggestion_agent'],
            llm=get_gemini_llm(temperature=0.8),
            allow_delegation=False,
            max_iter=5,
            verbose=True
        )

    @task
    def ingredient_detection_task(self) -> Task:
        task_config = self.tasks_config['ingredient_detection_task']

        return Task(
            description=task_config['description'],
            agent=self.ingredient_detection_agent(),
            expected_output=task_config['expected_output']
        )

    @task
    def dietary_filtering_task(self) -> Task:
        task_config = self.tasks_config['dietary_filtering_task']

        return Task(
            description=task_config['description'],
            agent=self.dietary_filtering_agent(),
            expected_output=task_config['expected_output'],
            context=[self.ingredient_detection_task()]
        )

    @task
    def nutrient_analysis_task(self) -> Task:
        task_config = self.tasks_config['nutrient_analysis_task']

        return Task(
            description=task_config['description'],
            agent=self.nutrient_analysis_agent(),
            expected_output=task_config['expected_output'],
            output_json=NutrientAnalysisOutput
        )

    @task
    def recipe_suggestion_task(self) -> Task:
        task_config = self.tasks_config['recipe_suggestion_task']

        return Task(
            description=task_config['description'],
            agent=self.recipe_suggestion_agent(),
            expected_output=task_config['expected_output'],
            output_json=RecipeSuggestionOutput,
            context=[self.dietary_filtering_task()]
        )


@CrewBase
class NourishBotRecipeCrew(BaseNourishBotCrew):

    @crew
    def crew(self) -> Crew:
        """Recipe generation workflow"""
        return Crew(
            agents=[
                self.ingredient_detection_agent(),
                self.dietary_filtering_agent(),
                self.recipe_suggestion_agent()
            ],
            tasks=[
                self.ingredient_detection_task(),
                self.dietary_filtering_task(),
                self.recipe_suggestion_task()
            ],
            process=Process.sequential,
            verbose=True
        )


@CrewBase
class NourishBotAnalysisCrew(BaseNourishBotCrew):

    @crew
    def crew(self) -> Crew:
        """Nutritional analysis workflow"""
        return Crew(
            agents=[
                self.nutrient_analysis_agent(),
            ],
            tasks=[
                self.nutrient_analysis_task(),
            ],
            process=Process.sequential,
            verbose=True
        )