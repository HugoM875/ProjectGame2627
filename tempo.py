# tempo.py
import pygame


class RelogioJogo:

  def __init__(self):
    self.dia = 1
    self.minutos_totais = 18 * 60 + 45
    self.acumulador_tempo = 0

  def atualizar(self, dt):
    self.acumulador_tempo += dt
    if self.acumulador_tempo >= 1000:
      self.minutos_totais += 1
      self.acumulador_tempo = 0

      if self.minutos_totais >= 24 * 60:
        self.minutos_totais = 0
        self.dia += 1

  def obter_hora_str(self):
    horas = (self.minutos_totais // 60) % 24
    minutos = self.minutos_totais % 60
    return f"Dia {self.dia} - {horas:02d}:{minutos:02d}"

  def obter_nivel_escuridao(self):
    minuto_19 = 19 * 60
    minuto_21 = 21 * 60

    if self.minutos_totais <= minuto_19:
      return 0
    elif self.minutos_totais >= minuto_21:
      return 180
    else:
      progresso = (self.minutos_totais - minuto_19) / (minuto_21 - minuto_19)
      return int(progresso * 180)

  def dormir(self):
    self.dia += 1
    self.minutos_totais = 8 * 60