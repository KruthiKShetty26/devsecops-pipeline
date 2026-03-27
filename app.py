from flask import Flask, jsonify, request, render_template_string
import datetime

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Run Security Scan", "status": "completed", "priority": "high"},
    {"id": 2, "title": "Deploy to Production", "status": "completed", "priority": "high"},
    {"id": 3, "title": "Code Quality Review", "status": "in-progress", "priority": "medium"},
    {"id": 4, "title": "Update Dependencies", "status": "pending", "priority": "low"},
]

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>DevSecOps Pipeline Manager</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            color: white;
            padding: 30px;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 2.8em;
            background: linear-gradient(90deg, #00d4ff, #7b2ff7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .header p { color: #aaa; font-size: 1.1em; }
        .badges {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 15px 0;
            flex-wrap: wrap;
        }
        .badge {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
        }
        .badge-blue { background: rgba(0,212,255,0.2); border: 1px solid #00d4ff; color: #00d4ff; }
        .badge-purple { background: rgba(123,47,247,0.2); border: 1px solid #7b2ff7; color: #b57bee; }
        .badge-green { background: rgba(0,255,136,0.2); border: 1px solid #00ff88; color: #00ff88; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-bottom: 35px;
        }
        .stat-card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        .stat-card .number {
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(90deg, #00d4ff, #7b2ff7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stat-card .label { color: #aaa; font-size: 0.9em; margin-top: 5px; }
        .input-area {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        .input-area h3 { margin-bottom: 15px; color: #00d4ff; }
        .input-row {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .input-row input, .input-row select {
            flex: 1;
            padding: 12px 15px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            color: white;
            font-size: 1em;
            min-width: 150px;
        }
        .input-row input::placeholder { color: #aaa; }
        .input-row select option { background: #302b63; }
        .btn {
            padding: 12px 25px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: all 0.3s;
        }
        .btn-primary {
            background: linear-gradient(90deg, #00d4ff, #7b2ff7);
            color: white;
        }
        .btn-primary:hover { opacity: 0.85; transform: translateY(-2px); }
        .tasks-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .tasks-header h3 { color: #00d4ff; font-size: 1.3em; }
        .task-card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
        }
        .task-card:hover {
            background: rgba(255,255,255,0.08);
            transform: translateX(5px);
        }
        .task-left { display: flex; align-items: center; gap: 15px; }
        .task-title { font-size: 1em; }
        .task-title.done { text-decoration: line-through; color: #aaa; }
        .status-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.78em;
            font-weight: bold;
        }
        .status-completed { background: rgba(0,255,136,0.2); color: #00ff88; border: 1px solid #00ff88; }
        .status-in-progress { background: rgba(0,212,255,0.2); color: #00d4ff; border: 1px solid #00d4ff; }
        .status-pending { background: rgba(255,170,0,0.2); color: #ffaa00; border: 1px solid #ffaa00; }
        .priority-high { color: #ff4757; font-size: 0.8em; }
        .priority-medium { color: #ffaa00; font-size: 0.8em; }
        .priority-low { color: #00ff88; font-size: 0.8em; }
        .task-actions { display: flex; gap: 8px; }
        .btn-small {
            padding: 6px 14px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.82em;
            font-weight: bold;
            transition: all 0.2s;
        }
        .btn-complete { background: rgba(0,255,136,0.2); color: #00ff88; border: 1px solid #00ff88; }
        .btn-delete { background: rgba(255,71,87,0.2); color: #ff4757; border: 1px solid #ff4757; }
        .btn-complete:hover { background: #00ff88; color: black; }
        .btn-delete:hover { background: #ff4757; color: white; }
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #aaa;
            font-size: 0.9em;
        }
        .pipeline-status {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-top: 10px;
            flex-wrap: wrap;
        }
        .pipeline-step {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            background: rgba(0,255,136,0.15);
            border: 1px solid #00ff88;
            color: #00ff88;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 DevSecOps Pipeline Manager</h1>
        <p>Automated CI/CD with Security Scanning & Continuous Deployment</p>
        <div class="badges">
            <span class="badge badge-blue">Jenkins CI/CD</span>
            <span class="badge badge-purple">SonarQube</span>
            <span class="badge badge-green">Docker</span>
            <span class="badge badge-blue">Trivy Security</span>
            <span class="badge badge-purple">GitHub</span>
        </div>
        <div class="pipeline-status">
            <span class="pipeline-step">✅ Checkout</span>
            <span class="pipeline-step">✅ Tests</span>
            <span class="pipeline-step">✅ SonarQube</span>
            <span class="pipeline-step">✅ Docker Build</span>
            <span class="pipeline-step">✅ Security Scan</span>
            <span class="pipeline-step">✅ Deployed</span>
        </div>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="number" id="total">0</div>
            <div class="label">Total Tasks</div>
        </div>
        <div class="stat-card">
            <div class="number" id="completed">0</div>
            <div class="label">Completed</div>
        </div>
        <div class="stat-card">
            <div class="number" id="inprogress">0</div>
            <div class="label">In Progress</div>
        </div>
        <div class="stat-card">
            <div class="number" id="pending">0</div>
            <div class="label">Pending</div>
        </div>
    </div>

    <div class="input-area">
        <h3>➕ Add New Task</h3>
        <div class="input-row">
            <input type="text" id="taskInput" placeholder="Enter task title..." />
            <select id="prioritySelect">
                <option value="high">🔴 High Priority</option>
                <option value="medium">🟡 Medium Priority</option>
                <option value="low">🟢 Low Priority</option>
            </select>
            <button class="btn btn-primary" onclick="addTask()">Add Task</button>
        </div>
    </div>

    <div class="tasks-header">
        <h3>📋 Pipeline Tasks</h3>
    </div>
    <div id="taskList"></div>

    <div class="footer">
        <p>DevSecOps CI/CD Pipeline | Powered by Jenkins + Docker + SonarQube</p>
        <p style="margin-top:5px;">© 2026 Kruthi K Shetty | 6th Semester Project</p>
    </div>

    <script>
        let tasks = [];

        async function loadTasks() {
            const res = await fetch('/api/tasks');
            tasks = await res.json();
            renderTasks();
            updateStats();
        }

        function updateStats() {
            document.getElementById('total').textContent = tasks.length;
            document.getElementById('completed').textContent = tasks.filter(t => t.status === 'completed').length;
            document.getElementById('inprogress').textContent = tasks.filter(t => t.status === 'in-progress').length;
            document.getElementById('pending').textContent = tasks.filter(t => t.status === 'pending').length;
        }

        function renderTasks() {
            const list = document.getElementById('taskList');
            list.innerHTML = '';
            tasks.forEach(task => {
                const statusClass = 'status-' + task.status.replace(' ', '-');
                const titleClass = task.status === 'completed' ? 'task-title done' : 'task-title';
                list.innerHTML += `
                    <div class="task-card">
                        <div class="task-left">
                            <div>
                                <div class="${titleClass}">${task.title}</div>
                                <div class="priority-${task.priority}">▲ ${task.priority} priority</div>
                            </div>
                        </div>
                        <div class="task-actions">
                            <span class="status-badge ${statusClass}">${task.status}</span>
                            ${task.status !== 'completed' ? `<button class="btn-small btn-complete" onclick="completeTask(${task.id})">✓ Done</button>` : ''}
                            <button class="btn-small btn-delete" onclick="deleteTask(${task.id})">✕</button>
                        </div>
                    </div>`;
            });
        }

        async function addTask() {
            const title = document.getElementById('taskInput').value.trim();
            const priority = document.getElementById('prioritySelect').value;
            if (!title) return alert('Please enter a task!');
            await fetch('/api/tasks', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title, priority})
            });
            document.getElementById('taskInput').value = '';
            loadTasks();
        }

        async function completeTask(id) {
            await fetch(`/api/tasks/${id}/complete`, {method: 'PUT'});
            loadTasks();
        }

        async function deleteTask(id) {
            await fetch(`/api/tasks/${id}`, {method: 'DELETE'});
            loadTasks();
        }

        loadTasks();
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    new_task = {
        "id": len(tasks) + 1,
        "title": da