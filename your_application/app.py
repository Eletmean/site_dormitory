import os
from fastapi import FastAPI

port = int(os.environ.get("PORT", 10000))  # Default to 10000 if PORT is not set

app = FastAPI()

# Add your routes and other configurations here

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)