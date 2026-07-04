from flask import Flask, render_template, request
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    title = request.form["title"]
    description = request.form["description"]

    prompt = f"""
You are a software testing expert.

Analyze the following bug.

Bug Title: {title}

Bug Description: {description}

Return ONLY plain text.

Priority:
Reason:
Suggested Team:
Estimated Fix Time:

Do NOT use:
#, ##, ###, *, **, ---, bullet points or markdown formatting.
"""

    response = model.generate_content(prompt)

    return render_template(
        "result.html",
        title=title,
        description=description,
        prediction=response.text
    )

if __name__ == "__main__":
    app.run(debug=True)