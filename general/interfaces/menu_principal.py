import os
import time
import sys
from msvcrt import getch 



"""
Limpia la pantalla del terminal.
"""
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


"""
Imprime un texto centrado horizontalmente en la terminal.
"""
def imprimir_centrado(texto):
    columnas = os.get_terminal_size().columns
    print(texto.center(columnas))



"""
Simula el efecto de una máquina de escribir, imprimiendo el texto letra por letra
con un pequeño retardo.
"""
def efecto_maquina(texto, delay=0.03):
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()
        time.sleep(delay)
    print()



"""
Muestra un mensaje centrado para que el usuario presione Enter y espera hasta que lo haga.
"""
def esperar_enter():
    imprimir_centrado("Presiona ENTER para continuar...")
    while True:
        try:
            if ord(getch()) == 13: 
                break
        except:
            input()  
            break


"""
Muestra un banner decorativo en ASCII art con colores,
centrado en pantalla, al iniciar el programa.
"""
def mostrar_banner():
    limpiar_pantalla()
    banner = r"""
    
    
    
    
    
    
 
    
    
    ███████╗██╗         ██████╗  █████╗ ███╗   ██╗ ██████╗ ██████╗     ██████╗ ███████╗██╗         ██████╗ ███████╗███╗   ██╗██╗████████╗ ██████╗ 
    ██╔════╝██║         ██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔═══██╗    ██╔══██╗██╔════╝██║         ██╔══██╗██╔════╝████╗  ██║██║╚══██╔══╝██╔═══██╗
    █████╗  ██║         ██████╔╝███████║██╔██╗ ██║██║     ██║   ██║    ██║  ██║█████╗  ██║         ██████╔╝█████╗  ██╔██╗ ██║██║   ██║   ██║   ██║
    ██╔══╝  ██║         ██╔══██╗██╔══██║██║╚██╗██║██║     ██║   ██║    ██║  ██║██╔══╝  ██║         ██╔══██╗██╔══╝  ██║╚██╗██║██║   ██║   ██║   ██║
    ███████╗███████╗    ██████╔╝██║  ██║██║ ╚████║╚██████╗╚██████╔╝    ██████╔╝███████╗███████╗    ██████╔╝███████╗██║ ╚████║██║   ██║   ╚██████╔╝
            ╚══════╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝     ╚═════╝ ╚══════╝╚══════╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝   ╚═╝    ╚═════╝      
                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    """
    print("\033[1;36m")  # Color cyan
    for linea in banner.split('\n'):
        imprimir_centrado(linea)
    print("\033[0m")  # Resetea el color


"""
Función principal de bienvenida del sistema bancario.
Muestra el banner, un mensaje de bienvenida y simula una carga del sistema.
"""
def bienvenida_banco():
    mostrar_banner()

    imprimir_centrado("\033[1;32mBIENVENIDO A LA SIMULACIÓN BANCARIA\033[0m")

    
    esperar_enter()
    
    limpiar_pantalla()
    efecto_maquina("\033[1;32mCargando sistema...\033[0m")
    time.sleep(1.5)
    limpiar_pantalla()
    imprimir_centrado("¡Sistema listo!")

