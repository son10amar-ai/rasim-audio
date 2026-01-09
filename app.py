import os
import requests
import yt_dlp
from flask import Flask, render_template, request, Response, stream_with_context
from urllib.parse import quote

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_data = None
    error = None

    if request.method == 'POST':
        url = request.form.get('video_url')
        if url:
            try:
                # إعدادات قوية لتجاوز حظر السيرفرات
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'quiet': True,
                    'no_warnings': True,
                    'nocheckcertificate': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    audio_data = {
                        'title': info.get('title', 'Rasim_Audio'),
                        'thumbnail': info.get('thumbnail'),
                        'audio_link': info.get('url')
                    }
            except Exception as e:
                print(f"Error: {e}")
                error = "عذراً، يوتيوب يفرض قيوداً على هذا الرابط، جرب رابطاً آخر."
            
    return render_template('station.html', data=audio_data, error=error)

@app.route('/download_mp3')
def download_mp3():
    target_url = request.args.get('url')
    filename = request.args.get('name', 'audio')
    
    # جلب الملف كبث مباشر لتوفير الذاكرة وتجنب التعليق
    req = requests.get(target_url, stream=True, timeout=30)
    
    def generate():
        for chunk in req.iter_content(chunk_size=1024 * 64):
            if chunk:
                yield chunk

    safe_filename = quote(f"{filename}.mp3")

    return Response(
        stream_with_context(generate()),
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{safe_filename}",
            "Content-Type": "audio/mpeg"
        }
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
    
