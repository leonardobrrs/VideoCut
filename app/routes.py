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
    
    # Pega Horas, Minutos e Segundos separadamente.
    # Se o campo estiver vazio, assume 0.
    s_h = request.form.get('start_h', 0, type=int)
    s_m = request.form.get('start_m', 0, type=int)
    s_s = request.form.get('start_s', 0, type=int)

    e_h = request.form.get('end_h', 0, type=int)
    e_m = request.form.get('end_m', 0, type=int)
    e_s = request.form.get('end_s', 0, type=int)

    # Converte tudo para o total de segundos
    start_seconds = (s_h * 3600) + (s_m * 60) + s_s
    end_seconds = (e_h * 3600) + (e_m * 60) + e_s

    # Para fins de log/debug (opcional)
    print(f"Início: {start_seconds}s | Fim: {end_seconds}s")

    # Validação 1: Campos obrigatórios e formato
    if file.filename == '' or start_seconds is None or end_seconds is None:
        flash('Faltam parâmetros ou o formato de tempo é inválido (use hh:mm:ss).')
        return redirect(url_for('index'))

    # Validação 2: Tempo final deve ser maior que inicial
    if start_seconds >= end_seconds:
        flash('O tempo final deve ser maior que o tempo inicial.')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = app.config['UPLOAD_FOLDER']
        input_path = os.path.join(upload_folder, filename)
        
        # Salva o arquivo temporariamente para verificar
        file.save(input_path)

        # --- NOVA VALIDAÇÃO: Duração do Vídeo ---
        try:
            # Carrega o clipe APENAS para ler a duração (sem carregar áudio/vídeo pesado)
            with VideoFileClip(input_path) as video_check:
                duration = video_check.duration
            
            # Validação 3: O corte não pode exceder o tamanho do vídeo
            if end_seconds > duration:
                # Remove o arquivo já que falhou
                os.remove(input_path) 
                flash(f'Erro: O tempo final ({end_seconds}) é maior que a duração do vídeo ({duration:.2f}s).')
                return redirect(url_for('index'))
                
        except Exception as e:
            # Se der erro ao ler o vídeo, apaga e avisa
            if os.path.exists(input_path): os.remove(input_path)
            flash(f'Erro ao ler o arquivo de vídeo: {str(e)}')
            return redirect(url_for('index'))
        # ----------------------------------------

        output_filename = f"cut_{filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Chama a função de corte
        success = cut_video(input_path, output_path, start_seconds, end_seconds)
        
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