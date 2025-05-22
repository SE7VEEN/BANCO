# transferencia.py

import time
import json, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from cliente.cuentas.gestion_cuenta import agregar_tarjeta_a_cuenta
from general.utils.utils import CUENTAS_PATH

def agregarTarjeta(proceso, cuentas_lock):
    id_cuenta = str(proceso.id_cuenta)
    pid = str(proceso.pid)
    try:
        if id_cuenta == "Visitante":
            actualizar_estado_pcb(pid, estado="Fallido", operacion="No se pudo agregar la nueva tarjeta")
            return False

        with cuentas_lock:
            # 2. Estado: Lock adquirido
            actualizar_estado_pcb(pid,
                estado="En ejecución",
                operacion="Procesando solicitud"
            )

        agregar_tarjeta_a_cuenta(id_cuenta)

            
        # f.seek(0)
        # f.truncate()
        # json.dump(cuentas, f, indent=4)

        # 4. Estado: Finalizado
        actualizar_estado_pcb(pid,
            estado="Finalizado",
            operacion=f"El usuario cuenta con una tarjeta nueva (cuenta: {id_cuenta})",
        )
        return True

    except Exception as e:
        actualizar_estado_pcb(pid, estado="Error", operacion=f"Error en cracion: {str(e)}")
        return False
