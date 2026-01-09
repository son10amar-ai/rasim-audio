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
                # إعدادات متقدمة جداً للتنكر وتجاوز الحظر
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'quiet': True,
                    'no_warnings': True,
                    'nocheckcertificate': True,
                    # استخدام هوية متصفح حقيقي ومشهور
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'referer': 'https://www.youtube.com/',
                    'geo_bypass': True,
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
                # رسالة خطأ ذكية توضح للمستخدم أن المشكلة من حماية يوتيوب
                error = "عذراً، يوتيوب يمنع السيرفر حالياً. جرب رابط فيديو آخر أو أعد المحاولة بعد دقيقة."
            
    return render_template('station.html', data=audio_data, error=error)

@app.route('/download_mp3')
def download_mp3():
    target_url = request.args.get('url')
    filename = request.args.get('name', 'audio')
    
    # رأس طلب (Header) لخداع يوتيوب أثناء سحب ملف الصوت
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Range': 'bytes=0-'
    }
    
    # سحب الملف بنظام البث المباشر (Stream)
    req = requests.get(target_url, stream=True, timeout=60, headers=headers)
    
    def generate():
        for chunk in req.iter_content(chunk_size=1024 * 128): # زيادة حجم القطعة لسرعة أكبر
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
    # ضمان العمل على منفذ Render الصحيح
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
    
