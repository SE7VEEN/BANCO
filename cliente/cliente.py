import json
import os
import random
import unicodedata
from faker import Faker  # Librería para generar datos ficticios

def quitar_acentos(texto):
    """Elimina acentos y caracteres especiales de un texto"""
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(c)
    )
    
def formatear_telefono(numero):
    """Convierte un número a formato 3-3-4 si tiene al menos 10 dígitos"""
    digitos = ''.join(filter(str.isdigit, numero))
    if len(digitos) >= 10:
        return f"{digitos[-10:-7]}-{digitos[-7:-4]}-{digitos[-4:]}"
    else:
        return numero  # Si tiene menos de 10 dígitos, se deja como está

        

class Client:
    def __init__(self, id_usuario=None, nombre=None, contrasena=None, num_telefono=None, direccion=None):
        """
        Inicializa un cliente con datos aleatorios si no se proporcionan valores
        """
        fake = Faker('es_MX')  # Configuración para datos en español
        
        self.id_usuario = id_usuario or self._generar_id_unico()
        self.nombre = nombre or quitar_acentos(fake.name())
        self.contrasena = contrasena or self._generar_contrasena()
        self.num_telefono = num_telefono or formatear_telefono(fake.phone_number())
        self.direccion = direccion or quitar_acentos(fake.address().replace('\n', ', '))

    def _generar_id_unico(self):
        """Genera un ID de usuario único numérico"""
        existentes = set()
        if os.path.exists('clientes.json'):
            with open('clientes.json', 'r') as f:
                clientes = json.load(f)
                existentes = {c['id_usuario'] for c in clientes}
        
        while True:
            nuevo_id = random.randint(1000, 9999)
            if nuevo_id not in existentes:
                return nuevo_id
            
  

    def _generar_contrasena(self):
        """Genera una contraseña aleatoria segura"""
        caracteres = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!^*'
        return ''.join(random.choice(caracteres) for _ in range(12))


    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'contrasena': self.contrasena,
            'num_telefono': self.num_telefono,
            'direccion': self.direccion
        }

def gestionar_clientes(accion, cliente=None, id_usuario=None, nuevo_data=None):
    """
    Gestiona clientes en un archivo JSON
    
    Parámetros:
    - accion: 'agregar', 'eliminar', 'modificar' o 'generar'
    - cliente: Objeto Client (necesario para agregar)
    - id_usuario: ID del usuario a eliminar o modificar
    - nuevo_data: Diccionario con nuevos datos (necesario para modificar)
    
    Retorna:
    - True si la operación fue exitosa, False en caso contrario
    """
    
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
            print("Error: Acción no válida. Use 'agregar', 'eliminar', 'modificar' o 'generar'.")
            return False
            
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(list(clientes_dict.values()), f, indent=4, ensure_ascii=False)
            
        return True
        
    except Exception as e:
        print(f"Error al gestionar clientes: {str(e)}")
        return False

if __name__ == "__main__":
    cliente_aleatorio = Client()
    gestionar_clientes('agregar', cliente=cliente_aleatorio)
    gestionar_clientes('eliminar', id_usuario=9819)
  
    gestionar_clientes('generar', nuevo_data={'cantidad': 5})
