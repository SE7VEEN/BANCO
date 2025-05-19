import os
import json
import sys

from .clientes import Client


def gestionar_clientes(accion, cliente=None, id_usuario=None, nuevo_data=None):
    archivo = 'clientes.json'
    
    try:
        if os.path.exists(archivo):
            with open(archivo, 'r') as f:
                clientes = json.load(f)
        else:
            clientes = []

        clientes_dict = {c['id_usuario']: c for c in clientes}

        if accion == 'agregar':
            if cliente.id_usuario in clientes_dict:
                print(f"Error: El ID de usuario {cliente.id_usuario} ya existe.")
                return False
            clientes_dict[cliente.id_usuario] = cliente.to_dict()
            print(f"Cliente {cliente.nombre} agregado correctamente.")

        elif accion == 'eliminar':
            if id_usuario not in clientes_dict:
                print(f"Error: El ID de usuario {id_usuario} no existe.")
                return False
            del clientes_dict[id_usuario]
            print(f"Cliente con ID {id_usuario} eliminado correctamente.")

        elif accion == 'modificar':
            if id_usuario not in clientes_dict:
                print(f"Error: El ID de usuario {id_usuario} no existe.")
                return False
            for key, value in nuevo_data.items():
                if key in clientes_dict[id_usuario]:
                    clientes_dict[id_usuario][key] = value
            print(f"Cliente con ID {id_usuario} modificado correctamente.")

        elif accion == 'generar':
            cantidad = nuevo_data.get('cantidad', 1)
            for _ in range(cantidad):
                cliente = Client()
                clientes_dict[cliente.id_usuario] = cliente.to_dict()
                print(f"Cliente {cliente.nombre} generado con ID {cliente.id_usuario}")

        else:
            print("Error: Acción no válida.")
            return False

        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(list(clientes_dict.values()), f, indent=4, ensure_ascii=False)

        return True

    except Exception as e:
        print(f"Error al gestionar clientes: {str(e)}")
        return False
