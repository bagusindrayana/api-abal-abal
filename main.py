import uvicorn
import os
from app.main import app

default_port = "8080"
try:
    port = int(float(os.environ.get("PORT", default_port)))
except TypeError:
    port = int(default_port)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)