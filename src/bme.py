import smbus2
import bme280

class BME:
    def __init__(self, address=0x76, port=1):
        self.address = address
        self.port = port
        self.bus = smbus2.SMBus(port)
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)

    def ler_temperatura(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data.temperature

    def fechar(self):
        self.bus.close()