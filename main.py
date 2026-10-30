from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

# GitHub Pages等からのアクセスを全許可（CORS設定）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

@app.post("/download")
def get_download_link(req: VideoRequest):
    try:
        ydl_opts = {
            'format': 'bv*+ba/b/best',
            'quiet': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['tv', 'web_embedded', 'mweb']
                }
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(req.url, download=False)
            download_url = info.get('url') or (info.get('requested_formats', [{}])[0].get('url'))
            title = info.get('title', 'youtube_video')

            return {
                "status": "success",
                "title": title,
                "download_url": download_url
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
