import os
from flask import Flask, redirect, request, render_template, jsonify, send_from_directory, url_for
import yt_dlp
import imageio_ffmpeg as ffmpeg

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/submit', methods=['POST'])
def submit():
    video_url = request.form['videoUrl']
    if not video_url:
        return jsonify({'error': 'Por favor, insira um link válido do YouTube.'}), 400

    try:
        download_path = os.path.join(os.getcwd(), 'downloads')
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        
        # Configuração do yt-dlp
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'cookiefile': 'cookies.txt'},

        # Baixar o vídeo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url)
            video_title = info_dict.get('title', None)
            video_extension = info_dict.get('ext', 'mp4')

        # Caminho completo do arquivo baixado
        filename = f"{video_title}.{video_extension}"
        file_path = os.path.join(download_path, filename)

        # Gera a URL de download
        download_url = url_for('download_file', filename=filename)

        return jsonify({'download_url': download_url})

    except Exception as e:
        return jsonify({'error': f'Ocorreu um erro: {e}'}), 500

@app.route('/submit2', methods=['POST'])
def submit2():
    video_url = request.form.get('videoUrl')
    if not video_url:
        return jsonify({'error': 'Por favor, insira um link válido do YouTube.'}), 400

    try:
        download_path = os.path.join(os.getcwd(), 'downloads')
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        # Localizar o caminho do ffmpeg automaticamente
        ffmpeg_path = ffmpeg.get_ffmpeg_exe()
        
        # Configuração do yt-dlp para baixar apenas o áudio e convertê-lo para MP3
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'cookiefile': 'cookies.txt',
            'ffmpeg_location': ffmpeg_path
        }
        
        # Baixar o vídeo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url)
            audio_title = info_dict.get('title', None)
            audio_extension = 'mp3'

        # Caminho completo do arquivo baixado
        filename = f"{audio_title}.{audio_extension}"
        file_path = os.path.join(download_path, filename)

        # Gera a URL de download
        download_url = url_for('download_file', filename=filename)

        return jsonify({'download_url': download_url})

    except Exception as e:
        return jsonify({'error': f'Ocorreu um erro: {e}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    download_path = os.path.join(os.getcwd(), 'downloads')
    return send_from_directory(directory=download_path, path=filename, as_attachment=True)



if __name__ == '__main__':
    app.run()