import os
import sys
import time

# Asegurar que el path incluya el directorio raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from servidor.hilos.clase_procesos import Proceso
from general.utils.utils import guardar_en_pcb, obtener_datos_cliente

def crear_proceso(tipo_usuario, id_usuario=None, operacion=None):
    """
    Crea y registra un proceso con los datos correspondientes.
    """
    if tipo_usuario == "Cliente":
        if not id_usuario:
            raise ValueError("Se requiere ID de usuario para clientes")

        datos_cliente = obtener_datos_cliente(id_usuario)
        if not datos_cliente:
            raise ValueError(f"Cliente con ID '{id_usuario}' no registrado")

        tipo_cuenta = datos_cliente.get('tipo_cuenta', 'Estándar')
        id_cuenta = datos_cliente.get('id_cuenta')

    elif tipo_usuario == "Visitante":
        if id_usuario is not None:
            raise ValueError("Visitante no debe tener ID de usuario")
        tipo_cuenta = None
        id_cuenta = None
    else:
        raise ValueError(f"Tipo de usuario desconocido: {tipo_usuario}")

    proceso = Proceso(
        tipo_usuario=tipo_usuario,
        id_usuario=id_usuario,
        id_cuenta=id_cuenta,
        tipo_cuenta=tipo_cuenta,
        operacion=operacion
    )

    # Guardar inmediatamente el proceso en estado "En ejecución"
    return proceso

def terminar_proceso(proceso):
    """
    Marca el proceso como finalizado y actualiza su información.
    """
    proceso.estado = "Finalizado"
    proceso.tiempo_fin = time.time()
    guardar_en_pcb(proceso.to_dict())

def ejecutar_operacion(tipo_usuario, id_usuario=None, operacion=None):
    """
    Ejecuta la operación simulando un proceso bancario.
    """
    try:
        proceso = crear_proceso(tipo_usuario, id_usuario, operacion)
        print(f"[Proceso {proceso.pid}] Iniciando operación: {operacion}")

        # Simula duración del proceso según la operación
        if "Consulta" in operacion:
            time.sleep(2)
        else:
            time.sleep(3)

        terminar_proceso(proceso)
        print(f"[Proceso {proceso.pid}] Operación '{operacion}' completada exitosamente.\n")

    except Exception as e:
        print(f"[Error] Fallo en operación '{operacion}': {str(e)}")
