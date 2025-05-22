import time
import json, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from cliente.cuentas.gestion_cuenta import agregar_tarjeta_a_cuenta
from general.utils.utils import CUENTAS_PATH

""" 
    La función definida agregarTarjeta, simula la cración de un nueva tarjeta
    para un cliente que esta registrado (creado) en la simulación de la base de datos (clientes.json), 
    posteriormente es guardado en la simulación de base datos para la tarjetas (tarjetas.json), 
"""
def agregarTarjeta(proceso, cuentas_lock):
    id_cuenta = str(proceso.id_cuenta)
    pid = str(proceso.pid)
    try:
        # Nos aseguramos que solo clientes puedan crear cuentas
        if id_cuenta == "Visitante":
            actualizar_estado_pcb(pid, estado="Fallido", operacion="No se pudo agregar la nueva tarjeta")
            return False

        # Hacemos uso de cuentas -> lock() para garantizar la protección de la base de datos    
        with cuentas_lock:
            #  Proceso en ejecución
            actualizar_estado_pcb(pid,
                estado="En ejecución",
                operacion="Procesando solicitud"
            )

        # Creamos y guardamos la nueva tarjeta del cliente
        agregar_tarjeta_a_cuenta(id_cuenta)

        # Se creo y guardo correctamente la tarjeta, proceos finalizado
        actualizar_estado_pcb(pid,
            estado="Finalizado",
            operacion=f"El usuario cuenta con una tarjeta nueva (cuenta: {id_cuenta})",
        )
        return True

    except Exception as e:
        actualizar_estado_pcb(pid, estado="Error", operacion=f"Error en cracion: {str(e)}")
        return False
