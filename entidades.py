# entidades.py
import pygame
from inventario import Inventario

class Fazendeiro:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 44
        self.altura = 56
        self.velocidade = 4

    def obter_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def desenhar(self, superficie):
        pygame.draw.ellipse(superficie, (60, 120, 75), (self.x + 4, self.y + self.altura - 6, 36, 10))
        pygame.draw.rect(superficie, (241, 196, 15), (self.x + 10, self.y + 24, 24, 22), border_radius=4)
        pygame.draw.rect(superficie, (41, 128, 185), (self.x + 12, self.y + 32, 20, 18), border_radius=3)
        pygame.draw.line(superficie, (30, 95, 138), (self.x + 15, self.y + 32), (self.x + 15, self.y + 42), 2)
        pygame.draw.line(superficie, (30, 95, 138), (self.x + 29, self.y + 32), (self.x + 29, self.y + 42), 2)
        pygame.draw.rect(superficie, (80, 50, 30), (self.x + 13, self.y + 50, 8, 6), border_radius=2)
        pygame.draw.rect(superficie, (80, 50, 30), (self.x + 23, self.y + 50, 8, 6), border_radius=2)
        pygame.draw.circle(superficie, (253, 215, 162), (self.x + 22, self.y + 16), 11)
        pygame.draw.circle(superficie, (40, 40, 40), (self.x + 18, self.y + 15), 1.5)
        pygame.draw.circle(superficie, (40, 40, 40), (self.x + 26, self.y + 15), 1.5)
        pygame.draw.ellipse(superficie, (211, 154, 73), (self.x + 4, self.y + 4, 36, 8))
        pygame.draw.rect(superficie, (190, 130, 55), (self.x + 13, self.y - 3, 18, 9), border_radius=4)
        pygame.draw.rect(superficie, (200, 50, 50), (self.x + 13, self.y + 3, 18, 3))

class Casa:
    def __init__(self, largura_tela):
        self.largura = 180
        self.altura = 130
        self.x = largura_tela - self.largura - 30
        self.y = 70
        self.inventario = Inventario(30)
        self.inventario.adicionar_item("tomate", 5)
        self.atualizar_rects()

    def atualizar_posicao(self, largura_tela):
        self.x = largura_tela - self.largura - 30
        self.atualizar_rects()

    def atualizar_rects(self):
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        self.colisao_rect = pygame.Rect(self.x - 10, self.y + self.altura - 40, self.largura + 20, 50)
        self.porta_rect = pygame.Rect(self.x + self.largura // 2 - 20, self.y + self.altura - 50, 40, 50)

    def desenhar(self, superficie):
        r = self.rect
        sombra_surf = pygame.Surface((self.largura + 10, self.altura + 10), pygame.SRCALPHA)
        pygame.draw.rect(sombra_surf, (0, 0, 0, 40), (5, 5, self.largura, self.altura), border_radius=10)
        superficie.blit(sombra_surf, (r.x - 2, r.y - 2))
        pygame.draw.rect(superficie, (205, 162, 122), r, border_radius=10)
        pygame.draw.rect(superficie, (139, 94, 60), r, 4, border_radius=10)
        pygame.draw.rect(superficie, (110, 110, 110), (r.x, r.y + r.height - 15, r.width, 15), border_bottom_left_radius=10, border_bottom_right_radius=10)
        pygame.draw.line(superficie, (80, 80, 80), (r.x, r.y + r.height - 15), (r.x + r.width, r.y + r.height - 15), 2)
        pontos_telhado = [(r.x - 15, r.y), (r.x + r.width // 2, r.y - 65), (r.x + r.width + 15, r.y)]
        pygame.draw.polygon(superficie, (168, 50, 50), pontos_telhado)
        pygame.draw.polygon(superficie, (115, 30, 30), pontos_telhado, 4)
        pygame.draw.rect(superficie, (140, 70, 50), (r.x + 25, r.y - 50, 22, 35))
        pygame.draw.rect(superficie, (100, 45, 30), (r.x + 22, r.y - 55, 28, 8))
        def desenhar_janela(jx, jy):
            pygame.draw.rect(superficie, (80, 50, 30), (jx - 3, jy - 3, 36, 36), border_radius=4)
            pygame.draw.rect(superficie, (255, 240, 180), (jx, jy, 30, 30), border_radius=2)
            pygame.draw.line(superficie, (80, 50, 30), (jx + 15, jy), (jx + 15, jy + 30), 2)
            pygame.draw.line(superficie, (80, 50, 30), (jx, jy + 15), (jx + 30, jy + 15), 2)
        desenhar_janela(r.x + 20, r.y + 25)
        desenhar_janela(r.x + r.width - 50, r.y + 25)
        pygame.draw.rect(superficie, (92, 53, 29), self.porta_rect, border_top_left_radius=6, border_top_right_radius=6)
        pygame.draw.rect(superficie, (60, 32, 16), self.porta_rect, 3, border_top_left_radius=6, border_top_right_radius=6)
        pygame.draw.circle(superficie, (230, 200, 100), (self.porta_rect.x + 30, self.porta_rect.y + 25), 4)

class Poco:
    def __init__(self, casa_obj):
        self.largura = 56
        self.altura = 64
        self.atualizar_posicao(casa_obj)

    def atualizar_posicao(self, casa_obj):
        # Coloca o poço logo à esquerda da casa
        self.x = casa_obj.x - self.largura - 25
        self.y = casa_obj.y + casa_obj.altura - self.altura
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        self.colisao_rect = pygame.Rect(self.x - 5, self.y + 20, self.largura + 10, self.altura - 20)

    def desenhar(self, superficie):
        r = self.rect
        # Sombra
        sombra = pygame.Surface((self.largura + 6, 16), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 45), (0, 0, self.largura + 6, 16))
        superficie.blit(sombra, (r.x - 3, r.y + r.height - 8))

        # Base de pedra circular/octogonal estilizada
        pygame.draw.rect(superficie, (130, 140, 150), (r.x + 4, r.y + 24, r.width - 8, 36), border_radius=6)
        pygame.draw.rect(superficie, (90, 100, 110), (r.x + 4, r.y + 24, r.width - 8, 36), 2, border_radius=6)
        # Linhas de tijolos de pedra
        pygame.draw.line(superficie, (70, 80, 90), (r.x + 12, r.y + 36), (r.x + r.width - 12, r.y + 36), 1)
        pygame.draw.line(superficie, (70, 80, 90), (r.x + 8, r.y + 48), (r.x + r.width - 8, r.y + 48), 1)

        # Água dentro do poço
        pygame.draw.ellipse(superficie, (52, 152, 219), (r.x + 10, r.y + 26, r.width - 20, 12))

        # Pilares de madeira do telhado
        pygame.draw.rect(superficie, (100, 60, 30), (r.x + 6, r.y + 6, 6, 26))
        pygame.draw.rect(superficie, (100, 60, 30), (r.x + r.width - 12, r.y + 6, 6, 26))

        # Telhado do poço
        p_telhado = [(r.x - 4, r.y + 8), (r.x + r.width // 2, r.y - 12), (r.x + r.width + 4, r.y + 8)]
        pygame.draw.polygon(superficie, (168, 50, 50), p_telhado)
        pygame.draw.polygon(superficie, (115, 30, 30), p_telhado, 2)

        # Pequeno balde pendurado
        pygame.draw.rect(superficie, (180, 180, 180), (r.x + r.width // 2 - 5, r.y + 22, 10, 12), border_radius=2)
        pygame.draw.line(superficie, (50, 50, 50), (r.x + r.width // 2, r.y + 10), (r.x + r.width // 2, r.y + 22), 1)

class MaquinaSementes:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 60, 70)
        self.fila_tomates = 0
        self.sementes_prontas = 0
        self.tempo_inicio = 0
        self.processando = False

    def atualizar(self, tempo_atual):
        if self.processando and self.fila_tomates > 0:
            if (tempo_atual - self.tempo_inicio) / 1000 >= 15:
                self.fila_tomates -= 1
                self.sementes_prontas += 3
                if self.fila_tomates > 0:
                    self.tempo_inicio = tempo_atual
                else:
                    self.processando = False

    def desenhar(self, superficie, fonte_pequena, tempo_atual):
        r = self.rect
        pygame.draw.rect(superficie, (120, 130, 140), r, border_radius=8)
        pygame.draw.rect(superficie, (80, 90, 100), r, 3, border_radius=8)
        pygame.draw.polygon(superficie, (160, 170, 180), [(r.x + 10, r.y), (r.x + r.width - 10, r.y), (r.x + r.width - 20, r.y - 12), (r.x + 20, r.y - 12)])
        visor = pygame.Rect(r.x + 12, r.y + 12, r.width - 24, 25)
        pygame.draw.rect(superficie, (40, 50, 60), visor, border_radius=4)
        if self.sementes_prontas > 0:
            txt = fonte_pequena.render(f"Prontas:{self.sementes_prontas}", True, (46, 204, 113))
            superficie.blit(txt, (visor.x + 2, visor.y + 5))
        elif self.fila_tomates > 0:
            txt = fonte_pequena.render(f"Fila: {self.fila_tomates}", True, (231, 76, 60))
            superficie.blit(txt, (visor.x + 4, visor.y + 5))
        cor_luz = (46, 204, 113) if self.processando else (150, 50, 50)
        pygame.draw.circle(superficie, cor_luz, (r.x + r.width // 2, r.y + 55), 5)
        if self.processando:
            seg = max(0, int(15 - (tempo_atual - self.tempo_inicio) / 1000))
            txt_t = fonte_pequena.render(f"{seg}s", True, (255, 209, 102))
            superficie.blit(txt_t, (r.x + 15, r.y + 45))

class Canteiro:
    def __init__(self, x, y, tamanho=48):
        self.rect = pygame.Rect(x, y, tamanho, tamanho)
        self.estado = "vazio"
        self.tempo_inicio = 0

    def atualizar(self, tempo_atual):
        if self.estado == "regado":
            if (tempo_atual - self.tempo_inicio) / 1000 >= 10:
                self.estado = "pronto"
                return True
        return False

    def desenhar(self, superficie, fonte_pequena, tempo_atual):
        r = self.rect
        pygame.draw.rect(superficie, (92, 64, 33), (r.x - 2, r.y - 2, r.width + 4, r.height + 4), border_radius=8)
        cor_terra = (107, 71, 37)
        if self.estado == "regado": cor_terra = (55, 35, 15)
        elif self.estado == "pronto": cor_terra = (115, 78, 42)
        pygame.draw.rect(superficie, cor_terra, r, border_radius=6)
        cx, cy = r.x + r.width // 2, r.y + r.height // 2
        if self.estado == "plantado":
            pygame.draw.circle(superficie, (120, 210, 80), (cx, cy + 2), 5)
            pygame.draw.rect(superficie, (80, 160, 50), (cx - 1, cy + 2, 2, 6))
        elif self.estado == "regado":
            pygame.draw.circle(superficie, (90, 190, 70), (cx, cy), 8)
            pygame.draw.circle(superficie, (150, 230, 255), (cx - 2, cy - 2), 2)
            seg = max(0, int(10 - (tempo_atual - self.tempo_inicio) / 1000))
            bg = pygame.Rect(r.x + 4, r.y + 30, 40, 16)
            pygame.draw.rect(superficie, (25, 25, 25), bg, border_radius=4)
            txt = fonte_pequena.render(f"{seg}s", True, (255, 209, 102))
            superficie.blit(txt, (bg.x + 7, bg.y + 1))
        elif self.estado == "pronto":
            pygame.draw.circle(superficie, (231, 76, 60), (cx - 6, cy + 2), 7)
            pygame.draw.circle(superficie, (231, 76, 60), (cx + 6, cy + 2), 7)
            pygame.draw.circle(superficie, (192, 57, 43), (cx, cy - 4), 8)
            pygame.draw.polygon(superficie, (46, 204, 113), [(cx, cy - 12), (cx - 4, cy - 8), (cx + 4, cy - 8)])