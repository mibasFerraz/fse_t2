from logger import Logger
from pid import PID
from bme import BME
from uart import Uart
from pwm import PWM
from time import sleep, time

class Forno:
    def __init__(self):
        self.logger = Logger()
        self.pid = PID(30.0, 0.2, 400.0, 1.0)
        self.bme = BME()
        self.uart = Uart()
        self.pwm = PWM()
        self.ligado = False
        self.funcionando = False
        self.modo = "curva"
        self.temp_interna = 0.0
        self.temp_ambiente = 25.0
        self.temp_referencia = 0.0

    def configuracao_inicial(self):
        self.uart.enviar("comando_enviar_estado_off")
        self.ligado = False
        self.uart.enviar("comando_enviar_estado_parado")
        self.funcionando = False
        self.uart.enviar("comando_enviar_controle_curva")
        self.modo = "curva"

        self.temp_ambiente = self.bme.ler_temperatura()
        self.uart.enviar("comando_enviar_temperatura_ambiente", self.temp_ambiente)

        init_vento = 40
        self.uart.enviar("comando_enviar_sinal_controle", -(init_vento))
        self.pwm.ligar(carga_vento = init_vento)
    
    def configuracao_final(self):
        self.uart.enviar("comando_enviar_estado_off")
        self.ligado = False
        self.uart.enviar("comando_enviar_estado_parado")
        self.funcionando = False
        self.uart.enviar("comando_enviar_controle_curva")
        self.modo = "curva"

        self.temp_ambiente = self.bme.ler_temperatura()
        self.uart.enviar("comando_enviar_temperatura_ambiente", self.temp_ambiente)

        init_vento = 40
        self.uart.enviar("comando_enviar_sinal_controle", -(init_vento))
        self.pwm.ligar(carga_vento = init_vento)
            
    def configurar_pid(self):
        return False

    def loop(self):
        tempo_inicio_curva = 0

        self.configurar_pid()

        print("Forno Ligado.\n")

        while True:
            sleep(0.3)
            self.logger.escrever(self.temp_interna, self.temp_ambiente, self.temp_referencia,
            abs(self.pid.sinal_de_controle) if self.pid.sinal_de_controle >= 0 else 0,
            abs(self.pid.sinal_de_controle) if self.pid.sinal_de_controle < 0 else 0)
            print("\n")

            if self.funcionando:
                if self.modo == "fixo": 
                    self.fixo()

                if self.modo == "curva":
                    self.curva(tempo_inicio_curva)

            self.temp_ambiente = self.bme.ler_temperatura()
            self.uart.enviar("comando_enviar_temperatura_ambiente", self.temp_ambiente)

            self.uart.enviar("comando_receber_comando_usuario")
            comando_usuario = self.uart.receber()[0]
            sleep(0.2)

            if comando_usuario == 0:
                sleep(0.2)
                continue

            if comando_usuario == 161:
                self.uart.enviar("comando_enviar_estado_on")
                self.ligado = True

            elif comando_usuario == 162:
                self.uart.enviar("comando_enviar_estado_off")
                self.ligado = False

            elif comando_usuario == 163:
                self.uart.enviar("comando_enviar_estado_on")
                self.ligado = True
                self.uart.enviar("comando_env_estado_funcionando")
                self.funcionando = True
                tempo_inicio_curva = time()

            elif comando_usuario == 164:
                self.uart.enviar("comando_enviar_estado_parado")
                self.funcionando = False
                self.pwm.controle(-75)

            elif comando_usuario == 165:
                if self.modo == "curva":
                    self.modo = "fixo"
                    self.uart.enviar("comando_enviar_controle_fixa")
                    continue
                self.modo = "curva"
                self.uart.enviar("comando_enviar_controle_curva")
                tempo_inicio_curva = time()

    def debug(self):
        inicia_debug = input("Iniciar em modo debug? (sim/nao)\n")
        if inicia_debug != 'sim':
            return False

        self.configurar_pid()

        self.temp_referencia = float(input("Qual a temperatura de referencia?\n"))
        print("Forno ligado\n")

        self.uart.enviar("comando_enviar_estado_on")
        self.ligado = True
        self.uart.enviar("comando_enviar_estado_funcionando")
        self.funcionando = True
        self.uart.enviar("comando_enviar_controle_curva")
        self.modo = "curva"

        self.uart.enviar("comando_enviar_temperatura_referencia", self.temp_referencia)
        self.pid.atualiza_referencia(self.temp_referencia)


        while True:
            self.temp_interna = self.uart.enviar_receber_float("comando_receber_temperatura_interna")
            print(f"Mansagem traduzida: {self.temp_interna}")

            controle = self.pid.controle(self.temp_interna)
            print(f"Controle: {controle}\n")
            self.uart.enviar("comando_enviar_sinal_controle", controle)
            self.pwm.controle(controle)

            sleep(1)