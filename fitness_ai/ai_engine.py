import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from groq import Groq


def build_prompt(profile, stats):
    gender_str = "Male" if profile["gender"] == "m" else "Female"
    return (
        "You are a professional fitness coach and nutritionist.\n"
        "Generate a personalised weekly wellness plan based on this data:\n\n"
        f"Name: {profile['name']}\n"
        f"Age: {profile['age']}\n"
        f"Gender: {gender_str}\n"
        f"Weight: {profile['weight_kg']} kg\n"
        f"Height: {profile['height_cm']} cm\n"
        f"Goal: {profile['goal']}\n"
        f"Experience: {profile['experience']}\n"
        f"Activity: {profile['activity']}\n"
        f"Health Conditions: {profile['health_conditions']}\n"
        f"BMI: {stats['bmi']} ({stats['bmi_category']})\n"
        f"Daily Calories: {stats['calorie_target']} kcal\n"
        f"Protein: {stats['protein_g']}g, "
        f"Carbs: {stats['carbs_g']}g, "
        f"Fat: {stats['fat_g']}g\n\n"
        "Write 4 sections:\n"
        "1. WEEKLY WORKOUT ROUTINE (7 days)\n"
        "2. DAILY MEAL PLAN\n"
        "3. SLEEP AND RECOVERY TIPS\n"
        "4. PERSONALISED TIPS\n"
    )


def generate_ai_plan(profile, stats):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("No API key found in .env file")
        return None
    try:
        client = Groq(api_key=api_key)
        prompt = build_prompt(profile, stats)
        print("Generating AI plan...")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2500,
        )
        text = response.choices[0].message.content
        print(text)
        return text
    except Exception as e:
        print(f"Error: {e}")
        return None