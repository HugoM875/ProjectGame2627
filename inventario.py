# inventario.py
import pygame


class Inventario:

  def __init__(self, num_slots=8):
    self.num_slots = num_slots
    self.slots = [None] * num_slots
    self.slots[0] = {"tipo": "semente", "qtd": 1}

  def adicionar(self, tipo, quantidade=1):
    for slot in self.slots:
      if slot and slot["tipo"] == tipo and slot["qtd"] < 20:
        espaco = 20 - slot["qtd"]
        adicionar = min(quantidade, espaco)
        slot["qtd"] += adicionar
        quantidade -= adicionar
        if quantidade <= 0:
          return True

    while quantidade > 0:
      slot_vazio = -1
      for i, slot in enumerate(self.slots):
        if slot is None:
          slot_vazio = i
          break
      if slot_vazio == -1:
        return False

      adicionar = min(quantidade, 20)
      self.slots[slot_vazio] = {"tipo": tipo, "qtd": adicionar}
      quantidade -= adicionar
    return True

  def remover(self, tipo, quantidade=1):
    for slot in self.slots:
      if slot and slot["tipo"] == tipo:
        if slot["qtd"] >= quantidade:
          slot["qtd"] -= quantidade
          if slot["qtd"] <= 0:
            self.slots[self.slots.index(slot)] = None
          return True
    return False

  def contar(self, tipo):
    total = 0
    for slot in self.slots:
      if slot and slot["tipo"] == tipo:
        total += slot["qtd"]
    return total

  def desenhar(self, superficie, largura_tela, altura_tela, fonte_slot):
    slot_tamanho = 48
    slot_espacamento = 8
    largura_total = (slot_tamanho * self.num_slots) + (
        slot_espacamento * (self.num_slots - 1)
    )
    inicio_x = (largura_tela - largura_total) // 2
    inicio_y = altura_tela - 70

    pygame.draw.rect(
        superficie, (44, 33, 24), (0, inicio_y - 10, largura_tela, 80)
    )
    pygame.draw.line(
        superficie, (75, 55, 38), (0, inicio_y - 10), (largura_tela, inicio_y - 10), 3
    )

    for i in range(self.num_slots):
      sx = inicio_x + i * (slot_tamanho + slot_espacamento)
      sy = inicio_y

      pygame.draw.rect(
          superficie,
          (60, 45, 32),
          (sx, sy, slot_tamanho, slot_tamanho),
          border_radius=6,
      )
      pygame.draw.rect(
          superficie,
          (90, 70, 50),
          (sx, sy, slot_tamanho, slot_tamanho),
          2,
          border_radius=6,
      )

      item = self.slots[i]
      if item:
        if item["tipo"] == "semente":
          pygame.draw.circle(superficie, (120, 210, 80), (sx + 20, sy + 18), 7)
          pygame.draw.rect(superficie, (80, 160, 50), (sx + 19, sy + 18, 2, 8))
        elif item["tipo"] == "tomate":
          pygame.draw.circle(superficie, (231, 76, 60), (sx + 20, sy + 20), 10)
          pygame.draw.polygon(
              superficie,
              (46, 204, 113),
              [(sx + 20, sy + 8), (sx + 16, sy + 12), (sx + 24, sy + 12)],
          )

        if item["qtd"] > 1:
          txt_qtd = fonte_slot.render(str(item["qtd"]), True, (255, 209, 102))
          superficie.blit(txt_qtd, (sx + 6, sy + 30))