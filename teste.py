import cv2
import pygame
import os
import sys

# Inicializa o pygame
pygame.init()

# Caminho do vídeo
video_path = os.path.join(os.path.dirname(__file__), "video.mp4")

# Verifica se o arquivo de vídeo existe
if not os.path.exists(video_path):
    print(f"Erro: O arquivo de vídeo '{video_path}' não foi encontrado.")
    sys.exit(1)

# Carrega o vídeo com OpenCV
cap = cv2.VideoCapture(video_path)

# Verifica se o vídeo foi carregado corretamente
if not cap.isOpened():
    print("Erro ao abrir o vídeo.")
    sys.exit(1)

# Obtém dimensões do vídeo
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Configura a janela do pygame
screen = pygame.display.set_mode((frame_width, frame_height))
pygame.display.set_caption("Show Video on Screen")

# Loop de reprodução do vídeo
clock = pygame.time.Clock()
running = True

while running and cap.isOpened():
    ret, frame = cap.read()
    if not ret:  # Sai do loop quando o vídeo termina
        break

    # Converte o frame de BGR (OpenCV) para RGB (pygame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Cria uma superfície do pygame a partir do frame
    frame_surface = pygame.surfarray.make_surface(frame)
    frame_surface = pygame.transform.rotate(frame_surface, -90)  # Rotaciona para exibição correta

    # Exibe o frame na tela
    screen.blit(frame_surface, (0, 0))
    pygame.display.flip()

    # Verifica eventos do pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Fecha a janela
            running = False

    # Controla a taxa de frames
    clock.tick(fps)

# Libera os recursos
cap.release()
pygame.quit()
