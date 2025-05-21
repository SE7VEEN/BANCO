import time
import shutil, json, sys
import threading
from pathlib import Path
from multiprocessing import Process

from servidor.hilos.operaciones import ejecutar_operacion
from general.utils.utils import PCB_PATH, CLIENTES_PATH, CUENTAS_PATH, inicializar_archivo
from cliente.clientes.gestor import gestionar_clientes
from cliente.cuentas.gestion_cuenta import crear_cuentas_automaticamente_por_clientes
from Implementaciones.Pt2.ejecucion2 import planificador
# from Implementaciones.Ejecucion import iniciar_simulacion
from servidor.PCB_manager import mostrar_pcb
from general.interfaces.menu_principal import bienvenida_banco

# Definimos rutas
BASE_DIR = Path(__file__).parent
DATOS_DIR = BASE_DIR / "general" / "datos"
ARCHIVOS_JSON = {
    "clientes.json": CLIENTES_PATH,
    "cuentas.json": CUENTAS_PATH,
    "pcb.json": PCB_PATH,
}

def limpiar_y_crear_datos():
    """Elimina el directorio de datos y reinicia los archivos JSON como listas vacías."""
    try:
        if DATOS_DIR.exists():
            shutil.rmtree(DATOS_DIR)
        DATOS_DIR.mkdir(parents=True, exist_ok=True)

        for nombre_archivo in ARCHIVOS_JSON.keys():
            ruta = DATOS_DIR / nombre_archivo
            with open(ruta, 'w') as f:
                json.dump([], f, indent=4)  # Archivo JSON limpio, bien formateado
        return True
    except Exception as e:
        print(f"✖ Error al limpiar datos: {str(e)}")
        return False

def lanzar_visualizador():
    """Inicia el visualizador en modo tiempo real."""
    visualizador = mostrar_pcb(PCB_PATH)
    visualizador.mostrar(modo_vivo=True)

# def lanzar_procesos():
#     """Inicia procesos basados en las solicitudes simuladas."""
#     solicitudes = iniciar_simulacion()
#     print("\n📦 Solicitudes generadas automáticamente:")
#     for i, solicitud in enumerate(solicitudes, 1):
#         print(f"{i}. Tipo: {solicitud[0]}, ID: {solicitud[1]}, Operación: {solicitud[2]}")

#     procesos = []
#     for args in solicitudes:
#         p = Process(target=ejecutar_operacion, args=args)
#         p.start()
#         procesos.append(p)
#         time.sleep(0.5)  # Delay para observar cambios en tiempo real

#     for p in procesos:
#         p.join()

if __name__ == "__main__":
    if not limpiar_y_crear_datos():
        sys.exit(1)
        
    bienvenida_banco()   

    # Inicializar archivos si no existen
    for ruta in ARCHIVOS_JSON.values():
        inicializar_archivo(ruta)

    # Generar datos iniciales
    gestionar_clientes('generar', nuevo_data={'cantidad': 3})
    crear_cuentas_automaticamente_por_clientes()


    # Lanzar visualizador de PCB en hilo independiente
    visor_hilo = threading.Thread(target=lanzar_visualizador, daemon=True)
    visor_hilo.start()
    planificador()
    # Ejecutar operaciones en procesos
    # lanzar_procesos()

    # Esperar entrada para finalizar
    input("\nPresione ENTER para terminar la simulación y cerrar la vista en tiempo real...\n")