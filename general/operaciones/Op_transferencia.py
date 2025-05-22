# transferencia.py

import time
import json, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from general.utils.utils import CUENTAS_PATH

def operacion_transferencia(proceso, id_cuenta_destino, monto, cuentas_lock):
    pid = str(proceso.pid)
    id_cuenta_origen = proceso.id_cuenta

    try:
        if monto <= 0:
            actualizar_estado_pcb(proceso, estado="Fallido", operacion="Monto inválido")
            return False

        with cuentas_lock:
            # 2. Estado: Lock adquirido
            actualizar_estado_pcb(pid,
                estado="En ejecución",
                operacion="Procesando transferencia"
            )

            # 3. Cargar cuentas
            with open(CUENTAS_PATH, 'r+') as f:
                cuentas = json.load(f)
                
                cuenta_origen = next((c for c in cuentas if c["id_cuenta"] == id_cuenta_origen), None)
                cuenta_destino = next((c for c in cuentas if c["id_cuenta"] == id_cuenta_destino), None)

                if not cuenta_origen:
                    actualizar_estado_pcb(pid, estado="Fallido", operacion="Cuenta origen no encontrada")
                    return False

                if not cuenta_destino:
                    actualizar_estado_pcb(pid, estado="Fallido", operacion="Cuenta destino no encontrada")
                    return False

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

                # 4. Simular procesamiento
                time.sleep(2)

                cuenta_origen["saldo"] = round(saldo_origen - monto, 2)
                cuenta_destino["saldo"] = round(cuenta_destino.get("saldo", 0) + monto, 2)

                # 5. Guardar cambios
                f.seek(0)
                f.truncate()
                json.dump(cuentas, f, indent=4)

        # 6. Estado: Finalizado
        actualizar_estado_pcb(pid,
            estado="Finalizado",
            operacion=f"Transferencia completada (${monto:.2f} a {id_cuenta_destino})",
        )
        return True

    except Exception as e:
        actualizar_estado_pcb(pid, estado="Error", operacion=f"Error en transferencia: {str(e)}")
        return False

