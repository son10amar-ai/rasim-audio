import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        url = request.form.get('video_url')
        if url:
            # تنظيف الرابط للتأكد من أنه يعمل بشكل صحيح
            video_id = ""
            if "v=" in url: video_id = url.split("v=")[1].split("&")[0]
            elif "youtu.be/" in url: video_id = url.split("youtu.be/")[1].split("?")[0]
            
            if video_id:
                # توجيه المستخدم لمحرك تحميل خارجي قوي لا يمكن حظره
                # هذا المحرك سيعطيك خيارات MP3 و MP4 مباشرة كما في MP3Juice
                download_service = f"https://www.y2mate.com/youtube/{video_id}"
                return redirect(download_service)
            else:
                error = "يرجى وضع رابط يوتيوب صحيح."
            
    return render_template('station.html', error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
    
