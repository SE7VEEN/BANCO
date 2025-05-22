import os
import time
import sys
from msvcrt import getch  # Para detectar Enter (Windows)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_centrado(texto):
    columnas = os.get_terminal_size().columns
    print(texto.center(columnas))

def efecto_maquina(texto, delay=0.03):
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def esperar_enter():
    print("\n" + "═" * 50)
    imprimir_centrado("Presiona ENTER para continuar...")
    while True:
        try:
            if ord(getch()) == 13:  # 13 = código ASCII de Enter
                break
        except:
            input()  # Fallback para otros sistemas
            break

def mostrar_banner():
    limpiar_pantalla()
    banner = r"""
        ██████╗░░█████╗░███╗░░██╗░█████╗░░█████╗░  ██████╗░███████╗███╗░░██╗██╗████████╗░█████╗░
        ██╔══██╗██╔══██╗████╗░██║██╔══██╗██╔══██╗  ██╔══██╗██╔════╝████╗░██║██║╚══██╔══╝██╔══██╗
        ██████╦╝███████║██╔██╗██║██║░░╚═╝██║░░██║  ██████╦╝█████╗░░██╔██╗██║██║░░░██║░░░██║░░██║
        ██╔══██╗██╔══██║██║╚████║██║░░██╗██║░░██║  ██╔══██╗██╔══╝░░██║╚████║██║░░░██║░░░██║░░██║
        ██████╦╝██║░░██║██║░╚███║╚█████╔╝╚█████╔╝  ██████╦╝███████╗██║░╚███║██║░░░██║░░░╚█████╔╝
        ╚═════╝░╚═╝░░╚═╝╚═╝░░╚══╝░╚════╝░░╚════╝░  ╚═════╝░╚══════╝╚═╝░░╚══╝╚═╝░░░╚═╝░░░░╚════╝░
        """

    print("\033[1;36m")  # Color cyan
    for linea in banner.split('\n'):
        imprimir_centrado(linea)
    print("\033[0m")  # Resetear color

def bienvenida_banco():
    mostrar_banner()
    print("\n" + "═" * 50)
    efecto_maquina("\033[1;32mBIENVENIDO A LA SIMULACIÓN BANCARIA\033[0m", 0.05)
    print("\n" + "═" * 50)
    imprimir_centrado("\033[1;37mSistema de gestión financiera virtual\033[0m")
    
    esperar_enter()
    
    limpiar_pantalla()
    efecto_maquina("\033[1;32mCargando sistema...\033[0m")
    time.sleep(1.5)
    limpiar_pantalla()
    imprimir_centrado("¡Sistema listo!")

if __name__ == "__main__":
    bienvenida_banco()