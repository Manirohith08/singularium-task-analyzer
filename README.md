# Singularium Smart Task Analyzer

A comprehensive task prioritization system designed to help users identify "what to work on next." This application uses a weighted algorithm to score tasks based on urgency, importance, effort, and dependencies, featuring a decoupled Django backend and a vanilla JavaScript frontend.

## 🚀 Setup Instructions

### Prerequisites
* Python 3.8+
* Git

### 1. Backend Setup (Django)
The backend serves as a REST API for analyzing task data.

# Clone the repository
git clone <your-repo-url>
cd task-analyzer

# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv
# Windows:
..\venv\Scripts\activate
# Mac/Linux:
source ../venv/bin/activate

# Install dependencies
pip install -r ../requirements.txt

# Run migrations (creates db.sqlite3)
python manage.py migrate

# Start the server
python manage.py runserver
