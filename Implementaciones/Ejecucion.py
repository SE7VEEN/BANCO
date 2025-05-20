import os, sys, time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.lanza_solicitud import lanzar_solicitudes
from Implementaciones.Prioridad_cola import PRIORIDAD, cola_procesos
from Implementaciones.Actualizacion_PCB import actualizar_estado_pcb
from Implementaciones.Planificacion import planificador
from servidor.hilos.procesos import crear_proceso


def iniciar_simulacion():
    solicitudes = lanzar_solicitudes()
    for tipo, id_usuario, operacion in solicitudes:
        proceso = crear_proceso(tipo, id_usuario, operacion)
        prioridad = PRIORIDAD.get(proceso.tipo_cuenta or proceso.tipo_usuario, 1)
        cola_procesos.put((prioridad, time.time(), proceso))
        actualizar_estado_pcb(proceso.pid, "En espera")
    
    planificador()
