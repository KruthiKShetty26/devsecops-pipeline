from flask import Flask, jsonify
import datetime
import platform

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>DevSecOps Pipeline</title>
        <style>
            body { font-family: Arial, sans-serif; background: #1a1a2e; color: white; text-align: center; padding: 50px; }
            h1 { color: #00d4ff; font-size: 3em; }
            .card { background: #16213e; border-radius: 15px; padding: 30px; margin: 20px auto; max-width: 600px; }
            .badge { background: #00d4ff; color: black; padding: 5px 15px; border-radius: 20px; font-weight: bold; }
            .green { color: #00ff88; font-size: 1.5em; }
            a { color: #00d4ff; text-decoration: none; margin: 10px; font-size: 1.2em; }
        </style>
    </head>
    <body>
        <h1>🚀 DevSecOps Pipeline</h1>
        <div class="card">
            <p class="green">✅ Application Running Successfully!</p>
            <p><span class="badge">CI/CD</span> &nbsp; <span class="badge">Docker</span> &nbsp; <span class="badge">Jenkins</span> &nbsp; <span class="badge">SonarQube</span></p>
            <br>
            <p>Automated pipeline with security scanning and continuous deployment</p>
        </div>
        <div class="card">
            <a href="/health">🏥 Health Check</a> &nbsp;&nbsp;
            <a href="/info">ℹ️ App Info</a>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'All systems operational',
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/info')
def info():
    return jsonify({
        'app': 'DevSecOps Pipeline App',
        'version': '2.0.0',
        'python': platform.python_version(),
        'platform': platform.system(),
        'pipeline': 'Jenkins CI/CD',
        'security_scan': 'SonarQube + Trivy',
        'containerized': 'Docker'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)