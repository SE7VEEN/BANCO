import time
import json, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from general.utils.utils import CUENTAS_PATH

""" 
    La función definida operacion_deposito, realiza un retiro para un cliente registrado que tiene con cuenta bancaria
    este puede realizar un retiro a su cuenta existente siempre que cuente con los fondos suficientes
"""

def operacion_retiroPersonal(proceso, monto, cuentas_lock):
    pid = str(proceso.pid)
    id_cuenta = proceso.id_cuenta

    try:
        # No se pueden retirar cantidad menor a 0
        if monto <= 0:
            actualizar_estado_pcb(pid, estado="Fallido", operacion="Monto inválido")
            return False

        # Hacemos uso de cuentas -> lock() para garantizar la protección de la simulación de la base de datos
        with cuentas_lock:
            # Proceso en ejecución
            actualizar_estado_pcb(pid,
                estado="En ejecución",
                operacion="Procesando retiro"
            )

            # Accedemos a las cuentas, para encontrar la cuenta del cliente y acceder a sus fondos
            with open(CUENTAS_PATH, 'r+') as f:
                cuentas = json.load(f)
                cuenta = next((c for c in cuentas if c["id_cuenta"] == id_cuenta), None)

                # Cuenta no encontrada
                if not cuenta:
                    actualizar_estado_pcb(pid, estado="Fallido", operacion="Cuenta no encontrada")
                    return False

                # Su cuenta esta inactiva
                if cuenta.get("estado_cuenta") != "activa":
                    actualizar_estado_pcb(pid, estado="Fallido", operacion=f"Cuenta inactiva ({id_cuenta})")
                    return False

                saldo_actual = cuenta.get("saldo", 0)
                if saldo_actual < monto:
                    actualizar_estado_pcb(pid, estado="Fallido", operacion="Fondos insuficientes")
                    return False

                time.sleep(1)
                cuenta["saldo"] = round(saldo_actual - monto, 2)
                f.seek(0)
                f.truncate()
                json.dump(cuentas, f, indent=4)

        # 6. Proceso finalizado: Retiro acompletado
        actualizar_estado_pcb(pid,
            estado="Finalizado",
            operacion=f"Retiro completado (-${monto:.2f})",
        )
        return True

    except Exception as e:
        actualizar_estado_pcb(pid, estado="Error", operacion=f"Error en retiro: {str(e)}")
        return False
