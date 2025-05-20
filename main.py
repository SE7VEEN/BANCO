import time
from servidor.hilos.operaciones import ejecutar_operacion, generar_solicitudes_automaticas
#from servidor.hilos.pcb import monitor_procesos
from general.utils.utils import PCB_PATH, CLIENTES_PATH, CUENTAS_PATH, DATOS_PATH, BASE_DIR,  inicializar_archivo, eliminar_carpeta_datos

from cliente.clientes.clientes import Client
from cliente.clientes.gestor import gestionar_clientes
from cliente.cuentas.gestion_cuenta import crear_cuentas_automaticamente_por_clientes

from multiprocessing import Process
from servidor.PCB_manager import mostrar_pcb
import shutil, os, json, sys
from pathlib import Path

BASE_DIR = Path(__file__).parent  # Apunta a BANCO/
DATOS_DIR = BASE_DIR / "general" / "datos"


def limpiar_y_crear_datos():
    try:
        # Eliminar la carpeta si existe
        if DATOS_DIR.exists():
            shutil.rmtree(DATOS_DIR)
        
        # Crear la carpeta nuevamente
        DATOS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Crear archivos JSON vacíos
        archivos_necesarios = ['clientes.json', 'cuentas.json', 'pcb.json']
        for archivo in archivos_necesarios:
            with open(DATOS_DIR / archivo, 'w') as f:
                json.dump([], f)
            
        return True
    except Exception as e:
        print(f"✖ Error al limpiar datos: {str(e)}")
        return False

if __name__ == "__main__":

    
    if not limpiar_y_crear_datos():
        sys.exit(1)  # Salir si hay error
    print("\n") 


    

    for f in [PCB_PATH, CLIENTES_PATH, CUENTAS_PATH]:
        inicializar_archivo(f)


    cliente_aleatorio = Client()
    #gestionar_clientes('agregar', cliente=cliente_aleatorio)
    gestionar_clientes('generar', nuevo_data={'cantidad': 8})
    print("\n")

    crear_cuentas_automaticamente_por_clientes()
    print("\n")

    solicitudes = generar_solicitudes_automaticas()

    print("Solicitudes generadas automáticamente:")
    for i, solicitud in enumerate(solicitudes, 1):
        print(f"{i}. Tipo: {solicitud[0]}, ID: {solicitud[1]}, Operación: {solicitud[2]}")

    print("\n")
    procesos = []
    for args in solicitudes:
        p = Process(target=ejecutar_operacion, args=args)
        p.start()
        procesos.append(p)
        time.sleep(0.5)

    for p in procesos:
        p.join()

    #monitor_procesos()
    #print("\nSistema bancario: Todas las operaciones completadas")

    print("\n")
    visualizador = mostrar_pcb(PCB_PATH)
    
    # Mostrar ayuda
    print("\nOpciones disponibles:")
    print("1. Vista en tiempo real")
    print("2. Ver JSON crudo")
    print("3. Salir")
    
    while True:
        opcion = input("\nSeleccione una opción (1-3): ")
        
        if opcion == "1":
            print("\nIniciando vista en tiempo real... (Presione Ctrl+C para salir)")
            try:
                visualizador.mostrar(modo_vivo=True)
            except KeyboardInterrupt:
                print("\nRegresando al menú principal...")
        elif opcion == "2":
            visualizador.mostrar_json_crudo()
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente de nuevo.")




