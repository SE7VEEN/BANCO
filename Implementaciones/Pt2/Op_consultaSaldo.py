import json
import sys
import os
import time
from decimal import Decimal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from general.utils.utils import CUENTAS_PATH

def operacion_consulta_saldo(proceso, cuentas_lock):
    
    pid = str(proceso.pid)
    id_cuenta = str(proceso.id_cuenta)
    
    try:
        # Estado: Procesando consulta
        actualizar_estado_pcb(pid,
            estado="En ejecución",
            operacion=f"Consultando saldo cuenta {id_cuenta}"
        )

        with cuentas_lock:
            with open(CUENTAS_PATH, 'r') as f:
                cuentas = json.load(f)
                cuenta = next((c for c in cuentas if c.get("id_cuenta") == id_cuenta), None)
                
                if cuenta:
                    time.sleep(1)
                    saldo = float(cuenta.get("saldo", 0))
                    
                    # Estado: Consulta exitosa
                    actualizar_estado_pcb(pid,
                        estado="Finalizado",
                        operacion=f"Saldo consultado: ${saldo:.2f}"
                    )

        # Estado: Cuenta no encontrada
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