import src.forno as forno
import src.menu as menu

if __name__ == "__main__":
    try:
        print("Programa inicializado.\n")
        forno = forno.Forno()
        menu = menu.Menu()
        forno.configuracao_inicial()

        menu.inicio()

    except KeyboardInterrupt:
        forno.configuracao_final()
        print("Programa encerado.\n")
    
