import os
from flask import request, render_template, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename

from app import app

from app.services import cut_video

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        flash('Nenhum arquivo enviado')
        return redirect(url_for('index'))
    
    file = request.files['video']
    start_time = request.form.get('start_time', type=float)
    end_time = request.form.get('end_time', type=float)

    if file.filename == '' or start_time is None or end_time is None:
        flash('Faltam parâmetros: arquivo, tempo inicial ou tempo final.')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_filename = "cortado_" + filename
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        file.save(input_path)
        
        success = cut_video(input_path, output_path, start_time, end_time)
        
        if success:
            return render_template('result.html', filename=output_filename)
        else:
            flash('Ocorreu um erro ao processar o vídeo.')
            return redirect(url_for('index'))

    flash('Tipo de arquivo não permitido.')
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)