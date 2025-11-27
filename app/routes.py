import os
from flask import request, render_template, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
from app import app
from app.services import cut_video
from moviepy.video.io.VideoFileClip import VideoFileClip
from app.services import cut_video, cleanup_old_files

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_video():
    cleanup_old_files([app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']])

    if 'video' not in request.files:
        flash('Nenhum arquivo enviado.')
        return redirect(url_for('index'))
    
    file = request.files['video']
    output_format = request.form.get('format', 'mp4')
    
    # 1. NOVIDADE: Checkbox "Processar Inteiro"
    # Se estiver marcado, ignoramos os tempos digitados
    process_full = 'process_full' in request.form

    # --- NOVO: Captura a opção de remover áudio ---
    remove_audio = 'remove_audio' in request.form

    resolution = request.form.get('resolution', 'original')

    s_h = request.form.get('start_h', 0, type=int)
    s_m = request.form.get('start_m', 0, type=int)
    s_s = request.form.get('start_s', 0, type=int)

    e_h = request.form.get('end_h', 0, type=int)
    e_m = request.form.get('end_m', 0, type=int)
    e_s = request.form.get('end_s', 0, type=int)

    start_seconds = (s_h * 3600) + (s_m * 60) + s_s
    end_seconds = (e_h * 3600) + (e_m * 60) + e_s

    # Validações iniciais (Só validamos tempo se NÃO for processar inteiro)
    if not process_full:
        if file.filename == '': # Validação básica
             flash('Selecione um arquivo.')
             return redirect(url_for('index'))
        
        if start_seconds >= end_seconds:
            flash('O tempo final deve ser maior que o tempo inicial.')
            return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        try:
            # Lemos a duração para validar e para usar no "Processar Inteiro"
            with VideoFileClip(input_path) as video_check:
                duration = video_check.duration
            
            # 2. Lógica do "Processar Inteiro"
            if process_full:
                start_seconds = 0
                end_seconds = duration
            
            # Validação: O corte não pode exceder o tamanho do vídeo
            if end_seconds > duration:
                os.remove(input_path) 
                flash(f'Erro: O tempo final ({end_seconds}) é maior que a duração do vídeo ({duration:.2f}s).')
                return redirect(url_for('index'))
            
            # 3. NOVIDADE: Limite de Tempo para GIFs (Ex: 15 segundos)
            if output_format == 'gif':
                gif_duration = end_seconds - start_seconds
                limit_seconds = 15 # Configure o limite aqui
                if gif_duration > limit_seconds:
                    os.remove(input_path)
                    flash(f'O limite de tempo para GIFs é {limit_seconds} segundos (seu trecho tem {gif_duration:.1f}s).')
                    return redirect(url_for('index'))
                
        except Exception as e:
            if os.path.exists(input_path): os.remove(input_path)
            flash(f'Erro ao ler o vídeo: {str(e)}')
            return redirect(url_for('index'))

        file_extension = output_format
        output_filename = f"cut_{os.path.splitext(filename)[0]}.{file_extension}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        success, error_message = cut_video(input_path, output_path, start_seconds, end_seconds, output_format=output_format, remove_audio=remove_audio, resolution=resolution)
        
        if success:
            # 4. NOVIDADE: Passamos o 'output_format' para o template
            return render_template('result.html', filename=output_filename, format=output_format)
        else:
            flash(f'Erro ao processar: {error_message}')
            return redirect(url_for('index'))

    flash('Tipo de arquivo não permitido.')
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

# Rota para servir o arquivo para o player (sem forçar download)
@app.route('/files/<filename>')
def get_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=False)