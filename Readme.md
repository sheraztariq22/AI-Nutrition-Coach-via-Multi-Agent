# 🍽️ AI NourishBot - Multi-Agent Nutrition Coach

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4)

*An intelligent multi-agent system powered by CrewAI and Google Gemini for personalized nutrition analysis and recipe generation*

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Technology Stack](#-technology-stack)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🌟 Overview

AI NourishBot is an advanced multi-agent system that combines computer vision and natural language processing to provide intelligent nutrition analysis and personalized recipe recommendations. Built using CrewAI's agent orchestration framework and powered by Google Gemini's vision models, it offers two primary workflows:

1. **Recipe Generation**: Analyzes fridge contents and suggests creative recipes based on available ingredients and dietary restrictions
2. **Nutritional Analysis**: Provides comprehensive nutritional breakdown of prepared dishes, including macros, vitamins, minerals, and health evaluation

---

## ✨ Features

### 🔍 **Vision-Powered Analysis**
- **Ingredient Detection**: Automatically identifies food items from images using Google Gemini Vision
- **Visual Recognition**: Handles various image qualities, lighting conditions, and backgrounds
- **Multi-item Detection**: Recognizes multiple ingredients in a single image

### 🥗 **Dietary Intelligence**
- **Restriction Filtering**: Supports vegan, keto, gluten-free, and other dietary preferences
- **Smart Substitutions**: Suggests alternatives when ingredients don't match restrictions
- **Allergen Awareness**: Filters out ingredients based on dietary constraints

### 📊 **Comprehensive Nutrition Analysis**
- **Calorie Estimation**: Accurate calorie counts per portion and total
- **Macro Tracking**: Detailed protein, carbohydrate, and fat breakdown
- **Micronutrient Analysis**: Vitamin and mineral content with %DV
- **Health Evaluation**: AI-generated assessment of meal healthiness

### 👨‍🍳 **Recipe Suggestions**
- **Creative Recipes**: Generates multiple recipe ideas from available ingredients
- **Step-by-Step Instructions**: Clear, easy-to-follow cooking directions
- **Calorie-Conscious**: Recipes matched to your dietary goals
- **Dietary Compliance**: All suggestions respect specified restrictions

### 🎨 **User Experience**
- **Interactive UI**: Clean, modern Gradio interface
- **Real-time Processing**: Live progress updates during analysis
- **Example Gallery**: Pre-loaded examples for quick testing
- **Error Handling**: Comprehensive error messages and troubleshooting guidance

---

## 🎬 Demo

### Recipe Generation Workflow
```
1. Upload image of fridge contents/ingredients
2. Enter dietary restrictions (optional)
3. Select "recipe" workflow
4. Get AI-generated recipe suggestions with ingredients and instructions
```

### Nutritional Analysis Workflow
```
1. Upload image of prepared dish
2. Select "analysis" workflow
3. Get detailed nutritional breakdown with health evaluation
```

---

## 🛠 Technology Stack

### Core Frameworks
- **[CrewAI](https://www.crewai.com/)** `v0.75.0` - Multi-agent orchestration framework
- **[Google Gemini](https://ai.google.dev/)** `v0.8.3` - Vision and language AI models
- **[LangChain](https://www.langchain.com/)** `v0.3.4` - LLM application framework
- **[Gradio](https://www.gradio.app/)** `v5.12.0` - Web UI framework

### AI/ML Libraries
- **google-generativeai** - Google's Generative AI Python SDK
- **langchain-google-genai** - LangChain integration for Gemini
- **Pillow** - Image processing

### Development Tools
- **Python** `3.9+` - Core programming language
- **python-dotenv** - Environment variable management
- **PyYAML** - Configuration file handling

---

## 🏗 Architecture

### Multi-Agent System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     AI NourishBot System                     │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
            ┌───────▼────────┐  ┌──────▼───────┐
            │ Recipe Workflow │  │   Analysis   │
            │                 │  │   Workflow   │
            └───────┬─────────┘  └──────┬───────┘
                    │                   │
        ┌───────────┼───────────┐      │
        │           │           │      │
   ┌────▼────┐ ┌───▼────┐ ┌───▼─────┐│
   │Ingredient│ │Dietary │ │ Recipe  ││
   │Detection │ │Filter  │ │Suggest  ││
   │  Agent   │ │Agent   │ │ Agent   ││
   └────┬─────┘ └───┬────┘ └───┬─────┘│
        │           │           │      │
        └───────────┼───────────┘      │
                    │                  │
              ┌─────▼──────┐    ┌─────▼──────┐
              │   Vision   │    │  Nutrient  │
              │   Tools    │    │  Analysis  │
              │            │    │   Agent    │
              └─────┬──────┘    └─────┬──────┘
                    │                 │
                    └────────┬────────┘
                             │
                    ┌────────▼─────────┐
                    │  Google Gemini   │
                    │  Vision API      │
                    └──────────────────┘
```

### Agent Responsibilities

| Agent | Role | Tools | Output |
|-------|------|-------|--------|
| **Ingredient Detection Agent** | Vision AI Specialist | `ExtractIngredientsTool`, `FilterIngredientsTool` | List of detected ingredients |
| **Dietary Filtering Agent** | Nutritionist AI Specialist | `DietaryFilterTool` | Filtered ingredient list |
| **Recipe Suggestion Agent** | Recipe Generation Specialist | None (LLM-based) | Recipe ideas with instructions |
| **Nutrient Analysis Agent** | Nutrition Analysis Specialist | `NutrientAnalysisTool` | Detailed nutritional breakdown |

---

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Google API Key with Gemini API access

### Step 1: Clone the Repository

```bash
git clone https://github.com/sheraztariq22/AI-Nutrition-Coach-via-Multi-Agent.git
cd AI-Nutrition-Coach-via-Multi-Agent
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Google API key
# GOOGLE_API_KEY=your_api_key_here
```

### Step 5: Get Google API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIzaSy...`)
5. Paste it into your `.env` file

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional
GEMINI_MODEL=gemini-1.5-flash
LOG_LEVEL=INFO
```

### Agent Configuration

Agents are configured in `src/config/agents.yaml`:

```yaml
ingredient_detection_agent:
  role: Vision AI Specialist
  goal: Detect ingredients from user-uploaded images
  backstory: You are a highly trained AI specializing in visual recognition...
```

### Task Configuration

Tasks are defined in `src/config/tasks.yaml`:

```yaml
ingredient_detection_task:
  description: Detect the ingredients from the {uploaded_image}...
  expected_output: A list of detected ingredients from the image.
```

---

## 🚀 Usage

### Running the Application

```bash
python app.py
```

The Gradio interface will launch at `http://127.0.0.1:5000`

### Using the Web Interface

1. **Upload an Image**: Click the upload area or drag & drop an image
2. **Enter Dietary Restrictions** (optional): e.g., "vegan", "keto", "gluten-free"
3. **Select Workflow Type**:
   - `recipe` - Generate recipe ideas from ingredients
   - `analysis` - Analyze nutritional content of a dish
4. **Click "Analyze"**: Wait for AI processing
5. **View Results**: Formatted results appear in the right panel

### Using Example Images

The interface includes pre-loaded examples. Click any example to:
- Auto-fill the input fields
- Click "Analyze" to see results immediately

### Command Line Testing

Test individual components:

```bash
# Test API connection
python test_setup.py

# Test tools directly
python test_tools.py

# Check available models
python check_available_models.py
```

---

## 📁 Project Structure

```
ai-nourishbot/
├── src/
│   ├── config/
│   │   ├── agents.yaml          # Agent definitions
│   │   └── tasks.yaml           # Task definitions
│   ├── crew.py                  # CrewAI orchestration
│   ├── models.py                # Pydantic data models
│   └── tools.py                 # Custom AI tools
├── examples/
│   ├── food-1.jpg              # Sample images
│   ├── food-2.jpg
│   ├── food-3.jpg
│   └── food-4.jpg
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── app.py                       # Main Gradio application
├── requirements.txt             # Python dependencies
├── test_setup.py               # API connection test
├── test_tools.py               # Tools test suite
├── check_available_models.py   # Model availability checker
├── README.md                    # This file
└── LICENSE                      # MIT License

```

---

## 📚 API Reference

### Core Classes

#### `NourishBotRecipeCrew`

Multi-agent crew for recipe generation workflow.

```python
crew = NourishBotRecipeCrew(
    image_data="path/to/image.jpg",
    dietary_restrictions="vegan"
)
result = crew.crew().kickoff(inputs=inputs)
```

#### `NourishBotAnalysisCrew`

Multi-agent crew for nutritional analysis workflow.

```python
crew = NourishBotAnalysisCrew(
    image_data="path/to/image.jpg"
)
result = crew.crew().kickoff(inputs=inputs)
```

### Custom Tools

#### `ExtractIngredientsTool`

Extracts ingredients from food images using Gemini Vision.

```python
ingredients = ExtractIngredientsTool.extract_ingredient("image.jpg")
```

#### `DietaryFilterTool`

Filters ingredients based on dietary restrictions.

```python
filtered = DietaryFilterTool.filter_based_on_restrictions(
    ingredients=["eggs", "milk", "flour"],
    dietary_restrictions="vegan"
)
```

#### `NutrientAnalysisTool`

Analyzes nutritional content from dish images.

```python
nutrition = NutrientAnalysisTool.analyze_image("dish.jpg")
```

---

## 🐛 Troubleshooting

### Common Issues

#### Issue: "GOOGLE_API_KEY not found"

**Solution:**
```bash
# Ensure .env file exists in project root
ls -la .env

# Check .env format (no quotes or spaces)
cat .env
# Should show: GOOGLE_API_KEY=AIzaSy...
```

#### Issue: "LLM Provider NOT provided"

**Solution:**
- Use the latest `src/crew.py` with CrewAI's native `LLM` class
- Ensure model format is `gemini/gemini-1.5-flash`

#### Issue: "Model not found" (404 error)

**Solution:**
```bash
# Check available models
python check_available_models.py

# Try alternative models in .env
GEMINI_MODEL=gemini-1.5-flash-latest
```

#### Issue: Rate Limit Exceeded

**Solution:**
- Wait 60 seconds and retry
- Check quota at [Google Cloud Console](https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas)
- Upgrade to paid tier if needed

### Debug Mode

Enable verbose logging:

```bash
# In .env file
LOG_LEVEL=DEBUG
```

### Getting Help

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions
2. Run diagnostic scripts: `python test_tools.py`
3. Review console output for error messages
4. Open an issue on GitHub with error logs

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Getting Started

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Test thoroughly**
   ```bash
   python test_tools.py
   python test_setup.py
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guide for Python code
- Add docstrings to all functions and classes
- Include tests for new features
- Update documentation as needed
- Keep commits atomic and well-described

### Areas for Contribution

- 🐛 **Bug Fixes**: Fix issues listed in GitHub Issues
- ✨ **Features**: Add meal planning, shopping lists, calorie tracking
- 📝 **Documentation**: Improve guides, add tutorials
- 🧪 **Testing**: Increase test coverage
- 🎨 **UI/UX**: Enhance Gradio interface
- 🌍 **Internationalization**: Add multi-language support

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 AI NourishBot Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgments

- **[CrewAI](https://www.crewai.com/)** - For the powerful multi-agent framework
- **[Google AI](https://ai.google.dev/)** - For Gemini vision and language models
- **[Gradio](https://www.gradio.app/)** - For the intuitive web interface
- **[LangChain](https://www.langchain.com/)** - For LLM orchestration tools

---

## 📞 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/sheraztariq22/AI-Nutrition-Coach-via-Multi-Agent/issues)
- **Discussions**: [Join the community](https://github.com/sheraztariq22/AI-Nutrition-Coach-via-Multi-Agent/discussions)
- **Email**: sheraztariq2978@gmail.com

---

## 🗺️ Roadmap

### Version 1.0 (Current)
- ✅ Basic ingredient detection
- ✅ Recipe generation
- ✅ Nutritional analysis
- ✅ Dietary restriction filtering

### Version 2.0 (Planned)
- [ ] Meal planning calendar
- [ ] Shopping list generation
- [ ] Multi-user support with profiles
- [ ] Recipe rating and favorites
- [ ] Nutrition goal tracking

### Version 3.0 (Future)
- [ ] Mobile app (iOS/Android)
- [ ] Integration with fitness trackers
- [ ] Social features (share recipes)
- [ ] AI meal prep suggestions
- [ ] Voice input support


<div align="center">

**Made with ❤️ using CrewAI and Google Gemini**

[⬆ Back to Top](#️-ai-nourishbot---multi-agent-nutrition-coach)

</div>