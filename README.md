# DevSecOps CI/CD Pipeline

![Pipeline Status](https://img.shields.io/badge/Pipeline-Passing-brightgreen)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Security](https://img.shields.io/badge/Security-Trivy%20Scanned-orange)
![Quality](https://img.shields.io/badge/Quality-SonarQube-blueviolet)

A complete end-to-end DevSecOps CI/CD pipeline built with Jenkins, Docker, SonarQube, and Trivy for a Python Flask web application.

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| GitHub | Source control and webhook trigger |
| Jenkins | CI/CD orchestration and pipeline |
| Docker | Containerization |
| SonarQube | Static code analysis and quality gates |
| Trivy | Docker image vulnerability scanning |

---

## 🏗️ Architecture
```
GitHub Push → Jenkins Pipeline → SonarQube Analysis → Docker Build → Trivy Scan → Deploy
```

---

## 🚀 Pipeline Stages

1. **Checkout** - Pull latest code from GitHub
2. **Install Dependencies** - Install Python packages
3. **Run Tests** - Execute pytest test suite
4. **SonarQube Analysis** - Static code analysis with quality gate
5. **Build Docker Image** - Containerize the application
6. **Trivy Security Scan** - Scan image for vulnerabilities
7. **Run Container** - Deploy the application locally

---

## 📁 Project Structure
```
devsecops-pipeline/
├── app.py                 # Flask web application
├── Dockerfile             # Docker container config
├── Jenkinsfile            # CI/CD pipeline definition
├── docker-compose.yml     # Jenkins + SonarQube setup
├── requirements.txt       # Python dependencies
└── tests/
    └── test_app.py        # Unit tests
```

---

## ⚙️ How to Run Locally

### Prerequisites
- Docker Desktop
- Python 3.x
- Git

### Start Jenkins and SonarQube
```bash
docker compose up -d
```

### Access Services
- **Flask App**: http://127.0.0.1:5000
- **Jenkins**: http://localhost:8080
- **SonarQube**: http://localhost:9000

### Run Flask App Directly
```bash
pip install -r requirements.txt
python app.py
```

---

## 📊 Results

- ✅ All pipeline stages passing
- ✅ SonarQube quality gate passed
- ✅ No critical vulnerabilities found by Trivy
- ✅ All unit tests passing
- ✅ Application successfully containerized

---

## 👩‍💻 Author

**Kruthi K Shetty**
6th Semester | 2026
DevSecOps CI/CD Pipeline Project
```

Save it as:
- **File name:** `README.md`
- **Save as type:** **"All Files (*.*)"**

Then run:
```
dir
