from queue import PriorityQueue
import sys, os, json, time, random
from multiprocessing import Lock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from servidor.hilos.procesos import crear_proceso
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from general.utils.utils import CUENTAS_PATH, inicializar_archivo
from servidor.hilos.pcb import safe_json_read

from general.operaciones.Op_depositoPersonal import operacion_depositoPersonal
from general.operaciones.Op_retiroPersonal import operacion_retiroPersonal
from general.operaciones.Op_deposito import operacion_deposito
from general.operaciones.Op_retiro import operacion_retiro
from general.operaciones.Op_consultaDatos import operacion_consulta_datos
from general.operaciones.Op_transferencia import operacion_transferencia
from general.operaciones.Op_consultaSaldo import operacion_consulta_saldo
from general.operaciones.agregarCliente import agregarCliente
from general.operaciones.agregarTarjeta import agregarTarjeta
from general.operaciones.Op_modificacionDatos import operacion_modificacion_datos
from general.operaciones.Op_bajaCuenta import operacion_baja_cuenta


# Configuraciones
cuentas_lock = Lock()

#OPERACIONES EN VENTANILLAS
OPERACIONES_VENTANILLA_CLIENTE = ["Deposito Personal", "Retiro Personal", "Transferencia", "Consulta Saldo", "Consulta Datos"]
OPERACIONES_VENTANILLA_VISITANTE = ["Deposito", "Retiro"]

#OPERACIONES DISPONIBLES CON ASESOR
OPERACIONES_ASESOR_VISITANTE = ["Consulta", "Creacion cuenta"]
OPERACIONES_ASESOR_CLIENTE = ["Consulta", "Modificacion de Datos", "Baja de Cuenta", "Agregar tarjeta", "Creacion cuenta"]


# Tiempos de simulación por operación
TIEMPOS_OPERACION = {
    "Deposito": 4.0,
    "Retiro": 2.5,
    "Transferencia": 1.0,
    "Solicitud de Tarjeta": 1.5,
    "Consulta": 1.5,
    "Consulta Saldo": 2.0,
    "Consulta Datos": 2.0,
    "Modificacion de Datos": 2.0,
    "Creacion de Cuentas": 4.0,
    "Baja de Cuenta": 3.5
}


def obtener_id_cuenta_aleatorio(archivo_cuentas=CUENTAS_PATH):
    try:
        with open(archivo_cuentas, 'r') as f:
            cuentas = json.load(f)
        # Filtrar cuentas que tengan el campo id_cuenta
        cuentas_validas = [c for c in cuentas if c.get('id_cuenta') is not None]
        if not cuentas_validas:
            return None
        cuenta_aleatoria = random.choice(cuentas_validas)
        return str(cuenta_aleatoria['id_cuenta'])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al leer el archivo: {e}")
        return None
    
def seleccionar_operacion_y_destino(tipo_usuario):
    """Selecciona aleatoriamente operación y destino según tipo de usuario"""
    if tipo_usuario == "Cliente":
        # Decidir si va a ventanilla o asesor
        if random.random() < 0.2:  # 70% probabilidad de ventanilla
            operacion = random.choice(OPERACIONES_VENTANILLA_CLIENTE)
            destino = "Ventanilla"
        else:
            operacion = random.choice(OPERACIONES_ASESOR_CLIENTE)
            destino = "Asesor"
    else:  # Visitante
        if random.random() < 0.9:  # 50% probabilidad de ventanilla
            operacion = random.choice(OPERACIONES_VENTANILLA_VISITANTE)
            destino = "Ventanilla"
        else:
            operacion = random.choice(OPERACIONES_ASESOR_VISITANTE)
            destino = "Asesor"
    
    return operacion, destino


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


def despachar_proceso_secuencial(proceso):
    """Ejecuta la operación correspondiente según el destino"""
    try: 
        time.sleep(1)
        mensaje = f"Dirigiendo a {proceso.destino}"
        actualizar_estado_pcb(proceso.pid, estado="Preparando", operacion=mensaje)
        time.sleep(2)
        actualizar_estado_pcb(proceso.pid, estado="Esperando", operacion="Esperando acceso a cuentas") 
        time.sleep(2)
        actualizar_estado_pcb(proceso.pid, estado="En ejecución", operacion=proceso.operacion)
        
        # Simular tiempo de operación
        tiempo = TIEMPOS_OPERACION.get(proceso.operacion, 3.0)
        time.sleep(tiempo)
        
        monto=random.uniform(10, 1000)

        # Ejecutar operaciones específicas
        if proceso.operacion == "Deposito Personal":
            operacion_depositoPersonal(proceso, monto, cuentas_lock=cuentas_lock)
        elif proceso.operacion == "Retiro Personal":
            operacion_retiroPersonal(proceso, monto, cuentas_lock=cuentas_lock)
        elif proceso.operacion == "Deposito":
            cuenta_destino = obtener_id_cuenta_aleatorio()            
            operacion_deposito(proceso, cuenta_destino, monto, cuentas_lock=cuentas_lock)
        elif proceso.operacion == "Retiro":
            cuenta_destino = obtener_id_cuenta_aleatorio()
            operacion_retiro(proceso, cuenta_destino, monto, cuentas_lock=cuentas_lock)
        elif proceso.operacion == "Transferencia":
            cuenta_destino = obtener_id_cuenta_aleatorio()
            operacion_transferencia(proceso, cuenta_destino, monto, cuentas_lock=cuentas_lock)
        elif proceso.operacion == "Consulta Saldo":
            operacion_consulta_saldo(proceso, cuentas_lock=cuentas_lock)
        elif proceso.operacion == "Consulta Datos":
            operacion_consulta_datos(proceso, cuentas_lock=cuentas_lock) 
        elif proceso.operacion == "Creacion cuenta":
            agregarCliente(proceso, cuentas_lock=cuentas_lock)
        elif proceso.operacion == "Agregar tarjeta":
            agregarTarjeta(proceso, cuentas_lock=cuentas_lock)                                  
        elif proceso.operacion == "Modificacion de Datos":
            operacion_modificacion_datos(proceso)
            actualizar_estado_pcb(proceso.pid, estado="Finalizado", operacion=proceso.operacion)
        elif proceso.operacion == "Baja de Cuenta":
            tipo_baja = random.choice(["temporal", "definitiva"])
            operacion_baja_cuenta(proceso, tipo_baja=tipo_baja)
        elif proceso.operacion == "Consulta": 
            actualizar_estado_pcb(proceso.pid, estado="Finalizado", operacion=f"{proceso.operacion} completada") 
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


    for i, (tipo, id_user, oper, dest) in enumerate(solicitudes, 1):
        proceso = crear_proceso(tipo, id_user, oper, destino=dest)  # Pasar destino aquí
        cola_prioridad.put((proceso.prioridad, time.time(), proceso))

    while not cola_prioridad.empty():
        _, _, proceso = cola_prioridad.get()
        despachar_proceso_secuencial(proceso)

