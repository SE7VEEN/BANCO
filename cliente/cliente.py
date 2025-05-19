import json
import os

class Client:
    def __init__(self, id_usuario, id_cuenta, nombre, contrasena, num_telefono, tarjetas, direccion):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.contrasena = contrasena
        self.num_telefono = num_telefono
        self.tarjetas = tarjetas
        self.direccion = direccion

    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'contrasena': self.contrasena,
            'num_telefono': self.num_telefono,
            'tarjetas': self.tarjetas,
            'direccion': self.direccion
        }

def gestionar_clientes(accion, cliente=None, id_usuario=None, nuevo_data=None):
    """
    Gestiona clientes en un archivo JSON
    
    Parámetros:
    - accion: 'agregar', 'eliminar' o 'modificar'
    - cliente: Objeto Client (necesario para agregar)
    - id_usuario: ID del usuario a eliminar o modificar
    - nuevo_data: Diccionario con nuevos datos (necesario para modificar)
    
    Retorna:
    - True si la operación fue exitosa, False en caso contrario
    """
    
    archivo = 'clientes.json'
    
    try:
        # Cargar clientes existentes
        if os.path.exists(archivo):
            with open(archivo, 'r') as f:
                clientes = json.load(f)
        else:
            clientes = []
            
        # Convertir la lista a un diccionario para fácil acceso por ID
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
                
            # Actualizar solo los campos proporcionados en nuevo_data
            for key, value in nuevo_data.items():
                if key in clientes_dict[id_usuario]:
                    clientes_dict[id_usuario][key] = value
                    
            print(f"Cliente con ID {id_usuario} modificado correctamente.")
            
        else:
            print("Error: Acción no válida. Use 'agregar', 'eliminar' o 'modificar'.")
            return False
            
        # Guardar los cambios
        with open(archivo, 'w') as f:
            json.dump(list(clientes_dict.values()), f, indent=4)
            
        return True
        
    except Exception as e:
        print(f"Error al gestionar clientes: {str(e)}")
        return False


