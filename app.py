from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# إعداد مجلد مؤقت للتحميلات ليتناسب مع بيئة Render
DOWNLOAD_FOLDER = '/tmp'

@app.route('/')
def index():
    # هذا السطر يقوم بتشغيل واجهتك البنفسجية (index.html)
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "الرجاء إدخال رابط الفيديو"

    # إعدادات المحرك مع تمويه لتجاوز حظر يوتيوب
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
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # جلب معلومات الفيديو وتحميله
            info = ydl.extract_info(url, download=True)
            # تحديد مسار الملف بعد التحويل لـ MP3
            file_path = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
            
            # إرسال الملف للمستخدم للتحميل
            return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"عذراً، حدث خطأ: {str(e)}"

if __name__ == '__main__':
    # تأكد أن المنفذ هو 10000 كما هو مطلوب في Render
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
