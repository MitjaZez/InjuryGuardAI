from flask import Flask, render_template, request
from risk_model import calculate_risk

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


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

        return render_template("result.html", data=form_data, result=result)

    return render_template("analyze.html")


if __name__ == "__main__":
    app.run(debug=True)