

---
title: AI_NutriCoach
app_file: app.py
sdk: gradio
sdk_version: 5.12.0
---
# AI NutriCoach (aka AI Dietary Crew)

AI NutriCoach is an AI-powered nutrition assistant that leverages advanced vision models and natural language processing to detect ingredients from food images, filter ingredients based on dietary restrictions, estimate calories, provide detailed nutrient analysis, and generate recipe suggestions. This project demonstrates the use of CrewAI, WatsonX, and other AI tools to deliver insightful and personalized nutritional feedback.

## Features

- **Ingredient Detection**  
  Detects ingredients from user-uploaded images using a vision AI model.

- **Dietary Filtering**  
  Filters detected ingredients based on user-defined dietary restrictions (e.g., vegan, gluten-free).

- **Calorie Estimation**  
  Estimates total calories from the detected ingredients.

- **Nutrient Analysis**  
  Provides a detailed breakdown of key nutrients such as protein, carbohydrates, fats, vitamins, and minerals.

- **Health Evaluation**  
  Summarizes the overall healthiness of the meal and provides a health evaluation.

- **Recipe Suggestion**  
  Generates recipe ideas based on the filtered ingredients and dietary restrictions.

## How It Works

The project is built using the CrewAI framework, which organizes agents and tasks into workflows for two primary use cases:

1. **Recipe Workflow**  
   Detects ingredients, filters them based on dietary restrictions, and suggests recipes.

2. **Analysis Workflow**  
   Directly estimates calories, performs nutrient analysis, and provides a health evaluation summary from a food image.

## Installation

### Prerequisites

- Python 3.8+
- Virtual environment (optional but recommended)
- Git

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <link>
   cd Smart-Nutritional-App
   ```
2. **Create and activate a virtual environment**:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```
3. **Install the required dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
4. **Create a .env file in the root directory with the following keys**:
   ```bash
    WATSONX_API_KEY=your_watsonx_api_key
    WATSONX_URL=your_watsonx_url
    WATSONX_PROJECT_ID=your_watsonx_project_id
   ```
## Usage
### Run the Application

You can run the application using the following commands:

1. For recipe suggestions

```bash
python main.py <image_path> <dietary_restrictions> recipe
```

Example:

```bash
python main.py food.jpg vegan recipe
```

2. For food analysis

```bash
python main.py <image_path> analysis
```

Example:

```bash
python main.py food.jpg analysis
```

3. For training (future functionality - TODO)

```bash
python main.py train <n_iterations> <output_filename> <image_path> <dietary_restrictions> <workflow_type>
```

## File Structure

```
Smart-Nutritional-App-Crew/
│
├── config/
│   ├── agents.yaml               # Configuration for agents
│   └── tasks.yaml                # Configuration for tasks
│
├── src/
│   ├── crew.py                   # Crew definitions (agents, tasks, workflows)
│   ├── tools.py                  # Tool definitions for ingredient detection, filtering, etc.
│   └── main.py                   # Main script for running the application
│
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

----------------------------------------------------------------------------------
Congratulations on completing the AI NourishBot project! By building this application, you've successfully explored the powerful capabilities of the Llama 3.2 90B vision-instruct Model and integrated it with AI-driven technologies to deliver practical, real-world solutions for dietary management. This marks the culmination of integrating all the components of the project—tools, agents, tasks, and workflows—into a cohesive application. With the Gradio interface, users can interact with your app intuitively and experience the power of AI-driven food analysis in real time.

As a final step, feel free to:

Test the app with different images and dietary restrictions.
Explore Gradio's documentation to customize the UI further if desired.
Share your app with others or deploy it on a cloud platform to make it accessible to a broader audience.
This project showcases how advanced AI technologies like LLMs and computer vision can be combined with intuitive design to create impactful applications. Keep pushing boundaries, experimenting, and exploring new use cases for generative AI! 🚀