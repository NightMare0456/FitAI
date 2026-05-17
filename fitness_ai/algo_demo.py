from algorithms import (
    bfs_progression, dfs_meal_plan, best_first_search,
    astar_weekly_schedule, minimax_cheat_advisor,
)

DIV  = "=" * 58
LINE = "-" * 58


def _header(title):
    print(f"\n{DIV}\n  {title}\n{DIV}")


def _start_node(experience):
    return {"beginner": "no exercise",
            "intermediate": "jogging",
            "advanced": "running"}.get(experience, "no exercise")


def _target_node(goal, experience):
    if goal == "lose weight":
        return "advanced HIIT" if experience == "advanced" else "HIIT"
    elif goal == "build muscle":
      
        if experience == "beginner":
            return "bodyweight basics"
        else:
            return "circuit training"
    else:
             
        return "long-distance running" if experience == "advanced" else "running"


# ── 1. BFS ──────────────────────────────────────────────────────

def demo_bfs(profile):
    _header("1. BFS — Exercise Progression Path")
    print("  Shortest step-by-step path from your current level")
    print("  to a target exercise (level-by-level exploration).\n")

    start  = _start_node(profile["experience"])
    target = _target_node(profile["goal"], profile["experience"])
    print(f"  Start  : {start}")
    print(f"  Target : {target}\n")

    path = bfs_progression(start, target)
    if path:
        steps = "  →  ".join(f"[{s}]" for s in path)
        print(f"  Path   : {steps}")
        print(f"\n  ✅ Shortest path: {len(path)} step(s)")
    else:
        print("  ❌ No path found.")


# ── 2. DFS ──────────────────────────────────────────────────────

def demo_dfs(profile, stats):
    _header("2. DFS — Meal Combination Explorer")
    print("  Backtracks through all 5-category meal combos to find")
    print("  the best match for BOTH your calorie AND protein targets.\n")

    cal_target  = stats["calorie_target"]
    prot_target = stats["protein_g"]
    print(f"  Calorie Target : {cal_target} kcal  |  Tolerance : ±200 kcal")
    print(f"  Protein Target : {prot_target} g\n")

    result = dfs_meal_plan(cal_target, prot_target, tolerance=200)
    if result:
        label = "✅ Match found (within tolerance):" if result["within_tolerance"] \
                else "✅ Closest combo found:"
        print(f"  {label}")
        print(f"  {'Category':<12}  {'Meal':<32}  {'Protein':>7}  {'Kcal':>5}")
        print(f"  {'-'*12}  {'-'*32}  {'-'*7}  {'-'*5}")
        for cat, meal in result["combo"]:
            print(f"  {cat:<12}  {meal['name']:<32}  "
                  f"{meal['protein']:>6}g  {meal['calories']:>5}")
        print(f"  {LINE}")
        print(f"  {'TOTAL':<46}  {result['total_prot']:>6}g  {result['total_cal']:>5} kcal")
        print(f"\n  Calorie diff : {result['cal_diff']} kcal  "
              f"({'✅ on target' if result['cal_diff'] <= 200 else '⚠ off target'})")
        print(f"  Protein diff : {result['prot_diff']} g  "
              f"({'✅ on target' if result['prot_diff'] <= 15 else '⚠ off target'})")


# ── 3. Best First Search ────────────────────────────────────────

def demo_best_first(profile):
    _header("3. Best First Search — Today's Workout Session")
    print(f"  Greedily picks best exercises using a heuristic for")
    print(f"  goal='{profile['goal']}', level='{profile['experience']}'.\n")

    selected = best_first_search(profile["goal"], profile["experience"], n=6)
    print(f"  {'#':<3}  {'Exercise':<20}  {'Muscle':<12}  "
          f"{'Cal/min':>7}  {'Level':>9}  {'Score':>6}")
    print(f"  {'-'*3}  {'-'*20}  {'-'*12}  {'-'*7}  {'-'*9}  {'-'*6}")
    for rank, item in enumerate(selected, 1):
        ex     = item["exercise"]
        lvl    = ["", "Easy", "Medium", "Hard"][ex["difficulty"]]
        stars  = "★" * ex["difficulty"] + "☆" * (3 - ex["difficulty"])
        print(f"  {rank:<3}  {ex['name']:<20}  {ex['muscle']:<12}  "
              f"{ex['cal_burn']:>7}  {stars:>9}  {item['score']:>6.2f}")
    print(f"\n  ✅ {len(selected)} exercises selected (difficulty ≤ {profile['experience']})")


# ── 4. A* ───────────────────────────────────────────────────────

def demo_astar(profile):
    _header("4. A* Search — Optimal 7-Day Schedule")
    print("  Minimises weekly fatigue g(n) while covering all required")
    print("  workout types h(n). f(n) = g(n) + h(n).\n")

    schedule = astar_weekly_schedule(profile["goal"], profile["experience"])
    if schedule:
        ICONS = {"Rest":"😴","Cardio":"🏃","Upper Body":"💪",
                 "Lower Body":"🦵","Full Body":"🔥","Core":"🎯"}
        print(f"  {'Day':<12}  Workout")
        print(f"  {'-'*12}  {'-'*20}")
        for day, wtype in schedule:
            print(f"  {day:<12}  {ICONS.get(wtype,'•')}  {wtype}")
        print(f"\n  ✅ Optimal schedule for: '{profile['goal']}'")
    else:
        print("  ❌ Could not build schedule.")


# ── 5. Minimax ──────────────────────────────────────────────────

def demo_minimax(stats):
    _header("5. Minimax — Cheat Meal Advisor (Alpha-Beta Pruning)")
    print("  MAX = craving brain (you)  |  MIN = health brain")
    print("  Score = satisfaction − calorie_penalty\n")

    rec, score, all_scores = minimax_cheat_advisor(stats["calorie_target"])
    print(f"  {'Option':<24}  {'Score':>6}")
    print(f"  {'-'*24}  {'-'*6}")
    for name, s in sorted(all_scores.items(), key=lambda x: -x[1]):
        tag = "  ◀ RECOMMENDED" if name == rec else ""
        print(f"  {name:<24}  {s:>6.2f}{tag}")
    print(f"\n  ✅ Minimax picks: {rec}  (score: {score:.2f})")
    print(f"     Best balance of satisfaction vs calorie impact.")


# ── Master runner ────────────────────────────────────────────────

def run_all_algorithms(profile, stats):
    print(f"\n{'#'*58}")
    print(f"  🤖  AI ALGORITHM RESULTS  —  {profile['name'].upper()}")
    print(f"{'#'*58}")
    demo_bfs(profile)
    demo_dfs(profile, stats)
    demo_best_first(profile)
    demo_astar(profile)
    demo_minimax(stats)
    print(f"\n{DIV}")
    print("  All 5 algorithms completed! ✅")
    print(DIV)