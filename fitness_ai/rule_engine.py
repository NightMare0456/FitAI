"""
rule_engine.py
==============
All health calculations — BMI, TDEE, calories, macros, water, body fat.

KEY FIX: Protein is now weight-based (g per kg bodyweight),
not a % of calories. This gives realistic, safe values.
"""


# ── BMI ────────────────────────────────────────────────────────

def calculate_bmi(weight_kg, height_cm):
    h = height_cm / 100
    bmi = round(weight_kg / (h ** 2), 1)
    if bmi < 18.5:
        cat = "Underweight"
    elif bmi < 25.0:
        cat = "Normal"
    elif bmi < 30.0:
        cat = "Overweight"
    else:
        cat = "Obese"
    return bmi, cat


# ── Ideal weight range (Devine formula) ────────────────────────

def ideal_weight_range(height_cm, gender):
    h_in = (height_cm - 152.4) / 2.54
    if gender == "m":
        base = 50.0 + 2.3 * h_in
    else:
        base = 45.5 + 2.3 * h_in
    low  = round(max(base - 5, 30), 1)
    high = round(base + 5, 1)
    return low, high


# ── BMR + TDEE (Mifflin-St Jeor) ──────────────────────────────

def calculate_tdee(weight_kg, height_cm, age, gender, activity):
    if gender == "m":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    multipliers = {
        "sedentary":         1.200,
        "lightly active":    1.375,
        "moderately active": 1.550,
        "very active":       1.725,
    }
    return round(bmr * multipliers.get(activity, 1.2))


# ── Calorie target ─────────────────────────────────────────────

def get_calorie_target(tdee, goal):
    if goal == "lose weight":
        return tdee - 500       # ~0.5 kg/week deficit
    elif goal == "build muscle":
        return tdee + 300       # lean bulk surplus
    return tdee


# ── Macros (weight-based protein, NOT % of calories) ──────────

PROTEIN_PER_KG = {
    "lose weight":     1.87,   # high to preserve muscle in deficit
    "build muscle":    1.67,   # standard muscle building
    "maintain fitness":1.47,   # general health
}

CARB_RATIO = {
    "lose weight":     0.40,  # of remaining cals after protein+fat
    "build muscle":    0.50,
    "maintain fitness":0.45,
}

def get_macros(calories, goal, weight_kg):
    """
    1. Calculate protein from bodyweight (g/kg) — most accurate method.
    2. Fat = 25–30% of total calories.
    3. Carbs = whatever is left.
    """
    # Protein (weight-based)
    protein_g = round(weight_kg * PROTEIN_PER_KG.get(goal, 1.6))
    protein_kcal = protein_g * 4

    # Fat (25% of total calories)
    fat_kcal = round(calories * 0.25)
    fat_g = round(fat_kcal / 9)

    # Carbs = remainder
    remaining_kcal = calories - protein_kcal - fat_kcal
    carbs_g = round(max(remaining_kcal, 0) / 4)

    return protein_g, carbs_g, fat_g


# ── Water intake ───────────────────────────────────────────────

def water_intake_litres(weight_kg, activity):
    base = weight_kg * 0.033
    bonus = {"moderately active": 0.35, "very active": 0.6}.get(activity, 0)
    return round(base + bonus, 1)


# ── Body fat estimate (Deurenberg formula) ─────────────────────

def body_fat_estimate(bmi, age, gender):
    sex = 1 if gender == "m" else 0
    bf = (1.20 * bmi) + (0.23 * age) - (10.8 * sex) - 5.4
    return round(bf, 1)


# ── Master stat builder ────────────────────────────────────────

def get_stats(profile):
    bmi, bmi_cat   = calculate_bmi(profile["weight_kg"], profile["height_cm"])
    ideal_low, ideal_high = ideal_weight_range(profile["height_cm"], profile["gender"])
    tdee           = calculate_tdee(
                         profile["weight_kg"], profile["height_cm"],
                         profile["age"], profile["gender"], profile["activity"])
    cal_target     = get_calorie_target(tdee, profile["goal"])
    protein, carbs, fat = get_macros(cal_target, profile["goal"], profile["weight_kg"])
    water          = water_intake_litres(profile["weight_kg"], profile["activity"])
    body_fat       = body_fat_estimate(bmi, profile["age"], profile["gender"])

    return {
        "bmi":            bmi,
        "bmi_category":   bmi_cat,
        "ideal_low":      ideal_low,
        "ideal_high":     ideal_high,
        "tdee":           tdee,
        "calorie_target": cal_target,
        "protein_g":      protein,
        "carbs_g":        carbs,
        "fat_g":          fat,
        "water_l":        water,
        "body_fat_pct":   body_fat,
    }


# ── Display ────────────────────────────────────────────────────

def display_stats(profile, stats):
    print("\n" + "=" * 55)
    print(f"  📊  STATS FOR {profile['name'].upper()}")
    print("=" * 55)
    print(f"  BMI              : {stats['bmi']}  ({stats['bmi_category']})")
    print(f"  Body Fat (est.)  : {stats['body_fat_pct']}%")
    print(f"  Ideal Weight     : {stats['ideal_low']} – {stats['ideal_high']} kg")
    print(f"  Maintenance kcal : {stats['tdee']} kcal/day")
    print(f"  Target kcal      : {stats['calorie_target']} kcal/day")
    print(f"  Protein          : {stats['protein_g']} g  "
          f"({PROTEIN_PER_KG.get(profile['goal'], 1.6)}g × {profile['weight_kg']}kg)")
    print(f"  Carbohydrates    : {stats['carbs_g']} g")
    print(f"  Fat              : {stats['fat_g']} g")
    print(f"  Water            : {stats['water_l']} L/day")
    print("=" * 55)