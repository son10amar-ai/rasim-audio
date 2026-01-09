from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import time

app = Flask(__name__)

# مجلد مؤقت لحفظ الملفات
DOWNLOAD_FOLDER = '/tmp'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "الرجاء وضع رابط صحيح"

    try:
        # إعدادات متقدمة لتخطي حماية يوتيوب
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
            # هذا السطر مهم جداً لتخطي الحماية
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            
            # إرسال الملف للمستخدم
            return send_file(file_path, as_attachment=True)

    except Exception as e:
        return f"حدث خطأ أثناء التحويل: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
