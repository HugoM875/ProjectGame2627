# main.py
import sys
import pygame
from entidades import Canteiro, Fazendeiro
from inventario import Inventario

pygame.init()

LARGURA_INI, ALTURA_INI = 1024, 768
TELA = pygame.display.set_mode((LARGURA_INI, ALTURA_INI), pygame.RESIZABLE)
pygame.display.set_caption("Minha Quintinha 2D")

# Cores e Fontes
COR_GRAMA = (102, 194, 115)
COR_GRAMA_ESCURA = (76, 153, 89)
FONTE_MENSAGEM = pygame.font.SysFont("Verdana", 15)
FONTE_PEQUENA = pygame.font.SysFont("Verdana", 11, bold=True)
FONTE_SLOT = pygame.font.SysFont("Verdana", 12, bold=True)

# Instâncias principais
fazendeiro = Fazendeiro(500, 450)
inventario = Inventario(8)

# Criar os canteiros encostados à esquerda
canteiros = [Canteiro(120, 140), Canteiro(178, 140), Canteiro(236, 140)]

mensagem = "Usa WASD para andar. Aproxima-te da terra e prime 'E'."
relogio = pygame.time.Clock()

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
        alcance = fazendeiro.obter_rect().inflate(25, 25)
        for canteiro in canteiros:
          if alcance.colliderect(canteiro.rect):
            if canteiro.estado == "pronto":
              canteiro.estado = "vazio"
              inventario.adicionar("tomate", 1)
              inventario.adicionar("semente", 1)  # Recicla a semente
              mensagem = "Tomate colhido! Adicionado ao inventário com +1 semente."
              break  # Para a execução para não plantar logo a seguir
            
            elif canteiro.estado == "vazio" and inventario.contar("semente") > 0:
              inventario.remover("semente", 1)
              canteiro.estado = "plantado"
              mensagem = "Semente plantada! Prime 'E' para regar."
              break
            
            elif canteiro.estado == "plantado":
              canteiro.estado = "regado"
              canteiro.tempo_inicio = tempo_atual
              mensagem = "Canteiro regado! Cresce em 10 segundos..."
              break

  # Movimentação e Atualizações
  teclas = pygame.key.get_pressed()
  fazendeiro.mover(teclas, largura_atual, altura_atual)

  for canteiro in canteiros:
    if canteiro.atualizar(tempo_atual):
      mensagem = "O tomateiro está pronto para colheita!"

  # Renderização
  TELA.fill(COR_GRAMA)
  for i in range(0, largura_atual, 80):
    pygame.draw.line(TELA, COR_GRAMA_ESCURA, (i, 0), (i, altura_atual - 70), 1)

  # Base da horta
  pygame.draw.rect(TELA, (110, 75, 40), (112, 128, 192, 64), border_radius=10)

  for canteiro in canteiros:
    canteiro.desenhar(TELA, FONTE_PEQUENA, tempo_atual)

  fazendeiro.desenhar(TELA)
  inventario.desenhar(TELA, largura_atual, altura_atual, FONTE_SLOT)

  # Mensagem no topo
  pygame.draw.rect(
      TELA, (30, 22, 16, 200), (20, 20, len(mensagem) * 8 + 20, 30), border_radius=6
  )
  txt_msg = FONTE_MENSAGEM.render(mensagem, True, (255, 209, 102))
  TELA.blit(txt_msg, (30, 25))

  pygame.display.flip()
  relogio.tick(60)