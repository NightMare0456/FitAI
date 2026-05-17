from collections import deque
import heapq


EXERCISE_GRAPH = {
    "no exercise":       ["walking", "stretching"],
    "walking":           ["jogging", "cycling"],
    "stretching":        ["yoga", "bodyweight basics"],
    "jogging":           ["running", "HIIT"],
    "cycling":           ["spinning", "interval cycling"],
    "yoga":              ["advanced yoga", "pilates"],
    "bodyweight basics": ["push-ups", "squats", "planks"],
    "running":           ["sprints", "long-distance running"],
    "HIIT":              ["advanced HIIT", "circuit training"],
    "push-ups":          ["diamond push-ups", "archer push-ups"],
    "squats":            ["jump squats", "pistol squats"],
    "planks":            ["side planks", "RKC plank"],
    "spinning":          [],
    "interval cycling":  [],
    "advanced yoga":     [],
    "pilates":           [],
    "sprints":           [],
    "long-distance running": [],
    "advanced HIIT":     [],
    "circuit training":  [],
    "diamond push-ups":  [],
    "archer push-ups":   [],
    "jump squats":       [],
    "pistol squats":     [],
    "side planks":       [],
    "RKC plank":         [],
}


EXERCISES = [
    {"name": "Deadlift",        "cal_burn": 8,  "muscle": "Full Body", "difficulty": 3},
    {"name": "Squat",           "cal_burn": 7,  "muscle": "Legs",      "difficulty": 2},
    {"name": "Bench Press",     "cal_burn": 6,  "muscle": "Chest",     "difficulty": 2},
    {"name": "Pull-ups",        "cal_burn": 7,  "muscle": "Back",      "difficulty": 3},
    {"name": "Plank",           "cal_burn": 3,  "muscle": "Core",      "difficulty": 1},
    {"name": "Burpees",         "cal_burn": 10, "muscle": "Full Body", "difficulty": 3},
    {"name": "Jump Rope",       "cal_burn": 11, "muscle": "Cardio",    "difficulty": 1},
    {"name": "Bicep Curl",      "cal_burn": 3,  "muscle": "Arms",      "difficulty": 1},
    {"name": "Lunges",          "cal_burn": 5,  "muscle": "Legs",      "difficulty": 1},
    {"name": "Push-ups",        "cal_burn": 5,  "muscle": "Chest",     "difficulty": 1},
    {"name": "Russian Twists",  "cal_burn": 4,  "muscle": "Core",      "difficulty": 2},
    {"name": "Box Jumps",       "cal_burn": 9,  "muscle": "Full Body", "difficulty": 2},
    {"name": "Shoulder Press",  "cal_burn": 5,  "muscle": "Shoulders", "difficulty": 2},
    {"name": "Leg Press",       "cal_burn": 6,  "muscle": "Legs",      "difficulty": 2},
    {"name": "Mountain Climbers","cal_burn": 8, "muscle": "Core",      "difficulty": 2},
    {"name": "Dumbbell Row",    "cal_burn": 5,  "muscle": "Back",      "difficulty": 1},
]


MAX_DIFFICULTY = {"beginner": 1, "intermediate": 2, "advanced": 3}


MEALS = {
    "Breakfast": [
        {"name": "Oats + Banana + PB",        "calories": 480, "protein": 18},
        {"name": "Scrambled Eggs + Toast",    "calories": 420, "protein": 26},
        {"name": "Greek Yogurt + Berries",    "calories": 290, "protein": 20},
        {"name": "Protein Shake + Oats",      "calories": 520, "protein": 38},
        {"name": "Egg Omelette + Veggies",    "calories": 380, "protein": 28},
        {"name": "Oats + Eggs + Milk",        "calories": 600, "protein": 36},
        {"name": "Pancakes + Eggs + Syrup",   "calories": 650, "protein": 24},
    ],
    "Lunch": [
        {"name": "Chicken Rice Bowl",         "calories": 650, "protein": 45},
        {"name": "Tuna Salad Wrap",           "calories": 500, "protein": 36},
        {"name": "Lentil Soup + Bread",       "calories": 540, "protein": 24},
        {"name": "Grilled Salmon + Quinoa",   "calories": 620, "protein": 48},
        {"name": "Turkey Sandwich + Salad",   "calories": 560, "protein": 38},
        {"name": "Beef Rice Bowl + Egg",      "calories": 780, "protein": 52},
        {"name": "Pasta + Chicken + Sauce",   "calories": 720, "protein": 44},
    ],
    "Dinner": [
        {"name": "Beef Stir Fry + Rice",      "calories": 680, "protein": 44},
        {"name": "Chicken Curry + Rice",      "calories": 640, "protein": 42},
        {"name": "Pasta + Lean Mince",        "calories": 600, "protein": 38},
        {"name": "Fish + Sweet Potato",       "calories": 550, "protein": 42},
        {"name": "Grilled Chicken + Veggies", "calories": 500, "protein": 46},
        {"name": "Steak + Rice + Salad",      "calories": 800, "protein": 58},
        {"name": "Salmon + Pasta + Butter",   "calories": 760, "protein": 48},
    ],
    "Snack 1": [
        {"name": "Protein Bar",               "calories": 210, "protein": 20},
        {"name": "Handful of Nuts",           "calories": 190, "protein":  6},
        {"name": "Apple + Peanut Butter",     "calories": 230, "protein":  8},
        {"name": "Cottage Cheese",            "calories": 160, "protein": 18},
        {"name": "Boiled Eggs (2)",           "calories": 155, "protein": 13},
        {"name": "PB + Banana Smoothie",      "calories": 380, "protein": 14},
    ],
    "Snack 2": [
        {"name": "Protein Shake",             "calories": 300, "protein": 30},
        {"name": "Banana + Milk",             "calories": 260, "protein": 10},
        {"name": "Rice Cakes + PB",           "calories": 220, "protein":  8},
        {"name": "Dates + Almonds",           "calories": 250, "protein":  6},
        {"name": "Hummus + Pita",             "calories": 280, "protein": 10},
        {"name": "Mass Gainer Shake",         "calories": 500, "protein": 32},
    ],
}

CHEAT_OPTIONS = {
    "Pizza (2 slices)":  {"calories": 600, "satisfaction": 9},
    "Burger + Fries":    {"calories": 900, "satisfaction": 9},
    "Ice Cream (1 cup)": {"calories": 350, "satisfaction": 7},
    "Dark Chocolate":    {"calories": 200, "satisfaction": 6},
    "Fried Chicken":     {"calories": 700, "satisfaction": 8},
    "Slice of Cake":     {"calories": 450, "satisfaction": 7},
    "Samosa (2 pcs)":    {"calories": 300, "satisfaction": 7},
    "Skip cheat meal":   {"calories": 0,   "satisfaction": 1},
}


# ═══════════════════════════════════════════════════════════════
#  1. BFS — Exercise Progression Finder
# ═══════════════════════════════════════════════════════════════

def bfs_progression(start: str, target: str):
    """
    BFS level-by-level search — guarantees the SHORTEST path
    (fewest progression steps) from start exercise to target.
    """
    if start == target:
        return [start]
    if start not in EXERCISE_GRAPH:
        return None

    visited = {start}
    queue   = deque([[start]])

    while queue:
        path = queue.popleft()
        node = path[-1]
        for neighbour in EXERCISE_GRAPH.get(node, []):
            if neighbour not in visited:
                new_path = path + [neighbour]
                if neighbour == target:
                    return new_path
                visited.add(neighbour)
                queue.append(new_path)
    return None


# ═══════════════════════════════════════════════════════════════
#  2. DFS — Meal Combination Explorer
# ═══════════════════════════════════════════════════════════════

def dfs_meal_plan(calorie_target: int, protein_target: int, tolerance: int = 200):
    """
    DFS with backtracking exhaustively explores all 5-category
    meal combinations and returns the combo closest to BOTH
    the calorie target and protein target using a combined score.

    Score = calorie_diff + protein_diff * 3
    (protein weighted higher so it's not ignored when cal is close)
    """
    categories = list(MEALS.keys())
    best = {"combo": None, "total_cal": 0, "total_prot": 0,
            "cal_diff": float("inf"), "prot_diff": float("inf"),
            "score": float("inf"), "within_tolerance": False}

    def dfs(idx, combo, cals, prot):
        if idx == len(categories):
            cal_diff  = abs(cals  - calorie_target)
            prot_diff = abs(prot  - protein_target)
            score     = cal_diff + prot_diff * 3   # weighted combined score
            if score < best["score"]:
                best["combo"]            = list(combo)
                best["total_cal"]        = cals
                best["total_prot"]       = prot
                best["cal_diff"]         = cal_diff
                best["prot_diff"]        = prot_diff
                best["score"]            = score
                best["within_tolerance"] = cal_diff <= tolerance
            return
        for meal in MEALS[categories[idx]]:
            combo.append((categories[idx], meal))
            dfs(idx + 1, combo, cals + meal["calories"], prot + meal["protein"])
            combo.pop()

    dfs(0, [], 0, 0)
    return best if best["combo"] else None


# ═══════════════════════════════════════════════════════════════
#  3. Best First Search — Exercise Session Builder
# ═══════════════════════════════════════════════════════════════

def best_first_search(goal: str, experience: str, n: int = 6):
    """
    Greedy Best First Search — expands the highest heuristic node.
    Exercises are filtered by difficulty for the user's experience level.

    Heuristic by goal:
      lose weight  → prioritise calorie burn
      build muscle → balance burn + difficulty
      maintain     → balanced score
    """
    max_diff = MAX_DIFFICULTY.get(experience, 3)

    # Filter pool to appropriate difficulty
    pool = [ex for ex in EXERCISES if ex["difficulty"] <= max_diff]

    def heuristic(ex):
        if goal == "lose weight":
            return ex["cal_burn"]
        elif goal == "build muscle":
            return ex["cal_burn"] * 0.5 + ex["difficulty"] * 2.5
        else:
            return ex["cal_burn"] * 0.6 + ex["difficulty"] * 1.5

    heap = [(-heuristic(ex), i, ex) for i, ex in enumerate(pool)]
    heapq.heapify(heap)

    selected, seen = [], set()
    while heap and len(selected) < n:
        neg_score, _, ex = heapq.heappop(heap)
        if ex["name"] not in seen:
            seen.add(ex["name"])
            selected.append({"exercise": ex, "score": round(-neg_score, 2)})
    return selected


# ═══════════════════════════════════════════════════════════════
#  4. A* — Weekly Workout Scheduler
# ═══════════════════════════════════════════════════════════════

DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
WORKOUT_TYPES = ["Rest","Cardio","Upper Body","Lower Body","Full Body","Core"]

FATIGUE_COST = {
    "Rest": 0, "Core": 1, "Cardio": 2,
    "Upper Body": 3, "Lower Body": 3, "Full Body": 5,
}

GOAL_TARGETS = {
    "lose weight":     {"Cardio": 3, "Full Body": 2, "Core": 1, "Rest": 1},
    "build muscle":    {"Upper Body": 2, "Lower Body": 2, "Full Body": 1, "Core": 1, "Rest": 1},
    "maintain fitness":{"Cardio": 2, "Upper Body": 1, "Lower Body": 1, "Core": 1, "Rest": 2},
}


def astar_weekly_schedule(goal: str, experience: str):
    """
    A* minimises total weekly fatigue (g) while ensuring all
    required workout types are met (h = unmet slots remaining).
    """
    target = dict(GOAL_TARGETS.get(goal, GOAL_TARGETS["maintain fitness"]))
    if experience == "beginner" and "Full Body" in target:
        extra = target.pop("Full Body")
        target["Cardio"] = target.get("Cardio", 0) + extra

    def heuristic(state):
        counts = {}
        for w in state:
            counts[w] = counts.get(w, 0) + 1
        return sum(max(0, need - counts.get(wt, 0))
                   for wt, need in target.items())

    open_set = [(heuristic(()), 0, 0, ())]
    best_g   = {}

    while open_set:
        f, _, g, state = heapq.heappop(open_set)
        if len(state) == 7 and heuristic(state) == 0:
            return list(zip(DAYS, state))
        if best_g.get(state, float("inf")) < g:
            continue
        best_g[state] = g
        if len(state) == 7:
            continue
        for wt in WORKOUT_TYPES:
            ns   = state + (wt,)
            ng   = g + FATIGUE_COST[wt]
            h    = heuristic(ns)
            heapq.heappush(open_set, (ng + h, ng, ng, ns))
    return None


# ═══════════════════════════════════════════════════════════════
#  5. Minimax — Cheat Meal Advisor (with Alpha-Beta Pruning)
# ═══════════════════════════════════════════════════════════════

def _score(vals):
    """Leaf eval: satisfaction minus calorie penalty (1000 kcal ≈ -5 pts)."""
    return vals["satisfaction"] - (vals["calories"] / 200)


def _minimax(options, depth, is_max, alpha, beta):
    """Minimax with alpha-beta pruning. MAX=craving, MIN=health brain."""
    if depth == 0 or not options:
        return 0.0, None

    if is_max:
        best_v, best_o = -float("inf"), None
        for name, vals in options.items():
            rest = {k: v for k, v in options.items() if k != name}
            cv, _ = _minimax(rest, depth - 1, False, alpha, beta)
            total = _score(vals) + 0.25 * cv
            if total > best_v:
                best_v, best_o = total, name
            alpha = max(alpha, best_v)
            if beta <= alpha:
                break
        return best_v, best_o
    else:
        best_v, best_o = float("inf"), None
        for name, vals in options.items():
            rest = {k: v for k, v in options.items() if k != name}
            cv, _ = _minimax(rest, depth - 1, True, alpha, beta)
            total = _score(vals) + 0.25 * cv
            if total < best_v:
                best_v, best_o = total, name
            beta = min(beta, best_v)
            if beta <= alpha:
                break
        return best_v, best_o


def minimax_cheat_advisor(calorie_budget: int):
    affordable = {k: v for k, v in CHEAT_OPTIONS.items()
                  if v["calories"] <= calorie_budget + 300}
    all_scores = {n: round(_score(v), 2) for n, v in affordable.items()}
    _, recommended = _minimax(affordable, depth=3,
                               is_max=True,
                               alpha=-float("inf"), beta=float("inf"))
    return recommended, all_scores.get(recommended, 0), all_scores