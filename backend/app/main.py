from fastapi import FastAPI

app = FastAPI(
    title="Ha-to-Pe File System",
    description="Ha-to-Pe File System",
    version="1.0.0",
)

@app.get("/")
def home():
    return {"message": "Ha-to-Pe is running..."}