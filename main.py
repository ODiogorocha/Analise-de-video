import cv2
import mediapipe as mp
import numpy as np

# Inicializa o mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Função para desenhar pontos-chave e linhas do caminho no frame
def draw_landmarks_and_differences(image1, image2, landmarks1, landmarks2):
    height, width, _ = image1.shape

    # Desenha pontos-chave e linhas entre pontos no primeiro vídeo
    for landmark in landmarks1:
        x = int(landmark.x * width)
        y = int(landmark.y * height)
        cv2.circle(image1, (x, y), 5, (0, 255, 0), -1)
    
    # Desenha pontos-chave e linhas entre pontos no segundo vídeo
    for landmark in landmarks2:
        x = int(landmark.x * width)
        y = int(landmark.y * height)
        cv2.circle(image2, (x, y), 5, (0, 255, 0), -1)
    
    # Desenha linhas de diferença
    for i in range(len(landmarks1)):
        x1, y1 = int(landmarks1[i].x * width), int(landmarks1[i].y * height)
        x2, y2 = int(landmarks2[i].x * width), int(landmarks2[i].y * height)
        cv2.line(image1, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Linha vermelha para diferenças
        cv2.line(image2, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Linha vermelha para diferenças

def process_video(video_path, output_path1, output_path2):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Erro ao abrir o vídeo {video_path}")
        return

    # Cria objetos VideoWriter para salvar os vídeos de saída
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out1 = cv2.VideoWriter(output_path1, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
    out2 = cv2.VideoWriter(output_path2, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

    previous_landmarks1 = None
    previous_landmarks2 = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Converte o frame para RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            if previous_landmarks1:
                # Cria duas imagens para comparar
                frame1 = frame.copy()
                frame2 = frame.copy()

                # Desenha os pontos e as diferenças
                draw_landmarks_and_differences(frame1, frame2, previous_landmarks1, landmarks)

                # Mostra os frames com as diferenças desenhadas
                cv2.imshow('Video 1 with Differences', frame1)
                cv2.imshow('Video 2 with Differences', frame2)

                # Salva os frames com as diferenças
                out1.write(frame1)
                out2.write(frame2)
            
            # Atualiza os pontos anteriores
            previous_landmarks1 = landmarks

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out1.release()
    out2.release()
    cv2.destroyAllWindows()

# Caminhos para os vídeos a serem comparados e os arquivos de saída
video_path = 'video.mp4'
output_path1 = 'output_video1.mp4'
output_path2 = 'output_video2.mp4'

# Processa o vídeo e salva os resultados com diferenças desenhadas
process_video(video_path, output_path1, output_path2)
