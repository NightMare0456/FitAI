def get_user_profile():
    print("\n" + "=" * 55)
    print("       AI FITNESS & WELLNESS PLANNER")
    print("=" * 55)

    name = input("\nEnter your name: ").strip()
    age  = int(input("Age: "))

    gender = ""
    while gender not in ["m", "f"]:
        gender = input("Gender (m/f): ").strip().lower()

    weight = float(input("Weight (kg): "))
    height = float(input("Height (cm): "))

    print("\nFitness Goal:")
    print("  1. Lose Weight")
    print("  2. Build Muscle")
    print("  3. Maintain / Stay Fit")
    goal_map = {"1": "lose weight", "2": "build muscle", "3": "maintain fitness"}
    goal = goal_map.get(input("Choose (1/2/3): ").strip(), "maintain fitness")

    print("\nExperience Level:")
    print("  1. Beginner")
    print("  2. Intermediate")
    print("  3. Advanced")
    level_map = {"1": "beginner", "2": "intermediate", "3": "advanced"}
    experience = level_map.get(input("Choose (1/2/3): ").strip(), "beginner")

    print("\nActivity Level:")
    print("  1. Sedentary (little/no exercise)")
    print("  2. Lightly Active (1-3 days/week)")
    print("  3. Moderately Active (3-5 days/week)")
    print("  4. Very Active (6-7 days/week)")
    activity_map = {
        "1": "sedentary", "2": "lightly active",
        "3": "moderately active", "4": "very active"
    }
    activity = activity_map.get(input("Choose (1/2/3/4): ").strip(), "sedentary")

    raw = input("\nAny health conditions or injuries?\n(e.g. back pain, diabetes, knee issues — or press Enter to skip): ").strip()
    health_conditions = raw if raw else "None"

    return {
        "name":              name,
        "age":               age,
        "gender":            gender,
        "weight_kg":         weight,
        "height_cm":         height,
        "goal":              goal,
        "experience":        experience,
        "activity":          activity,
        "health_conditions": health_conditions,
    }
