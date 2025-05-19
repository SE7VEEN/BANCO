import json
from uuid import uuid4
from datetime import datetime
from multiprocessing import Process, Lock
import time
import os

# Lock global para sincronizar acceso a recursos compartidos
pcb_lock = Lock()
clientes_lock = Lock()
cuentas_lock = Lock()

class Proceso:
    def __init__(self, tipo_usuario, pid=None, ppid=None, estado="En espera", id_usuario=None, id_cuenta = None, tipo_cuenta=None, operacion=None):
        self.pid = pid or str(uuid4().int)[:5]  # ID único de 5 dígitos
        self.ppid = ppid                        # Parent PID
        self.estado = estado
        self.id_cuenta = id_cuenta
        self.id_usuario = id_usuario
        self.tipo_usuario = tipo_usuario        # "Cliente" o "Visitante"
        self.tipo_cuenta = tipo_cuenta          # "Estándar", "Premium", None
        self.operacion = operacion
        self.timestamp = datetime.now().strftime("%H:%M:%S")

    def to_dict(self):
        return {
            "PID": self.pid,
            "PPID": self.ppid,
            "Estado": self.estado,
            "IDUsuario" : self.id_usuario,
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
            inicializar_archivo('pcb.json')
            with open('pcb.json', 'r+') as f:
                pcb = json.load(f)
                pcb.append(proceso.to_dict())
                f.seek(0)
                json.dump(pcb, f, indent=4)
        except Exception as e:
            print(f"Error crítico al actualizar PCB: {str(e)}")
            raise

def validar_cliente(id_usuario):
    """Verifica si el cliente existe en clientes.json"""
    with clientes_lock:
        try:
            inicializar_archivo('clientes.json')
            with open('clientes.json', 'r') as f:
                clientes = json.load(f)
            return any(c.get('id_usuario') == id_usuario for c in clientes)
        except Exception as e:
            print(f"Error validando cliente: {str(e)}")
            return False

def obtener_tipo_cuenta(id_usuario):
    """Obtiene el tipo de cuenta desde cuentas.json"""
    with cuentas_lock:
        try:
            with open('cuentas.json', 'r') as f:
                cuentas = json.load(f)
            for cuenta in cuentas:
                if cuenta.get('id_cuenta') == id_usuario:
                    return cuenta.get('tipo_cuenta', 'Estándar')
            return 'Estándar'
        except Exception as e:
            print(f"Error obteniendo tipo de cuenta: {str(e)}")
            return 'Estándar'
        
def obtener_datos_cliente(id_usuario):
    """Obtiene todos los datos del cliente incluyendo id_cuenta"""
    with cuentas_lock:
        try:
            with open('cuentas.json', 'r') as f:
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
            
        tipo_cuenta = obtener_tipo_cuenta(datos_cliente.get('id_cuenta'))
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
        
        # Actualizar estado
        proceso.estado = "Finalizado"
        guardar_en_pcb(proceso)
        print(f"[Proceso {proceso.pid}] {operacion} completada exitosamente")
        
    except Exception as e:
        print(f"[Error] En operacion {operacion}: {str(e)}")

def monitor_procesos():
    """Muestra el estado actual de los procesos"""
    try:
        with pcb_lock:
            inicializar_archivo('pcb.json')
            with open('pcb.json', 'r') as f:
                procesos = json.load(f)
        
        print("\n=== MONITOR DE PROCESOS ===")
        print(f"Procesos totales: {len(procesos)}")
        print("Últimos 5 procesos:")
        for p in procesos[-5:]:
            print(f"PID: {p['PID']} | Estado: {p['Estado']} | Operación: {p['Operacion']}")
    except Exception as e:
        print(f"Error en monitor: {str(e)}")


def obtener_tipo_cuenta(id_cuenta):
    """Obtiene el tipo de cuenta desde cuentas.json usando id_cuenta"""
    with cuentas_lock:
        try:
            inicializar_archivo('cuentas.json')
            with open('cuentas.json', 'r') as f:
                cuentas = json.load(f)
            for cuenta in cuentas:
                if cuenta.get('id_cuenta') == id_cuenta:
                    return cuenta.get('tipo_cuenta', 'Estándar')
            return 'Estándar'
        except Exception as e:
            print(f"Error obteniendo tipo de cuenta: {str(e)}")
            return 'Estándar'

if __name__ == "__main__":

    operaciones = ["Deposito", "Retiro", "Transferencia", "Consulta de saldo"]
    # Inicialización de archivos
    for f in ['pcb.json', 'clientes.json', 'cuentas.json']:
        inicializar_archivo(f)
    
    # Datos de prueba (ahora necesitamos id_cuenta en clientes.json)
    solicitudes = [
        ("Cliente", 1, "Retiro"),      # ID 1 debe existir en clientes.json con id_cuenta
        ("Cliente", 2, "Deposito"),
        ("Cliente", 3, "Consulta de saldo"),
        ("Visitante", None, "Creacion de cuenta"),
        ("Visitante", None, "Consulta de servicios")
    ]
    
    # Lanzamiento de procesos
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