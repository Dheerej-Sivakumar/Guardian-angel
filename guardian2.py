import tkinter as tk
from tkinter import ttk, messagebox
import random, json, os

# ---------- Config ----------
PROGRESS_FILE = "guardian_progress.json"
MILESTONES = {1: "Welcome Badge 🎉", 3: "Consistency Badge 🟢", 7: "Caring Companion Badge 💙"}
DEFAULT_FREQ = 10  # default seconds between water reminders
# ----------------------------

# Persistence
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"completed": 0, "badges": []}

def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f)

class GuardianApp:
    def __init__(self, root):
        self.root = root
        root.title("Guardian Angel — Full Demo MVP")
        root.geometry("420x560")
        root.configure(bg="black")

        self.progress = load_progress()

        # Guardian emoji + bubble
        self.canvas = tk.Canvas(root, width=380, height=240, bg="black", highlightthickness=0)
        self.canvas.pack(pady=6)
        self.angel = self.canvas.create_text(190, 160, text="👼", font=("Arial", 72), fill="white")
        self.bubble_var = tk.StringVar(value="Hello — I'm your Guardian 👋")
        self.bubble_label = tk.Label(
            self.canvas, textvariable=self.bubble_var, font=("Arial", 12),
            bg="#fff6d1", fg="black", wraplength=260, bd=2, relief="solid", padx=8, pady=6
        )
        self.canvas.create_window(190, 50, window=self.bubble_label)

        # Slider for frequency adjustment
        ctrl = tk.Frame(root, bg="black"); ctrl.pack(pady=6)
        tk.Label(ctrl, text="Seconds between water nudges:", fg="white", bg="black").pack(anchor="w")
        self.freq_scale = tk.Scale(ctrl, from_=5, to=60, orient="horizontal", length=320,
                                   bg="black", fg="white", troughcolor="white")
        self.freq_scale.set(DEFAULT_FREQ)
        self.freq_scale.pack(pady=4)

        # Input buttons
        tk.Label(root, text="Inputs (simulated):", fg="white", bg="black").pack(pady=(10, 2))
        btns = tk.Frame(root, bg="black"); btns.pack(pady=4)
        self.make_cloud_button(btns, "💧 Hydrate", self.hydrate).pack(side="left", padx=4, pady=4)
        self.make_cloud_button(btns, "💨 Breathing", self.breathing).pack(side="left", padx=4, pady=4)
        self.make_cloud_button(btns, "🪑 Posture", self.posture).pack(side="left", padx=4, pady=4)
        self.make_cloud_button(btns, "😴 Sleep", self.sleep).pack(side="left", padx=4, pady=4)

        # Action buttons
        actions = tk.Frame(root, bg="black"); actions.pack(pady=6)
        self.make_cloud_button(actions, "✅ I did it", self.mark_done).pack(side="left", padx=6)
        self.make_cloud_button(actions, "😟 I'm stressed", self.comfort_mode).pack(side="left", padx=6)

        # Progress + badges
        pf = tk.Frame(root, bg="black"); pf.pack(pady=8)
        tk.Label(pf, text="Progress:", fg="white", bg="black").pack(anchor="w")
        self.pb = ttk.Progressbar(pf, orient="horizontal", length=340, mode="determinate"); self.pb.pack(pady=4)
        self.badges_var = tk.StringVar(value=", ".join(self.progress.get("badges", [])) or "No badges yet.")
        tk.Label(root, textvariable=self.badges_var, fg="white", bg="black", wraplength=380).pack()

        # State
        self.running = True
        self.root.after(self.freq_scale.get() * 1000, self.water_loop)
        self.update_progressbar()

    # Cloud-style button
    def make_cloud_button(self, parent, text, command):
        return tk.Button(parent, text=text, command=command,
                         bg="white", fg="black",
                         relief="flat", font=("Arial", 10, "bold"),
                         padx=8, pady=4, bd=0)

    # Auto water loop
    def water_loop(self):
        if self.running:
            self.bubble_var.set("💧 Time for a sip of water!")
            self.root.after(self.freq_scale.get() * 1000, self.water_loop)

    # Simulated inputs
    def hydrate(self):
        self.bubble_var.set("💧 Hydration check: have a glass of water now!")

    def breathing(self):
        self.bubble_var.set("💨 Hey, I sense your heart rate is high... slow breathe for 30s.")

    def posture(self):
        self.bubble_var.set("🪑 Posture check: straighten your back, shoulders relaxed.")

    def sleep(self):
        self.bubble_var.set("😴 It's late — try to wind down for a good sleep.")

    # Progress + milestones
    def mark_done(self):
        self.progress["completed"] = self.progress.get("completed", 0) + 1
        save_progress(self.progress)
        self.update_progressbar()
        self.check_milestones()
        self.bubble_var.set("👼 Great job! You followed a nudge 💪")

    def update_progressbar(self):
        maxv = max(max(MILESTONES.keys()), 1)
        cur = self.progress.get("completed", 0)
        self.pb["maximum"] = maxv
        self.pb["value"] = min(cur, maxv)
        self.badges_var.set(", ".join(self.progress.get("badges", [])) or "No badges yet.")

    def check_milestones(self):
        cur = self.progress.get("completed", 0)
        badges = set(self.progress.get("badges", []))
        for t, name in MILESTONES.items():
            if cur >= t and name not in badges:
                badges.add(name)
                self.progress["badges"] = list(badges)
                save_progress(self.progress)
                messagebox.showinfo("Milestone!", f"You earned: {name}")
        self.update_progressbar()

    # Stress comfort
    def comfort_mode(self):
        self.bubble_var.set("🌿 I'm here. Try 4-4-4 breathing: inhale 4, hold 4, exhale 4.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GuardianApp(root)
    root.mainloop()
