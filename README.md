<<<<<<< HEAD
# AWS-Sim: Serverless Web Application Console

A professional-grade Serverless Web Application project built with Python Flask. This project simulates a real-world AWS architecture locally, designed for Cloud/DevOps engineers to showcase their understanding of serverless concepts.

![Dashboard Preview](https://img.shields.io/badge/AWS--Sim-Active-success?style=for-the-badge&logo=amazonaws)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Framework-black?style=for-the-badge&logo=flask)

## 🚀 Architecture Simulation

The project replicates the core components of a serverless cloud environment:

1.  **API Gateway**: Handled via Flask RESTful routes for endpoint management and logging.
2.  **AWS Lambda**: Simulated Python functions that handle logic (e.g., image processing triggers).
3.  **Amazon S3**: Local file storage simulation with automatic metadata indexing.
4.  **Amazon DynamoDB**: NoSQL-style storage using a local JSON database schema.
5.  **Amazon CloudFront**: Delivery analytics simulation with edge-location latency monitoring.
6.  **Amazon CloudWatch**: Real-time infrastructure monitoring and execution logs.

## 🛠️ Features

*   **Professional Dashboard**: Dark-mode console inspired by the AWS Management Console.
*   **Authentication (IAM)**: Simulated IAM login with secure session management.
*   **Storage Management**: Upload files to "S3 buckets" and view metadata.
*   **Lambda Monitoring**: Track function execution status, runtime, and memory usage.
*   **Live Metrics**: Real-time load monitoring using Chart.js integration.
*   **Activity Logs**: Audit trail of API requests and Lambda invocations.

## 📂 Project Structure

```text
serverless-cloud-app/
├── app.py              # Main Flask Backend & Service Simulators
├── requirements.txt    # Project Dependencies
├── data/
│   └── db.json         # Simulated DynamoDB (NoSQL Data)
├── uploads/            # Simulated S3 Bucket Storage
├── templates/
│   ├── index.html      # Cloud Console Dashboard
│   └── login.html      # IAM Login Interface
└── static/
    └── css/
        └── style.css   # Modern Professional UI Styles
```

## 🏃 Getting Started

### Prerequisites

*   Python 3.8 or higher installed.

### Installation & Run

1.  **Clone the repository** (or navigate to the folder).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Start the AWS Simulator**:
    ```bash
    python app.py
    ```
4.  **Access the Console**:
    Open `http://127.0.0.1:5000` in your browser.

### Default Credentials (IAM)
*   **Username**: `admin`
*   **Password**: `password123`

## 💡 Resume Integration

This project demonstrates proficiency in:
*   **Cloud Architecture**: Understanding how serverless components interact.
*   **Backend Engineering**: Building scalable Python applications with Flask.
*   **Frontend UI/UX**: Designing professional-grade monitoring dashboards.
*   **DevOps Principles**: Simulating logging, monitoring, and state management.

---
*Created for Cloud & DevOps Portfolio Excellence.*
=======
# aws-serverless-simulator
>>>>>>> 70d71aaad66a9a0be8ea737e2c0b34439735ea4d
