# retiro.py

import time
import json, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from general.utils.utils import CUENTAS_PATH

def operacion_retiroPersonal(proceso, monto, cuentas_lock):
    pid = str(proceso.pid)
    id_cuenta = proceso.id_cuenta

    try:
        if monto <= 0:
            actualizar_estado_pcb(pid, estado="Fallido", operacion="Monto inválido")
            return False


        with cuentas_lock:
            # 2. Estado: Lock adquirido
            actualizar_estado_pcb(pid,
                estado="En ejecución",
                operacion="Procesando retiro"
            )

            # 3. Cargar cuentas
            with open(CUENTAS_PATH, 'r+') as f:
                cuentas = json.load(f)
                cuenta = next((c for c in cuentas if c["id_cuenta"] == id_cuenta), None)

                if not cuenta:
                    actualizar_estado_pcb(pid, estado="Fallido", operacion="Cuenta no encontrada")
                    return False

                if cuenta.get("estado_cuenta") != "activa":
                    actualizar_estado_pcb(pid, estado="Fallido", operacion=f"Cuenta inactiva ({id_cuenta})")
                    return False

                saldo_actual = cuenta.get("saldo", 0)
                if saldo_actual < monto:
                    actualizar_estado_pcb(pid, estado="Fallido", operacion="Fondos insuficientes")
                    return False

                # 4. Simular procesamiento
                time.sleep(1)
                cuenta["saldo"] = round(saldo_actual - monto, 2)

                # 5. Guardar cambios
                f.seek(0)
                f.truncate()
                json.dump(cuentas, f, indent=4)

        # 6. Estado: Finalizado
        actualizar_estado_pcb(pid,
            estado="Finalizado",
            operacion=f"Retiro completado (-${monto:.2f})",
        )
        return True

    except Exception as e:
        actualizar_estado_pcb(pid, estado="Error", operacion=f"Error en retiro: {str(e)}")
        return False
