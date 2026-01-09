from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url: return "رابط غير صحيح"
    
    # مجلد التحميل المؤقت
    out_dir = '/tmp'
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{out_dir}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        # هذه الإعدادات لتجاوز حظر يوتيوب في Render
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            path = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            return send_file(path, as_attachment=True)
    except Exception as e:
        return f"خطأ: يوتيوب يرفض الطلب حالياً. جرب رابطاً آخر أو انتظر قليلاً."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
