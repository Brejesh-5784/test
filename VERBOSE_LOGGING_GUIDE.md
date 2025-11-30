# FitSync Pro Chatbot - Verbose Logging Guide

## ✅ Fixed Issues:
1. **NameError resolved** - Functions are now defined before they're called
2. **Verbose logging added** - You can now see what's happening at each step

## 🔍 What You'll See with Verbose Mode:

### When Generating Meal Plans:
```
🔍 [VERBOSE] Starting meal plan generation...
✅ [VERBOSE] Profile loaded: Male, 30y, Goal: Gain Muscle
🎯 [VERBOSE] Target: 2400 kcal, 140g protein
🤖 [VERBOSE] Calling Gemini AI for meal plan...
🔍 [VERBOSE] Sending request to Gemini API (model: gemini-2.5-flash)
🔍 [VERBOSE] Prompt length: 1234 characters
✅ [VERBOSE] Response received from Gemini API
📊 [VERBOSE] Response length: 5678 characters
🔍 [VERBOSE] Parsing JSON response...
✅ [VERBOSE] JSON parsed successfully! Found 5 meals
✅ [VERBOSE] Meal plan generated successfully!
📊 [VERBOSE] Generated 5 meal times
📊 [VERBOSE] Rendering meal plan...
✅ [VERBOSE] Meal plan rendered successfully!
```

### When Generating Workout Plans:
```
🔍 [VERBOSE] Starting workout plan generation...
✅ [VERBOSE] Profile loaded: Male, 30y, Level: Intermediate
🎯 [VERBOSE] Goal: Gain Muscle
🤖 [VERBOSE] Calling Gemini AI for workout plan...
🔍 [VERBOSE] Sending workout request to Gemini API (model: gemini-2.5-flash)
🔍 [VERBOSE] Prompt length: 2345 characters
✅ [VERBOSE] Response received from Gemini API
📊 [VERBOSE] Response length: 8901 characters
🔍 [VERBOSE] Parsing JSON response...
✅ [VERBOSE] JSON parsed successfully! Found 7 days
✅ [VERBOSE] Workout plan generated successfully!
📊 [VERBOSE] Generated 7 days of workouts
📊 [VERBOSE] Rendering workout plan...
✅ [VERBOSE] Workout plan rendered successfully!
```

### When Chatting with AI:
```
🔍 [VERBOSE] Processing your question...
✅ [VERBOSE] Using your profile for personalized response
🤖 [VERBOSE] Calling Gemini AI (model: gemini-2.5-flash)...
✅ [VERBOSE] Response received successfully!
```

### If Errors Occur:
```
❌ [VERBOSE] JSON parsing error: Expecting value: line 1 column 1 (char 0)
📄 [VERBOSE] Raw response: {"error": "..."}
```

## 📍 Where to See Verbose Logs:

### 1. In the Browser (Streamlit UI):
- Verbose messages appear in the UI with colored icons
- Look for messages starting with **[VERBOSE]**

### 2. In the Terminal:
- Run this command to see backend logs:
```bash
# View the process output
source venv/bin/activate && streamlit run chatbot_app.py --server.port=8503
```

- The terminal will show:
  - API calls being made
  - Response sizes
  - JSON parsing status
  - Any errors with details

### 3. Check Process Output:
If running in background, check logs with:
```bash
# See what's happening in real-time
tail -f ~/.streamlit/logs/streamlit.log
```

## 🎯 Understanding the Verbose Messages:

| Icon | Meaning |
|------|---------|
| 🔍 | Processing/Analyzing |
| ✅ | Success |
| ❌ | Error |
| 🤖 | AI API Call |
| 📊 | Data Processing |
| 🎯 | Target/Goal Info |
| 💬 | Chat Message |
| 🍽️ | Meal Plan |
| 🏋️ | Workout Plan |

## 🐛 Debugging Tips:

### If Meal Plan Fails:
1. Check the verbose logs for API errors
2. Look for JSON parsing errors
3. Verify your API key is valid
4. Check if you hit rate limits

### If Workout Plan Fails:
1. Same as above
2. Check if the model is available
3. Verify your profile is saved

### If Chat Fails:
1. Check if profile is loaded (optional for chat)
2. Verify API connection
3. Look for rate limit messages

## 🚀 Testing the Verbose Mode:

1. **Open the app:** http://localhost:8503

2. **Fill your profile:**
   - Gender: Male
   - Age: 30
   - Height: 175 cm
   - Weight: 75 kg
   - Goal: Gain Muscle
   - Fitness Level: Intermediate

3. **Click "Generate Meal Plan"** and watch the verbose logs appear

4. **Click "Generate Workout Plan"** and see the detailed process

5. **Ask a question** like "What are the best protein sources?" and see the AI processing

## 📝 Example Test Sequence:

```bash
# 1. Start the app
source venv/bin/activate
streamlit run chatbot_app.py --server.port=8503

# 2. In browser: http://localhost:8503
# 3. Fill profile and save
# 4. Click "Generate Meal Plan"
# 5. Watch verbose logs in both UI and terminal
# 6. Click "Generate Workout Plan"
# 7. Watch verbose logs again
# 8. Ask: "How much protein do I need?"
# 9. See the chat processing logs
```

## 🔧 Troubleshooting:

### Error: "NameError: name 'display_meal_plan' is not defined"
**Status:** ✅ FIXED
- Functions are now defined before they're called
- Restart the app if you still see this

### Error: "API key not valid"
**Solution:**
1. Check your .env file
2. Run: `python test_api_key.py`
3. Get a new key from: https://aistudio.google.com/app/apikey

### Error: "Rate limit exceeded"
**Solution:**
1. Wait 60 seconds
2. The free tier has limits
3. Consider upgrading your API plan

### Error: "JSON parsing failed"
**Solution:**
1. Check the raw response in verbose logs
2. The AI might have returned non-JSON text
3. Try regenerating the plan

## 📊 Performance Monitoring:

The verbose logs show:
- **Prompt length** - How much data you're sending
- **Response length** - How much data you're receiving
- **Processing time** - Implicit from the log sequence
- **Success/failure** - Clear indicators

## 🎓 Learning from Logs:

Use verbose mode to:
- Understand how the AI processes your requests
- Debug issues quickly
- Learn about API interactions
- Monitor your usage
- Optimize your prompts

---

**Your chatbot is now running with full verbose logging at:**
http://localhost:8503

All errors are fixed and you can see exactly what's happening at each step!
