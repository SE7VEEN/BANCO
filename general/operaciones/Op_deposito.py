# transferencia.py

import time
import json, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from general.utils.utils import CUENTAS_PATH

""" 
    La función definida operacion_deposito, realiza un deposito para un visitante que no cuenta con una cuenta,
    este puede realizar un deposito a alguna cuenta existente en la simulación de la base de datos, para ello
    el visitante debe de contar con el identificador de la cuenta destino, se le confirma si el destinatario ha recibido
    el deposito a su cuenta
"""
def operacion_deposito(proceso, id_cuenta_destino, monto, cuentas_lock):
    pid = str(proceso.pid)

    try:
        # El deposito es menor 0, entonces no puede realizar la operación
        if monto <= 0:
            actualizar_estado_pcb(pid, estado="Fallido", operacion="Monto inválido")
            return False

        # Hacemos uso de cuentas -> lock() para garantizar la protección de la base de datos
        with cuentas_lock:
            # Proceso en ejecución
            actualizar_estado_pcb(pid,
                estado="En ejecución",
                operacion="Procesando deposito"
            )

            # Accdemos a las cuentas para busca la cuenta de destino
            with open(CUENTAS_PATH, 'r+') as f:
                cuentas = json.load(f)
                
                cuenta_destino = next((c for c in cuentas if c["id_cuenta"] == id_cuenta_destino), None)

                # Cuenta no encontrada
                if not cuenta_destino:
                    actualizar_estado_pcb(pid, estado="Fallido", operacion="Cuenta de destino no encontrada")
                    return False

                # La cuenta proporcionada se encuentra de baja 
                if cuenta_destino.get("estado_cuenta") != "activa":
                    actualizar_estado_pcb(pid, estado="Fallido", operacion="Cuenta de destino inactiva")
                    return False

                # rectificamos el monto 
                if monto <= 0:
                    actualizar_estado_pcb(pid, estado="Fallido", operacion=f"Error en deposito")
                    return False

                time.sleep(1)
                cuenta_destino["saldo"] = round(cuenta_destino.get("saldo", 0) + monto, 2)
                f.seek(0)
                f.truncate()
                json.dump(cuentas, f, indent=4)

        # 6. Proceso finalizado, deposito realizado
        actualizar_estado_pcb(pid,
            estado="Finalizado",
            operacion=f"Deposito completado (${monto:.2f} a {id_cuenta_destino})",
        )
        return True

    except Exception as e:
        actualizar_estado_pcb(pid, estado="Error", operacion=f"Error en deposito: {str(e)}")
        return False
