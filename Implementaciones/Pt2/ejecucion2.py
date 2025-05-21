from queue import PriorityQueue
import sys, os, json, time, random
from multiprocessing import Lock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from servidor.hilos.procesos import crear_proceso
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from general.utils.utils import CUENTAS_PATH, inicializar_archivo
from servidor.hilos.pcb import safe_json_read

from Implementaciones.Pt2.Op_depositoPersonal import operacion_depositoPersonal
from Implementaciones.Pt2.Op_retiroPersonal import operacion_retiroPersonal
from Implementaciones.Pt2.Op_deposito import operacion_deposito
from Implementaciones.Pt2.Op_transferencia import operacion_transferencia
from Implementaciones.Pt2.Op_consultaSaldo import operacion_consulta_saldo

# Configuraciones
cuentas_lock = Lock()

#OPERACIONES EN VENTANILLAS
OPERACIONES_VENTANILLA_CLIENTE = ["Deposito Personal", "Retiro Personal", "Transferencia", "Consulta Saldo"]
OPERACIONES_VENTANILLA_VISITANTE = ["Deposito"] #retiro

#OPERACIONES DISPONIBLES CON ASESOR
OPERACIONES_ASESOR_VISITANTE = ["Consulta"]
OPERACIONES_ASESOR_CLIENTE = ["Consulta", "Modificacion de Datos", "Creacion de Cuentas", "Baja de Cuenta"]

# Tiempos de simulación por operación
TIEMPOS_OPERACION = {
    "Deposito": 2.0,
    "Retiro": 2.5,
    "Transferencia": 3.0,
    "Solicitud de Tarjeta": 1.5,
    "Consulta": 1.0,
    "Modificacion de Datos": 2.0,
    "Creacion de Cuentas": 4.0,
    "Baja de Cuenta": 3.5
}

def seleccionar_operacion_y_destino(tipo_usuario):
    """Selecciona aleatoriamente operación y destino según tipo de usuario"""
    if tipo_usuario == "Cliente":
        # Decidir si va a ventanilla o asesor
        if random.random() < 0.7:  # 70% probabilidad de ventanilla
            operacion = random.choice(OPERACIONES_VENTANILLA_CLIENTE)
            destino = "Ventanilla"
        else:
            operacion = random.choice(OPERACIONES_ASESOR_CLIENTE)
            destino = "Asesor"
    else:  # Visitante
        if random.random() < 0.5:  # 50% probabilidad de ventanilla
            operacion = random.choice(OPERACIONES_VENTANILLA_VISITANTE)
            destino = "Ventanilla"
        else:
            operacion = random.choice(OPERACIONES_ASESOR_VISITANTE)
            destino = "Asesor"
    
    return operacion, destino

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
    """Ejecuta la operación correspondiente según el destino"""
    try:
        mensaje = f"Procesando {proceso.operacion} en {proceso.destino}"
        actualizar_estado_pcb(proceso.pid, estado="En ejecución", operacion=mensaje)
        
        # Simular tiempo de operación
        tiempo = TIEMPOS_OPERACION.get(proceso.operacion, 1.0)
        time.sleep(tiempo)
        
        # Ejecutar operaciones específicas
        if proceso.operacion == "Deposito Personal":
            operacion_depositoPersonal(proceso, monto=random.uniform(10, 1000), cuentas_lock=cuentas_lock)
        elif proceso.operacion == "Retiro Personal":
            operacion_retiroPersonal(proceso, monto=50.0, cuentas_lock=cuentas_lock)
        elif proceso.operacion == "Deposito":
            cuenta_destino = obtener_id_cuenta_aleatorio()            
            operacion_deposito(proceso, cuenta_destino, monto=50.0, cuentas_lock=cuentas_lock)
        elif proceso.operacion == "Transferencia":
            cuenta_destino = obtener_id_cuenta_aleatorio()
            operacion_transferencia(proceso, cuenta_destino, monto=50.0, cuentas_lock=cuentas_lock)
        elif proceso.operacion == "Consulta Saldo":
            operacion_consulta_saldo(proceso, cuentas_lock=cuentas_lock)
        else:
            # Para otras operaciones solo registramos finalización
            actualizar_estado_pcb(proceso.pid, estado="Finalizado", 
                                operacion=f"{proceso.operacion} completada")
            
    except Exception as e:
        actualizar_estado_pcb(proceso.pid, estado="Error", 
                            operacion=f"Error en {proceso.operacion}: {str(e)}")

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

