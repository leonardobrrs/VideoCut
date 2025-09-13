from moviepy import VideoFileClip

def cut_video(input_path, output_path, start_time, end_time):
    """
    Corta um vídeo de um tempo inicial a um tempo final.
    Os tempos são em segundos.
    """
    try:
        print(f"Carregando o vídeo: {input_path}")
        with VideoFileClip(input_path) as video:
            # Cria o subclip com o intervalo desejado
            new_clip = video.subclipped(start_time, end_time)

            print(f"Escrevendo o novo vídeo em: {output_path}")
            # Escreve o resultado em um novo arquivo
            new_clip.write_videofile(output_path, codec="libx264")

        print("Corte concluído com sucesso!")
        return True
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return False