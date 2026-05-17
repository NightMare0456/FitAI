import sys
from io import StringIO

from user_profile import get_user_profile
from rule_engine  import get_stats, display_stats
from algo_demo    import run_all_algorithms

DIVIDER = "=" * 55

def main():
    try:
        profile = get_user_profile()
        stats   = get_stats(profile)
        display_stats(profile, stats)

        # Capture algorithm output so we can save it too
        old_stdout = sys.stdout
        sys.stdout = buffer = StringIO()
        run_all_algorithms(profile, stats)
        sys.stdout = old_stdout
        algo_output = buffer.getvalue()
        print(algo_output)  # still show it on screen

        save = input("\n💾  Save results to a text file? (y/n): ").strip().lower()
        if save == "y":
            filename = f"{profile['name'].replace(' ', '_')}_fitness_plan.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"FITNESS PLAN FOR {profile['name'].upper()}\n")
                f.write(DIVIDER + "\n\n")
                f.write("STATS\n")
                f.write(f"  BMI           : {stats['bmi']} ({stats['bmi_category']})\n")
                f.write(f"  Daily Calories: {stats['calorie_target']} kcal\n")
                f.write(f"  Protein       : {stats['protein_g']} g\n")
                f.write(f"  Carbs         : {stats['carbs_g']} g\n")
                f.write(f"  Fat           : {stats['fat_g']} g\n\n")
                f.write("ALGORITHM RESULTS\n")
                f.write(DIVIDER + "\n")
                f.write(algo_output)
            print(f"✅  Saved as: {filename}")

        print("\n👋  Stay consistent — great things take time!\n")

    except KeyboardInterrupt:
        print("\n\nExited. See you next time!")
        sys.exit(0)

if __name__ == "__main__":
    main()
