from queue import PriorityQueue
import sys, os, json, time, random
from multiprocessing import Lock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from servidor.hilos.procesos import crear_proceso
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from general.utils.utils import CUENTAS_PATH, inicializar_archivo
from Implementaciones.Pt2.Op_depositoPersonal import operacion_depositoPersonal
from Implementaciones.Pt2.Op_retiro import operacion_retiro
from Implementaciones.Pt2.Op_deposito import operacion_deposito
from Implementaciones.Pt2.Op_transferencia import operacion_transferencia
from Implementaciones.Pt2.Op_consultaSaldo import operacion_consulta_saldo
from servidor.hilos.pcb import safe_json_read

# Configuraciones
cuentas_lock = Lock()

OPERACIONES_CLIENTES = ["Depósito", "Consulta"]
OPERACIONES_VISITANTES = ["Consulta"]

# === Generar solicitudes automáticas ===
def generar_solicitudes_automaticas():
    """Genera solicitudes con operaciones y destinos aleatorios"""
    cuentas = safe_json_read(CUENTAS_PATH, [])
    solicitudes = []

    # Procesar clientes registrados
    for cuenta in cuentas:
        if 'id_usuario' in cuenta:
            operacion, destino = seleccionar_operacion_y_destino("Cliente")
            solicitudes.append(("Cliente", cuenta['id_usuario'], operacion, destino))

    # Añadir visitantes (2-4 aleatorios)
    for _ in range(random.randint(2, 4)):
        operacion, destino = seleccionar_operacion_y_destino("Visitante")
        solicitudes.append(("Visitante", None, operacion, destino))

    return solicitudes


# === Despachar proceso (versión secuencial) ===
def despachar_proceso_secuencial(proceso):
    actualizar_estado_pcb(proceso.pid, estado="En ejecución", operacion=f"Asignado a {proceso.destino}")

    if proceso.operacion == "Depósito":
        operacion_deposito(proceso, monto=100.0, cuentas_lock=cuentas_lock)
    elif proceso.operacion == "Consulta":
        time.sleep(1)
        actualizar_estado_pcb(proceso.pid, estado="Finalizado", operacion="Consulta realizada")
    else:
        actualizar_estado_pcb(proceso.pid, estado="Error", operacion="Operación no implementada")

# === Planificador principal (sin multiprocessing) ===

def planificador():
    solicitudes = generar_solicitudes_automaticas()
    cola_prioridad = PriorityQueue()

    print("\n=== Solicitudes generadas ===")
    for i, (tipo, id_user, oper, dest) in enumerate(solicitudes, 1):
        print(f"{i}. {tipo:8} -> {oper:20} en {dest:10} (ID: {id_user or 'N/A'})")
        proceso = crear_proceso(tipo, id_user, oper, destino=dest)  # Pasar destino aquí
        cola_prioridad.put((proceso.prioridad, time.time(), proceso))

    print("\n=== Procesando solicitudes ===")
    while not cola_prioridad.empty():
        _, _, proceso = cola_prioridad.get()
        print(f"PID {proceso.pid}: {proceso.tipo_usuario} - {proceso.operacion} en {proceso.destino}")
        despachar_proceso_secuencial(proceso)
