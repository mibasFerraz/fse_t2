import csv
from datetime import datetime
import os


class Logger:
    def __init__(self, caminho = "log.csv"):
        self.caminho_arquivo = caminho
        self.nome_arquivo = self.gerar_arquivo_log()
          
    def escrever(self, tempInterna, tempExterna, tempUsuario, cargaResistor, cargaVento):
        log_data = [
            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            tempInterna,
            tempExterna,
            tempUsuario,
            cargaResistor,
            cargaVento,
        ]

        with open(self.caminho_arquivo, mode="a") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(log_data)           
            
    def gerar_arquivo_log(self):
        nome_arquivo = "log_" + datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + ".csv"
        self.caminho_arquivo += nome_arquivo

        if not os.path.isfile(self.caminho_arquivo):
            with open(self.caminho_arquivo, "w") as f:
                f.write("dataHora;tempInterna;tempExterna;tempUsuario;cargaResistor;cargaVento\n")

        return nome_arquivo   