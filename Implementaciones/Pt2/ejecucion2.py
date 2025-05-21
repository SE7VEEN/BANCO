import json
import random
import time, sys, os
from queue import PriorityQueue
from multiprocessing import Process, Semaphore, Lock


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from servidor.hilos.procesos import crear_proceso
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from general.utils.utils import CUENTAS_PATH, inicializar_archivo
from Implementaciones.Pt2.Operacion import operacion_deposito  # Debes tener esta función implementada

# Configuraciones de concurrencia
cuentas_lock = Lock()
ventanillas = Semaphore(2)
asesores = Semaphore(2)

# Operaciones válidas
OPERACIONES_CLIENTES = ["Deposito", "Consulta"]
OPERACIONES_VISITANTES = ["Consulta"]

#from servidor.hilos.operaciones import generar_solicitudes_automaticas, ejecutar_operacion
from multiprocessing import Process

""" def lanzar_solicitudes():
    solicitudes = generar_solicitudes_automaticas()
    procesos = []
    for tipo, id_usuario, operacion in solicitudes:
        p = Process(target=ejecutar_operacion, args=(tipo, id_usuario, operacion))
        p.start()
        procesos.append(p)
    for p in procesos:
        p.join()

    return solicitudes """

""" def generar_solicitudes_automaticas():
    operaciones_clientes = ["NULL"]
    operaciones_visitantes = ["NULL"]
    solicitudes = []

    with cuentas_lock:
        inicializar_archivo(CUENTAS_PATH)
        with open(CUENTAS_PATH, 'r') as f:
            cuentas = json.load(f)

    for cuenta in cuentas:
        id_usuario = cuenta.get('id_usuario')
        if id_usuario:
            for _ in range(random.randint(1, 1)):
                operacion = random.choice(operaciones_clientes)
                solicitudes.append(("Cliente", id_usuario, operacion))

    for _ in range(random.randint(1, 1)):
        operacion = random.choice(operaciones_visitantes)
        solicitudes.append(("Visitante", None, operacion))
        solicitudes.append(("Visitante", None, operacion))

    return solicitudes """

# 1. Generar solicitudes automáticas
def generar_solicitudes_automaticas():
    solicitudes = []

    with cuentas_lock:
        inicializar_archivo(CUENTAS_PATH)
        with open(CUENTAS_PATH, 'r') as f:
            cuentas = json.load(f)

    for cuenta in cuentas:
        id_usuario = cuenta.get('id_usuario')
        if id_usuario:
            operacion = random.choice(OPERACIONES_CLIENTES)
            solicitudes.append(("Cliente", id_usuario, operacion))

    for _ in range(2):
        operacion = random.choice(OPERACIONES_VISITANTES)
        solicitudes.append(("Visitante", None, operacion))

    return solicitudes

# 2. Despachar proceso a ventanilla o asesor
def despachar_proceso(proceso, semaforo):
    try:
        # Actualización consistente del PCB con lock
        with cuentas_lock:
            actualizar_estado_pcb(
                pid=proceso.pid, 
                estado="En ejecucion",
                prioridad=proceso.prioridad,
                destino=proceso.destino
            )

        if proceso.operacion == "Deposito":
            operacion_deposito(proceso, monto=100.0, cuentas_lock=cuentas_lock)
            with cuentas_lock:
                actualizar_estado_pcb(
                    pid=proceso.pid,
                    estado="Finalizado",
                    destino=proceso.destino
                )

        elif proceso.operacion == "Consulta":
            time.sleep(1)  # Simulación
            with cuentas_lock:
                actualizar_estado_pcb(
                    pid=proceso.pid,
                    estado="Finalizado",
                    destino=proceso.destino
                )
        else:
            with cuentas_lock:
                actualizar_estado_pcb(
                    pid=proceso.pid,
                    estado="Error",
                    destino=proceso.destino
                )

    except Exception as e:
        with cuentas_lock:
            actualizar_estado_pcb(
                pid=proceso.pid,
                estado="Error",
                destino=proceso.destino
            )
        print(f"Error procesando {proceso.pid}: {str(e)}")
        
    finally:
        semaforo.release()




# 3. Planificador de prioridades con FIFO dentro de cada nivel
def planificador():
    solicitudes = generar_solicitudes_automaticas()
    cola_prioridad = PriorityQueue()

    for tipo, id_usuario, operacion in solicitudes:
        proceso = crear_proceso(tipo, id_usuario, operacion)
        cola_prioridad.put((proceso.prioridad, time.time(), proceso))  # time.time() para preservar orden FIFO

    procesos_en_ejecucion = []

    while not cola_prioridad.empty():
        _, _, proceso = cola_prioridad.get()

        if proceso.destino == "Ventanilla":
            sem = ventanillas
        elif proceso.destino == "Asesor":
            sem = asesores
        else:
            actualizar_estado_pcb(proceso.pid, estado="Error", operacion="Destino no valido")
            continue

        sem.acquire()
        p = Process(target=despachar_proceso, args=(proceso, sem))
        p.start()
        procesos_en_ejecucion.append(p)

    for p in procesos_en_ejecucion:
        p.join()

if __name__ == '__main__':
    planificador()
