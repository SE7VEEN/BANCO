# transferencia.py

import time
import json, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
from cliente.clientes.gestor import gestionar_clientes  
from cliente.cuentas.gestion_cuenta import crear_cuentas_automaticamente_por_clientes
from general.utils.utils import CUENTAS_PATH

def agregarCliente(proceso, cuentas_lock):
    tipo_usuario = str(proceso.tipo_usuario)
    pid = str(proceso.pid)
    try:
        if tipo_usuario == "Visitante":
            actualizar_estado_pcb(pid, estado="Fallido", operacion="No se pudo agregar el Cliente, ya tiene cuenta")
            return False

        with cuentas_lock:
            # 2. Estado: Lock adquirido
            actualizar_estado_pcb(pid,
                estado="En ejecución",
                operacion="Procesando solicitud"
            )


        actualizar_estado_pcb(pid,
                estado="En ejecución",
                operacion="Procesando solicitud"
            )

        gestionar_clientes('generar', nuevo_data={'cantidad': 1})
        crear_cuentas_automaticamente_por_clientes()
        time.sleep(2)

            
        # f.seek(0)
        # f.truncate()
        # json.dump(cuentas, f, indent=4)

        # 4. Estado: Finalizado
        actualizar_estado_pcb(pid,
            estado="Finalizado",
            operacion=f"Usuario registrado: Es un placer tenerlo con nosotros",
        )
        return True

    except Exception as e:
        actualizar_estado_pcb(pid, estado="Error", operacion=f"Error en cracion: {str(e)}")
        return False
