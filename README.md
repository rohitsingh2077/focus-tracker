# Focus Tracker

A clean, minimal **Flask + SQLite**-based Focus Tracker app with user authentication, task management, and timestamps. Perfect for small personal productivity dashboards.

---

## Features

*  Add, toggle, and delete tasks
*  User login/signup system
*  Timestamp saved with every task
*  SQLite database (no external setup required)
*  Simple and customizable UI

---

##  Tech Stack

* **Backend:** Python + Flask
* **Database:** SQLite
* **Frontend:** HTML + CSS + JavaScript (vanilla)

---

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/focus-tracker.git
cd focus-tracker
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
python app.py
```

Go to: `http://127.0.0.1:5000`

---

##  Project Structure

```
focus-tracker/
├── app.py                # Main Flask app
├── focus.db              # SQLite database (auto-generated)
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── index.html
│   ├── login.html
│   └── signup.html
├── static/               # Optional CSS/JS
│   └── style.css
└── README.md

## License

MIT License — Feel free to fork and improve!

---

## Contributing

Pull requests welcome! If you find bugs or want new features, open an issue or PR.

---

Happy focusing! ✨
