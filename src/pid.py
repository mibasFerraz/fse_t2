class PID:
        def __init__(self, Kp, Ki, Kd, T=1, MIN=-100, MAX=100):
                self.Kp = Kp
                self.Ki = Ki
                self.Kd = Kd
                self.T = T
                self.MIN = MIN
                self.MAX = MAX
                self.referencia = 0.0
                self.erro_total = 0.0
                self.erro_anterior = 0.0
                self.sinal_de_controle = 0

        def atualiza_referencia(self, referencia):
                self.referencia = referencia

        def configura_constantes(self, Kp, Ki, Kd):
                self.Kp = Kp
                self.Ki = Ki
                self.Kd = Kd

        def controle(self, saida_medida):
                erro = self.referencia - saida_medida
                self.erro_total += erro

                if self.erro_total >= self.MAX:
                        self.erro_total = self.MAX

                elif self.erro_total <= self.MIN:
                        self.erro_total = self.MIN

                delta_erro = erro - self.erro_anterior
                self.sinal_de_controle = self.Kp * erro + (self.Ki * self.T) * self.erro_total + (self.Kd / self.T) * delta_erro
                
                if self.sinal_de_controle >= self.MAX:
                        self.sinal_de_controle = self.MAX

                elif self.sinal_de_controle <= self.MIN:
                        self.sinal_de_controle = self.MIN

                self.erro_anterior = erro

                return int(self.sinal_de_controle)
