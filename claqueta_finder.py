import cv2
import numpy as np
import librosa

def encontrar_claqueta_audio(ruta_archivo):
    # Cargar audio
    y, sr = librosa.load(ruta_archivo)
    
    # Calcular la envolvente de fuerza de onset (spectral flux)
    # Esto mide cuán rápido cambia el espectro de la señal, 
    # lo cual es un gran indicador de transientes (sonidos cortos y agudos como un clic)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    
    # Encontrar el frame con el valor máximo en la envolvente de onset
    # Este es el punto de mayor cambio espectral, probablemente la claqueta.
    claqueta_frame = np.argmax(onset_env)
    
    # Convertir el frame a tiempo
    timestamp_claqueta = librosa.frames_to_time([claqueta_frame], sr=sr)[0]
    
    # Obtener FPS del video para convertir el timestamp a número de frame de video
    cap = cv2.VideoCapture(ruta_archivo)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    video_frame = int(timestamp_claqueta * fps)

    # Devolvemos el frame en una lista para compatibilidad con show_onset_frames
    return [video_frame], timestamp_claqueta

def show_onset_frames(video_path, onset_frames):
    """
    Reads a video and displays the frames specified by onset_frames.

    Args:
        video_path (str): The path to the video file.
        onset_frames (list): A list of frame numbers to display.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file: {video_path}")
        return

    for frame_number in onset_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()

        if ret:
            cv2.imshow(f'Frame {frame_number}', frame)
            cv2.waitKey(0)
        else:
            print(f"Warning: Could not read frame {frame_number}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # --- IMPORTANT ---
    # Replace this with your actual list of onset frames.
    video_path = 'data/claqueta.MP4'
    onset_frames, _ = encontrar_claqueta_audio(video_path)
    show_onset_frames(video_path, onset_frames)

    print(onset_frames)