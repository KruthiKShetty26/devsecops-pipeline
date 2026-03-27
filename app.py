from flask import Flask, jsonify, request, render_template_string
import datetime

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Run Security Scan", "status": "completed", "priority": "high", "time": "09:00 AM"},
    {"id": 2, "title": "Deploy to Production", "status": "completed", "priority": "high", "time": "09:30 AM"},
    {"id": 3, "title": "Code Quality Review", "status": "in-progress", "priority": "medium", "time": "10:00 AM"},
    {"id": 4, "title": "Update Dependencies", "status": "pending", "priority": "low", "time": "10:30 AM"},
]

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>DevSecOps Manager</title>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Inter, sans-serif;
            background: #0a0a0f;
            min-height: 100vh;
            color: white;
            overflow-x: hidden;
        }
        .bg-orbs {
            position: fixed;
            width: 100%; height: 100%;
            top: 0; left: 0;
            z-index: 0;
            pointer-events: none;
        }
        .orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.15;
        }
        .orb1 { width: 600px; height: 600px; background: #6c63ff; top: -200px; left: -200px; }
        .orb2 { width: 400px; height: 400px; background: #ff6584; bottom: -100px; right: -100px; }
        .orb3 { width: 300px; height: 300px; background: #43e97b; top: 50%; left: 50%; }
        .container { position: relative; z-index: 1; max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        .header { text-align: center; margin-bottom: 50px; }
        .header .tag {
            display: inline-block;
            background: rgba(108,99,255,0.2);
            border: 1px solid rgba(108,99,255,0.5);
            color: #a89cff;
            padding: 6px 18px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 500;
            margin-bottom: 20px;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        .header h1 {
            font-size: 3.2em;
            font-weight: 700;
            background: linear-gradient(135deg, #fff 0%, #a89cff 50%, #ff6584 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.2;
            margin-bottom: 15px;
        }
        .header p { color: rgba(255,255,255,0.4); font-size: 1em; font-weight: 300; }
        .tech-pills {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        .pill {
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: 500;
            border: 1px solid rgba(255,255,255,0.1);
            background: rgba(255,255,255,0.05);
            color: rgba(255,255,255,0.6);
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }
        .stat {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 20px;
            padding: 25px 20px;
            text-align: center;
            transition: all 0.3s;
        }
        .stat:hover { background: rgba(255,255,255,0.06); transform: translateY(-3px); }
        .stat .num {
            font-size: 2.8em;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 8px;
        }
        .stat .lbl { font-size: 0.78em; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 1px; }
        .num-total { color: #a89cff; }
        .num-done { color: #43e97b; }
        .num-progress { color: #f7971e; }
        .num-pending { color: #ff6584; }
        .glass-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 24px;
            padding: 28px;
            margin-bottom: 20px;
        }
        .card-title {
            font-size: 0.75em;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: rgba(255,255,255,0.3);
            margin-bottom: 18px;
            font-weight: 500;
        }
        .input-row { display: flex; gap: 12px; flex-wrap: wrap; }
        .input-row input {
            flex: 1;
            padding: 14px 18px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 14px;
            color: white;
            font-size: 0.95em;
            font-family: Inter, sans-serif;
            outline: none;
            transition: all 0.3s;
            min-width: 200px;
        }
        .input-row input:focus { border-color: rgba(108,99,255,0.5); background: rgba(108,99,255,0.05); }
        .input-row input::placeholder { color: rgba(255,255,255,0.2); }
        .input-row select {
            padding: 14px 18px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 14px;
            color: white;
            font-family: Inter, sans-serif;
            font-size: 0.95em;
            outline: none;
            cursor: pointer;
        }
        .input-row select option { background: #1a1a2e; }
        .btn-add {
            padding: 14px 28px;
            background: linear-gradient(135deg, #6c63ff, #ff6584);
            border: none;
            border-radius: 14px;
            color: white;
            font-weight: 600;
            font-size: 0.95em;
            cursor: pointer;
            font-family: Inter, sans-serif;
            transition: all 0.3s;
            white-space: nowrap;
        }
        .btn-add:hover { opacity: 0.85; transform: translateY(-2px); box-shadow: 0 10px 30px rgba(108,99,255,0.3); }
        .task-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 18px 22px;
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px;
            margin-bottom: 10px;
            transition: all 0.3s;
        }
        .task-item:hover { background: rgba(255,255,255,0.05); border-color: rgba(255,255,255,0.1); transform: translateX(4px); }
        .task-left { display: flex; align-items: center; gap: 14px; }
        .task-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
        .dot-completed { background: #43e97b; box-shadow: 0 0 10px #43e97b; }
        .dot-in-progress { background: #f7971e; box-shadow: 0 0 10px #f7971e; }
        .dot-pending { background: #ff6584; box-shadow: 0 0 10px #ff6584; }
        .task-info {}
        .task-name { font-size: 0.95em; font-weight: 500; margin-bottom: 4px; }
        .task-name.done { text-decoration: line-through; opacity: 0.4; }
        .task-meta { font-size: 0.75em; color: rgba(255,255,255,0.3); }
        .task-right { display: flex; align-items: center; gap: 8px; }
        .status-tag {
            padding: 4px 12px;
            border-radius: 10px;
            font-size: 0.72em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .tag-completed { background: rgba(67,233,123,0.1); color: #43e97b; border: 1px solid rgba(67,233,123,0.2); }
        .tag-in-progress { background: rgba(247,151,30,0.1); color: #f7971e; border: 1px solid rgba(247,151,30,0.2); }
        .tag-pending { background: rgba(255,101,132,0.1); color: #ff6584; border: 1px solid rgba(255,101,132,0.2); }
        .action-btn {
            padding: 6px 14px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 0.78em;
            font-weight: 600;
            font-family: Inter, sans-serif;
            transition: all 0.2s;
        }
        .btn-done { background: rgba(67,233,123,0.1); color: #43e97b; border: 1px solid rgba(67,233,123,0.2); }
        .btn-done:hover { background: #43e97b; color: #0a0a0f; }
        .btn-del { background: rgba(255,101,132,0.1); color: #ff6584; border: 1px solid rgba(255,101,132,0.2); }
        .btn-del:hover { background: #ff6584; color: white; }
        .pipeline-bar {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0;
            margin-top: 25px;
            flex-wrap: wrap;
        }
        .pipe-step {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            background: rgba(67,233,123,0.08);
            border: 1px solid rgba(67,233,123,0.2);
            color: #43e97b;
            font-size: 0.78em;
            font-weight: 500;
        }
        .pipe-step:first-child { border-radius: 12px 0 0 12px; }
        .pipe-step:last-child { border-radius: 0 12px 12px 0; }
        .pipe-arrow { color: rgba(255,255,255,0.2); font-size: 0.8em; }
        .footer { text-align: center; margin-top: 50px; color: rgba(255,255,255,0.2); font-size: 0.82em; line-height: 1.8; }
    </style>
</head>
<body>
    <div class="bg-orbs">
        <div class="orb orb1"></div>
        <div class="orb orb2"></div>
        <div class="orb orb3"></div>
    </div>
    <div class="container">
        <div class="header">
            <div class="tag">6th Semester Project</div>
            <h1>DevSecOps<br>Manager</h1>
            <p>Automated CI/CD with Security Scanning and Continuous Deployment</p>
            <div class="tech-pills">
                <span class="pill">Jenkins</span>
                <span class="pill">Docker</span>
                <span class="pill">SonarQube</span>
                <span class="pill">Trivy</span>
                <span class="pill">GitHub</span>
                <span class="pill">Python Flask</span>
            </div>
            <div class="pipeline-bar" style="margin-top:25px;">
                <div class="pipe-step">Checkout</div>
                <div class="pipe-step">Tests</div>
                <div class="pipe-step">SonarQube</div>
                <div class="pipe-step">Docker Build</div>
                <div class="pipe-step">Security Scan</div>
                <div class="pipe-step">Deployed</div>
            </div>
        </div>

        <div class="stats">
            <div class="stat"><div class="num num-total" id="total">0</div><div class="lbl">Total</div></div>
            <div class="stat"><div class="num num-done" id="completed">0</div><div class="lbl">Completed</div></div>
            <div class="stat"><div class="num num-progress" id="inprogress">0</div><div class="lbl">In Progress</div></div>
            <div class="stat"><div class="num num-pending" id="pending">0</div><div class="lbl">Pending</div></div>
        </div>

        <div class="glass-card">
            <div class="card-title">Add New Task</div>
            <div class="input-row">
                <input type="text" id="taskInput" placeholder="What needs to be done?" />
                <select id="prioritySelect">
                    <option value="high">High Priority</option>
                    <option value="medium">Medium Priority</option>
                    <option value="low">Low Priority</option>
                </select>
                <button class="btn-add" onclick="addTask()">+ Add Task</button>
            </div>
        </div>

        <div class="glass-card">
            <div class="card-title">Pipeline Tasks</div>
            <div id="taskList"></div>
        </div>

        <div class="footer">
            <p>DevSecOps CI/CD Pipeline &nbsp;|&nbsp; Jenkins + Docker + SonarQube + Trivy</p>
            <p>Kruthi K Shetty &nbsp;|&nbsp; 6th Semester &nbsp;|&nbsp; 2026</p>
        </div>
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
            if (tasks.length === 0) {
                list.innerHTML = '<p style="text-align:center;color:rgba(255,255,255,0.2);padding:30px;">No tasks yet. Add one above!</p>';
                return;
            }
            tasks.forEach(task => {
                const dotClass = 'dot-' + task.status.replace(' ', '-');
                const tagClass = 'tag-' + task.status.replace(' ', '-');
                const nameClass = task.status === 'completed' ? 'task-name done' : 'task-name';
                list.innerHTML += `
                <div class="task-item">
                    <div class="task-left">
                        <div class="task-dot ${dotClass}"></div>
                        <div class="task-info">
                            <div class="${nameClass}">${task.title}</div>
                            <div class="task-meta">${task.priority} priority &nbsp;|&nbsp; ${task.time || 'just now'}</div>
                        </div>
                    </div>
                    <div class="task-right">
                        <span class="status-tag ${tagClass}">${task.status}</span>
                        ${task.status !== 'completed' ? `<button class="action-btn btn-done" onclick="completeTask(${task.id})">Done</button>` : ''}
                        <button class="action-btn btn-del" onclick="deleteTask(${task.id})">Remove</button>
                    </div>
                </div>`;
            });
        }
        async function addTask() {
            const title = document.getElementById('taskInput').value.trim();
            const priority = document.getElementById('prioritySelect').value;
            if (!title) return alert('Please enter a task!');
            const now = new Date();
            const time = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            await fetch('/api/tasks', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title, priority, time})
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
        "title": data['title'],
        "status": "pending",
        "priority": data.get('priority', 'medium'),
        "time": data.get('time', datetime.datetime.now().strftime("%I:%M %p"))
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'completed'
            return jsonify(task)
    return jsonify({"error": "Not found"}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({"message": "Deleted"})

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/info')
def info():
    return jsonify({
        'app': 'DevSecOps Manager',
        'version': '3.0.0',
        'pipeline': 'Jenkins CI/CD',
        'security': 'SonarQube + Trivy',
        'container': 'Docker'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)