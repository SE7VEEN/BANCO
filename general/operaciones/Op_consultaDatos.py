import json
import sys
import os
import time
from decimal import Decimal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from general.utils.utils import CLIENTES_PATH, CUENTAS_PATH


""" 
    La función definida operacion_consulta_datos, realiza una consulta de la información asociada al cliente,
    esto incluye sus datos personales y datos bancariso como sus cuentas posteriormente son retornados para su visualización  
"""

def operacion_consulta_datos(proceso, cuentas_lock):
    pid = str(proceso.pid)
    id_cuenta = str(proceso.id_cuenta)
    id_usuario = str(proceso.id_usuario)

    try:

        # Proceso en ejecución
        actualizar_estado_pcb(pid,
            estado="En ejecución",
            operacion=f"Consultando datos cuenta {id_cuenta}"
        )

        # Hacemos uso de cuentas -> lock() para garantizar la protección de la base de datos
        with cuentas_lock:
            # Primero buscar el cliente por id_usuario, para acceder a su nombre y telefono
            with open(CLIENTES_PATH, 'r') as f:
                clientes = json.load(f)
                cliente = next((c for c in clientes if str(c.get("id_usuario")) == id_usuario), None)
                if not cliente:
                    raise ValueError(f"No se encontró cliente con id_usuario {id_usuario}")
                id_nombre = str(cliente.get("nombre"))
                telefono = str(cliente.get("num_telefono"))

            # Luego buscar la cuenta por id_cuenta
            with open(CUENTAS_PATH, 'r') as f:
                cuentas = json.load(f)
                cuenta = next((c for c in cuentas if str(c.get("id_cuenta")) == id_cuenta), None)
                if not cuenta:
                    raise ValueError(f"No se encontró cuenta con id_cuenta {id_cuenta}")
                
                saldo = float(cuenta.get("saldo", 0))
                # Proceso en ejecución: mostramos los datos del cliente 
                actualizar_estado_pcb(pid,
                    estado="En ejecución",
                    operacion=f"Usuario: {id_nombre}\nID_usuario: {id_usuario}\nTelefono: {telefono}\nCuenta: {id_cuenta}\nSaldo: {saldo}"
                )
                time.sleep(5)

                # Consulta con éxito: proceso terminado
                actualizar_estado_pcb(pid,
                    estado="Finalizado",
                    operacion=f"Datos consultados (Usuario: {id_usuario})"
                )
                return id_usuario

    except Exception as e:
        import traceback
        actualizar_estado_pcb(pid,
            estado="Error",
            operacion=f"Error consultando datos: {str(e)}\n{traceback.format_exc()}"
        )
        return None