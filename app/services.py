from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import time

def cut_video(input_path, output_path, start_seconds, end_seconds, output_format='mp4', remove_audio=False, resolution='original'):
    """
    Corta o vídeo e salva no formato desejado.
    Retorna: (Sucesso: bool, Mensagem de Erro: str ou None)
    """
    try:
        video = VideoFileClip(input_path)
        
        # 1. Corta
        cut = video.subclipped(start_seconds, end_seconds)
        
        # 2. Redimensiona (Se necessário) - Válido para MP4 e GIF
        if resolution != 'original' and resolution.isdigit():
            target_height = int(resolution)
            # Verifica se o vídeo já não é menor que o alvo para não "esticar"
            if video.h > target_height:
                cut = cut.resized(height=target_height)
        
        # 3. Processamento por formato
        if output_format == 'mp3':
            if video.audio:
                cut.audio.write_audiofile(output_path)
            else:
                video.close()
                return False, "O vídeo original não possui áudio."

        elif output_format == 'gif':
            # Para GIF, forçamos 480px se o usuário deixou em 'original', 
            # ou usamos o que ele escolheu (se for menor que 480)
            if resolution == 'original':
                cut = cut.resized(width=480)
            cut.write_gif(output_path, fps=10)
        
        else:
            # Padrão MP4
            if remove_audio:
                cut = cut.without_audio()
                
            cut.write_videofile(output_path, codec="libx264", audio_codec="aac", preset='fast')
            
        video.close()
        return True, None
        
    except Exception as e:
        # Fecha o arquivo em caso de erro também
        if 'video' in locals():
            try: video.close()
            except: pass
            
        error_msg = str(e)
        print(f"ERRO CRÍTICO MOVIEPY: {error_msg}")
        return False, error_msg # Falha, retorna o motivo

def cleanup_old_files(folder_paths, max_age_seconds=1800):
    """
    Remove arquivos das pastas especificadas que são mais antigos que 'max_age_seconds'.
    Padrão: 1800 segundos (30 minutos).
    """
    current_time = time.time()
    
    for folder in folder_paths:
        if not os.path.exists(folder):
            continue
            
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            
            # Pula se não for arquivo
            if not os.path.isfile(file_path):
                continue
                
            try:
                file_age = current_time - os.path.getmtime(file_path)
                
                if file_age > max_age_seconds:
                    os.remove(file_path)
                    print(f"Limpeza: Arquivo removido por idade: {filename}")
            except Exception as e:
                print(f"Erro ao tentar remover {filename}: {e}")