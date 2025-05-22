import time
import json, sys, os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb  # asegúrate de tener esta función
from general.utils.utils import CUENTAS_PATH

""" 
    La función definida operacion_deposito, realiza un deposito para un cliente registrado que cuenta con cuenta bancaria
    este puede realizar un deposito a su cuenta existente en la simulación de la base de datos
"""

def operacion_depositoPersonal(proceso, monto, cuentas_lock):
    pid = str(proceso.pid)
    id_cuenta = proceso.id_cuenta

    try:
        # El monto debe ser mayor a 0 para realizar el deposito
        if monto <= 0:
            actualizar_estado_pcb(pid, estado="Fallido", operacion="Monto inválido")
            return False

        # Hacemos uso de cuentas -> lock() para garantizar la protección de la base de datos
        with cuentas_lock:
            # Proceso en ejecucion
            actualizar_estado_pcb(pid,
                estado="En ejecución",
                operacion="Procesando deposito",
            )

            # Accedemos a las cuentas para realizar el deposito, buscamos la cuenta del cliente
            with open(CUENTAS_PATH, 'r+') as f:
                cuentas = json.load(f)
                cuenta = next((c for c in cuentas if c["id_cuenta"] == id_cuenta), None)

                # No se encontro la cuenta para realizar el deposito
                if not cuenta:
                    actualizar_estado_pcb(pid, estado="Fallido", operacion="Cuenta no encontrada - DP")
                    return False

                time.sleep(1)
                cuenta["saldo"] = cuenta.get("saldo", 0) + monto

                f.seek(0)
                f.truncate()
                json.dump(cuentas, f, indent=4)

        # 6. Proceso finalizado, desposito acompletado 
        actualizar_estado_pcb(pid,
            estado="Finalizado",
            operacion=f"Deposito completado (+${monto:.2f})",
        )
        return True

    except Exception as e:
        actualizar_estado_pcb(pid, estado="Error", operacion=f"Error en deposito: {str(e)}")
        return False
