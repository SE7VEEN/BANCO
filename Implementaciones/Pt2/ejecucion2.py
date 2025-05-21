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

OPERACIONES_CLIENTES = ["Deposito Personal", "Retiro", "Transferencia", "Consulta", "Consulta Saldo"]
OPERACIONES_VISITANTES = ["Consulta", "Deposito",]

def obtener_id_cuenta_aleatorio(archivo_cuentas=CUENTAS_PATH):
    try:
        with open(archivo_cuentas, 'r') as f:
            cuentas = json.load(f)
            
        # Filtrar cuentas que tengan el campo id_cuenta
        cuentas_validas = [c for c in cuentas if c.get('id_cuenta') is not None]
        
        if not cuentas_validas:
            return None
            
        cuenta_aleatoria = random.choice(cuentas_validas)
        return cuenta_aleatoria['id_cuenta']
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al leer el archivo: {e}")
        return None

# === Generar solicitudes automáticas ===
def generar_solicitudes_automaticas():
    cuentas = safe_json_read(CUENTAS_PATH, [])
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

# === Despachar proceso (versión secuencial) ===
def despachar_proceso_secuencial(proceso):
    actualizar_estado_pcb(proceso.pid, estado="En ejecución", operacion=f"Asignado a {proceso.destino}")

    if proceso.operacion == "Deposito Personal":
        operacion_depositoPersonal(proceso, monto=100.0, cuentas_lock=cuentas_lock)
    elif proceso.operacion == "Deposito":
        cuenta_destino = obtener_id_cuenta_aleatorio()
        operacion_deposito(proceso, cuenta_destino, monto=50.0, cuentas_lock=cuentas_lock)
    elif proceso.operacion == "Retiro":
        operacion_retiro(proceso, monto=50.0, cuentas_lock=cuentas_lock)
    elif proceso.operacion == "Transferencia":
        cuenta_destino = obtener_id_cuenta_aleatorio()
        operacion_transferencia(proceso, cuenta_destino, monto=50.0, cuentas_lock=cuentas_lock)
    elif proceso.operacion == "Consulta Saldo":
        cuenta_destino = obtener_id_cuenta_aleatorio()
        operacion_consulta_saldo(proceso, cuenta_destino, cuentas_lock=cuentas_lock)
    elif proceso.operacion == "Consulta":
        time.sleep(1)
        actualizar_estado_pcb(proceso.pid, estado="Finalizado", operacion="Consulta realizada")
    else:
        actualizar_estado_pcb(proceso.pid, estado="Error", operacion="Operación no implementada")

# === Planificador principal (sin multiprocessing) ===
def planificador():
    solicitudes = generar_solicitudes_automaticas()
    cola_prioridad = PriorityQueue()

    for tipo, id_usuario, operacion in solicitudes:
        proceso = crear_proceso(tipo, id_usuario, operacion)
        cola_prioridad.put((proceso.prioridad, time.time(), proceso))

    while not cola_prioridad.empty():
        _, _, proceso = cola_prioridad.get()
        despachar_proceso_secuencial(proceso)

# === Punto de entrada ===
if __name__ == '__main__':
    planificador()
