import os
import yt_dlp
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        url = request.form.get('video_url')
        if url:
            try:
                # إعدادات لاستخراج الرابط المباشر فقط لتجاوز حظر السيرفر
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'quiet': True,
                    'no_warnings': True,
                    'nocheckcertificate': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    direct_link = info.get('url')
                    # توجيه المستخدم مباشرة لصفحة googlevideo كما في صورتك الناجحة
                    return redirect(direct_link)
                    
            except Exception as e:
                error = "عذراً، يوتيوب يمنع الوصول حالياً. جرب رابطاً آخر."
            
    return render_template('station.html', error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
                    
