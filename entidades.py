# entidades.py
import pygame


class Fazendeiro:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.largura = 44
    self.altura = 56
    self.velocidade = 4

  def mover(self, teclas, largura_tela, altura_tela):
    if (teclas[pygame.K_a] or teclas[pygame.K_LEFT]) and self.x > 20:
      self.x -= self.velocidade
    if (
        teclas[pygame.K_d] or teclas[pygame.K_RIGHT]
    ) and self.x < largura_tela - self.largura - 20:
      self.x += self.velocidade
    if (teclas[pygame.K_w] or teclas[pygame.K_UP]) and self.y > 30:
      self.y -= self.velocidade
    if (
        teclas[pygame.K_s] or teclas[pygame.K_DOWN]
    ) and self.y < altura_tela - self.altura - 90:
      self.y += self.velocidade

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


class Canteiro:

  def __init__(self, x, y, tamanho=48):
    self.rect = pygame.Rect(x, y, tamanho, tamanho)
    self.estado = "vazio"  # 'vazio', 'plantado', 'regado', 'pronto'
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