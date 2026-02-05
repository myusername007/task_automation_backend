from fastapi import FastAPI

app = FastAPI(title="Task Automation Backend")

@app.get("/health")
def health():
    return {"status": "ok"}