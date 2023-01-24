import serial
import time
from src.modbus import Modbus

import struct


class Uart:
    def __init__(self):
        self.serial = serial.Serial("/dev/serial0", 9600, timeout=2)
        self.modbus = Modbus()
        self.cerificar_conexao()

    def cerificar_conexao(self):
        conectado = self.serial.is_open
        if not conectado:
            print("Erro na UART\n")

        return conectado

    def receber(self):
        if self.cerificar_conexao():
            print("Esperando resposta.\n")
            time.sleep(0.2)
            buffer = self.serial.read(9)

            resposta = self.modbus.decodificar_mensagem(buffer)
            print("Mensagem recebida: \n", resposta)

            return resposta if resposta != None else struct.pack("<f", 0.0)

    def enviar(self, mensagem, valor=None):
        if self.cerificar_conexao():
            msg = self.modbus.codificar_mensagem(mensagem, valor)
            print("Mensagem enviada: \n", msg)
            self.serial.write(msg)
            time.sleep(0.2)

    def enviar_receber_float(self, mensagem, valor=None):
        self.enviar(mensagem, valor)
        return round(struct.unpack("<f", self.receber())[0], 2)

    def close(self):
        self.serial.close()
        print("Conexao UART encerrada\n")
