import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_data = None
    error = None

    if request.method == 'POST':
        url = request.form.get('video_url')
        if url:
            try:
                # استخدام API خارجي مستقر لتجاوز حظر السيرفرات المجانية
                api_url = f"https://api.vevioz.com/api/button/mp3?url={url}"
                # هذا المحرك سيقوم بتوليد زر تحميل مباشر
                audio_data = {
                    'title': "جاهز للتحميل",
                    'thumbnail': "https://via.placeholder.com/150/ff00ff/ffffff?text=MP3",
                    'audio_link': api_url
                }
            except Exception as e:
                error = "حدث خطأ في الاتصال، جرب رابطاً آخر."
            
    return render_template('station.html', data=audio_data, error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
    
