# FitSync Pro - AI Fitness Concierge

An AI-powered fitness application that generates personalized meal plans and workout routines using Google Gemini AI.

## Features

- **Personalized Nutrition**: AI-generated meal plans based on your BMR and fitness goals
- **Custom Workouts**: 7-day workout splits tailored to your profile
- **Data Visualization**: Interactive charts showing macro distribution and training volume
- **Observability**: View the AI's reasoning process for transparency

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file from the example:
```bash
cp .env.example .env
```

3. Add your Gemini API key to `.env`:
```
GEMINI_API_KEY=your_actual_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## Docker Deployment

Build and run with Docker:
```bash
docker build -t fitsync-pro .
docker run -p 8080:8080 --env-file .env fitsync-pro
```

## Deploy to Google Cloud Run

```bash
gcloud run deploy fitsync-pro \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_api_key
```

## Tech Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 1.5 Pro
- **Data Processing**: Pandas
- **Visualization**: Altair
- **Deployment**: Docker + Google Cloud Run
