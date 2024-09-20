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

# Função para processar o vídeo da câmera
def process_camera():
    cap = cv2.VideoCapture(0)  # Abre a câmera (0 para câmera padrão)

    if not cap.isOpened():
        print("Erro ao acessar a câmera")
        return

    while True:
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

            # Mostra o frame com a silhueta
            cv2.imshow('Camera with Silhouette and Landmarks', frame_with_silhouette)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Inicia o processamento da câmera
process_camera()
