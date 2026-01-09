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
                # إعدادات جلب أفضل جودة صوت متاحة فقط
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'quiet': True,
                    'no_warnings': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    # استخراج رابط الصوت المباشر وعنوان المقطع
                    audio_url = info.get('url')
                    title = info.get('title', 'Rasim_Audio')
                    thumbnail = info.get('thumbnail')

                    audio_data = {
                        'title': title,
                        'thumbnail': thumbnail,
                        'audio_link': audio_url
                    }
                    
            except Exception as e:
                print(f"Error: {e}")
                error = "عذراً، تعذر معالجة الرابط. تأكد من أنه رابط يوتيوب صحيح."
            
    return render_template('station.html', data=audio_data, error=error)

@app.route('/download_mp3')
def download_mp3():
    target_url = request.args.get('url')
    filename = request.args.get('name', 'audio')
    
    # طلب الملف من المصدر
    req = requests.get(target_url, stream=True, timeout=20)
    
    def generate():
        for chunk in req.iter_content(chunk_size=1024 * 32):
            if chunk:
                yield chunk

    # ترميز الاسم لدعم العربية بشكل كامل
    safe_filename = quote(f"{filename}.mp3")

    return Response(
        stream_with_context(generate()),
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{safe_filename}",
            "Content-Type": "audio/mpeg",
            "Content-Length": req.headers.get('Content-Length', '')
        }
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
                    
