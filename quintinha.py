import sys
import pygame

pygame.init()

# Configuração de Janela Redimensionável
LARGURA_INI, ALTURA_INI = 1024, 768
TELA = pygame.display.set_mode((LARGURA_INI, ALTURA_INI), pygame.RESIZABLE)
pygame.display.set_caption("Minha Quintinha 2D - Fazenda Acolhedora")

# Paleta de Cores Cozy
COR_GRAMA = (102, 194, 115)
COR_GRAMA_ESCURA = (76, 153, 89)
COR_CAMPO_BORDA = (92, 64, 33)
COR_PAINEL = (44, 33, 24)
COR_TEXTO = (245, 239, 230)
COR_DESTAQUE = (255, 209, 102)

# Fontes
FONTE_UI = pygame.font.SysFont("Verdana", 18, bold=True)
FONTE_MENSAGEM = pygame.font.SysFont("Verdana", 15)
FONTE_PEQUENA = pygame.font.SysFont("Verdana", 11, bold=True)

# Estado do Jogador
fazendeiro_x, fazendeiro_y = 500, 450
largura_f, altura_f = 44, 56
velocidade = 4
sementes = 1
tomates_colhidos = 0

# Canteiros pequenos encostados à esquerda
TAMANHO_CANTEIRO = 48
canteiros = [
    {"rect": pygame.Rect(120, 140, TAMANHO_CANTEIRO, TAMANHO_CANTEIRO), "estado": "vazio", "tempo_inicio": 0},
    {"rect": pygame.Rect(178, 140, TAMANHO_CANTEIRO, TAMANHO_CANTEIRO), "estado": "vazio", "tempo_inicio": 0},
    {"rect": pygame.Rect(236, 140, TAMANHO_CANTEIRO, TAMANHO_CANTEIRO), "estado": "vazio", "tempo_inicio": 0},
]

mensagem = "Usa WASD para andar. Aproxima-te da terra e prime 'E'."
relogio = pygame.time.Clock()

def desenhar_fazendeiro(superficie, x, y):
    pygame.draw.ellipse(superficie, (60, 120, 75), (x + 4, y + altura_f - 6, 36, 10))
    pygame.draw.rect(superficie, (241, 196, 15), (x + 10, y + 24, 24, 22), border_radius=4)
    pygame.draw.rect(superficie, (41, 128, 185), (x + 12, y + 32, 20, 18), border_radius=3)
    pygame.draw.line(superficie, (30, 95, 138), (x + 15, y + 32), (x + 15, y + 42), 2)
    pygame.draw.line(superficie, (30, 95, 138), (x + 29, y + 32), (x + 29, y + 42), 2)
    pygame.draw.rect(superficie, (80, 50, 30), (x + 13, y + 50, 8, 6), border_radius=2)
    pygame.draw.rect(superficie, (80, 50, 30), (x + 23, y + 50, 8, 6), border_radius=2)
    pygame.draw.circle(superficie, (253, 215, 162), (x + 22, y + 16), 11)
    pygame.draw.circle(superficie, (40, 40, 40), (x + 18, y + 15), 1.5)
    pygame.draw.circle(superficie, (40, 40, 40), (x + 26, y + 15), 1.5)
    pygame.draw.ellipse(superficie, (211, 154, 73), (x + 4, y + 4, 36, 8))
    pygame.draw.rect(superficie, (190, 130, 55), (x + 13, y - 3, 18, 9), border_radius=4)
    pygame.draw.rect(superficie, (200, 50, 50), (x + 13, y + 3, 18, 3))

def desenhar_canteiro(superficie, c):
    r = c["rect"]
    estado = c["estado"]
    
    pygame.draw.rect(superficie, COR_CAMPO_BORDA, (r.x - 2, r.y - 2, r.width + 4, r.height + 4), border_radius=8)
    
    cor_terra = (107, 71, 37)
    if estado == "regado":
        cor_terra = (55, 35, 15)
    elif estado == "pronto":
        cor_terra = (115, 78, 42)
    
    pygame.draw.rect(superficie, cor_terra, r, border_radius=6)
    
    centro_x, centro_y = r.x + r.width // 2, r.y + r.height // 2
    
    if estado == "plantado":
        pygame.draw.circle(superficie, (120, 210, 80), (centro_x, centro_y + 2), 5)
        pygame.draw.rect(superficie, (80, 160, 50), (centro_x - 1, centro_y + 2, 2, 6))
    elif estado == "regado":
        pygame.draw.circle(superficie, (90, 190, 70), (centro_x, centro_y), 8)
        pygame.draw.circle(superficie, (150, 230, 255), (centro_x - 2, centro_y - 2), 2)
    elif estado == "pronto":
        pygame.draw.circle(superficie, (231, 76, 60), (centro_x - 6, centro_y + 2), 7)
        pygame.draw.circle(superficie, (231, 76, 60), (centro_x + 6, centro_y + 2), 7)
        pygame.draw.circle(superficie, (192, 57, 43), (centro_x, centro_y - 4), 8)
        pygame.draw.polygon(superficie, (46, 204, 113), [(centro_x, centro_y - 12), (centro_x - 4, centro_y - 8), (centro_x + 4, centro_y - 8)])

while True:
    tempo_atual = pygame.time.get_ticks()
    largura_atual, altura_atual = TELA.get_size()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
            elif evento.key == pygame.K_e:
                rect_fazendeiro = pygame.Rect(fazendeiro_x, fazendeiro_y, largura_f, altura_f)
                alcance = rect_fazendeiro.inflate(25, 25)
                
                for canteiro in canteiros:
                    if alcance.colliderect(canteiro["rect"]):
                        estado = canteiro["estado"]
                        if estado == "vazio" and sementes > 0:
                            canteiro["estado"] = "plantado"
                            sementes -= 1
                            mensagem = "Semente plantada! Prime 'E' para regar."
                        elif estado == "plantado":
                            canteiro["estado"] = "regado"
                            canteiro["tempo_inicio"] = tempo_atual
                            mensagem = "Canteiro regado! Cresce em 10 segundos..."
                        elif estado == "pronto":
                            canteiro["estado"] = "vazio"
                            tomates_colhidos += 1
                            sementes += 1
                            mensagem = "Tomate colhido! Ganhaste +1 semente."

    teclas = pygame.key.get_pressed()
    if (teclas[pygame.K_a] or teclas[pygame.K_LEFT]) and fazendeiro_x > 20:
        fazendeiro_x -= velocidade
    if (teclas[pygame.K_d] or teclas[pygame.K_RIGHT]) and fazendeiro_x < largura_atual - largura_f - 20:
        fazendeiro_x += velocidade
    if (teclas[pygame.K_w] or teclas[pygame.K_UP]) and fazendeiro_y > 80:
        fazendeiro_y -= velocidade
    if (teclas[pygame.K_s] or teclas[pygame.K_DOWN]) and fazendeiro_y < altura_atual - altura_f - 60:
        fazendeiro_y += velocidade

    for canteiro in canteiros:
        if canteiro["estado"] == "regado":
            tempo_passado = (tempo_atual - canteiro["tempo_inicio"]) / 1000
            if tempo_passado >= 10:
                canteiro["estado"] = "pronto"
                mensagem = "O tomateiro está pronto para colheita!"

    TELA.fill(COR_GRAMA)

    for i in range(0, largura_atual, 80):
        pygame.draw.line(TELA, COR_GRAMA_ESCURA, (i, 70), (i, altura_atual - 50), 1)

    # Base da horta reposicionada à esquerda
    pygame.draw.rect(TELA, (110, 75, 40), (112, 128, 192, 64), border_radius=10)

    for canteiro in canteiros:
        desenhar_canteiro(TELA, canteiro)
        
        if canteiro["estado"] == "regado":
            r = canteiro["rect"]
            seg_restantes = max(0, int(10 - (tempo_atual - canteiro["tempo_inicio"]) / 1000))
            bg_tempo = pygame.Rect(r.x + 4, r.y + 30, 40, 16)
            pygame.draw.rect(TELA, (25, 25, 25), bg_tempo, border_radius=4)
            txt_tempo = FONTE_PEQUENA.render(f"{seg_restantes}s", True, COR_DESTAQUE)
            TELA.blit(txt_tempo, (bg_tempo.x + 7, bg_tempo.y + 1))

    desenhar_fazendeiro(TELA, fazendeiro_x, fazendeiro_y)

    # HUD Superior
    pygame.draw.rect(TELA, COR_PAINEL, (0, 0, largura_atual, 65))
    pygame.draw.line(TELA, (75, 55, 38), (0, 65), (largura_atual, 65), 4)
    
    txt_sementes = FONTE_UI.render(f"🌱 Sementes: {sementes}", True, COR_TEXTO)
    txt_colhidos = FONTE_UI.render(f"🍅 Tomates: {tomates_colhidos}", True, COR_TEXTO)
    TELA.blit(txt_sementes, (30, 20))
    TELA.blit(txt_colhidos, (250, 20))

    # Barra Inferior
    pygame.draw.rect(TELA, COR_PAINEL, (0, altura_atual - 45, largura_atual, 45))
    pygame.draw.line(TELA, (75, 55, 38), (0, altura_atual - 45), (largura_atual, altura_atual - 45), 2)
    txt_msg = FONTE_MENSAGEM.render(mensagem, True, COR_DESTAQUE)
    TELA.blit(txt_msg, (20, altura_atual - 32))

    pygame.display.flip()
    relogio.tick(60)