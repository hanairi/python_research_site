import os
from flask import Flask, render_template, send_from_directory
from utils import extract_paper_details
from docx import Document

app = Flask(__name__, static_folder='static')

PAPERS_FOLDER = os.path.join(os.getcwd(), "papers")  # ✅ Ensure absolute path

def get_papers():
    papers = []
    for filename in os.listdir(PAPERS_FOLDER):
        if filename.endswith(".docx"):
            paper_details = extract_paper_details(os.path.join(PAPERS_FOLDER, filename))
            papers.append({"name": filename, **paper_details})
    return papers

@app.route('/')
def home():
    papers = get_papers()
    return render_template('index.html', papers=papers)

@app.route('/papers/<filename>')
def view_paper(filename):
    paper_details = extract_paper_details(os.path.join(PAPERS_FOLDER, filename))
    return render_template('paper.html', filename=filename, **paper_details)

# ✅ Fix Download Route
@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(PAPERS_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
