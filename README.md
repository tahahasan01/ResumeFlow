# Modern Resume Parser

A full-stack resume parser with a modern web interface, updated to run on the latest Python versions. Extracts key information like skills, experience, and education from PDF and DOCX files using local NLP models, and provides a detailed ATS (Applicant Tracking System) score breakdown.

---

✨ **Features**
- **Comprehensive Extraction:** Extracts name, email, mobile number, skills, experience, education, certifications, projects, and more.
- **ATS Scoring:** Provides a detailed ATS score breakdown across 10 categories (File Format, Contact Info, Education, Experience, Skills Section, Certifications, Projects, ATS Keyword Match, Design/Layout, Spelling/Grammar) with actionable feedback.
- **Modern Backend:** Built with FastAPI, providing a robust and fast API for resume parsing.
- **Sleek Frontend:** A user-friendly, two-column, and responsive interface built with React and Material-UI for a great user experience.
- **Local NLP Processing:** All parsing is done locally using spaCy and NLTK, requiring no external APIs or internet connection for the core processing.
- **Cross-Platform Support:** Ingests and analyzes both PDF and DOCX files on any operating system.

---

🛠️ **Tech Stack**
- **Backend**: Python, FastAPI, Uvicorn, spaCy, NLTK
- **Frontend**: React.js, Material-UI
- **NLP Models**: spaCy, NLTK

---

⚡ **Quickstart**

### 1. Clone the Repository
```bash
git clone https://github.com/tahahasan01/pyresparser.git
cd pyresparser
```

### 2. Install Backend Dependencies
From the project's **root directory**, run:
```bash
# Install Python packages
pip install -r requirements.txt

# Download NLP models
python -m spacy download en_core_web_sm
python -m nltk.downloader words stopwords punkt wordnet maxent_ne_chunker averaged_perceptron_tagger
```

### 3. Install Frontend Dependencies
Navigate to the `frontend` directory:
```bash
cd frontend
npm install
```

### 4. Run the Application
You will need to run the backend and frontend servers in two separate terminals.

**Terminal 1: Start the Backend (from the root directory)**
```bash
python -m uvicorn pyresparser.api:app --reload --port 8000
```

**Terminal 2: Start the Frontend (from the `frontend` directory)**
```bash
npm start
```

The application will be available at `http://localhost:3000`.

---

📂 **Project Structure**
```
pyresparser/
├── frontend/         # React.js frontend application
├── pyresparser/      # Python backend and parsing logic
│   ├── api.py        # FastAPI entrypoint
│   ├── resume_parser.py # Core parsing class
│   ├── utils.py      # Extraction utility functions
│   └── skills.csv    # Default skills list
├── requirements.txt  # Python dependencies
├── setup.py          # Project setup script
└── README.md         # This file
```

---

🧑‍💻 **Usage**
- **Upload Resumes:** Use the "Upload Resume" area on the web UI to choose a PDF or DOCX file.
- **Parse:** Click the "Parse Resume" button to process the resume.
- **View Results:**
  - A summary card will display all key extracted information (name, email, phone, education, experience, skills, certifications, projects).
  - Below the summary, a detailed ATS score breakdown (10 categories) with actionable comments will be shown in a table.
  - The interface uses a modern two-column layout for clarity and ease of use.

---

📝 **Customization**
- **Skills:** To add or change the skills that the parser looks for, you can edit the `pyresparser/skills.csv` file.
- **Extraction Logic:** The core extraction logic can be modified in `pyresparser/utils.py`.

---

🤝 **Contributing**
Pull requests and issues are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

📄 **License**
This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.
# ResumeFlow
