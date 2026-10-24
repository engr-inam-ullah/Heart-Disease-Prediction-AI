# ❤️ Heart Disease Prediction AI

## 📌 Project Overview

Heart Disease Prediction AI is a machine learning web application designed to predict the possible presence of heart disease based on 13 patient health features. The application uses a trained Logistic Regression model to generate predictions through a Flask web interface.

It provides a user registration and login system, a patient information form, and a prediction results page. The project is developed for educational purposes to demonstrate the practical application of machine learning in healthcare.

## ✨ Features

- User registration and login system.
- Heart disease prediction using 13 patient health features.
- Trained Logistic Regression machine learning model.
- Prediction results and probability display when supported by the model.
- Flask-based backend.
- SQLite database for user accounts.
- User-friendly interface built with HTML and CSS.
- Model integration using Joblib.
- Jupyter Notebook for data analysis and model training.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Web Framework:** Flask
- **Machine Learning:** Scikit-learn
- **Data Processing:** Pandas
- **Model Serialization:** Joblib
- **Database:** SQLite
- **Frontend:** HTML and CSS
- **Development Environment:** Visual Studio Code and Jupyter Notebook

## 📂 Project Structure

```text
Heart_Disease_Prediction_AI/
│
├── app.py
├── requirements.txt
├── README.md
├── heart_disease_logistic_model.joblib
│
└── web/
    └── heartcare/
        ├── index.html
        ├── login.html
        ├── signup.html
        ├── prediction.html
        ├── style.css
        ├── login.css
        └── images/
```

## ⚙️ How It Works

1. The user registers for an account and logs in.
2. The user enters the required patient health information.
3. The Flask application processes the input data.
4. The trained Logistic Regression model analyzes the 13 features.
5. The application displays the prediction result and, when supported, a model probability.

The model predicts the possible presence or absence of heart disease based on the data and preprocessing used during training.

## 🚀 Installation and Setup

### Prerequisites

- Python 3.9 or later.
- Visual Studio Code or another Python-compatible editor.
- Required project files, including the trained model.

### Step 1: Open the Project

Open Visual Studio Code and select **File → Open Folder**. Choose the `Heart_Disease_Prediction_AI` project folder.

### Step 2: Create a Virtual Environment (Recommended)

```bash
python -m venv .venv
```

On Windows, activate it using:

```bash
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

### Step 5: Open the Application

Open your browser and visit:

```text
http://127.0.0.1:5000
```

Register an account, log in, and navigate to the prediction page to try the application.

## 🧠 Machine Learning Model

The application uses a trained Logistic Regression model saved as:

`heart_disease_logistic_model.joblib`

The model accepts 13 patient health features. The feature names, order, category encodings, and preprocessing must match those used during model training.

The model output is an estimate based on its training data and should not be interpreted as a confirmed medical diagnosis.

## 🔒 Security Considerations

- Store secret keys in environment variables rather than hard-coding them.
- Never upload passwords, private credentials, or `.env` files.
- Keep databases containing personal information private.
- Disable Flask debug mode in production.
- Use HTTPS and appropriate session security for public deployment.
- Validate user inputs before passing them to the model.
- Apply suitable protections to authentication and database operations.

## ☁️ Deployment

The application can be configured for deployment on a Python-compatible hosting platform, such as Render.

Example configuration:

**Build Command**
```bash
pip install -r requirements.txt
```

**Start Command**
```bash
gunicorn app:app
```

Install `gunicorn` and add it to `requirements.txt` if it is not already included. Configure a strong `SECRET_KEY` environment variable in the hosting platform. Confirm that the application supports production deployment before publishing it.

## ⚠️ Disclaimer

This project is intended for educational and demonstration purposes only. It is not a medical device and must not be used to diagnose, treat, or rule out heart disease.

Machine learning predictions may be inaccurate and are not a substitute for professional medical advice. Always consult a qualified healthcare professional for medical concerns.

## 👨‍💻 Project Purpose

This project demonstrates how machine learning can be integrated into a web application using Python, Flask, and Scikit-learn. It also provides practical experience with model deployment, database integration, user authentication, and frontend development.
