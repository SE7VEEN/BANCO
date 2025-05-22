import json
import os
from general.utils.utils import CLIENTES_PATH, CUENTAS_PATH



""" 
    La función definida operacion_baja_cuenta, realiza la simulación dar de baja una cuenta en forma
    temporal o definitiva que es pedida por un cliente registrado (creado) el cual tiene una cuenta asociada,
    en la simulación de la base de datos (cuentas.json), para ello accedemos a sus datos para seguidamente 
    borrarlos y actualizar nuestra simulación de base de datos
"""

def operacion_baja_cuenta(proceso, tipo_baja="temporal"):
    id_usuario = proceso.id_usuario

    try:
        # accedemos a los datos de (cuentas.json)
        with open(CUENTAS_PATH, 'r', encoding='utf-8') as f:
            cuentas = json.load(f)

        # Buscar cuenta del usuario
        cuenta_usuario = next((c for c in cuentas if c['id_usuario'] == id_usuario), None)
        if not cuenta_usuario:
            raise ValueError(f"No se encontró cuenta para el usuario con ID {id_usuario}")

    	# Realizamos la baja de cuenta (temporal o definitiva)
        if tipo_baja == "temporal":
            cuenta_usuario['estado_cuenta'] = "temporal"
            mensaje = "Baja temporal realizada correctamente."
        elif tipo_baja == "definitiva":
            cuentas = [c for c in cuentas if c['id_usuario'] != id_usuario]
            mensaje = f"Cuenta eliminada para usuario {id_usuario}."
        else:
            raise ValueError("Tipo de baja no válido. Use 'temporal' o 'definitiva'.")

        # Actualizamos la simualación de base de datos
        with open(CUENTAS_PATH, 'w', encoding='utf-8') as f:
            json.dump(cuentas, f, indent=4, ensure_ascii=False)

        # En caso de ser definitiva, definitivamente eliminamos al cliente
        if tipo_baja == "definitiva":
            with open(CLIENTES_PATH, 'r', encoding='utf-8') as f:
                clientes = json.load(f)
            clientes = [c for c in clientes if c['id_usuario'] != id_usuario]
            with open(CLIENTES_PATH, 'w', encoding='utf-8') as f:
                json.dump(clientes, f, indent=4, ensure_ascii=False)

        # La cuenta ha sido dada de baja con exito, proceso terminado
        from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
        actualizar_estado_pcb(proceso.pid, estado="Finalizado", operacion=mensaje)

    except Exception as e:
        from Implementaciones.Pt2.actualizar import actualizar_estado_pcb
        actualizar_estado_pcb(proceso.pid, estado="Error", operacion=f"Error en Baja de Cuenta: {str(e)}")
