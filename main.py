import cv2
import mediapipe as mp

# Inicializa o mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Lista de pares de pontos para desenhar as linhas da silhueta do corpo
POSE_CONNECTIONS = [
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER),
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
    (mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST),
    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW),
    (mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST),
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP),
    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_HIP),
    (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP),
    (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE),
    (mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE),
    (mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE),
    (mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE)
]

# Função para desenhar a silhueta e os pontos-chave
def draw_silhouette_and_keypoints(image, landmarks):
    height, width, _ = image.shape

    # Desenha a silhueta (linhas conectando os pontos) em azul
    for connection in POSE_CONNECTIONS:
        point1 = landmarks[connection[0].value]
        point2 = landmarks[connection[1].value]

        x1 = int(point1.x * width)
        y1 = int(point1.y * height)
        x2 = int(point2.x * width)
        y2 = int(point2.y * height)

        # Desenha a linha conectando os pontos (silhueta em azul)
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 3)  # Azul (BGR)

    # Desenha os pontos-chave em verde
    for landmark in landmarks:
        x = int(landmark.x * width)
        y = int(landmark.y * height)
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)  # Verde (BGR)

# Função para processar o vídeo
def process_video_with_shadow(video_path, output_path1, output_path2):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Erro ao abrir o vídeo {video_path}")
        return

    # Cria objetos VideoWriter para salvar os vídeos de saída
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out1 = cv2.VideoWriter(output_path1, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
    out2 = cv2.VideoWriter(output_path2, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Converte o frame para RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Desenha a silhueta em azul e os pontos-chave em verde no frame original
            frame_with_silhouette = frame.copy()
            draw_silhouette_and_keypoints(frame_with_silhouette, landmarks)

            # Cria a imagem de "sombra" (somente a silhueta em fundo preto)
            silhouette_frame = frame.copy()
            silhouette_frame[:] = (0, 0, 0)  # Fundo preto
            draw_silhouette_and_keypoints(silhouette_frame, landmarks)

            # Mostra os dois frames: original com silhueta e a sombra
            cv2.imshow('Original Video with Silhouette and Landmarks', frame_with_silhouette)
            cv2.imshow('Shadow Video with Silhouette Only', silhouette_frame)

            # Salva os frames com a silhueta e a sombra (somente a silhueta)
            out1.write(frame_with_silhouette)  # Vídeo original com silhueta azul e pontos verdes
            out2.write(silhouette_frame)  # Vídeo sombra com a silhueta

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out1.release()
    out2.release()
    cv2.destroyAllWindows()

# Caminhos para o vídeo a ser analisado e os arquivos de saída
video_path = 'video.mp4'
output_path1 = 'output_with_silhouette.mp4'  # Vídeo original com silhueta azul e pontos verdes
output_path2 = 'output_shadow_silhouette.mp4'  # Vídeo apenas com a silhueta (sombra)

# Processa o vídeo e salva o resultado com a silhueta e a sombra
process_video_with_shadow(video_path, output_path1, output_path2)
