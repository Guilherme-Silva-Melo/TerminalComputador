import pygame
import os
from pyvidplayer2 import Video

pygame.init()

WIDTH, HEIGHT = (1920,1080)
#WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Terminal Menu")

def abrirVideo(video_path):
    vid = Video(video_path)
    vid.resize((WIDTH, HEIGHT))
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN)):
                running = False

        screen.fill((0, 0, 0))
        
        if vid.active:
            vid.draw(screen, (0, 0), force_draw=True)
            pygame.display.update()
        else:
            running = False

        clock.tick(24)

    vid.close()
    main()

menu_items = {
    "ARQUIVOS": ["20/01/1996 -> Varginha - MG", "19/05/1986 -> Rio de Janeiro - RJ"], 
    "CONFIDENCIAL": [], 
    "VIDEOS": ["Abrir Video"], 
    "UTILIDADE": ["LETRAS", "ALFABETOS", "TELEFONE"]
}

TEXTO_VARGINHA = [
    "RELATÓRIO CONFIDENCIAL - FORÇAS ARMADAS BRASILEIRAS",
    "CLASSIFICAÇÃO: ULTRASSECRETO",
    "DATA: 22/01/1996",
    "LOCAL: Varginha, MG - Brasil",
    "RELATÓRIO Nº: 0196/SE",
    "",
    "Em resposta aos eventos em Varginha, foi realizada uma operação especial para conter e recuperar entidades biológicas desconhecidas.",
    "Duas entidades foram encontradas vivas e uma terceira sem sinais vitais. Elas tinham altura entre 1,20 e 1,50 metros, corpo delgado,",
    "pele escura e oleosa, cabeça grande, olhos vermelhos e amendoados, boca pequena, nariz reduzido a fendas e ausência de orelhas.",
    "Tinham três dedos longos nas mãos e pés alongados. Não comunicavam verbalmente, mas demonstravam compreensão não verbal.",
    "As entidades estavam debilitadas e foram isoladas para análise médica. Uma delas faleceu em menos de 24 horas sem sinais de trauma físico.",
    "Elas foram transportadas sob protocolo de segurança máxima para instalações de pesquisa sigilosas. Evidências foram lacradas e enviadas",
    "para análise em laboratórios de segurança nacional.",
    "Foi recomendado restringir informações ao público, monitorar a região para novas ocorrências e reportar diretamente ao alto comando",
    "qualquer evolução no caso.",
    "",
    "ASSINATURA:",
    "Gen. Dantas",
    "Forças Armadas do Brasil",
    "DOCUMENTO CLASSIFICADO. ACESSO RESTRITO."
]

selected_item = 0
submenu_item = 0
in_submenu = False
password = "1234"
content_unlocked = False
show_password_prompt = False
input_text = ""
show_varginha_report = False

# Variáveis para controle de scroll
scroll_y = 0
scroll_speed = 30  # Velocidade de scroll
max_scroll = 0  # Para armazenar o limite máximo de scroll

def draw_menu():
    global scroll_y
    screen.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    title_text = font.render("TERMINAL PESSOAL", True, (0, 255, 0))
    screen.blit(title_text, (20, 20))

    if show_varginha_report:
        report_lines = TEXTO_VARGINHA
        
        max_scroll = len(report_lines) * 30 - HEIGHT + 60  # Calcular o limite de scroll com base no número de linhas
        
        for i, line in enumerate(report_lines):
            text_surface = font.render(line, True, (144, 238, 144))
            screen.blit(text_surface, (20, 60 + i * 30 - scroll_y))  # Aplicar o deslocamento do scroll
        
    else:
        menu_keys = list(menu_items.keys())
        for i, item in enumerate(menu_keys):
            color = (0, 255, 0) if i == selected_item else (0, 128, 0)
            item_text = font.render(item, True, color)
            screen.blit(item_text, (20, 100 + i * 40))

        if in_submenu:
            submenu_items = menu_items[menu_keys[selected_item]]
            for j, content in enumerate(submenu_items):
                color = (144, 238, 144) if j == submenu_item else (0, 128, 0)
                content_text = font.render(content, True, color)
                screen.blit(content_text, (220, 120 + j * 40))

        if show_password_prompt:
            prompt_text = font.render("Insira a senha:", True, (0, 255, 0))
            screen.blit(prompt_text, (220, 120))
            password_text = font.render(input_text, True, (144, 238, 144))
            screen.blit(password_text, (220, 160))

def main():
    global selected_item, submenu_item, in_submenu, content_unlocked, input_text, show_password_prompt, show_varginha_report, scroll_y

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if show_varginha_report:
                        show_varginha_report = False
                    elif in_submenu:
                        in_submenu = False
                    else:
                        content_unlocked = False
                        show_password_prompt = False
                elif not show_password_prompt and not content_unlocked:
                    if in_submenu:
                        if event.key == pygame.K_UP:
                            submenu_item = (submenu_item - 1) % len(menu_items[list(menu_items.keys())[selected_item]])
                        elif event.key == pygame.K_DOWN:
                            submenu_item = (submenu_item + 1) % len(menu_items[list(menu_items.keys())[selected_item]])
                        elif event.key == pygame.K_RETURN:
                            submenu_selection = menu_items[list(menu_items.keys())[selected_item]][submenu_item]
                            if submenu_selection == "20/01/1996 -> Varginha - MG":
                                show_varginha_report = True
                            else:
                                content_unlocked = True
                    else:
                        if event.key == pygame.K_UP:
                            selected_item = (selected_item - 1) % len(menu_items)
                        elif event.key == pygame.K_DOWN:
                            selected_item = (selected_item + 1) % len(menu_items)
                        elif event.key == pygame.K_RETURN:
                            selected_category = list(menu_items.keys())[selected_item]
                            if selected_category == "CONFIDENCIAL":
                                show_password_prompt = True
                                input_text = ""
                            elif selected_category == "VIDEOS":
                                abrirVideo('videoMorse.mp4')
                            else:
                                in_submenu = True
                elif show_password_prompt:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        if input_text == password:
                            content_unlocked = False
                            show_password_prompt = False
                            abrirVideo('youveBeen.mp4')
                        else:
                            input_text = ""
                    elif event.unicode.isprintable():
                        input_text += event.unicode

                # Scroll
                if show_varginha_report:
                    if event.key == pygame.K_DOWN:
                        scroll_y = min(scroll_y + scroll_speed, max_scroll)
                    elif event.key == pygame.K_UP:
                        scroll_y = max(scroll_y - scroll_speed, 0)
        
        draw_menu()
        pygame.display.flip()
        clock.tick(24)

    pygame.quit()

if __name__ == "__main__":
    main()
