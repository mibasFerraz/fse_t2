import forno

if __name__ == "__main__":
    try:
        print("Programa inicializado.\n")
        forno = forno.Forno()
        forno.configuracao_inicial()

        if not forno.debug():
            forno.loop()

    except KeyboardInterrupt:
        forno.configuracao_final()
        print("Programa encerado.\n")
    
