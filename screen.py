import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF| pygame.FULLSCREEN)
pygame.display.set_caption("Terminal Menu")

# Shader CRT
vertex_shader = """
#version 330 core
layout(location = 0) in vec2 position;
layout(location = 1) in vec2 texCoords;
out vec2 fragTexCoords;
void main() {
    fragTexCoords = texCoords;
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment_shader = """
#version 330 core
in vec2 fragTexCoords;
out vec4 FragColor;
uniform sampler2D screenTexture;
void main() {
    vec3 color = texture(screenTexture, fragTexCoords).rgb;

    // Apply CRT scanline effect
    float scanline = sin(fragTexCoords.y * 800.0) * 0.04;
    color -= scanline;

    FragColor = vec4(color, 1.0);
}
"""

shader = compileProgram(
    compileShader(vertex_shader, GL_VERTEX_SHADER),
    compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

# Quad para renderizar a textura
def create_quad():
    vertices = [
        -1.0,  1.0, 0.0, 1.0,
        -1.0, -1.0, 0.0, 0.0,
         1.0, -1.0, 1.0, 0.0,
         1.0,  1.0, 1.0, 1.0,
    ]
    vertices = (GLfloat * len(vertices))(*vertices)

    indices = [0, 1, 2, 2, 3, 0]
    indices = (GLuint * len(indices))(*indices)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(GLfloat), ctypes.c_void_p(2 * sizeof(GLfloat)))
    glEnableVertexAttribArray(1)

    return vao

quad_vao = create_quad()

# Configurações de renderização
texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, WIDTH, HEIGHT, 0, GL_RGB, GL_UNSIGNED_BYTE, None)

def render_to_texture():
    surface = pygame.display.get_surface()
    flipped_surface = pygame.transform.flip(surface, False, True)  # Inverter verticalmente
    buffer = pygame.image.tostring(flipped_surface, "RGB")
    glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, WIDTH, HEIGHT, GL_RGB, GL_UNSIGNED_BYTE, buffer)



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
    pygame.display.get_surface().fill((0, 0, 0))

    # Inicializa fonte
    pygame.font.init()
    font = pygame.font.Font(None, 36)  # Fonte padrão, tamanho 36

    # Título do terminal
    title_text = font.render("TERMINAL PESSOAL", True, (0, 255, 0))
    pygame.display.get_surface().blit(title_text, (20, 20))

    # Renderizar os itens do menu lateral
    for i, item in enumerate(menu_items):
        color = (0, 255, 0) if i == selected_item else (0, 128, 0)
        item_text = font.render(item, True, color)
        pygame.display.get_surface().blit(item_text, (20, 100 + i * 40))

    # Caixa principal
    pygame.draw.rect(pygame.display.get_surface(), (0, 255, 0), (200, 100, 550, 400), 2)

    # Mostrar conteúdo ou solicitar senha
    if content_unlocked:
        category_items = items[selected_item]
        for j, content in enumerate(category_items):
            content_text = font.render(content, True, (144, 238, 144))
            pygame.display.get_surface().blit(content_text, (220, 120 + j * 40))
    elif show_password_prompt:
        prompt_text = font.render("Insira a senha:", True, (0, 255, 0))
        pygame.display.get_surface().blit(prompt_text, (220, 120))
        password_text = font.render(input_text, True, (144, 238, 144))
        pygame.display.get_surface().blit(password_text, (220, 160))

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
        render_to_texture()

        # Renderizar com OpenGL
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(shader)
        glBindVertexArray(quad_vao)
        glBindTexture(GL_TEXTURE_2D, texture)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
