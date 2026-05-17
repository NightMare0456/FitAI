"""
gui.py — Professional Desktop GUI for AI Fitness & Wellness Planner
Uses CustomTkinter for a modern, rounded, polished look.

Install : pip install customtkinter
Run     : python gui.py
"""

import sys, threading
from io import StringIO
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from rule_engine import get_stats, PROTEIN_PER_KG
from algo_demo   import run_all_algorithms

# ── Global theme ──────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

BG     = "#0b0d14"
PANEL  = "#111420"
CARD   = "#161926"
CARD2  = "#1c2030"
ACCENT = "#00e676"
CYAN   = "#00bcd4"
TEXT   = "#e8eaf6"
MUTED  = "#5a6070"
WARN   = "#ffb74d"

FH1  = ("Segoe UI", 22, "bold")
FH2  = ("Segoe UI", 14, "bold")
FSM  = ("Segoe UI", 11)
FXS  = ("Segoe UI",  9)
FM   = ("Consolas", 10)


# ══════════════════════════════════════════════════════════════
class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("AI Fitness & Wellness Planner")
        self.geometry("1120x740")
        self.minsize(980, 660)
        self.configure(fg_color=BG)
        self._profile = None
        self._stats   = None
        self._build()

    # ── Layout ────────────────────────────────────────────────
    def _build(self):
        self.sidebar = ctk.CTkFrame(self, width=230, fg_color=PANEL,
                                    corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.body = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.body.pack(side="left", fill="both", expand=True)

        self._build_sidebar()

        self.pages = {}
        for name in ("profile", "stats", "algorithms"):
            f = ctk.CTkFrame(self.body, fg_color=BG, corner_radius=0)
            self.pages[name] = f

        self._build_profile_page()
        self._build_stats_page()
        self._build_algo_page()
        self._show("profile")

    # ── Sidebar ───────────────────────────────────────────────
    def _build_sidebar(self):
        logo = ctk.CTkFrame(self.sidebar, fg_color=CARD, corner_radius=0)
        logo.pack(fill="x")
        ctk.CTkLabel(logo, text="🏋️", font=("Segoe UI", 44),
                     text_color=ACCENT).pack(pady=(30, 2))
        ctk.CTkLabel(logo, text="FitAI", font=("Segoe UI", 24, "bold"),
                     text_color=ACCENT).pack()
        ctk.CTkLabel(logo, text="Wellness Planner", font=FXS,
                     text_color=MUTED).pack(pady=(2, 24))

        ctk.CTkFrame(self.sidebar, height=1, fg_color=CARD2).pack(fill="x")

        self._nav_btns = {}
        nav = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav.pack(fill="x", padx=12, pady=16)

        for key, icon, label in [
            ("profile",    "👤", "Profile"),
            ("stats",      "📊", "My Stats"),
            ("algorithms", "🤖", "Algorithms"),
        ]:
            btn = ctk.CTkButton(
                nav, text=f"  {icon}  {label}",
                font=("Segoe UI", 12, "bold"),
                anchor="w", height=46, corner_radius=10,
                fg_color="transparent", text_color=TEXT,
                hover_color=CARD2,
                command=lambda k=key: self._show(k),
            )
            btn.pack(fill="x", pady=3)
            self._nav_btns[key] = btn

        # Algorithm tags at bottom
        ctk.CTkFrame(self.sidebar, height=1,
                     fg_color=CARD2).pack(fill="x", side="bottom", pady=0)
        info = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        info.pack(side="bottom", padx=16, pady=14)
        ctk.CTkLabel(info, text="Algorithms used", font=FXS,
                     text_color=MUTED).pack(anchor="w", pady=(0, 6))
        tags_frame = ctk.CTkFrame(info, fg_color="transparent")
        tags_frame.pack(anchor="w")
        tags = [("BFS", ACCENT), ("DFS", ACCENT), ("Best First", CYAN),
                ("A*", CYAN), ("Minimax", WARN)]
        for i, (t, col) in enumerate(tags):
            ctk.CTkLabel(tags_frame, text=t, font=("Segoe UI", 8, "bold"),
                         text_color=BG, fg_color=col,
                         corner_radius=6, width=62, height=20
                         ).grid(row=i//3, column=i%3, padx=2, pady=2)

    def _show(self, name):
        for f in self.pages.values():
            f.pack_forget()
        self.pages[name].pack(fill="both", expand=True)
        for k, btn in self._nav_btns.items():
            btn.configure(fg_color=CARD if k == name else "transparent",
                          text_color=ACCENT if k == name else TEXT)

    # ── Page header ───────────────────────────────────────────
    def _page_header(self, parent, icon, title, sub):
        hdr = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=0)
        hdr.pack(fill="x")
        inner = ctk.CTkFrame(hdr, fg_color="transparent")
        inner.pack(anchor="w", padx=28, pady=16)
        ctk.CTkLabel(inner, text=f"{icon}  {title}",
                     font=FH1, text_color=ACCENT).pack(anchor="w")
        ctk.CTkLabel(inner, text=sub, font=FXS,
                     text_color=MUTED).pack(anchor="w", pady=(2,0))

    # ══════════════════════════════════════════════════════════
    #  PROFILE PAGE
    # ══════════════════════════════════════════════════════════
    def _build_profile_page(self):
        page = self.pages["profile"]
        self._page_header(page, "👤", "Your Profile",
                          "Enter your details to generate a personalised plan")

        scroll = ctk.CTkScrollableFrame(page, fg_color=BG, corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=24, pady=16)
        scroll.grid_columnconfigure(0, weight=1)
        scroll.grid_columnconfigure(1, weight=1)

        left  = ctk.CTkFrame(scroll, fg_color=CARD, corner_radius=16)
        right = ctk.CTkFrame(scroll, fg_color=CARD, corner_radius=16)
        left.grid(row=0, column=0, sticky="nsew", padx=(0,10))
        right.grid(row=0, column=1, sticky="nsew", padx=(10,0))

        self._inputs = {}

        def section(parent, title):
            ctk.CTkLabel(parent, text=title, font=FH2,
                         text_color=ACCENT).pack(anchor="w", padx=22, pady=(20,4))
            ctk.CTkFrame(parent, height=1, fg_color=CARD2).pack(fill="x", padx=22, pady=(0,10))

        def text_field(parent, key, label, ph):
            f = ctk.CTkFrame(parent, fg_color="transparent")
            f.pack(fill="x", padx=22, pady=5)
            ctk.CTkLabel(f, text=label, font=FXS, text_color=MUTED).pack(anchor="w")
            e = ctk.CTkEntry(f, placeholder_text=ph, height=42,
                             corner_radius=10, border_width=1,
                             border_color=CARD2, fg_color=CARD2,
                             text_color=TEXT, placeholder_text_color=MUTED,
                             font=FSM)
            e.pack(fill="x", pady=(3,0))
            self._inputs[key] = e

        def combo_field(parent, key, label, opts):
            f = ctk.CTkFrame(parent, fg_color="transparent")
            f.pack(fill="x", padx=22, pady=5)
            ctk.CTkLabel(f, text=label, font=FXS, text_color=MUTED).pack(anchor="w")
            c = ctk.CTkComboBox(f, values=opts, height=42, corner_radius=10,
                                border_width=1, border_color=CARD2,
                                fg_color=CARD2, text_color=TEXT,
                                button_color=ACCENT,
                                button_hover_color="#00c853",
                                dropdown_fg_color=CARD,
                                dropdown_text_color=TEXT,
                                dropdown_hover_color=CARD2,
                                font=FSM, state="readonly")
            c.set(opts[0])
            c.pack(fill="x", pady=(3,0))
            self._inputs[key] = c

        # Left column
        section(left, "Personal Info")
        text_field(left, "name",   "Full Name",   "e.g. Asif")
        text_field(left, "age",    "Age",         "e.g. 21")
        text_field(left, "weight", "Weight (kg)", "e.g. 70")
        text_field(left, "height", "Height (cm)", "e.g. 172")

        gf = ctk.CTkFrame(left, fg_color="transparent")
        gf.pack(fill="x", padx=22, pady=8)
        ctk.CTkLabel(gf, text="Gender", font=FXS, text_color=MUTED).pack(anchor="w")
        gr = ctk.CTkFrame(gf, fg_color="transparent")
        gr.pack(anchor="w", pady=(4,0))
        self._gender = ctk.StringVar(value="m")
        for txt, val in [("Male","m"),("Female","f")]:
            ctk.CTkRadioButton(gr, text=txt, variable=self._gender, value=val,
                               fg_color=ACCENT, hover_color="#00c853",
                               text_color=TEXT, font=FSM).pack(side="left", padx=(0,20))
        ctk.CTkFrame(left, height=18, fg_color="transparent").pack()

        # Right column
        section(right, "Fitness Info")
        combo_field(right, "goal", "Fitness Goal",
                    ["lose weight", "build muscle", "maintain fitness"])
        combo_field(right, "experience", "Experience Level",
                    ["beginner", "intermediate", "advanced"])
        combo_field(right, "activity", "Activity Level",
                    ["sedentary", "lightly active", "moderately active", "very active"])

        hf = ctk.CTkFrame(right, fg_color="transparent")
        hf.pack(fill="x", padx=22, pady=5)
        ctk.CTkLabel(hf, text="Health Conditions / Injuries",
                     font=FXS, text_color=MUTED).pack(anchor="w")
        self._health = ctk.CTkTextbox(hf, height=90, corner_radius=10,
                                      border_width=1, border_color=CARD2,
                                      fg_color=CARD2, text_color=TEXT, font=FSM)
        self._health.insert("1.0", "None")
        self._health.pack(fill="x", pady=(3,0))
        ctk.CTkFrame(right, height=18, fg_color="transparent").pack()

        # Generate button
        btn_wrap = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_wrap.grid(row=1, column=0, columnspan=2, pady=20)
        self._gen_btn = ctk.CTkButton(
            btn_wrap, text="⚡   GENERATE MY PLAN",
            font=("Segoe UI", 14, "bold"),
            height=54, width=320, corner_radius=14,
            fg_color=ACCENT, hover_color="#00c853",
            text_color=BG, command=self._on_generate)
        self._gen_btn.pack()
        self._status = ctk.CTkLabel(btn_wrap, text="", font=FXS, text_color=MUTED)
        self._status.pack(pady=5)

    # ══════════════════════════════════════════════════════════
    #  STATS PAGE
    # ══════════════════════════════════════════════════════════
    def _build_stats_page(self):
        page = self.pages["stats"]
        self._page_header(page, "📊", "My Stats", "Your personalised health metrics")
        self._stats_body = ctk.CTkScrollableFrame(page, fg_color=BG, corner_radius=0)
        self._stats_body.pack(fill="both", expand=True, padx=24, pady=16)
        ctk.CTkLabel(self._stats_body,
                     text="Generate your plan first → go to the Profile tab",
                     font=FSM, text_color=MUTED).pack(pady=80)

    def _render_stats(self, profile, stats):
        for w in self._stats_body.winfo_children():
            w.destroy()

        # Greeting
        g = ctk.CTkFrame(self._stats_body, fg_color=CARD, corner_radius=16)
        g.pack(fill="x", pady=(0,14))
        gi = ctk.CTkFrame(g, fg_color="transparent")
        gi.pack(anchor="w", padx=24, pady=16)
        ctk.CTkLabel(gi, text=f"Hey {profile['name']} 👋",
                     font=FH2, text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(gi,
                     text=f"{profile['goal'].title()}  ·  "
                          f"{profile['experience'].title()}  ·  "
                          f"{profile['activity'].title()}",
                     font=FXS, text_color=MUTED).pack(anchor="w", pady=(4,0))

        # Stat pills — row 1
        def pill(parent, label, value, unit, col):
            p = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=14)
            p.grid(row=0, column=parent._col, sticky="ew",
                   padx=5, pady=4, ipadx=10, ipady=10)
            parent.grid_columnconfigure(parent._col, weight=1)
            parent._col += 1
            ctk.CTkLabel(p, text=label, font=FXS, text_color=MUTED).pack()
            ctk.CTkLabel(p, text=str(value),
                         font=("Segoe UI", 20, "bold"), text_color=col).pack()
            ctk.CTkLabel(p, text=unit, font=FXS, text_color=MUTED).pack()

        row1 = ctk.CTkFrame(self._stats_body, fg_color="transparent")
        row1.pack(fill="x", pady=(0,8))
        row1._col = 0
        pill(row1, "BMI",       stats["bmi"],            stats["bmi_category"], ACCENT)
        pill(row1, "Calories",  stats["calorie_target"], "kcal/day",            CYAN)
        pill(row1, "Body Fat",  f"{stats['body_fat_pct']}%", "estimate",        WARN)
        pill(row1, "Water",     f"{stats['water_l']}L",  "per day",             "#ab47bc")

        row2 = ctk.CTkFrame(self._stats_body, fg_color="transparent")
        row2.pack(fill="x", pady=(0,14))
        row2._col = 0
        pill(row2, "Protein",  f"{stats['protein_g']}g",
             f"{PROTEIN_PER_KG.get(profile['goal'],1.6)}g/kg", "#ef9a9a")
        pill(row2, "Carbs",    f"{stats['carbs_g']}g",   "per day", "#ff7043")
        pill(row2, "Fat",      f"{stats['fat_g']}g",     "per day", "#ffa726")
        pill(row2, "Ideal Wt", f"{stats['ideal_low']}–{stats['ideal_high']}kg", "range", "#66bb6a")

        # Detail table
        detail = ctk.CTkFrame(self._stats_body, fg_color=CARD, corner_radius=16)
        detail.pack(fill="x", pady=(0,16))
        ctk.CTkLabel(detail, text="Full Breakdown", font=FH2,
                     text_color=CYAN).pack(anchor="w", padx=24, pady=(16,8))
        ctk.CTkFrame(detail, height=1, fg_color=CARD2).pack(fill="x", padx=24)

        rows = [
            ("Maintenance Calories", f"{stats['tdee']} kcal/day"),
            ("Target Calories",      f"{stats['calorie_target']} kcal/day"),
            ("BMI",                  f"{stats['bmi']} — {stats['bmi_category']}"),
            ("Ideal Weight Range",   f"{stats['ideal_low']} – {stats['ideal_high']} kg"),
            ("Body Fat (est.)",      f"{stats['body_fat_pct']}%"),
            ("Daily Water",          f"{stats['water_l']} litres"),
            ("Health Conditions",    profile['health_conditions']),
        ]
        for lbl, val in rows:
            r = ctk.CTkFrame(detail, fg_color="transparent")
            r.pack(fill="x", padx=24, pady=4)
            ctk.CTkLabel(r, text=lbl, font=FXS, text_color=MUTED,
                         width=200, anchor="w").pack(side="left")
            ctk.CTkLabel(r, text=val, font=("Segoe UI", 11, "bold"),
                         text_color=TEXT, anchor="w").pack(side="left")
        ctk.CTkFrame(detail, height=16, fg_color="transparent").pack()

    # ══════════════════════════════════════════════════════════
    #  ALGORITHMS PAGE
    # ══════════════════════════════════════════════════════════
    def _build_algo_page(self):
        page = self.pages["algorithms"]
        self._page_header(page, "🤖", "Algorithm Results",
                          "BFS  ·  DFS  ·  Best First  ·  A*  ·  Minimax")

        toolbar = ctk.CTkFrame(page, fg_color=PANEL, height=44, corner_radius=0)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)

        self._save_btn = ctk.CTkButton(
            toolbar, text="💾  Save", font=FXS,
            height=28, width=110, corner_radius=8,
            fg_color=CYAN, hover_color="#0097a7",
            text_color=BG, command=self._save_algo, state="disabled")
        self._save_btn.pack(side="right", padx=16, pady=8)

        # Use tk.Text directly — CTkTextbox disabled+tags don't work on Windows
        txt_frame = ctk.CTkFrame(page, fg_color="#0d1117", corner_radius=0)
        txt_frame.pack(fill="both", expand=True)

        self._algo_box = tk.Text(
            txt_frame,
            bg="#0d1117", fg=TEXT,
            font=FM, wrap="word",
            relief="flat", bd=0,
            padx=18, pady=14,
            insertbackground=ACCENT,
            selectbackground=ACCENT,
            selectforeground=BG,
            state="normal",
        )
        sb = tk.Scrollbar(txt_frame, command=self._algo_box.yview,
                          bg=CARD2, troughcolor=CARD2,
                          activebackground=MUTED, relief="flat", width=10)
        self._algo_box.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self._algo_box.pack(fill="both", expand=True)

        # Colour tags
        self._algo_box.tag_configure("grn",  foreground=ACCENT)
        self._algo_box.tag_configure("cyan", foreground=CYAN)
        self._algo_box.tag_configure("warn", foreground=WARN)
        self._algo_box.tag_configure("dim",  foreground=MUTED)
        self._algo_box.tag_configure("bold", foreground=TEXT,
                                      font=("Consolas", 10, "bold"))

        self._algo_box.insert("end",
            "\n  👈  Go to the Profile tab, fill in your details,\n"
            "  and click ⚡ GENERATE MY PLAN to see results here.\n")
        self._algo_box.configure(state="disabled")
        self._algo_text = ""

    def _render_algo(self, output):
        self._algo_text = output
        self._algo_box.configure(state="normal")
        self._algo_box.delete("1.0", "end")

        for line in output.splitlines(keepends=True):
            s = line.strip()
            if s.startswith("=") or s.startswith("#"):
                self._algo_box.insert("end", line, "grn")
            elif any(s.startswith(f"{n}.") for n in range(1, 6)):
                self._algo_box.insert("end", line, "bold")
            elif "✅" in line:
                self._algo_box.insert("end", line, "cyan")
            elif "◀" in line or "RECOMMENDED" in line:
                self._algo_box.insert("end", line, "warn")
            elif s.startswith("-"):
                self._algo_box.insert("end", line, "dim")
            else:
                self._algo_box.insert("end", line)

        self._algo_box.configure(state="disabled")
        self._save_btn.configure(state="normal")

    def _save_algo(self):
        try:
            fname = "fitness_algorithm_results.txt"
            with open(fname, "w", encoding="utf-8") as f:
                f.write(self._algo_text)
            messagebox.showinfo("Saved", f"Results saved as:\n{fname}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ══════════════════════════════════════════════════════════
    #  GENERATE
    # ══════════════════════════════════════════════════════════
    def _on_generate(self):
        try:
            name   = self._inputs["name"].get().strip()
            age    = self._inputs["age"].get().strip()
            weight = self._inputs["weight"].get().strip()
            height = self._inputs["height"].get().strip()

            if not name:
                raise ValueError("Please enter your name.")
            if not age.isdigit():
                raise ValueError("Age must be a whole number.")
            if not weight.replace(".", "").isdigit():
                raise ValueError("Weight must be a number.")
            if not height.replace(".", "").isdigit():
                raise ValueError("Height must be a number.")

            profile = {
                "name":              name,
                "age":               int(age),
                "gender":            self._gender.get(),
                "weight_kg":         float(weight),
                "height_cm":         float(height),
                "goal":              self._inputs["goal"].get(),
                "experience":        self._inputs["experience"].get(),
                "activity":          self._inputs["activity"].get(),
                "health_conditions": self._health.get("1.0", "end").strip(),
            }
            stats = get_stats(profile)
            self._render_stats(profile, stats)
            self._show("stats")

            self._gen_btn.configure(state="disabled", text="⏳  Running...")
            self._status.configure(text="Calculating...", text_color=WARN)

            def run():
                old = sys.stdout
                sys.stdout = buf = StringIO()
                run_all_algorithms(profile, stats)
                sys.stdout = old
                out = buf.getvalue()
                self.after(0, lambda: self._on_done(out))

            threading.Thread(target=run, daemon=True).start()

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def _on_done(self, output):
        self._render_algo(output)
        self._gen_btn.configure(state="normal", text="⚡   GENERATE MY PLAN")
        self._status.configure(text="✅ Done! Check Stats & Algorithms tabs.",
                               text_color=ACCENT)


# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()