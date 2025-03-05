import math

class RadioLinkCalculator:
    def __init__(self):
        # Constantes físicas
        self.c = 3e8  # Velocidade da luz (m/s)

    def calcular_perda_espaco_livre(self, frequencia, distancia):
        """
        Calcula a perda de espaço livre usando a fórmula de Friis

        :param frequencia: Frequência do sinal em Hz
        :param distancia: Distância entre antenas em metros
        :return: Perda de espaço livre em dB
        """
        # Fórmula de perda de espaço livre (dB)
        perda_espaco_livre = 20 * math.log10(distancia) + 20 * math.log10(frequencia) - 147.55
        return perda_espaco_livre

    def calcular_perda_elevacao(self, altura_tx, altura_rx, distancia):
        """
        Calcula a perda adicional devido à diferença de altura das antenas

        :param altura_tx: Altura da antena transmissora em metros
        :param altura_rx: Altura da antena receptora em metros
        :param distancia: Distância entre antenas em metros
        :return: Perda de elevação em dB
        """
        # Cálculo de perda de elevação (modelo simplificado)
        diferenca_altura = abs(altura_tx - altura_rx)
        perda_elevacao = 6.2 * math.pow((diferenca_altura / distancia), 2)
        return perda_elevacao

    def calcular_potencia_recebida(self,
                                   potencia_transmissao,  # dBm
                                   ganho_tx,  # dBi
                                   ganho_rx,  # dBi
                                   perda_cabo_tx,  # dB
                                   perda_cabo_rx,  # dB
                                   perda_conector,  # dB
                                   perda_centelhador,  # dB
                                   frequencia,  # Hz
                                   distancia,  # metros
                                   altura_tx,  # metros
                                   altura_rx  # metros
                                   ):
        """
        Calcula a potência final recebida considerando todos os parâmetros

        :return: Potência recebida em dBm
        """
        # Perda de espaço livre
        perda_espaco_livre = self.calcular_perda_espaco_livre(frequencia, distancia)

        # Perda de elevação
        perda_elevacao = self.calcular_perda_elevacao(altura_tx, altura_rx, distancia)

        # Cálculo do balanço de potência
        potencia_recebida = (
                potencia_transmissao +  # Potência de transmissão
                ganho_tx -  # Ganho da antena transmissora
                perda_cabo_tx -  # Perda de cabo na transmissão
                perda_conector -  # Perda de conectores
                perda_centelhador -  # Perda de centelhador
                perda_espaco_livre +  # Perda de espaço livre
                ganho_rx -  # Ganho da antena receptora
                perda_cabo_rx -  # Perda de cabo na recepção
                perda_elevacao  # Perda de elevação
        )

        return potencia_recebida

    def interface_usuario(self):
        """
        Interface interativa para coleta de dados e cálculo
        """
        print("=== Calculadora de Potência de Enlace de Rádio ===")

        # Dados de entrada
        print("\nInformações de Transmissão:")
        potencia_transmissao = float(input("Potência de transmissão do rádio (dBm): "))
        frequencia = float(input("Frequência do sinal (Hz): "))

        # Dados da antena transmissora
        print("\nAntena Transmissora:")
        ganho_tx = float(input("Ganho da antena (dBi): "))
        altura_tx = float(input("Altura da antena (metros): "))
        perda_cabo_tx = float(input("Perda de cabo (dB): "))

        # Dados da antena receptora
        print("\nAntena Receptora:")
        ganho_rx = float(input("Ganho da antena (dBi): "))
        altura_rx = float(input("Altura da antena (metros): "))
        perda_cabo_rx = float(input("Perda de cabo (dB): "))

        # Dados de conexão
        print("\nInformações de Conexão:")
        distancia = float(input("Distância entre antenas (metros): "))
        perda_conector = float(input("Perda de conector (dB): "))
        perda_centelhador = float(input("Perda de centelhador (dB): "))

        # Calcular potência recebida
        potencia_recebida = self.calcular_potencia_recebida(
            potencia_transmissao,
            ganho_tx,
            ganho_rx,
            perda_cabo_tx,
            perda_cabo_rx,
            perda_conector,
            perda_centelhador,
            frequencia,
            distancia,
            altura_tx,
            altura_rx
        )

        # Exibir resultados
        print("\n=== Resultados ===")
        print(f"Potência Recebida: {potencia_recebida:.2f} dBm")
        print(f"Potência Recebida: {10 ** ((potencia_recebida - 30) / 10):.4f} mW")


# Execução do programa
if __name__ == "__main__":
    calculadora = RadioLinkCalculator()
    calculadora.interface_usuario()