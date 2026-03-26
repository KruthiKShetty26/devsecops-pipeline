from app import app

def test_home():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_health():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
```

Save it as `test_app.py` inside the `tests` folder (not the main folder — inside `tests`).

Then run:
```
dir tests