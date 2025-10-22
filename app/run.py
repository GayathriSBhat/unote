# ...existing code...
from uvicorn import run

if __name__ == "__main__":
    # runs the app exported as `app` in app/main.py
    run("app.main:app", host="0.0.0.0", port=8000, reload=True)