import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Actualizacion_PCB import actualizar_estado_pcb
from Implementaciones.Semaforos import atender_con_asesor, atender_en_ventanilla
from Implementaciones.Prioridad_cola import cola_procesos


def planificador():
    while not cola_procesos.empty():
        _, _, proceso = cola_procesos.get()
        actualizar_estado_pcb(proceso.pid, "En cola")

        if proceso.operacion in ["Consulta saldo", "Transferencia"]:
            atender_en_ventanilla(proceso)
        else:
            atender_con_asesor(proceso)

