# inventario.py
import pygame
import uuid

class Item:
    def __init__(self, tipo, qtd=1):
        self.id = str(uuid.uuid4())
        self.tipo = tipo
        self.qtd = qtd
        self.max_qtd = 20

    def copiar(self):
        novo = Item(self.tipo, self.qtd)
        novo.id = self.id
        return novo

class Inventario:
    def __init__(self, num_slots, num_cols=6):
        self.num_slots = num_slots
        self.slots = [None] * num_slots
        self.slot_tamanho = 48
        self.espacamento = 8
        self.num_cols = num_cols  # Permite definir colunas diferentes (ex: 8 para o jogador, 6 para a casa)

    def adicionar_item(self, tipo, qtd=1):
        resto = qtd
        for slot in self.slots:
            if slot and slot.tipo == tipo and slot.qtd < slot.max_qtd:
                pode = min(resto, slot.max_qtd - slot.qtd)
                slot.qtd += pode
                resto -= pode
                if resto == 0: return True
        while resto > 0:
            livre = -1
            for i in range(self.num_slots):
                if self.slots[i] is None:
                    livre = i; break
            if livre == -1: return False
            adic = min(resto, 20)
            self.slots[livre] = Item(tipo, adic)
            resto -= adic
        return True

    def remover_por_id(self, item_id, qtd=1):
        for i in range(self.num_slots):
            if self.slots[i] and self.slots[i].id == item_id:
                if self.slots[i].qtd > qtd:
                    self.slots[i].qtd -= qtd
                else:
                    self.slots[i] = None
                return True
        return False

    def obter_slot_por_pos(self, mx, my, inicio_x, inicio_y):
        for i in range(self.num_slots):
            col = i % self.num_cols
            row = i // self.num_cols
            sx = inicio_x + col * (self.slot_tamanho + self.espacamento)
            sy = inicio_y + row * (self.slot_tamanho + self.espacamento)
            if sx <= mx <= sx + self.slot_tamanho and sy <= my <= sy + self.slot_tamanho:
                return i
        return None

    def desenhar(self, superficie, inicio_x, inicio_y, alpha_fundo=230, item_arrastado_id=None):
        num_rows = (self.num_slots + self.num_cols - 1) // self.num_cols
        largura_painel = self.num_cols * self.slot_tamanho + (self.num_cols - 1) * self.espacamento + 20
        altura_painel = num_rows * self.slot_tamanho + (num_rows - 1) * self.espacamento + 20
        
        painel_rect = pygame.Rect(inicio_x - 10, inicio_y - 10, largura_painel, altura_painel)
        
        s = pygame.Surface((painel_rect.width, painel_rect.height), pygame.SRCALPHA)
        s.fill((50, 40, 30, alpha_fundo))
        superficie.blit(s, (painel_rect.x, painel_rect.y))
        pygame.draw.rect(superficie, (100, 80, 60), painel_rect, 2, border_radius=10)

        for i in range(self.num_slots):
            col = i % self.num_cols
            row = i // self.num_cols
            sx = inicio_x + col * (self.slot_tamanho + self.espacamento)
            sy = inicio_y + row * (self.slot_tamanho + self.espacamento)
            
            slot_rect = pygame.Rect(sx, sy, self.slot_tamanho, self.slot_tamanho)
            pygame.draw.rect(superficie, (30, 20, 10), slot_rect, border_radius=5)
            pygame.draw.rect(superficie, (80, 60, 40), slot_rect, 1, border_radius=5)

            item = self.slots[i]
            if item and item.id != item_arrastado_id:
                if item.tipo == "semente":
                    pygame.draw.circle(superficie, (120, 210, 80), (sx + 24, sy + 19), 10)
                    pygame.draw.rect(superficie, (80, 160, 50), (sx + 22, sy + 19, 4, 15))
                elif item.tipo == "tomate":
                    pygame.draw.circle(superficie, (231, 76, 60), (sx + 24, sy + 22), 13)
                    pygame.draw.polygon(superficie, (46, 204, 113), [(sx + 24, sy + 8), (sx + 18, sy + 14), (sx + 30, sy + 14)])

                if item.qtd > 1:
                    f = pygame.font.SysFont("Verdana", 10, bold=True)
                    t = f.render(str(item.qtd), True, (255, 209, 102))
                    superficie.blit(t, (sx + self.slot_tamanho - 12, sy + self.slot_tamanho - 14))