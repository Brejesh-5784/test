import streamlit as st
import pandas as pd
import altair as alt
import json
from google.genai import Client
from google.genai import types
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="FitSync Pro - AI Fitness Concierge",
    page_icon="💪",
    layout="wide"
)

# Initialize Gemini client
@st.cache_resource
def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
        st.stop()
    client = Client(api_key=api_key)
    return client

client = get_gemini_client()

# Tool: Calculate BMR and Daily Targets
def calculate_targets(gender, age, height_cm, weight_kg, goal):
    """
    Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation
    and daily calorie/protein targets based on fitness goal.
    """
    # BMR calculation
    if gender.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    
    # Activity multiplier (assuming moderate activity)
    tdee = bmr * 1.55
    
    # Adjust based on goal
    if goal == "Lose Weight":
        daily_calories = tdee - 500
        protein_g = weight_kg * 2.2  # Higher protein for weight loss
    elif goal == "Gain Muscle":
        daily_calories = tdee + 300
        protein_g = weight_kg * 2.0
    else:  # Maintain
        daily_calories = tdee
        protein_g = weight_kg * 1.8
    
    return {
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "daily_calories": round(daily_calories, 1),
        "daily_protein_g": round(protein_g, 1)
    }

# Agent 1: Nutritionist
def generate_meal_plan(targets, gender, age, goal):
    """Generate a 1-day meal plan using Gemini with structured JSON output."""
    prompt = f"""You are a professional nutritionist. Create a detailed 1-day meal plan for:
- Gender: {gender}
- Age: {age}
- Goal: {goal}
- Daily Calorie Target: {targets['daily_calories']} kcal
- Daily Protein Target: {targets['daily_protein_g']}g

Generate a meal plan with 4 meals (Breakfast, Lunch, Snack, Dinner).

Return ONLY valid JSON in this exact format:
{{
  "meals": [
    {{
      "meal": "Breakfast",
      "food": "Oatmeal with berries and almonds",
      "calories": 350,
      "protein_g": 12,
      "carbs_g": 55,
      "fats_g": 8
    }}
  ]
}}

Ensure the total calories and protein match the targets closely."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        raw_json = response.text
        meal_data = json.loads(raw_json)
        return meal_data, raw_json
    except Exception as e:
        st.error(f"Error generating meal plan: {str(e)}")
        return None, None

# Agent 2: Fitness Coach
def generate_workout_plan(gender, age, goal):
    """Generate a 7-day workout split using Gemini with structured JSON output."""
    prompt = f"""You are a professional fitness coach. Create a 7-day workout split for:
- Gender: {gender}
- Age: {age}
- Goal: {goal}

Generate a balanced weekly workout plan with varied focus areas.

Return ONLY valid JSON in this exact format:
{{
  "workouts": [
    {{
      "day": "Monday",
      "focus": "Upper Body Push",
      "total_sets": 18,
      "intensity_score": 8
    }}
  ]
}}

Include all 7 days. Intensity score should be 1-10. Total sets should vary between 12-24."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        raw_json = response.text
        workout_data = json.loads(raw_json)
        return workout_data, raw_json
    except Exception as e:
        st.error(f"Error generating workout plan: {str(e)}")
        return None, None

# Main App UI
st.title("💪 FitSync Pro - AI Fitness Concierge")
st.markdown("*Your personalized meal plans and workout routines powered by AI*")

# Sidebar Configuration
st.sidebar.header("⚙️ Your Profile")
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
age = st.sidebar.number_input("Age", min_value=15, max_value=100, value=30)
height_cm = st.sidebar.number_input("Height (cm)", min_value=120, max_value=250, value=170)
weight_kg = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
goal = st.sidebar.selectbox("Goal", ["Lose Weight", "Maintain", "Gain Muscle"])

generate_button = st.sidebar.button("🚀 Generate My Plan", type="primary")

if generate_button:
    with st.spinner("Calculating your targets..."):
        # Calculate targets
        targets = calculate_targets(gender, age, height_cm, weight_kg, goal)
        
        # Display targets
        st.header("📊 Your Daily Targets")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("BMR", f"{targets['bmr']} kcal")
        col2.metric("TDEE", f"{targets['tdee']} kcal")
        col3.metric("Daily Calories", f"{targets['daily_calories']} kcal")
        col4.metric("Daily Protein", f"{targets['daily_protein_g']}g")
        
        st.divider()
        
        # Agent 1: Meal Plan
        st.header("🍽️ Your Personalized Meal Plan")
        with st.spinner("AI Nutritionist is creating your meal plan..."):
            meal_data, meal_raw_json = generate_meal_plan(targets, gender, age, goal)
            
            if meal_data and "meals" in meal_data:
                # Convert to DataFrame
                df_meals = pd.DataFrame(meal_data["meals"])
                
                # Display meal table
                st.subheader("Daily Meal Breakdown")
                st.dataframe(df_meals, use_container_width=True)
                
                # Calculate totals
                total_calories = df_meals["calories"].sum()
                total_protein = df_meals["protein_g"].sum()
                total_carbs = df_meals["carbs_g"].sum()
                total_fats = df_meals["fats_g"].sum()
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Calories", f"{total_calories} kcal")
                col2.metric("Total Protein", f"{total_protein}g")
                col3.metric("Total Carbs", f"{total_carbs}g")
                col4.metric("Total Fats", f"{total_fats}g")
                
                # Macro Distribution Pie Chart
                st.subheader("Macronutrient Distribution")
                macro_data = pd.DataFrame({
                    "Macro": ["Protein", "Carbs", "Fats"],
                    "Grams": [total_protein, total_carbs, total_fats]
                })
                
                pie_chart = alt.Chart(macro_data).mark_arc().encode(
                    theta=alt.Theta(field="Grams", type="quantitative"),
                    color=alt.Color(field="Macro", type="nominal", 
                                   scale=alt.Scale(domain=["Protein", "Carbs", "Fats"],
                                                 range=["#FF6B6B", "#4ECDC4", "#FFE66D"])),
                    tooltip=["Macro", "Grams"]
                ).properties(
                    width=400,
                    height=400
                )
                
                st.altair_chart(pie_chart, use_container_width=True)
                
                # Show agent thought process
                with st.expander("🔍 See Agent Thought Process (Nutritionist)"):
                    st.json(meal_raw_json)
        
        st.divider()
        
        # Agent 2: Workout Plan
        st.header("🏋️ Your 7-Day Workout Split")
        with st.spinner("AI Fitness Coach is designing your workout plan..."):
            workout_data, workout_raw_json = generate_workout_plan(gender, age, goal)
            
            if workout_data and "workouts" in workout_data:
                # Convert to DataFrame
                df_workouts = pd.DataFrame(workout_data["workouts"])
                
                # Display workout table
                st.subheader("Weekly Workout Schedule")
                st.dataframe(df_workouts, use_container_width=True)
                
                # Volume Bar Chart
                st.subheader("Training Volume by Day")
                bar_chart = alt.Chart(df_workouts).mark_bar().encode(
                    x=alt.X("day:N", sort=["Monday", "Tuesday", "Wednesday", "Thursday", 
                                          "Friday", "Saturday", "Sunday"],
                           title="Day of Week"),
                    y=alt.Y("total_sets:Q", title="Total Sets (Volume)"),
                    color=alt.Color("intensity_score:Q", 
                                   scale=alt.Scale(scheme="redyellowgreen", reverse=True),
                                   title="Intensity"),
                    tooltip=["day", "focus", "total_sets", "intensity_score"]
                ).properties(
                    width=700,
                    height=400
                )
                
                st.altair_chart(bar_chart, use_container_width=True)
                
                # Show agent thought process
                with st.expander("🔍 See Agent Thought Process (Fitness Coach)"):
                    st.json(workout_raw_json)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>FitSync Pro - Kaggle Capstone Project | Powered by Google Gemini AI</p>
</div>
""", unsafe_allow_html=True)
