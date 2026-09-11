# entidades.py
import pygame


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
    pygame.draw.ellipse(
        superficie, (60, 120, 75), (self.x + 4, self.y + self.altura - 6, 36, 10)
    )
    pygame.draw.rect(
        superficie,
        (241, 196, 15),
        (self.x + 10, self.y + 24, 24, 22),
        border_radius=4,
    )
    pygame.draw.rect(
        superficie,
        (41, 128, 185),
        (self.x + 12, self.y + 32, 20, 18),
        border_radius=3,
    )
    pygame.draw.line(
        superficie,
        (30, 95, 138),
        (self.x + 15, self.y + 32),
        (self.x + 15, self.y + 42),
        2,
    )
    pygame.draw.line(
        superficie,
        (30, 95, 138),
        (self.x + 29, self.y + 32),
        (self.x + 29, self.y + 42),
        2,
    )
    pygame.draw.rect(
        superficie, (80, 50, 30), (self.x + 13, self.y + 50, 8, 6), border_radius=2
    )
    pygame.draw.rect(
        superficie, (80, 50, 30), (self.x + 23, self.y + 50, 8, 6), border_radius=2
    )
    pygame.draw.circle(superficie, (253, 215, 162), (self.x + 22, self.y + 16), 11)
    pygame.draw.circle(superficie, (40, 40, 40), (self.x + 18, self.y + 15), 1.5)
    pygame.draw.circle(superficie, (40, 40, 40), (self.x + 26, self.y + 15), 1.5)
    pygame.draw.ellipse(
        superficie, (211, 154, 73), (self.x + 4, self.y + 4, 36, 8)
    )
    pygame.draw.rect(
        superficie,
        (190, 130, 55),
        (self.x + 13, self.y - 3, 18, 9),
        border_radius=4,
    )
    pygame.draw.rect(
        superficie, (200, 50, 50), (self.x + 13, self.y + 3, 18, 3)
    )


class Casa:

  def __init__(self, largura_tela):
    # Coordenadas calculadas para colar à extremidade direita com margem elegante
    self.largura = 180
    self.altura = 130
    self.x = largura_tela - self.largura - 30
    self.y = 70
    self.atualizar_rects()

  def atualizar_posicao(self, largura_tela):
    self.x = largura_tela - self.largura - 30
    self.atualizar_rects()

  def atualizar_rects(self):
    self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
    # Porta centrada na parte inferior da casa
    self.porta_rect = pygame.Rect(
        self.x + self.largura // 2 - 20, self.y + self.altura - 50, 40, 50
    )

  def desenhar(self, superficie):
    r = self.rect

    # Sombra suave da casa
    sombra_surf = pygame.Surface(
        (self.largura + 10, self.altura + 10), pygame.SRCALPHA
    )
    pygame.draw.rect(
        sombra_surf, (0, 0, 0, 40), (5, 5, self.largura, self.altura), border_radius=10
    )
    superficie.blit(sombra_surf, (r.x - 2, r.y - 2))

    # Paredes principais (Tons de madeira aconchegantes)
    pygame.draw.rect(superficie, (205, 162, 122), r, border_radius=10)
    pygame.draw.rect(superficie, (139, 94, 60), r, 4, border_radius=10)

    # Detalhe de alpendre/base em pedra
    pygame.draw.rect(
        superficie,
        (110, 110, 110),
        (r.x, r.y + r.height - 15, r.width, 15),
        border_bottom_left_radius=10,
        border_bottom_right_radius=10,
    )
    pygame.draw.line(
        superficie,
        (80, 80, 80),
        (r.x, r.y + r.height - 15),
        (r.x + r.width, r.y + r.height - 15),
        2,
    )

    # Telhado detalhado (Duas águas com beiral sobressalente)
    pontos_telhado = [
        (r.x - 15, r.y),
        (r.x + r.width // 2, r.y - 65),
        (r.x + r.width + 15, r.y),
    ]
    pygame.draw.polygon(superficie, (168, 50, 50), pontos_telhado)
    pygame.draw.polygon(superficie, (115, 30, 30), pontos_telhado, 4)

    # Chaminé elegante
    pygame.draw.rect(superficie, (140, 70, 50), (r.x + 25, r.y - 50, 22, 35))
    pygame.draw.rect(superficie, (100, 45, 30), (r.x + 22, r.y - 55, 28, 8))

    # Janelas duplas acolhedoras com cruz e moldura
    def desenhar_janela(jx, jy):
      pygame.draw.rect(
          superficie, (80, 50, 30), (jx - 3, jy - 3, 36, 36), border_radius=4
      )
      pygame.draw.rect(
          superficie, (255, 240, 180), (jx, jy, 30, 30), border_radius=2
      )
      pygame.draw.line(
          superficie, (80, 50, 30), (jx + 15, jy), (jx + 15, jy + 30), 2
      )
      pygame.draw.line(
          superficie, (80, 50, 30), (jx, jy + 15), (jx + 30, jy + 15), 2
      )

    desenhar_janela(r.x + 20, r.y + 25)
    desenhar_janela(r.x + r.width - 50, r.y + 25)

    # Porta de madeira rica com puxador
    pygame.draw.rect(
        superficie, (92, 53, 29), self.porta_rect, border_top_left_radius=6, border_top_right_radius=6
    )
    pygame.draw.rect(
        superficie, (60, 32, 16), self.porta_rect, 3, border_top_left_radius=6, border_top_right_radius=6
    )
    pygame.draw.circle(
        superficie, (230, 200, 100), (self.porta_rect.x + 30, self.porta_rect.y + 25), 4
    )


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
    pygame.draw.rect(
        superficie,
        (92, 64, 33),
        (r.x - 2, r.y - 2, r.width + 4, r.height + 4),
        border_radius=8,
    )

    cor_terra = (107, 71, 37)
    if self.estado == "regado":
      cor_terra = (55, 35, 15)
    elif self.estado == "pronto":
      cor_terra = (115, 78, 42)

    pygame.draw.rect(superficie, cor_terra, r, border_radius=6)
    cx, cy = r.x + r.width // 2, r.y + r.height // 2

    if self.estado == "plantado":
      pygame.draw.circle(superficie, (120, 210, 80), (cx, cy + 2), 5)
      pygame.draw.rect(superficie, (80, 160, 50), (cx - 1, cy + 2, 2, 6))
    elif self.estado == "regado":
      pygame.draw.circle(superficie, (90, 190, 70), (cx, cy), 8)
      pygame.draw.circle(superficie, (150, 230, 255), (cx - 2, cy - 2), 2)

      seg_restantes = max(0, int(10 - (tempo_atual - self.tempo_inicio) / 1000))
      bg_tempo = pygame.Rect(r.x + 4, r.y + 30, 40, 16)
      pygame.draw.rect(superficie, (25, 25, 25), bg_tempo, border_radius=4)
      txt_tempo = fonte_pequena.render(
          f"{seg_restantes}s", True, (255, 209, 102)
      )
      superficie.blit(txt_tempo, (bg_tempo.x + 7, bg_tempo.y + 1))

    elif self.estado == "pronto":
      pygame.draw.circle(superficie, (231, 76, 60), (cx - 6, cy + 2), 7)
      pygame.draw.circle(superficie, (231, 76, 60), (cx + 6, cy + 2), 7)
      pygame.draw.circle(superficie, (192, 57, 43), (cx, cy - 4), 8)
      pygame.draw.polygon(
          superficie,
          (46, 204, 113),
          [(cx, cy - 12), (cx - 4, cy - 8), (cx + 4, cy - 8)],
      )