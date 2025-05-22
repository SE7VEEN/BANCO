import time
import json, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from general.utils.utils import CUENTAS_PATH

""" 
    La función definida transferencia, realiza la simulación de pasar fondos entre clientes existente que tienen 
    cuentas bancarias asociadas, para realizar esta operación el cliente que desea pasar sus fondos a otra cuenta,
    debe de contar con el identificador de la cuenta destino y proporcinoar la cantidad a transferir
"""

def operacion_transferencia(proceso, id_cuenta_destino, monto, cuentas_lock):
    pid = str(proceso.pid)
    id_cuenta_origen = proceso.id_cuenta

    try:
        if monto <= 0:
            actualizar_estado_pcb(proceso, estado="Fallido", operacion="Monto inválido")
            return False

        # Hacemos uso de cuentas -> lock() para garantizar la protección de la simulación de la base de datos
        with cuentas_lock:
            actualizar_estado_pcb(pid,
                estado="En ejecución",
                operacion="Procesando transferencia"
            )

            # accedemos a las cuentas para encontrar las cuentas origen y destino para realizar la operación
            with open(CUENTAS_PATH, 'r+') as f:
                cuentas = json.load(f)
                
                cuenta_origen = next((c for c in cuentas if c["id_cuenta"] == id_cuenta_origen), None)
                cuenta_destino = next((c for c in cuentas if c["id_cuenta"] == id_cuenta_destino), None)

                # Primero confirmamos si ambos se encuentran
                if not cuenta_origen:
                    actualizar_estado_pcb(pid, estado="Fallido", operacion="Cuenta origen no encontrada")
                    return False

                if not cuenta_destino:
                    actualizar_estado_pcb(pid, estado="Fallido", operacion="Cuenta destino no encontrada")
                    return False

                # Luego verificamos si alguna de las dos esta inactiva
                if cuenta_origen.get("estado_cuenta") != "activa":
                    actualizar_estado_pcb(pid, estado="Fallido", operacion=f"Cuenta origen inactiva ({id_cuenta_origen})")
                    return False

                if cuenta_destino.get("estado_cuenta") != "activa":
                    actualizar_estado_pcb(pid, estado="Fallido", operacion=f"Cuenta destino inactiva ({id_cuenta_destino})")
                    return False

                saldo_origen = cuenta_origen.get("saldo", 0)
                if saldo_origen < monto:
                    actualizar_estado_pcb(pid, estado="Fallido", operacion="Fondos insuficientes en cuenta origen")
                    return False
                
                time.sleep(2)

                # Realizamos la transferencia 
                cuenta_origen["saldo"] = round(saldo_origen - monto, 2)
                cuenta_destino["saldo"] = round(cuenta_destino.get("saldo", 0) + monto, 2)

                f.seek(0)
                f.truncate()
                json.dump(cuentas, f, indent=4)

        # Proceos finalizado, la transferencia se acompleto
        actualizar_estado_pcb(pid,
            estado="Finalizado",
            operacion=f"Transferencia completada (${monto:.2f} a {id_cuenta_destino})",
        )
        return True

    except Exception as e:
        actualizar_estado_pcb(pid, estado="Error", operacion=f"Error en transferencia: {str(e)}")
        return False

