#from models import Proceso
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from servidor.hilos.clase_procesos import Proceso
from general.utils.utils import guardar_en_pcb, obtener_datos_cliente


def crear_proceso(tipo_usuario, id_usuario=None, operacion=None):
    if tipo_usuario == "Cliente":
        if not id_usuario:
            raise ValueError("Se requiere ID de usuario para clientes")
        datos_cliente = obtener_datos_cliente(id_usuario)
        if not datos_cliente:
            raise ValueError("Cliente no registrado")
        tipo_cuenta = datos_cliente.get('tipo_cuenta', 'Estándar')
        id_cuenta = datos_cliente.get('id_cuenta')
    else:
        if id_usuario is not None:
            raise ValueError("Visitante no debe tener ID")
        tipo_cuenta = None
        id_cuenta = None

    proceso = Proceso(
        tipo_usuario=tipo_usuario,
        id_usuario=id_usuario,
        id_cuenta=id_cuenta,
        tipo_cuenta=tipo_cuenta,
        operacion=operacion
    )

    guardar_en_pcb(proceso)
    return proceso

def terminar_proceso(proceso):
    proceso.estado = "Finalizado"
    guardar_en_pcb(proceso)

def ejecutar_operacion(tipo_usuario, id_usuario=None, operacion=None):
    try:
        proceso = crear_proceso(tipo_usuario, id_usuario, operacion)
        print(f"[Proceso {proceso.pid}] Iniciando {operacion}...")

        # Simulación de tiempo de procesamiento
        time.sleep(2 if "Consulta" in operacion else 3)

        terminar_proceso(proceso)
        print(f"[Proceso {proceso.pid}] {operacion} completada exitosamente")
        
    except Exception as e:
        print(f"[Error] Operación fallida: {str(e)}")
