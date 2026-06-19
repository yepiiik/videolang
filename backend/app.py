from fastapi import FastAPI

from routers.youtube import router as youtube_router

app = FastAPI(
    title="VideoLang API",
    version="1.0.0"
)

app.include_router(youtube_router)


@app.get("/")
def root():
    return {
        "message": "VideoLang Backend is running!"
    }