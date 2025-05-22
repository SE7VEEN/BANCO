import time
import json, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from cliente.clientes.gestor import gestionar_clientes  
from cliente.cuentas.gestion_cuenta import crear_cuentas_automaticamente_por_clientes
from general.utils.utils import CUENTAS_PATH


""" 
    La función definida agregarCliente, simula la cración de un nuevo cliente
    que tiene sus datos personales definidos en la clase cliente.py, posteriormente 
    es guardado en la simulación de base datos (cliente.json), 
"""
def agregarCliente(proceso, cuentas_lock):
    tipo_usuario = str(proceso.tipo_usuario)
    pid = str(proceso.pid)
    try:
        if tipo_usuario == "Cliente":
            actualizar_estado_pcb(pid, estado="Fallido", operacion="No se pudo agregar el Cliente, ya tiene cuenta")
            return False

        # Hacemos uso de cuentas -> lock() para garantizar la protección de la base de datos
        with cuentas_lock:
            # Proceso en ejecución
            actualizar_estado_pcb(pid,
                estado="En ejecución",
                operacion="Procesando solicitud"
            )

        # Proceso en ejecución
        actualizar_estado_pcb(pid,
                estado="En ejecución",
                operacion="Procesando solicitud"
            )

        # Cramos un nuevo cliente con el gestor de clientes
        gestionar_clientes('generar', nuevo_data={'cantidad': 1}) #cliente nuevo
        crear_cuentas_automaticamente_por_clientes() # Como hay un nuevo cliente, le asignamos sus cuentas bancarias
        time.sleep(2)

        # Cliente creado con exito, proceso terminado
        actualizar_estado_pcb(pid,
            estado="Finalizado",
            operacion=f"Usuario registrado: Es un placer tenerlo con nosotros",
        )
        return True

    except Exception as e:
        actualizar_estado_pcb(pid, estado="Error", operacion=f"Error en cracion: {str(e)}")
        return False
