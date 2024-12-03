import pygame

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)
pygame.display.set_caption("Terminal Menu")

# Dados do menu
menu_items = ["ARQUIVOS", "CONFIDENCIAL", "VIDEOS", "UTILIDADE"]
items = [
    ["20/01/1996 -> Varginha - MG", "19/05/1986 -> Rio de Janeiro - RJ"],
    ["NAO CONFIE NELES"],
    ["Video 1", "Video 2"],
    ["LETRAS", "ALFABETOS", "TELEFONE"]
]
selected_item = 0
password = "1234"
content_unlocked = False
show_password_prompt = False
input_text = ""

def draw_menu():
    screen.fill((0, 0, 0))  # Fundo preto

    # Inicializa fonte
    pygame.font.init()
    font = pygame.font.Font(None, 36)  # Fonte padrão, tamanho 36

    # Título do terminal
    title_text = font.render("TERMINAL PESSOAL", True, (0, 255, 0))
    screen.blit(title_text, (20, 20))

    # Renderizar os itens do menu lateral
    for i, item in enumerate(menu_items):
        color = (0, 255, 0) if i == selected_item else (0, 128, 0)
        item_text = font.render(item, True, color)
        screen.blit(item_text, (20, 100 + i * 40))

    # Caixa principal
    pygame.draw.rect(screen, (0, 255, 0), (200, 100, 550, 400), 2)

    # Mostrar conteúdo ou solicitar senha
    if content_unlocked:
        category_items = items[selected_item]
        for j, content in enumerate(category_items):
            content_text = font.render(content, True, (144, 238, 144))
            screen.blit(content_text, (220, 120 + j * 40))
    elif show_password_prompt:
        prompt_text = font.render("Insira a senha:", True, (0, 255, 0))
        screen.blit(prompt_text, (220, 120))
        password_text = font.render(input_text, True, (144, 238, 144))
        screen.blit(password_text, (220, 160))

# Loop principal
def main():
    global selected_item, content_unlocked, input_text, show_password_prompt
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Navegação do menu
            if event.type == pygame.KEYDOWN:
                if not show_password_prompt and not content_unlocked:
                    if event.key == pygame.K_UP:
                        selected_item = (selected_item - 1) % len(menu_items)
                    elif event.key == pygame.K_DOWN:
                        selected_item = (selected_item + 1) % len(menu_items)
                    elif event.key == pygame.K_RETURN:
                        if menu_items[selected_item] == "CONFIDENCIAL":  # Verifica se é CONFIDENCIAL
                            show_password_prompt = True
                            input_text = ""
                        else:
                            content_unlocked = True  # Caso contrário, desbloqueia diretamente o conteúdo
                            show_password_prompt = False
                elif show_password_prompt:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        if input_text == password:
                            content_unlocked = True
                            show_password_prompt = False
                        else:
                            # Senha incorreta, limpa o campo de senha e permite nova tentativa
                            input_text = ""
                            show_password_prompt = True  # Permite que o usuário tente novamente
                    elif event.unicode.isprintable():
                        input_text += event.unicode
                elif content_unlocked:
                    if event.key == pygame.K_RETURN:
                        content_unlocked = False  # Retornar ao menu principal

        # Desenhar o menu
        draw_menu()

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
