from flask import Flask, render_template, request, redirect, session, url_for
import csv
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"


# Load questions from CSV
def load_questions():
    questions = []
    with open("questions.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append(row)
    return questions


questions = load_questions()


# Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["username"] = username
        session["current_question"] = 0
        session["score"] = 0
        return redirect(url_for("quiz"))
    return render_template("login.html")


# Quiz Page
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "username" not in session:
        return redirect(url_for("login"))

    current = session.get("current_question", 0)

    if current >= len(questions):
        return redirect(url_for("result"))

    question = questions[current]

    if request.method == "POST":
        selected_answer = request.form["answer"]
        correct_answer = question["answer"]

        if selected_answer == correct_answer:
            session["score"] += 1

        session["current_question"] += 1
        return redirect(url_for("quiz"))

    return render_template(
        "quiz.html", question=question, q_number=current + 1, total=len(questions)
    )


# Result Page
@app.route("/result")
def result():
    score = session.get("score", 0)
    total = len(questions)
    username = session.get("username", "User")
    return render_template("result.html", score=score, total=total, username=username)


# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)