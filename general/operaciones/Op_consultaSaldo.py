import json
import sys
import os
import time
from decimal import Decimal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from general.utils.utils import CUENTAS_PATH

""" 
    La función definida operacion_consulta_saldo, realiza la consulta del saldo de un cliente
    para ello accedemos a sus datos bancarios para que seguidamente retornemos para su visualización 
"""

def operacion_consulta_saldo(proceso, cuentas_lock):
    
    pid = str(proceso.pid)
    id_cuenta = str(proceso.id_cuenta)
    
    try:
        # Proceso en ejecución
        actualizar_estado_pcb(pid,
            estado="En ejecución",
            operacion=f"Consultando saldo cuenta {id_cuenta}"
        )

        # Hacemos uso de cuentas -> lock() para garantizar la protección de la base de datos
        with cuentas_lock:
            with open(CUENTAS_PATH, 'r') as f:
                cuentas = json.load(f)
                cuenta = next((c for c in cuentas if c.get("id_cuenta") == id_cuenta), None)
                
                if cuenta:
                    time.sleep(1)
                    saldo = float(cuenta.get("saldo", 0))
                    
                    # Proceso terminado: consulta exitosa
                    actualizar_estado_pcb(pid,
                        estado="Finalizado",
                        operacion=f"Saldo consultado: ${saldo:.2f}"
                    )
                return saldo

        # Proceso fallido
        actualizar_estado_pcb(pid,
            estado="Fallido",
            operacion=f"Cuenta {id_cuenta} no encontrada"
        )
        return None

    except Exception as e:
        actualizar_estado_pcb(pid,
            estado="Error",
            operacion=f"Error consultando saldo: {str(e)}"
        )
        return None