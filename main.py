# main.py
import sys
import pygame
from entidades import Canteiro, Casa, Fazendeiro, MaquinaSementes
from inventario import Inventario
from tempo import RelogioJogo

pygame.init()

LARGURA_INI, ALTURA_INI = 1024, 768
TELA = pygame.display.set_mode((LARGURA_INI, ALTURA_INI), pygame.RESIZABLE)
pygame.display.set_caption("Minha Quintinha 2D")

COR_GRAMA = (102, 194, 115)
COR_GRAMA_ESCURA = (76, 153, 89)
FONTE_MENSAGEM = pygame.font.SysFont("Verdana", 15)
FONTE_PEQUENA = pygame.font.SysFont("Verdana", 11, bold=True)
FONTE_SLOT = pygame.font.SysFont("Verdana", 12, bold=True)

fazendeiro = Fazendeiro(500, 450)
inventario = Inventario(8)
relogio_jogo = RelogioJogo()
casa = Casa(LARGURA_INI)
maquina_sementes = MaquinaSementes(330, 134)

canteiros = [Canteiro(120, 140), Canteiro(178, 140), Canteiro(236, 140)]
mensagem = "Pressiona 'E' na máquina para recolher sementes ou colocar tomates."
relogio = pygame.time.Clock()

while True:
  dt = relogio.tick(60)
  relogio_jogo.atualizar(dt)
  tempo_atual = pygame.time.get_ticks()
  largura_atual, altura_atual = TELA.get_size()

  casa.atualizar_posicao(largura_atual)

  for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

    elif evento.type == pygame.KEYDOWN:
      if evento.key == pygame.K_f:
        pygame.display.toggle_fullscreen()
      elif evento.key == pygame.K_e:
        alcance = fazendeiro.obter_rect().inflate(25, 25)

        if alcance.colliderect(casa.porta_rect):
          horas_atuais = relogio_jogo.minutos_totais // 60
          if horas_atuais >= 21 or horas_atuais < 6:
            relogio_jogo.dormir()
            mensagem = f"Bom dia! Acordaste no {relogio_jogo.obter_hora_str()}"
          else:
            mensagem = "Ainda é cedo para dormir! Podes ir para a cama a partir das 21:00."
        
        elif alcance.colliderect(maquina_sementes.rect):
          if maquina_sementes.sementes_prontas > 0:
            if inventario.adicionar("semente", maquina_sementes.sementes_prontas):
              mensagem = f"Recolhiste {maquina_sementes.sementes_prontas} sementes!"
              maquina_sementes.sementes_prontas = 0
            else:
              mensagem = "Inventário cheio! Não consegues recolher as sementes."
          elif inventario.contar("tomate") > 0:
            inventario.remover("tomate", 1)
            if not maquina_sementes.processando:
              maquina_sementes.tempo_inicio = tempo_atual
              maquina_sementes.processando = True
            maquina_sementes.fila_tomates += 1
            mensagem = "Tomate inserido na máquina! Produz 3 sementes em 15s."
          else:
            mensagem = "Não tens tomates ou sementes prontas na máquina!"
        else:
          for canteiro in canteiros:
            if alcance.colliderect(canteiro.rect):
              if canteiro.estado == "pronto":
                canteiro.estado = "vazio"
                inventario.adicionar("tomate", 1)
                inventario.adicionar("semente", 1)
                mensagem = "Tomate colhido! +1 semente."
                break
              elif canteiro.estado == "vazio" and inventario.contar("semente") > 0:
                inventario.remover("semente", 1)
                canteiro.estado = "plantado"
                mensagem = "Semente plantada!"
                break
              elif canteiro.estado == "plantado":
                canteiro.estado = "regado"
                canteiro.tempo_inicio = tempo_atual
                mensagem = "Canteiro regado!"
                break

  maquina_sementes.atualizar(tempo_atual)

  teclas = pygame.key.get_pressed()

  fazendeiro.x_antigo = fazendeiro.x
  fazendeiro.y_antigo = fazendeiro.y

  if (teclas[pygame.K_a] or teclas[pygame.K_LEFT]) and fazendeiro.x > 20:
    fazendeiro.x -= fazendeiro.velocidade
    if fazendeiro.obter_rect().colliderect(casa.rect):
      fazendeiro.x = fazendeiro.x_antigo
  if (teclas[pygame.K_d] or teclas[pygame.K_RIGHT]) and fazendeiro.x < largura_atual - fazendeiro.largura - 20:
    fazendeiro.x += fazendeiro.velocidade
    if fazendeiro.obter_rect().colliderect(casa.rect):
      fazendeiro.x = fazendeiro.x_antigo

  if (teclas[pygame.K_w] or teclas[pygame.K_UP]) and fazendeiro.y > 30:
    fazendeiro.y -= fazendeiro.velocidade
    if fazendeiro.obter_rect().colliderect(casa.rect):
      fazendeiro.y = fazendeiro.y_antigo
  if (teclas[pygame.K_s] or teclas[pygame.K_DOWN]) and fazendeiro.y < altura_atual - fazendeiro.altura - 90:
    fazendeiro.y += fazendeiro.velocidade
    if fazendeiro.obter_rect().colliderect(casa.rect):
      fazendeiro.y = fazendeiro.y_antigo

  for canteiro in canteiros:
    if canteiro.atualizar(tempo_atual):
      mensagem = "O tomateiro está pronto para colheita!"

  TELA.fill(COR_GRAMA)
  for i in range(0, largura_atual, 80):
    pygame.draw.line(TELA, COR_GRAMA_ESCURA, (i, 0), (i, altura_atual - 70), 1)

  pygame.draw.rect(TELA, (110, 75, 40), (112, 128, 192, 64), border_radius=10)

  for canteiro in canteiros:
    canteiro.desenhar(TELA, FONTE_PEQUENA, tempo_atual)

  maquina_sementes.desenhar(TELA, FONTE_PEQUENA, tempo_atual)
  casa.desenhar(TELA)
  fazendeiro.desenhar(TELA)

  nivel_escuro = relogio_jogo.obter_nivel_escuridao()
  if nivel_escuro > 0:
    overlay = pygame.Surface((largura_atual, altura_atual), pygame.SRCALPHA)
    overlay.fill((10, 10, 40, nivel_escuro))
    TELA.blit(overlay, (0, 0))

  inventario.desenhar(TELA, largura_atual, altura_atual, FONTE_SLOT)

  pygame.draw.rect(TELA, (30, 22, 16, 200), (20, 20, 160, 35), border_radius=6)
  txt_relogio = FONTE_MENSAGEM.render(
      relogio_jogo.obter_hora_str(), True, (255, 209, 102)
  )
  TELA.blit(txt_relogio, (30, 27))

  pygame.draw.rect(
      TELA, (30, 22, 16, 200), (190, 20, len(mensagem) * 8 + 20, 35), border_radius=6
  )
  txt_msg = FONTE_MENSAGEM.render(mensagem, True, (255, 209, 102))
  TELA.blit(txt_msg, (200, 27))

  pygame.display.flip()