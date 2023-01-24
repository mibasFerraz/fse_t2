from src.crc16 import calcula_crc
import struct

class Modbus:
    def __init__(self):
        id_matricula = [5,3,4,5]

        self.comandos = {
            # receber
            "comando_receber_temperatura_interna":        [0x01, 0x23, 0xC1, *id_matricula],
            "comando_receber_temperatura_referencia":     [0x01, 0x23, 0xC2, *id_matricula],
            "comando_receber_comando_usuario":            [0x01, 0x23, 0xC3, *id_matricula],

            # enviar
            "comando_enviar_sinal_controle":              [0x01, 0x16, 0xD1, *id_matricula],
            "comando_enviar_temperatura_referencia":      [0x01, 0x16, 0xD2, *id_matricula],
            "comando_enviar_estado_on":                   [0x01, 0x16, 0xD3, *id_matricula, 1],
            "comando_enviar_estado_off":                  [0x01, 0x16, 0xD3, *id_matricula, 0],
            "comando_enviar_controle_curva":              [0x01, 0x16, 0xD4, *id_matricula, 1],
            "comando_enviar_controle_fixa":               [0x01, 0x16, 0xD4, *id_matricula, 0],
            "comando_enviar_estado_funcionando":          [0x01, 0x16, 0xD5, *id_matricula, 1],
            "comando_enviar_estado_parado":               [0x01, 0x16, 0xD5, *id_matricula, 0],
            "comando_enviar_temperatura_ambiente":        [0x01, 0x23, 0xD6, *id_matricula],
        }

        self.receber_do_usuario = {
            0xA1: "receber_ligar",
            0xA2: "receber_desligar",
            0xA3: "receber_funcionando",
            0xA4: "receber_parado",
            0xA5: "receber_trocar_modo",
        }

    def codificar_mensagem(self, comando, value=None):
        mensagem_em_bytes = bytes(self.comandos[comando])
        if value:
            if type(value) == int:
                value_bytes = struct.pack("<i", value)
            elif type(value) == float:
                value_bytes = struct.pack("<f", value)
            mensagem_em_bytes += value_bytes

        codigo_crc = calcula_crc(mensagem_em_bytes).to_bytes(2, byteorder='little')
        return mensagem_em_bytes + codigo_crc

    def decodificar_mensagem(self, mensagem):

        if len(mensagem) == 9:
            data = mensagem[3:7]
            if self.verifica_crc(mensagem):
                return data
            else:
                print("CRC invalido")
                return None

        print("Mensagem invalida")
        return None

    def verifica_crc(self, buffer):
        received_crc = buffer[7:9]
        crc = calcula_crc(buffer[0:7]).to_bytes(2, byteorder='little')

        return received_crc == crc
