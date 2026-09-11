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

fazendeiro = Fazendeiro(500, 450)
inventario_jogador = Inventario(8, num_cols=8)
inventario_jogador.adicionar_item("semente", 1)

relogio_jogo = RelogioJogo()
casa = Casa(LARGURA_INI)
maquina_sementes = MaquinaSementes(330, 134)
canteiros = [Canteiro(120, 140), Canteiro(178, 140), Canteiro(236, 140)]

bau_aberto = False
item_arrastado = None

mensagem = "Usa 'E' nos canteiros/máquina e 'C' perto da casa para abrir o baú."
relogio = pygame.time.Clock()

while True:
    dt = relogio.tick(60)
    relogio_jogo.atualizar(dt)
    tempo_atual = pygame.time.get_ticks()
    largura_atual, altura_atual = TELA.get_size()

    casa.atualizar_posicao(largura_atual)

    # Posicionamento dos inventários
    slot_tam, esp = 48, 8
    
    largura_total_jog = (slot_tam * 8) + (esp * 7)
    inicio_x_jog = (largura_atual - largura_total_jog) // 2
    inicio_y_jog = altura_atual - 70
    rect_inv_jog = pygame.Rect(inicio_x_jog - 10, inicio_y_jog - 10, largura_total_jog + 20, 70)

    num_cols_casa = 6
    num_rows_casa = 5 
    largura_total_casa = (slot_tam * num_cols_casa) + (esp * (num_cols_casa - 1))
    altura_total_casa = (slot_tam * num_rows_casa) + (esp * (num_rows_casa - 1))
    inicio_x_casa = (largura_atual - largura_total_casa) // 2
    inicio_y_casa = altura_atual // 2 - altura_total_casa // 2
    rect_inv_casa = pygame.Rect(inicio_x_casa - 10, inicio_y_casa - 10, largura_total_casa + 20, altura_total_casa + 20)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mx, my = evento.pos
            
            if bau_aberto and rect_inv_casa.collidepoint(mx, my):
                s_casa = casa.inventario.obter_slot_por_pos(mx, my, inicio_x_casa, inicio_y_casa)
                if s_casa is not None:
                    if item_arrastado is None:
                        if casa.inventario.slots[s_casa]:
                            item = casa.inventario.slots[s_casa]
                            item_arrastado = {'item': item, 'origem': 'casa', 'slot_idx': s_casa}
                            casa.inventario.slots[s_casa] = None
                    else:
                        if item_arrastado['origem'] == 'casa':
                            origem_idx = item_arrastado['slot_idx']
                            item_destino = casa.inventario.slots[s_casa]
                            casa.inventario.slots[origem_idx] = item_destino
                            casa.inventario.slots[s_casa] = item_arrastado['item']
                        else:
                            casa.inventario.slots[s_casa] = item_arrastado['item']
                        item_arrastado = None

            elif rect_inv_jog.collidepoint(mx, my):
                s_jog = inventario_jogador.obter_slot_por_pos(mx, my, inicio_x_jog, inicio_y_jog)
                if s_jog is not None:
                    if item_arrastado is None:
                        if inventario_jogador.slots[s_jog]:
                            item = inventario_jogador.slots[s_jog]
                            item_arrastado = {'item': item, 'origem': 'jogador', 'slot_idx': s_jog}
                            inventario_jogador.slots[s_jog] = None
                    else:
                        if item_arrastado['origem'] == 'jogador':
                            origem_idx = item_arrastado['slot_idx']
                            item_destino = inventario_jogador.slots[s_jog]
                            inventario_jogador.slots[origem_idx] = item_destino
                            inventario_jogador.slots[s_jog] = item_arrastado['item']
                        else:
                            inventario_jogador.slots[s_jog] = item_arrastado['item']
                        item_arrastado = None
            elif item_arrastado:
                if item_arrastado['origem'] == 'jogador':
                    inventario_jogador.slots[item_arrastado['slot_idx']] = item_arrastado['item']
                else:
                    casa.inventario.slots[item_arrastado['slot_idx']] = item_arrastado['item']
                item_arrastado = None

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
            elif evento.key == pygame.K_c:
                alcance = fazendeiro.obter_rect().inflate(35, 35)
                if alcance.colliderect(casa.colisao_rect):
                    bau_aberto = not bau_aberto
                    if not bau_aberto: item_arrastado = None
                    mensagem = "Inventário da casa aberto!" if bau_aberto else "Inventário fechado."
                else:
                    mensagem = "Estás muito longe da casa!"
            elif evento.key == pygame.K_e:
                alcance = fazendeiro.obter_rect().inflate(25, 25)
                if alcance.colliderect(casa.porta_rect):
                    if relogio_jogo.minutos_totais // 60 >= 21 or relogio_jogo.minutos_totais // 60 < 6:
                        relogio_jogo.dormir()
                        mensagem = f"Bom dia! {relogio_jogo.obter_hora_str()}"
                    else:
                        mensagem = "Ainda é cedo para dormir!"
                elif alcance.colliderect(maquina_sementes.rect):
                    if maquina_sementes.sementes_prontas > 0:
                        if inventario_jogador.adicionar_item("semente", maquina_sementes.sementes_prontas):
                            mensagem = f"Recolhiste {maquina_sementes.sementes_prontas} sementes!"
                            maquina_sementes.sementes_prontas = 0
                        else:
                            mensagem = "Inventário cheio!"
                    elif inventario_jogador.remover_por_id(next((item.id for item in inventario_jogador.slots if item and item.tipo == "tomate"), None), 1):
                        if not maquina_sementes.processando:
                            maquina_sementes.tempo_inicio = tempo_atual
                            maquina_sementes.processando = True
                        maquina_sementes.fila_tomates += 1
                        mensagem = "Tomate inserido na máquina!"
                    else:
                        mensagem = "Não tens tomates ou sementes prontas!"
                else:
                    for canteiro in canteiros:
                        if alcance.colliderect(canteiro.rect):
                            if canteiro.estado == "pronto":
                                canteiro.estado = "vazio"
                                inventario_jogador.adicionar_item("tomate", 1)
                                inventario_jogador.adicionar_item("semente", 1)
                                mensagem = "Tomate colhido!"
                                break
                            elif canteiro.estado == "vazio" and inventario_jogador.remover_por_id(next((item.id for item in inventario_jogador.slots if item and item.tipo == "semente"), None), 1):
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
        if fazendeiro.obter_rect().colliderect(casa.colisao_rect): fazendeiro.x = fazendeiro.x_antigo
    if (teclas[pygame.K_d] or teclas[pygame.K_RIGHT]) and fazendeiro.x < largura_atual - fazendeiro.largura - 20:
        fazendeiro.x += fazendeiro.velocidade
        if fazendeiro.obter_rect().colliderect(casa.colisao_rect): fazendeiro.x = fazendeiro.x_antigo
    if (teclas[pygame.K_w] or teclas[pygame.K_UP]) and fazendeiro.y > 30:
        fazendeiro.y -= fazendeiro.velocidade
        if fazendeiro.obter_rect().colliderect(casa.colisao_rect): fazendeiro.y = fazendeiro.y_antigo
    if (teclas[pygame.K_s] or teclas[pygame.K_DOWN]) and fazendeiro.y < altura_atual - fazendeiro.altura - 90:
        fazendeiro.y += fazendeiro.velocidade
        if fazendeiro.obter_rect().colliderect(casa.colisao_rect): fazendeiro.y = fazendeiro.y_antigo

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

    if relogio_jogo.obter_nivel_escuridao() > 0:
        overlay = pygame.Surface((largura_atual, altura_atual), pygame.SRCALPHA)
        overlay.fill((10, 10, 40, relogio_jogo.obter_nivel_escuridao()))
        TELA.blit(overlay, (0, 0))

    inventario_jogador.desenhar(TELA, inicio_x_jog, inicio_y_jog, alpha_fundo=230)

    if bau_aberto:
        casa.inventario.desenhar(TELA, inicio_x_casa, inicio_y_casa, alpha_fundo=245)

    pygame.draw.rect(TELA, (30, 22, 16, 200), (20, 20, 160, 35), border_radius=6)
    TELA.blit(FONTE_MENSAGEM.render(relogio_jogo.obter_hora_str(), True, (255, 209, 102)), (30, 27))

    pygame.draw.rect(TELA, (30, 22, 16, 200), (190, 20, len(mensagem) * 8 + 20, 35), border_radius=6)
    TELA.blit(FONTE_MENSAGEM.render(mensagem, True, (255, 209, 102)), (200, 27))

    pygame.display.flip()