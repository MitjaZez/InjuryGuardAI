from flask import Flask, render_template, request, redirect, url_for, flash, session
from risk_model import calculate_risk
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, get_db_connection

app = Flask(__name__)
app.secret_key = "injuryguard-secret-key"

init_db()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        password_hash = generate_password_hash(password)

        conn = get_db_connection()

        existing_user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if existing_user:
            conn.close()
            flash("Korisnik sa ovom email adresom već postoji.")
            return redirect(url_for("register"))

        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )

        conn.commit()
        conn.close()

        flash("Registracija je uspešna. Sada se možete prijaviti.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            flash("Uspešno ste se prijavili.")
            return redirect(url_for("home"))

        flash("Neispravna email adresa ili lozinka.")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Uspešno ste se odjavili.")
    return redirect(url_for("home"))

@app.route("/history")
def history():
    if not session.get("user_id"):
        flash("Morate biti prijavljeni da biste videli istoriju analiza.")
        return redirect(url_for("login"))

    conn = get_db_connection()

    analyses = conn.execute("""
        SELECT *
        FROM analyses
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (session["user_id"],)).fetchall()

    conn.close()

    return render_template("history.html", analyses=analyses)

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        form_data = {
            "athlete_name": request.form.get("athlete_name"),
            "sport": request.form.get("sport"),
            "weekly_sessions": int(request.form.get("weekly_sessions")),
            "training_duration": int(request.form.get("training_duration")),
            "intensity": int(request.form.get("intensity")),
            "fatigue": int(request.form.get("fatigue")),
            "sleep_quality": int(request.form.get("sleep_quality")),
            "pain_level": int(request.form.get("pain_level")),
            "rest_days": int(request.form.get("rest_days")),
            "previous_injury": request.form.get("previous_injury")
        }

        result = calculate_risk(form_data)

        saved_to_history = False

        if session.get("user_id"):
            conn = get_db_connection()

            conn.execute("""
                INSERT INTO analyses (
                    user_id,
                    athlete_name,
                    sport,
                    risk_score,
                    risk_level,
                    recommendation
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                session["user_id"],
                form_data["athlete_name"],
                form_data["sport"],
                result["risk_score"],
                result["risk_level"],
                result["recommendation"]
            ))

            conn.commit()
            conn.close()

            saved_to_history = True

        return render_template(
            "result.html",
            data=form_data,
            result=result,
            saved_to_history=saved_to_history
        )

    return render_template("analyze.html")


if __name__ == "__main__":
    app.run(debug=True)