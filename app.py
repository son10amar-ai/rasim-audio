import os
import yt_dlp
import requests
from flask import Flask, request, render_template_string, Response, stream_with_context
from urllib.parse import quote, unquote

app = Flask(__name__)

# واجهة الموقع الاحترافية مدمجة لضمان التشغيل
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RASIM MP3 - محول الموسيقى</title>
    <style>
        body { background: #050005; color: #f0f; font-family: 'Segoe UI', sans-serif; text-align: center; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 15px; }
        .card { width: 100%; max-width: 400px; background: #000; border: 2px solid #f0f; border-radius: 30px; padding: 30px; box-shadow: 0 0 25px rgba(255, 0, 255, 0.4); }
        h2 { text-shadow: 0 0 10px #f0f; letter-spacing: 1px; margin-bottom: 25px; }
        input { width: 100%; padding: 15px; background: #111; border: 1px solid #f0f; border-radius: 12px; color: #fff; margin-bottom: 20px; box-sizing: border-box; outline: none; }
        .btn-main { width: 100%; padding: 15px; background: #f0f; color: #000; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.3s; }
        .btn-main:hover { background: #fff; box-shadow: 0 0 20px #fff; }
        .result-box { margin-top: 15px; border: 1px solid #333; padding: 20px; border-radius: 20px; background: #080808; }
        .thumb { width: 100%; border-radius: 15px; border: 1px solid #f0f; margin-bottom: 15px; }
        .title { color: #fff; font-size: 14px; margin-bottom: 20px; display: block; font-weight: bold; }
        .dl-btn { display: block; width: 100%; padding: 15px; background: #00ffff; color: #000; border-radius: 12px; text-decoration: none; font-weight: bold; font-size: 16px; transition: 0.3s; box-shadow: 0 0 15px rgba(0, 255, 255, 0.3); }
        .dl-btn:hover { transform: translateY(-3px); filter: brightness(1.1); }
    </style>
</head>
<body>
    <div class="card">
        <h2>RASIM MP3 🎵</h2>
        <form method="POST">
            <input type="text" name="video_url" placeholder="ضع رابط فيديو يوتيوب هنا..." required>
            <button type="submit" class="btn-main">تحويل إلى MP3 ⚡</button>
        </form>

        {% if data %}
        <div class="result-box">
            <img src="{{ data.thumbnail }}" class="thumb">
            <span class="title">{{ data.title }}</span>
            <a href="/download_mp3?url={{ data.audio_link | urlencode }}&name={{ data.title | urlencode }}" class="dl-btn">
                تحميل الملف (MP3) ↓
            </a>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_data = None
    if request.method == 'POST':
        url = request.form.get('video_url')
        if url:
            try:
                # خيارات التحميل الأساسية
                ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    audio_data = {
                        'title': info.get('title', 'Rasim_Audio'),
                        'thumbnail': info.get('thumbnail'),
                        'audio_link': info.get('url')
                    }
            except Exception:
                pass
    return render_template_string(HTML_TEMPLATE, data=audio_data)

@app.route('/download_mp3')
def download_mp3():
    target_url = unquote(request.args.get('url'))
    filename = unquote(request.args.get('name', 'audio'))
    # توجيه البيانات مباشرة للمستخدم
    req = requests.get(target_url, stream=True)
    def generate():
        for chunk in req.iter_content(chunk_size=1024 * 32):
            if chunk: yield chunk

    return Response(
        stream_with_context(generate()),
        headers={
            "Content-Disposition": f"attachment; filename={quote(filename)}.mp3",
            "Content-Type": "audio/mpeg"
        }
    )

if __name__ == "__main__":
    # تحديد المنفذ تلقائياً لمنصة Render
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

