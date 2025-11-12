from moviepy import VideoFileClip

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
    
def time_to_seconds(time_str):

    if not time_str or time_str.strip() == '':
        return 0.0

    try:
        parts = str(time_str).split(':')
        parts.reverse()
        
        total_seconds = 0
        for i, part in enumerate(parts):
            
            part_value = 0
            if part.strip():
                part_value = float(part)

            if i == 0:  # Segundos
                total_seconds += part_value
            elif i == 1:  # Minutos
                total_seconds += part_value * 60
            elif i == 2:  # Horas
                total_seconds += part_value * 3600
        
        return total_seconds
        
    except (ValueError, AttributeError):
        return None