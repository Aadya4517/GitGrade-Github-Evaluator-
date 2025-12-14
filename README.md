# GitGrade-Github-Evaluator-

A Desktop Tool to Evaluate GitHub Profiles & Repositories

GitGrade is a Python-based desktop application that analyzes public GitHub repositories and provides a structured evaluation of a developer’s coding profile.
It generates an overall score, repository-wise insights, strengths, improvement suggestions, and a learning roadmap — all through a simple graphical interface.

🚀 Features
🔹 Profile-Level Evaluation

Overall score (0–100)

Developer level classification:

Beginner

Intermediate

Advanced

Repository count and analysis timestamp

🔹 Repository-Wise Analysis

For each analyzed repository:

Individual score

Detected programming languages

Project structure evaluation

Code quality heuristics (sample-based)

Documentation presence

Testing & CI/CD signals

Strengths and improvement suggestions

🔹 Learning Roadmap

A personalized roadmap is generated at the end based on the overall developer level.

🔹 Desktop UI

Built using Tkinter

Warm, minimal, distraction-free design

Scrollable repository insights

Works completely offline after fetching public GitHub data

🧠 What GitGrade Evaluates

GitGrade evaluates repositories using publicly available GitHub metadata:

Project structure (files and folders)

Code quality heuristics (sampled files)

README documentation

Presence of test files

CI/CD workflow configuration

Repository size and complexity indicators

Note: Analysis is based on public GitHub data and sampled files, not full static code analysis.

🛠️ Tech Stack

Python 3

Tkinter – GUI

GitHub REST API (Public)

AST module – Python code structure analysis

Requests – API handling

📦 Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/gitgrade.git
cd gitgrade

2️⃣ Install dependencies
pip install requests


(Tkinter comes preinstalled with Python)

▶️ How to Run
python gitgrade_desktop_final_no_token.py

🧪 How to Use

Enter a GitHub username or profile URL

Aadya4517


or

https://github.com/Aadya4517


Click Analyze

View:

Overall score & developer level

Repository-wise breakdown

Strengths & improvement areas

Personalized learning roadmap

⚠️ Limitations

Analyzes public repositories only

Uses sampling, not full static analysis

GitHub API rate limits apply (unauthenticated access)

Results are heuristic-based, not absolute measurements

🎯 Use Cases

Student portfolio evaluation

Self-assessment for developers

Hackathon project screening

Academic project demonstration

GitHub profile insights

🔮 Future Enhancements

GitHub token support for higher API limits

Export reports as PDF

Deeper multi-language analysis

Web-based version

Offline demo mode

📸 Screenshots

"C:\Users\aadya\Videos\Recording 2025-12-14 145912.mp4"
<img width="1903" height="990" alt="image" src="https://github.com/user-attachments/assets/f456d2ac-1d03-48fe-b3e9-644c2d4f79ad" />


🏁 Conclusion

GitGrade demonstrates how public GitHub data can be transformed into actionable developer insights using structured heuristics and a clean user interface.
It emphasizes clarity, explainability, and stability over over-engineering.
