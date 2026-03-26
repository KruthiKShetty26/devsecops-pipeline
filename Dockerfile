FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Save it as:
- **File name:** `Dockerfile` (no extension at all!)
- **Save as type:** **"All Files (*.*)"**

Save it in the **main project folder** (`devsecops-pipeline`), not inside `tests`.

Then run:
```
dir