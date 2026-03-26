from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hello from DevSecOps Pipeline!</h1>'

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Save it as `app.py` inside the `devsecops-pipeline` folder.

---

**4. Create another file called `requirements.txt`** and paste this:
```
flask==3.0.0
pytest==7.4.0