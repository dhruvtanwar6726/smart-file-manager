from flask import Flask, render_template, request, jsonify
import os
from collections import defaultdict

# Initialize the Flask app
app = Flask(__name__)

# Set the root directory to scan (Desktop in this case)
ROOT_DIR = os.path.expanduser("~\\Desktop")

# Define file type categories based on file extensions
CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    'Documents': ['.pdf', '.docx', '.txt', '.xls', '.xlsx', '.pptx'],
    'Code': ['.py', '.java', '.cpp', '.js', '.html', '.css', '.ts'],
    'Audio': ['.mp3', '.wav', '.aac'],
    'Video': ['.mp4', '.mkv', '.avi'],
    'Archives': ['.zip', '.rar', '.7z'],
    'Others': []  # Used if extension doesn't match any known category
}

# Helper function to determine the category of a file based on its extension
def get_category(ext):
    for category, ext_list in CATEGORIES.items():
        if ext in ext_list:
            return category
    return 'Others'

# Scan the given directory and organize files into: Category -> Extension -> List of files
def scan_files(start_path):
    categorized = defaultdict(lambda: defaultdict(list))  # Nested dict structure
    for root, dirs, files in os.walk(start_path):  # Walk through all subfolders
        for file in files:
            ext = os.path.splitext(file)[1].lower()  # Get file extension
            cat = get_category(ext)  # Determine the category
            full_path = os.path.join(root, file)  # Get the full file path
            categorized[cat][ext].append(full_path)  # Add file to categorized structure
    return categorized

# Pre-scan all files when the server starts
all_files = scan_files(ROOT_DIR)

# Home route to render the file explorer UI
@app.route('/')
def index():
    return render_template('index.html', categorized_files=all_files)

# API endpoint to search for files containing the query string in their names
@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '').lower()
    results = []
    # Traverse through the categorized structure to search files
    for ext_map in all_files.values():
        for paths in ext_map.values():
            for path in paths:
                if query in os.path.basename(path).lower():
                    results.append(path)
    return jsonify(results)

# API endpoint to open a file from the browser (uses OS default app)
@app.route('/open_file', methods=['POST'])
def open_file():
    data = request.get_json()
    path = data.get("path")
    if path and os.path.exists(path):
        try:
            os.startfile(path)  # Open the file using the system default program
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    return jsonify({"status": "error", "message": "Invalid path"})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
