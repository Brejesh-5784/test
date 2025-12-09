# 💪 FitSync Pro - AI Fitness Chatbot

An intelligent AI-powered fitness chatbot that provides personalized meal plans, detailed workout routines, and answers all your fitness questions using Google Gemini AI.

## ✨ Features

### 🤖 AI Chatbot Interface
- Natural conversation with your personal AI fitness coach
- Ask anything about nutrition, training, supplements, or recovery
- Get instant, personalized advice based on your profile

### 🍽️ Comprehensive Meal Plans
- Multiple food options for each meal (breakfast, lunch, snacks, dinner)
- Specific quantities and measurements for every ingredient
- Flexible choices based on your convenience and preferences
- Complete macro breakdown (calories, protein, carbs, fats)
- Dietary preference support (vegetarian, vegan, no dairy, etc.)
- Hydration and meal timing tips

### 🏋️ Detailed Workout Plans
- Complete 7-day workout splits
- Specific exercises with sets, reps, and rest periods
- Tempo guidance for each exercise
- Warm-up and cool-down routines
- Progressive overload tips
- Recovery recommendations

### 📊 Smart Calculations
- BMR (Basal Metabolic Rate) calculation
- TDEE (Total Daily Energy Expenditure)
- Personalized calorie and protein targets
- Goal-based adjustments (lose weight, maintain, gain muscle)

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)
- A Google Gemini API key ([Get one free here](https://aistudio.google.com/app/apikey))

### Step 1: Clone the Repository
```bash
git clone https://github.com/Brejesh-5784/test.git
cd test
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Key
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
# Replace the example key with your actual key from Google AI Studio
```

Your `.env` file should look like:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 5: Test Your API Key (Optional but Recommended)
```bash
python test_api_key.py
```

You should see:
```
✅ SUCCESS! API key is valid and working!
```

### Step 6: Run the Application

**Option A: Chatbot Version (Recommended)**
```bash
streamlit run chatbot_app.py
```

**Option B: Simple Form Version**
```bash
streamlit run app.py
```

### Step 7: Open in Browser
The app will automatically open in your browser at:
- **Local URL**: http://localhost:8501 (or 8502, 8503)
- **Network URL**: http://YOUR_IP:8501

## 📱 How to Use

### 1. Set Up Your Profile
- Fill in your details in the sidebar:
  - Gender, Age, Height, Weight
  - Fitness Goal (Lose Weight, Maintain, Gain Muscle)
  - Fitness Level (Beginner, Intermediate, Advanced)
  - Dietary Preferences (optional)
- Click "💾 Save Profile"

### 2. Generate Your Plans
- Click "🍽️ Generate Meal Plan" for personalized nutrition
- Click "🏋️ Generate Workout Plan" for your training schedule
- Each meal has multiple food options to choose from
- Each workout day has detailed exercises with instructions

### 3. Chat with AI
- Type any fitness question in the chat box
- Examples:
  - "What are the best protein sources for muscle gain?"
  - "How do I improve my bench press?"
  - "What should I eat before a workout?"
  - "How much water should I drink daily?"
  - "Can you explain progressive overload?"

## 📂 Project Structure

```
test/
├── chatbot_app.py          # Main chatbot application (recommended)
├── app.py                  # Simple form-based version
├── test_api_key.py         # API key validation script
├── list_models.py          # List available Gemini models
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── .env                   # Your API key (create this)
├── Dockerfile             # Docker configuration
├── README.md              # This file
├── EXAMPLE_QUERIES.md     # Sample questions to ask
├── VERBOSE_LOGGING_GUIDE.md  # Debugging guide
└── PUSH_TO_GITHUB.md      # Git instructions
```

## 🐳 Docker Deployment

### Build and Run with Docker
```bash
# Build the image
docker build -t fitsync-pro .

# Run the container
docker run -p 8080:8080 --env-file .env fitsync-pro
```

Access at: http://localhost:8080

## ☁️ Deploy to Google Cloud Run

```bash
gcloud run deploy fitsync-pro \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_api_key
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Model**: Google Gemini 2.5 Flash
- **Data Processing**: Pandas
- **Visualization**: Altair
- **Environment**: Python-dotenv
- **Deployment**: Docker + Google Cloud Run

## 🔧 Troubleshooting

### API Key Issues
```bash
# Test your API key
python test_api_key.py

# Common issues:
# - Make sure there are no spaces in your .env file
# - Use Google AI Studio key, not Google Cloud key
# - Check if key is expired or revoked
```

### Port Already in Use
```bash
# If port 8501 is busy, Streamlit will auto-increment to 8502, 8503, etc.
# Or specify a custom port:
streamlit run chatbot_app.py --server.port 8504
```

### Module Not Found
```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Python Version Issues
```bash
# Check your Python version (needs 3.8+)
python3 --version

# If too old, install newer Python from python.org
```

## 📝 Example Questions to Ask

- "Create a vegetarian meal plan for me"
- "What exercises target the lower chest?"
- "How many calories should I eat to lose 1 pound per week?"
- "What's the difference between whey and casein protein?"
- "How do I prevent muscle soreness?"
- "What are good pre-workout snacks?"
- "How long should I rest between sets?"

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Powered by Google Gemini AI
- Built with Streamlit
- Created for fitness enthusiasts worldwide

## 📧 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Run `python test_api_key.py` to verify your setup
3. Check the console output for error messages
4. Make sure all dependencies are installed

---

**Made with ❤️ for fitness and AI enthusiasts**
