import json
from uuid import uuid4
from datetime import datetime
from multiprocessing import Process, Lock
import time
import os
import random

# Lock global para sincronizar acceso a recursos compartidos
pcb_lock = Lock()
clientes_lock = Lock()
cuentas_lock = Lock()

    # Inicialización de archivos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Ruta hacia la carpeta general/datos
DATOS_PATH = os.path.join(BASE_DIR, 'general', 'datos')

# Rutas de archivos
CUENTAS_PATH = os.path.join(DATOS_PATH, 'cuentas.json')
CLIENTES_PATH = os.path.join(DATOS_PATH, 'clientes.json')
PCB_PATH = os.path.join(DATOS_PATH, 'pcb.json')


class Proceso:
    def __init__(self, tipo_usuario, pid=None, ppid=None, estado="En espera", id_usuario=None, id_cuenta=None, tipo_cuenta=None, operacion=None):
        self.pid = pid or str(os.getpid())   # ID único de 5 dígitos
        self.ppid = ppid or str(os.getppid())                      # Parent PID
        self.estado = estado
        self.id_cuenta = id_cuenta
        self.id_usuario = id_usuario
        self.tipo_usuario = tipo_usuario        # "Cliente" o "Visitante"
        self.tipo_cuenta = tipo_cuenta          # "Estándar", "Premium", None
        self.operacion = operacion or str("NULL")
        self.timestamp = datetime.now().strftime("%H:%M:%S")

    def to_dict(self):
        return {
            "PID": self.pid,
            "PPID": self.ppid,
            "Estado": self.estado,
            "IDUsuario": self.id_usuario,
            "IDCuenta": self.id_cuenta,
            "TipoUsuario": self.tipo_usuario,
            "TipoCuenta": self.tipo_cuenta,
            "Operacion": self.operacion,
            "Timestamp": self.timestamp
        }

def inicializar_archivo(filename, default=[]):
    """Asegura que el archivo JSON exista"""
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump(default, f)

def guardar_en_pcb(proceso):
    """Guarda el proceso en PCB.json con sincronización"""
    with pcb_lock:
        try:
            inicializar_archivo(PCB_PATH)
            with open(PCB_PATH, 'r+') as f:
                pcb = json.load(f)
                pcb.append(proceso.to_dict())
                f.seek(0)
                json.dump(pcb, f, indent=4)
        except Exception as e:
            print(f"Error crítico al actualizar PCB: {str(e)}")
            raise

def obtener_datos_cliente(id_usuario):
    """Obtiene todos los datos del cliente incluyendo id_cuenta"""
    with cuentas_lock:
        try:
            inicializar_archivo(CUENTAS_PATH)
            with open(CUENTAS_PATH, 'r') as f:
                cuentas = json.load(f)
            for cuenta in cuentas:
                if cuenta.get('id_usuario') == id_usuario:
                    return cuenta
            return None
        except Exception as e:
            print(f"Error obteniendo datos del cliente: {str(e)}")
            return None

def crear_proceso(tipo_usuario, id_usuario=None, operacion=None):
    """
    Crea y registra un nuevo proceso en el sistema
    
    Args:
        tipo_usuario: "Cliente" o "Visitante"
        id_usuario: Requerido para clientes
        operacion: Tipo de operación bancaria
    
    Returns:
        Objeto Proceso creado
    """
    if tipo_usuario == "Cliente":
        if not id_usuario:
            raise ValueError("Se requiere ID de usuario para clientes")
            
        datos_cliente = obtener_datos_cliente(id_usuario)
        if not datos_cliente:
            raise ValueError("Cliente no registrado o ID inválido")
            
        tipo_cuenta = datos_cliente.get('tipo_cuenta', 'Estándar')
        id_cuenta = datos_cliente.get('id_cuenta')
    else:
        if id_usuario is not None:
            raise ValueError("Visitante no debe tener ID de usuario")
        tipo_cuenta = None
        id_cuenta = None

    proceso = Proceso(
        id_usuario=id_usuario,
        id_cuenta=id_cuenta,
        tipo_usuario=tipo_usuario,
        tipo_cuenta=tipo_cuenta,
        operacion=operacion
    )
    
    guardar_en_pcb(proceso)
    return proceso

def terminar_proceso(self, proceso):
    # Actualizar estado
    proceso.estado = "Finalizado"
    guardar_en_pcb(proceso)

def ejecutar_operacion(tipo_usuario, id_usuario=None, operacion=None):
    """
    Ejecuta una operación bancaria en un proceso independiente
    
    Args:
        tipo_usuario: "Cliente" o "Visitante"
        id_usuario: Para clientes registrados
        operacion: Tipo de operación
    """


    try:
        proceso = crear_proceso(tipo_usuario, id_usuario, operacion)
        print(f"[Proceso {proceso.pid}] Iniciando {operacion}...")
        
        # Simulación de tiempo de procesamiento
        time.sleep(2 if "Consulta" in operacion else 3)

        terminar_proceso(proceso)

        print(f"[Proceso {proceso.pid}] {operacion} completada exitosamente")
        
    except Exception as e:
        print(f"[Error] En operacion {operacion}: {str(e)}")

def monitor_procesos():
    """Muestra el estado actual de los procesos"""
    try:
        with pcb_lock:
            inicializar_archivo(PCB_PATH)
            with open(PCB_PATH, 'r') as f:
                procesos = json.load(f)
        
        print("\n=== MONITOR DE PROCESOS ===")
        print(f"Procesos totales: {len(procesos)}")
        print("Últimos 5 procesos:")
        for p in procesos[-5:]:
            print(f"PID: {p['PID']} | Estado: {p['Estado']} | Operación: {p['Operacion']}")
    except Exception as e:
        print(f"Error en monitor: {str(e)}")

def generar_solicitudes_automaticas():
    """Genera solicitudes automáticas basadas en cuentas existentes"""
    #operaciones_clientes = ["Deposito", "Retiro", "Transferencia", "Consulta de saldo"]
    operaciones_clientes = ["NULL"]
    #operaciones_visitantes = ["Creacion de cuenta", "Consulta de servicios", "Informacion de productos"]
    operaciones_visitantes = ["NULL"]
    
    solicitudes = []
    
    # Cargar cuentas existentes
    with cuentas_lock:
        inicializar_archivo(CUENTAS_PATH)
        with open(CUENTAS_PATH, 'r') as f:
            cuentas = json.load(f)
    
    # Generar solicitudes para clientes existentes
    for cuenta in cuentas:
        id_usuario = cuenta.get('id_usuario')
        if id_usuario:
            # 1-3 operaciones por cliente
            for _ in range(random.randint(1, 3)):
                operacion = random.choice(operaciones_clientes)
                solicitudes.append(("Cliente", id_usuario, operacion))
    
    # Generar solicitudes para visitantes (1-3)
    for _ in range(random.randint(2, 6)):
        operacion = random.choice(operaciones_visitantes)
        solicitudes.append(("Visitante", None, operacion))
    
    return solicitudes

if __name__ == "__main__":


    for f in [PCB_PATH, CLIENTES_PATH, CUENTAS_PATH]:
        inicializar_archivo(f)
    
    # Generar solicitudes automáticas
    solicitudes = generar_solicitudes_automaticas()
    
    # Mostrar las solicitudes generadas
    print("Solicitudes generadas automáticamente:")
    for i, solicitud in enumerate(solicitudes, 1):
        print(f"{i}. Tipo: {solicitud[0]}, ID: {solicitud[1]}, Operación: {solicitud[2]}")
    
    # Lanzamiento de procesos
    procesos = []
    for args in solicitudes:
        p = Process(target=ejecutar_operacion, args=args)
        p.start()
        procesos.append(p)
        time.sleep(0.5)  # Pequeña pausa entre procesos
    
    for p in procesos:
        p.join()
    
    monitor_procesos()
    print("\nSistema bancario: Todas las operaciones completadas")