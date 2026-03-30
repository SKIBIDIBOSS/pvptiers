from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "secret123"

# ========================
# DATA STORAGE
# ========================
players = []
queue = []
results = []
high_results = []

# ========================
# LOGIN
# ========================
ADMIN_USER = "skibidiboss123"
ADMIN_PASS = "skibidiboss123"

TESTER_USER = "lining123"
TESTER_PASS = "lining123"

# ========================
# TIER LOGIC
# ========================
def calculate_tier(opponent_tier, score):
    # Example logic
    if opponent_tier.startswith("HT"):
        if score >= 4:
            return opponent_tier
    if opponent_tier.startswith("LT"):
        if score >= 3:
            return opponent_tier
    return "No Change"

# ========================
# ROUTES
# ========================

@app.route("/")
def home():
    return render_template("index.html", players=players)

# -------- QUEUE --------
@app.route("/queue", methods=["GET", "POST"])
def queue_page():
    if request.method == "POST":
        ign = request.form["ign"]
        queue.append({"ign": ign})
    return render_template("queue.html", queue=queue)

# -------- ADMIN LOGIN --------
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["user"] == ADMIN_USER and request.form["pass"] == ADMIN_PASS:
            session["admin"] = True
            return redirect("/admin")
    return render_template("login_admin.html")

# -------- TESTER LOGIN --------
@app.route("/tester_login", methods=["GET", "POST"])
def tester_login():
    if request.method == "POST":
        if request.form["user"] == TESTER_USER and request.form["pass"] == TESTER_PASS:
            session["tester"] = True
            return redirect("/tester")
    return render_template("login_tester.html")

# -------- ADMIN PANEL --------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        return redirect("/admin_login")

    if request.method == "POST":
        players.append({
            "name": request.form["name"],
            "tier": request.form["tier"],
            "region": request.form["region"]
        })

    return render_template("admin.html", players=players)

# -------- TESTER PANEL --------
@app.route("/tester", methods=["GET", "POST"])
def tester():
    if not session.get("tester"):
        return redirect("/tester_login")

    return render_template("tester.html", queue=queue)

# -------- COMPLETE TEST --------
@app.route("/complete_test", methods=["POST"])
def complete_test():
    ign = request.form["ign"]
    opponent_tier = request.form["tier"]
    score = int(request.form["score"])

    new_tier = calculate_tier(opponent_tier, score)

    result = {
        "ign": ign,
        "opponent_tier": opponent_tier,
        "score": score,
        "result": new_tier
    }

    results.append(result)

    # HIGH RESULT condition
    if score >= 4:
        high_results.append(result)

    return redirect("/results")

# -------- RESULTS --------
@app.route("/results")
def results_page():
    return render_template("results.html", results=results)

# -------- HIGH RESULTS --------
@app.route("/high_results")
def high_results_page():
    return render_template("high_results.html", results=high_results)

# ========================
# RUN
# ========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
