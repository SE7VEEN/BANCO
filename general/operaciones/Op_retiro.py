import time
import json, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from general.utils.utils import CUENTAS_PATH

""" 
    La función definida operacion_deposito, realiza un retiro para un visitante que no tiene con una cuenta bancaria asociada,
    este puede realizar un retiro a alguna cuenta existente en la simulación de la base de datos, para ello
    el visitante debe de contar con el identificador de la cuenta destino, se le confirma al visitante de su retiro
    a la cuenta destino
"""

def operacion_retiro(proceso, id_cuenta_destino, monto, cuentas_lock):
    pid = str(proceso.pid)

    try:
        # Monto mayor a cero para realizar el retiro
        if monto <= 0:
            actualizar_estado_pcb(pid, estado="Fallido", operacion="Monto inválido")
            return False

        # Hacemos uso de cuentas -> lock() para garantizar la protección de la simulación de la base de datos
        with cuentas_lock:
            # Proceso en Ejecución
            actualizar_estado_pcb(pid,
                estado="En ejecución",
                operacion="Procesando retiro"
            )

            # Accedemos a las cuentas, buscamos la cuenta destino y accedemos a sus fondos 
            with open(CUENTAS_PATH, 'r+') as f:
                cuentas = json.load(f)
                
                cuenta_destino = next((c for c in cuentas if c["id_cuenta"] == id_cuenta_destino), None)

                if not cuenta_destino:
                    actualizar_estado_pcb(pid, estado="Fallido", operacion="Cuenta de destino no encontrada")
                    return False

                if cuenta_destino.get("estado_cuenta") != "activa":
                    actualizar_estado_pcb(pid, estado="Fallido", operacion="Cuenta de destino inactiva")
                    return False

                if monto <= 0:
                    actualizar_estado_pcb(pid, estado="Fallido", operacion=f"Error en el retiro")
                    return False

                # 4. Simular procesamiento
                time.sleep(1)

                cuenta_destino["saldo"] = round(cuenta_destino.get("saldo", 0) - monto, 2)

                # 5. Guardar cambios
                f.seek(0)
                f.truncate()
                json.dump(cuentas, f, indent=4)

        # Proceso finalizado: retiro con éxito
        actualizar_estado_pcb(pid,
            estado="Finalizado",
            operacion=f"Retiro completado (${monto:.2f} de {id_cuenta_destino})",
        )
        return True

    except Exception as e:
        actualizar_estado_pcb(pid, estado="Error", operacion=f"Error en deposito: {str(e)}")
        return False
