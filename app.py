
from pathlib import Path
import os
import secrets
import sqlite3

import joblib
import pandas as pd
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    send_from_directory,
)
from werkzeug.security import generate_password_hash, check_password_hash


# ---------------- Project paths ----------------
BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web" / "heartcare"
IMAGES_DIR = WEB_DIR / "images"
MODEL_PATH = BASE_DIR / "heart_disease_logistic_model.joblib"

# SQLite location can be configured for persistent hosting.
DB_PATH = Path(os.environ.get("DATABASE_PATH", str(BASE_DIR / "users.db")))


# ---------------- Flask setup ----------------
app = Flask(
    __name__,
    template_folder=str(WEB_DIR),
    static_folder=str(WEB_DIR),
    static_url_path="",
)

# Set SECRET_KEY in your hosting environment.
# Do not use a hard-coded production secret.
app.secret_key = os.environ.get("SECRET_KEY")

if not app.secret_key:
    if os.environ.get("RENDER"):
        raise RuntimeError("Please set SECRET_KEY in Render environment variables.")
    app.secret_key = secrets.token_hex(32)


# ---------------- Load ML model ----------------
if not MODEL_PATH.is_file():
    raise FileNotFoundError(
        f"Trained model file not found: {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)


# Keep the feature order identical to model training.
FEATURES = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
]


# ---------------- Database ----------------
def db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=10)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with db() as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        )


init_db()


# ---------------- Home and pages ----------------
@app.route("/")
def home():
    if (WEB_DIR / "index.html").is_file():
        return send_from_directory(str(WEB_DIR), "index.html")
    return redirect("/prediction")


@app.route("/index.html")
def home_html():
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return send_from_directory(str(WEB_DIR), "login.html")

    ident = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not ident or not password:
        return redirect("/login?error=1")

    con = db()
    try:
        row = con.execute(
            "SELECT * FROM users WHERE email = ? OR lower(name) = ?",
            (ident.lower(), ident.lower()),
        ).fetchone()
    finally:
        con.close()

    if row and check_password_hash(row["password"], password):
        session.clear()
        session["user"] = row["name"]
        return redirect("/prediction")

    return redirect("/login?error=1")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return send_from_directory(str(WEB_DIR), "signup.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm", "")

    if not name or not email or not password:
        return redirect("/signup?error=empty")

    if len(password) < 6:
        return redirect("/signup?error=short")

    if password != confirm:
        return redirect("/signup?error=match")

    con = db()
    try:
        con.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (
                name,
                email,
                generate_password_hash(password, method="pbkdf2:sha256"),
            ),
        )
        con.commit()
    except sqlite3.IntegrityError:
        return redirect("/signup?error=exists")
    except sqlite3.Error:
        app.logger.exception("Signup database error")
        return redirect("/signup?error=server")
    finally:
        con.close()

    return redirect("/login?registered=1")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/login")


@app.route("/prediction")
def prediction():
    if "user" not in session:
        return redirect("/login")

    return render_template(
        "prediction.html",
        result=None,
        probability=None,
        error=None,
    )


@app.route("/prediction.html")
def prediction_html():
    return redirect("/prediction")


@app.route("/images/<path:filename>")
def serve_image(filename):
    if not IMAGES_DIR.is_dir():
        return "Images directory not found", 404
    return send_from_directory(str(IMAGES_DIR), filename)


# ---------------- Heart disease prediction ----------------
@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect("/login")

    try:
        patient_data = {}

        for feature in FEATURES:
            raw_value = request.form.get(feature, "").strip()

            if not raw_value:
                return render_template(
                    "prediction.html",
                    result=None,
                    probability=None,
                    error=f"Please provide a value for {feature}.",
                ), 400

            value = float(raw_value)

            if not pd.notna(value):
                raise ValueError("Input must be a valid number.")

            patient_data[feature] = value

        input_df = pd.DataFrame([patient_data], columns=FEATURES)

        prediction_value = int(model.predict(input_df)[0])
        probability = None

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_df)[0]
            probability = round(float(max(probabilities)) * 100, 2)

        if prediction_value == 1:
            result = "The model predicts possible heart disease."
        else:
            result = "The model predicts no heart disease."

        return render_template(
            "prediction.html",
            result=result,
            probability=probability,
            error=None,
        )

    except (ValueError, TypeError):
        return render_template(
            "prediction.html",
            result=None,
            probability=None,
            error="Please enter valid numeric values in every field.",
        ), 400

    except Exception:
        app.logger.exception("Prediction failed")
        return render_template(
            "prediction.html",
            result=None,
            probability=None,
            error="Prediction failed. Please try again later.",
        ), 500


# ---------------- Local development ----------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False,
    )
