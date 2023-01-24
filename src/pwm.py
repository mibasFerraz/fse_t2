import RPi.GPIO as GPIO

class PWM:
    def __init__(self, pino_resistencia=23, pino_vento=24, frequencia=100):
        self.pino_resistencia = pino_resistencia
        self.pino_vento = pino_vento
        self.frequencia = frequencia
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pino_resistencia, GPIO.OUT)
        GPIO.setup(self.pino_vento, GPIO.OUT)

        self.resistor_pwm = GPIO.PWM(self.pino_resistencia, self.frequencia)
        self.vento_pwm = GPIO.PWM(self.pino_vento, self.frequencia)

    def ligar(self, carga_resistencia=0, carga_vento=40):
        self.vento_pwm.start(carga_vento)
        self.resistor_pwm.start(carga_resistencia)

    def desligar(self):
        self.resistor_pwm.stop()
        self.vento_pwm.stop()
        self.cleanup()

    def mudar_carga_vento(self, carga):
        carga = abs(carga)
        if carga != 0:
            carga = 40 if carga < 40 else carga

        print(f"carga vento: {carga}")
        self.vento_pwm.ChangeDutyCycle(carga)

    def mudar_carga_resistencia(self, carga):
        print(f"carga resistor: {carga}")
        self.resistor_pwm.ChangeDutyCycle(carga)

    def mudar_frequencia(self, frequencia):
        self.frequencia = frequencia
        self.resistor_pwm.ChangeFrequency(self.frequencia)
        self.vento_pwm.ChangeFrequency(self.frequencia)

    def controle(self, controle):
        if controle >= 0:
            self.mudar_carga_vento(0)
            self.mudar_carga_resistencia(controle)
            return

        self.mudar_carga_vento(controle)
        self.mudar_carga_resistencia(0)  

    def cleanup(self):
        GPIO.cleanup()