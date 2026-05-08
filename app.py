import os
import json
import time
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'cloud-serverless-secret-key-99'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DATA_FILE'] = 'data/db.json'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.dirname(app.config['DATA_FILE']), exist_ok=True)

# --- Database Simulation (DynamoDB Mock) ---

def load_db():
    if not os.path.exists(app.config['DATA_FILE']):
        # Default fallback if file missing
        initial_data = {
            "users": [{"username": "admin", "password": generate_password_hash("password123")}],
            "storage": [],
            "lambda_functions": [
                {"name": "AuthFunction", "runtime": "Python 3.11", "status": "Active", "last_invoked": "1m ago", "memory": "128MB"},
                {"name": "DataProcessor", "runtime": "Python 3.11", "status": "Active", "last_invoked": "5m ago", "memory": "256MB"}
            ],
            "api_logs": []
        }
        save_db(initial_data)
        return initial_data
    with open(app.config['DATA_FILE'], 'r') as f:
        return json.load(f)

def save_db(data):
    with open(app.config['DATA_FILE'], 'w') as f:
        json.dump(data, f, indent=4)

# --- Flask-Login Setup ---

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    db = load_db()
    for user in db['users']:
        if user['username'] == user_id:
            return User(user['username'], user['username'])
    return None

# --- Simulated AWS Services Logic ---

def simulate_lambda_execution(func_name, payload):
    """Simulates a Lambda function invocation with logging."""
    db = load_db()
    execution_id = f"req-{random.randint(1000, 9999)}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Update lambda last invoked
    for fn in db['lambda_functions']:
        if fn['name'] == func_name:
            fn['last_invoked'] = "Just now"
            break
            
    # Add to API logs (simulating API Gateway -> Lambda)
    log_entry = {
        "method": "INVOKE",
        "path": f"lambda://{func_name}",
        "status": 200,
        "latency": f"{random.randint(10, 500)}ms",
        "timestamp": timestamp,
        "request_id": execution_id
    }
    db['api_logs'].insert(0, log_entry)
    db['api_logs'] = db['api_logs'][:20] # Keep last 20
    save_db(db)
    return {"status": "success", "execution_id": execution_id}

# --- Routes ---

@app.route('/')
@login_required
def index():
    db = load_db()
    
    # Generate some dynamic "CloudFront" analytics
    analytics = {
        "requests": random.randint(5000, 15000),
        "data_transfer": f"{random.uniform(1.5, 5.2):.1f} TB",
        "error_rate": f"{random.uniform(0.01, 0.05):.2f}%",
        "latency": f"{random.randint(20, 80)}ms"
    }
    
    # System Health Simulation
    health = {
        "status": "Healthy",
        "uptime": "99.99%",
        "regions": ["us-east-1", "eu-west-1", "ap-south-1"]
    }

    return render_template('index.html', 
                           storage=db['storage'], 
                           lambdas=db['lambda_functions'], 
                           logs=db['api_logs'],
                           dynamodb=db.get('dynamodb_records', []),
                           analytics=analytics,
                           health=health)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        db = load_db()
        user_found = None
        for u in db['users']:
            if u['username'] == username:
                user_found = u
                break
        
        if user_found and check_password_hash(user_found['password'], password):
            user_obj = User(username, username)
            login_user(user_obj)
            return redirect(url_for('index'))
        else:
            flash('Invalid Cloud Credentials. Please try again.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- Simulated API Endpoints (API Gateway) ---

@app.route('/api/v1/storage/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Update DynamoDB simulation
        db = load_db()
        file_size = os.path.getsize(filepath)
        size_str = f"{file_size / 1024:.1f} KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.1f} MB"
        
        db['storage'].append({
            "id": f"s3-{random.randint(1000, 9999)}",
            "name": filename,
            "size": size_str,
            "type": filename.split('.')[-1].upper() if '.' in filename else 'UNKNOWN',
            "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "bucket": "prod-deployment-assets"
        })
        
        # Trigger Lambda Simulation
        simulate_lambda_execution("ProcessImageUpload", {"file": filename})
        
        save_db(db)
        return redirect(url_for('index'))

@app.route('/api/v1/lambda/invoke/<name>', methods=['POST'])
@login_required
def invoke_lambda(name):
    result = simulate_lambda_execution(name, request.json or {})
    return jsonify(result)

import psutil

@app.route('/api/v1/metrics')
@login_required
def get_metrics():
    # Simulate real-time CloudWatch metrics using psutil for realism
    cpu = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory().percent
    
    return jsonify({
        "cpu": cpu,
        "memory": memory,
        "requests": random.randint(100, 1000),
        "errors": random.randint(0, 5)
    })

if __name__ == '__main__':
    # Professional start message
    print("\n" + "="*50)
    print(" AWS SIMULATOR - SERVERLESS CLOUD DASHBOARD")
    print("="*50)
    print(" STATUS: Online")
    print(" REGION: local-dev-1")
    print(f" URL: http://127.0.0.1:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000)
