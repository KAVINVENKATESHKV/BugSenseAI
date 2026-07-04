from flask import Flask, render_template, request, send_file
import google.generativeai as genai
import os
from dotenv import load_dotenv
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io

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


@app.route("/download")
def download():

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>BugSense AI Report</b>", styles["Title"]))
    story.append(Paragraph("This is a sample AI Bug Report.", styles["Normal"]))
    story.append(Paragraph("Priority: High", styles["Normal"]))
    story.append(Paragraph("Suggested Team: Backend Team", styles["Normal"]))
    story.append(Paragraph("Estimated Fix Time: 2 Days", styles["Normal"]))

    doc.build(story)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="BugSenseAI_Report.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)