from servidor.hilos.operaciones import ejecutar_operacion, generar_solicitudes_automaticas
from servidor.hilos.pcb import monitor_procesos
from general.utils.utils import PCB_PATH, CLIENTES_PATH, CUENTAS_PATH, inicializar_archivo

from multiprocessing import Process
import time

if __name__ == "__main__":
    for f in [PCB_PATH, CLIENTES_PATH, CUENTAS_PATH]:
        inicializar_archivo(f)

    solicitudes = generar_solicitudes_automaticas()

    print("Solicitudes generadas automáticamente:")
    for i, solicitud in enumerate(solicitudes, 1):
        print(f"{i}. Tipo: {solicitud[0]}, ID: {solicitud[1]}, Operación: {solicitud[2]}")

    procesos = []
    for args in solicitudes:
        p = Process(target=ejecutar_operacion, args=args)
        p.start()
        procesos.append(p)
        time.sleep(0.5)

    for p in procesos:
        p.join()

    monitor_procesos()
    print("\nSistema bancario: Todas las operaciones completadas")
