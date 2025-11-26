from moviepy import VideoFileClip
import os
import time

def cut_video(input_path, output_path, start_time, end_time):
    """
    Corta um vídeo de um tempo inicial a um tempo final.
    Os tempos são em segundos.
    """
    try:
        print(f"Carregando o vídeo: {input_path}")
        with VideoFileClip(input_path) as video:
            new_clip = video.subclipped(start_time, end_time)

            print(f"Escrevendo o novo vídeo em: {output_path}")
            new_clip.write_videofile(output_path, codec="libx264")

        print("Corte concluído com sucesso!")
        return True
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return False
    
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
            
            # Pula se não for arquivo (ex: subpastas)
            if not os.path.isfile(file_path):
                continue
                
            try:
                # Verifica a idade do arquivo
                file_age = current_time - os.path.getmtime(file_path)
                
                if file_age > max_age_seconds:
                    os.remove(file_path)
                    print(f"Limpeza: Arquivo removido por idade: {filename}")
            except Exception as e:
                print(f"Erro ao tentar remover {filename}: {e}")