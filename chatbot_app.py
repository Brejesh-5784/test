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
    page_title="FitSync Pro Chatbot - AI Fitness Assistant",
    page_icon="💬",
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

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

# Tool: Calculate BMR and Daily Targets
def calculate_targets(gender, age, height_cm, weight_kg, goal):
    """Calculate BMR and daily targets."""
    if gender.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    
    tdee = bmr * 1.55
    
    if goal == "Lose Weight":
        daily_calories = tdee - 500
        protein_g = weight_kg * 2.2
    elif goal == "Gain Muscle":
        daily_calories = tdee + 300
        protein_g = weight_kg * 2.0
    else:
        daily_calories = tdee
        protein_g = weight_kg * 1.8
    
    return {
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "daily_calories": round(daily_calories, 1),
        "daily_protein_g": round(protein_g, 1)
    }

# Generate comprehensive meal plan with multiple food options
def generate_comprehensive_meal_plan(targets, gender, age, goal, dietary_preferences=""):
    """Generate detailed meal plan with multiple food options per meal."""
    prompt = f"""You are a professional nutritionist. Create a comprehensive meal plan for:
- Gender: {gender}
- Age: {age}
- Goal: {goal}
- Daily Calorie Target: {targets['daily_calories']} kcal
- Daily Protein Target: {targets['daily_protein_g']}g
{f"- Dietary Preferences: {dietary_preferences}" if dietary_preferences else ""}

Generate a detailed meal plan with 5 meals (Breakfast, Mid-Morning Snack, Lunch, Evening Snack, Dinner).
For EACH meal, provide 3-4 different food options so the user has variety and choices.

Return ONLY valid JSON in this exact format:
{{
  "meals": [
    {{
      "meal_time": "Breakfast",
      "options": [
        {{
          "option_name": "Option 1: High Protein Oatmeal Bowl",
          "foods": [
            {{"item": "Oatmeal", "quantity": "1 cup cooked"}},
            {{"item": "Whey protein powder", "quantity": "1 scoop"}},
            {{"item": "Banana", "quantity": "1 medium"}},
            {{"item": "Almonds", "quantity": "10 pieces"}},
            {{"item": "Honey", "quantity": "1 tsp"}}
          ],
          "calories": 450,
          "protein_g": 35,
          "carbs_g": 55,
          "fats_g": 12
        }},
        {{
          "option_name": "Option 2: Egg White Scramble",
          "foods": [
            {{"item": "Egg whites", "quantity": "4 eggs"}},
            {{"item": "Whole wheat toast", "quantity": "2 slices"}},
            {{"item": "Avocado", "quantity": "1/4 piece"}},
            {{"item": "Spinach", "quantity": "1 cup"}},
            {{"item": "Cherry tomatoes", "quantity": "5 pieces"}}
          ],
          "calories": 420,
          "protein_g": 32,
          "carbs_g": 48,
          "fats_g": 10
        }}
      ]
    }}
  ],
  "daily_totals": {{
    "total_calories": 2100,
    "total_protein_g": 165,
    "total_carbs_g": 220,
    "total_fats_g": 65
  }},
  "hydration_tip": "Drink 3-4 liters of water throughout the day",
  "meal_timing_tips": [
    "Eat breakfast within 1 hour of waking",
    "Space meals 3-4 hours apart",
    "Have your last meal 2-3 hours before bed"
  ]
}}

Make sure to provide diverse, realistic food options with specific quantities."""

    try:
        print("🔍 [VERBOSE] Sending request to Gemini API (model: gemini-2.5-flash)")
        print(f"🔍 [VERBOSE] Prompt length: {len(prompt)} characters")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        print("✅ [VERBOSE] Response received from Gemini API")
        raw_json = response.text
        print(f"📊 [VERBOSE] Response length: {len(raw_json)} characters")
        print(f"🔍 [VERBOSE] Parsing JSON response...")
        
        meal_data = json.loads(raw_json)
        print(f"✅ [VERBOSE] JSON parsed successfully! Found {len(meal_data.get('meals', []))} meals")
        return meal_data, raw_json
    except json.JSONDecodeError as e:
        print(f"❌ [VERBOSE] JSON parsing error: {str(e)}")
        print(f"📄 [VERBOSE] Raw response: {raw_json[:500]}...")
        return None, f"JSON Error: {str(e)}"
    except Exception as e:
        print(f"❌ [VERBOSE] API Error: {str(e)}")
        return None, str(e)

# Generate detailed workout plan with reps and sets
def generate_detailed_workout_plan(gender, age, goal, fitness_level="Intermediate"):
    """Generate comprehensive workout plan with exercises, sets, reps, and rest periods."""
    prompt = f"""You are a professional fitness coach. Create a detailed 7-day workout split for:
- Gender: {gender}
- Age: {age}
- Goal: {goal}
- Fitness Level: {fitness_level}

Generate a complete weekly workout plan with specific exercises, sets, reps, rest periods, and tempo.

Return ONLY valid JSON in this exact format:
{{
  "weekly_plan": [
    {{
      "day": "Monday",
      "focus": "Upper Body Push (Chest, Shoulders, Triceps)",
      "warm_up": "5 min cardio + dynamic stretching",
      "exercises": [
        {{
          "exercise_name": "Barbell Bench Press",
          "sets": 4,
          "reps": "8-10",
          "rest_seconds": 90,
          "tempo": "2-0-2-0",
          "notes": "Focus on controlled descent, explosive push"
        }},
        {{
          "exercise_name": "Incline Dumbbell Press",
          "sets": 3,
          "reps": "10-12",
          "rest_seconds": 60,
          "tempo": "2-0-2-0",
          "notes": "30-45 degree incline"
        }},
        {{
          "exercise_name": "Dumbbell Shoulder Press",
          "sets": 3,
          "reps": "10-12",
          "rest_seconds": 60,
          "tempo": "2-0-2-0",
          "notes": "Keep core tight"
        }},
        {{
          "exercise_name": "Cable Lateral Raises",
          "sets": 3,
          "reps": "12-15",
          "rest_seconds": 45,
          "tempo": "2-1-2-0",
          "notes": "Control the weight, no swinging"
        }},
        {{
          "exercise_name": "Tricep Rope Pushdowns",
          "sets": 3,
          "reps": "12-15",
          "rest_seconds": 45,
          "tempo": "2-1-2-0",
          "notes": "Full extension at bottom"
        }}
      ],
      "cool_down": "5 min stretching focusing on chest and shoulders",
      "total_sets": 16,
      "estimated_duration_minutes": 60,
      "intensity_score": 8
    }}
  ],
  "weekly_summary": {{
    "total_training_days": 5,
    "rest_days": 2,
    "total_sets_per_week": 95,
    "focus_areas": ["Upper Body", "Lower Body", "Core"]
  }},
  "progression_tips": [
    "Increase weight by 2.5-5% when you can complete all sets with good form",
    "Track your workouts in a journal",
    "Prioritize progressive overload"
  ],
  "recovery_tips": [
    "Get 7-9 hours of sleep",
    "Stay hydrated",
    "Consider foam rolling after workouts"
  ]
}}

Include all 7 days with varied exercises. Tempo format: eccentric-pause-concentric-pause (in seconds)."""

    try:
        print("🔍 [VERBOSE] Sending workout request to Gemini API (model: gemini-2.5-flash)")
        print(f"🔍 [VERBOSE] Prompt length: {len(prompt)} characters")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        print("✅ [VERBOSE] Response received from Gemini API")
        raw_json = response.text
        print(f"📊 [VERBOSE] Response length: {len(raw_json)} characters")
        print(f"🔍 [VERBOSE] Parsing JSON response...")
        
        workout_data = json.loads(raw_json)
        print(f"✅ [VERBOSE] JSON parsed successfully! Found {len(workout_data.get('weekly_plan', []))} days")
        return workout_data, raw_json
    except json.JSONDecodeError as e:
        print(f"❌ [VERBOSE] JSON parsing error: {str(e)}")
        print(f"📄 [VERBOSE] Raw response: {raw_json[:500]}...")
        return None, f"JSON Error: {str(e)}"
    except Exception as e:
        print(f"❌ [VERBOSE] API Error: {str(e)}")
        return None, str(e)

# Chat with AI about fitness
def chat_with_ai(user_message, user_profile):
    """Chat with AI about fitness, nutrition, and workouts."""
    st.write("🔍 **[VERBOSE]** Processing your question...")
    
    context = ""
    if user_profile:
        context = f"""User Profile:
- Gender: {user_profile['gender']}
- Age: {user_profile['age']}
- Height: {user_profile['height_cm']} cm
- Weight: {user_profile['weight_kg']} kg
- Goal: {user_profile['goal']}
- Daily Calorie Target: {user_profile['targets']['daily_calories']} kcal
- Daily Protein Target: {user_profile['targets']['daily_protein_g']}g
"""
        st.write(f"✅ **[VERBOSE]** Using your profile for personalized response")

    prompt = f"""{context}

You are FitSync Pro AI, an expert fitness and nutrition coach. Answer the user's question with:
- Specific, actionable advice
- Scientific backing when relevant
- Personalized recommendations based on their profile
- Encouragement and motivation

User Question: {user_message}

Provide a helpful, detailed response."""

    try:
        st.write("🤖 **[VERBOSE]** Calling Gemini AI (model: gemini-2.5-flash)...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        st.write("✅ **[VERBOSE]** Response received successfully!")
        return response.text
    except Exception as e:
        st.error(f"❌ **[VERBOSE]** Error: {str(e)}")
        return f"Error: {str(e)}"

# Helper functions to display meal and workout plans (MUST BE BEFORE MAIN UI)
def display_meal_plan(meal_data):
    """Display comprehensive meal plan."""
    st.write("📊 Rendering meal plan...")
    st.subheader("🍽️ Your Personalized Meal Plan")
    
    for meal in meal_data.get("meals", []):
        st.markdown(f"### {meal['meal_time']}")
        
        for idx, option in enumerate(meal.get("options", []), 1):
            with st.expander(f"✨ {option['option_name']}", expanded=(idx == 1)):
                st.markdown("**Foods:**")
                for food in option.get("foods", []):
                    st.markdown(f"- {food['item']}: `{food['quantity']}`")
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Calories", f"{option['calories']} kcal")
                col2.metric("Protein", f"{option['protein_g']}g")
                col3.metric("Carbs", f"{option['carbs_g']}g")
                col4.metric("Fats", f"{option['fats_g']}g")
        
        st.divider()
    
    # Daily totals
    if "daily_totals" in meal_data:
        st.subheader("📊 Daily Totals")
        totals = meal_data["daily_totals"]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Calories", f"{totals['total_calories']} kcal")
        col2.metric("Total Protein", f"{totals['total_protein_g']}g")
        col3.metric("Total Carbs", f"{totals['total_carbs_g']}g")
        col4.metric("Total Fats", f"{totals['total_fats_g']}g")
    
    # Tips
    if "hydration_tip" in meal_data:
        st.info(f"💧 {meal_data['hydration_tip']}")
    
    if "meal_timing_tips" in meal_data:
        st.success("⏰ **Meal Timing Tips:**\n" + "\n".join([f"- {tip}" for tip in meal_data["meal_timing_tips"]]))
    
    st.write("✅  Meal plan rendered successfully!")

def display_workout_plan(workout_data):
    """Display detailed workout plan."""
    st.write("📊  Rendering workout plan...")
    st.subheader("🏋️ Your Personalized Workout Plan")
    
    for day_plan in workout_data.get("weekly_plan", []):
        with st.expander(f"📅 {day_plan['day']} - {day_plan['focus']}", expanded=False):
            st.markdown(f"**Warm-up:** {day_plan.get('warm_up', 'N/A')}")
            st.markdown(f"**Duration:** ~{day_plan.get('estimated_duration_minutes', 'N/A')} minutes")
            st.markdown(f"**Intensity:** {day_plan.get('intensity_score', 'N/A')}/10")
            
            st.markdown("---")
            st.markdown("### Exercises")
            
            # Create exercise table
            exercises = day_plan.get("exercises", [])
            if exercises:
                df = pd.DataFrame([{
                    "Exercise": ex["exercise_name"],
                    "Sets": ex["sets"],
                    "Reps": ex["reps"],
                    "Rest (sec)": ex["rest_seconds"],
                    "Tempo": ex.get("tempo", "N/A"),
                    "Notes": ex.get("notes", "")
                } for ex in exercises])
                
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown(f"**Cool-down:** {day_plan.get('cool_down', 'N/A')}")
    
    # Weekly summary
    if "weekly_summary" in workout_data:
        st.subheader("📈 Weekly Summary")
        summary = workout_data["weekly_summary"]
        col1, col2, col3 = st.columns(3)
        col1.metric("Training Days", summary.get("total_training_days", "N/A"))
        col2.metric("Rest Days", summary.get("rest_days", "N/A"))
        col3.metric("Total Sets/Week", summary.get("total_sets_per_week", "N/A"))
    
    # Tips
    if "progression_tips" in workout_data:
        st.success("💪 **Progression Tips:**\n" + "\n".join([f"- {tip}" for tip in workout_data["progression_tips"]]))
    
    if "recovery_tips" in workout_data:
        st.info("🛌 **Recovery Tips:**\n" + "\n".join([f"- {tip}" for tip in workout_data["recovery_tips"]]))
    
    st.write("✅  Workout plan rendered successfully!")

# Main App UI
st.title("💬 FitSync Pro Chatbot - Your AI Fitness Assistant")
st.markdown("*Get personalized meal plans, detailed workouts, and chat with your AI fitness coach*")

# Sidebar for profile setup
with st.sidebar:
    st.header("⚙️ Your Profile")
    
    with st.form("profile_form"):
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.number_input("Age", min_value=15, max_value=100, value=30)
        height_cm = st.number_input("Height (cm)", min_value=120, max_value=250, value=170)
        weight_kg = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        goal = st.selectbox("Goal", ["Lose Weight", "Maintain", "Gain Muscle"])
        fitness_level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
        dietary_preferences = st.text_input("Dietary Preferences (optional)", placeholder="e.g., vegetarian, no dairy")
        
        submit_profile = st.form_submit_button("💾 Save Profile", type="primary")
        
        if submit_profile:
            targets = calculate_targets(gender, age, height_cm, weight_kg, goal)
            st.session_state.user_profile = {
                "gender": gender,
                "age": age,
                "height_cm": height_cm,
                "weight_kg": weight_kg,
                "goal": goal,
                "fitness_level": fitness_level,
                "dietary_preferences": dietary_preferences,
                "targets": targets
            }
            st.success("✅ Profile saved!")
    
    if st.session_state.user_profile:
        st.divider()
        st.subheader("📊 Your Targets")
        targets = st.session_state.user_profile["targets"]
        st.metric("Daily Calories", f"{targets['daily_calories']} kcal")
        st.metric("Daily Protein", f"{targets['daily_protein_g']}g")
        st.metric("BMR", f"{targets['bmr']} kcal")
    
    st.divider()
    st.subheader("🎯 Quick Actions")
    
    if st.button("🍽️ Generate Meal Plan", use_container_width=True):
        if not st.session_state.user_profile:
            st.error("Please save your profile first!")
        else:
            with st.spinner("Creating your personalized meal plan..."):
                st.write("🔍 **[VERBOSE]** Starting meal plan generation...")
                profile = st.session_state.user_profile
                st.write(f"✅ Profile loaded: {profile['gender']}, {profile['age']}y, Goal: {profile['goal']}")
                st.write(f"🎯 Target: {profile['targets']['daily_calories']} kcal, {profile['targets']['daily_protein_g']}g protein")
                st.write("🤖  Calling Gemini AI for meal plan...")
                
                meal_data, raw = generate_comprehensive_meal_plan(
                    profile["targets"],
                    profile["gender"],
                    profile["age"],
                    profile["goal"],
                    profile["dietary_preferences"]
                )
                
                if meal_data:
                    st.write("✅  Meal plan generated successfully!")
                    st.write(f"📊  Generated {len(meal_data.get('meals', []))} meal times")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "meal_plan",
                        "data": meal_data
                    })
                    st.rerun()
                else:
                    st.error(f"❌ **[VERBOSE]** Failed to generate meal plan: {raw}")
    
    if st.button("🏋️ Generate Workout Plan", use_container_width=True):
        if not st.session_state.user_profile:
            st.error("Please save your profile first!")
        else:
            with st.spinner("Creating your personalized workout plan..."):
                st.write("🔍  Starting workout plan generation...")
                profile = st.session_state.user_profile
                st.write(f"✅  Profile loaded: {profile['gender']}, {profile['age']}y, Level: {profile['fitness_level']}")
                st.write(f"🎯 Goal: {profile['goal']}")
                st.write("🤖  Calling Gemini AI for workout plan...")
                
                workout_data, raw = generate_detailed_workout_plan(
                    profile["gender"],
                    profile["age"],
                    profile["goal"],
                    profile["fitness_level"]
                )
                
                if workout_data:
                    st.write("✅  Workout plan generated successfully!")
                    st.write(f"📊  Generated {len(workout_data.get('weekly_plan', []))} days of workouts")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "workout_plan",
                        "data": workout_data
                    })
                    st.rerun()
                else:
                    st.error(f"❌ Failed to generate workout plan: {raw}")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.divider()

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant"):
            if message["content"] == "meal_plan":
                display_meal_plan(message["data"])
            elif message["content"] == "workout_plan":
                display_workout_plan(message["data"])
            else:
                st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about fitness, nutrition, or workouts..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get AI response
    with st.spinner("Thinking..."):
        response = chat_with_ai(prompt, st.session_state.user_profile)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()

# Welcome message
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.write("""
        👋 **Welcome to FitSync Pro Chatbot!**
        
        I'm your AI fitness assistant. Here's what I can help you with:
        
        - 🍽️ **Comprehensive Meal Plans** - Multiple food options for each meal with specific quantities
        - 🏋️ **Detailed Workout Plans** - Complete exercises with sets, reps, rest periods, and tempo
        - 💬 **Fitness Chat** - Ask me anything about nutrition, training, supplements, or recovery
        - 📊 **Progress Tracking** - Get personalized advice based on your profile
        
        **Get Started:**
        1. Fill out your profile in the sidebar
        2. Click "Generate Meal Plan" or "Generate Workout Plan"
        3. Or just ask me a question!
        
        Try asking:
        - "What are the best protein sources for muscle gain?"
        - "How do I improve my bench press?"
        - "What should I eat before a workout?"
        """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>FitSync Pro Chatbot | Powered by Google Gemini AI | Your Personal Fitness Coach 24/7</p>
</div>
""", unsafe_allow_html=True)
