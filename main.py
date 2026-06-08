from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL do'}), 400
    try:
        ydl_opts = {
            'quiet': True,
            'noplaylist': True,
            'format': 'best[ext=mp4]/best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            for f in info.get('formats', []):
                if f.get('url') and f.get('acodec') != 'none' and f.get('vcodec') != 'none':
                    formats.append({
                        'quality': f.get('format_note', f.get('height', 'Video')),
                        'url': f.get('url'),
                        'ext': f.get('ext', 'mp4')
                    })
            if not formats:
                for f in info.get('formats', []):
                    if f.get('url'):
                        formats.append({
                            'quality': f.get('format_note', 'Video'),
                            'url': f.get('url'),
                            'ext': f.get('ext', 'mp4')
                        })
            return jsonify({'links': formats[-5:]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
