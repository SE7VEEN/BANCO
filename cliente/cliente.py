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

class Client:
    def _init_(self, id_usuario=None, nombre=None, contrasena=None, num_telefono=None, 
                 tarjetas=None, direccion=None):
        """
        Inicializa un cliente con datos aleatorios si no se proporcionan valores
        """
        fake = Faker('es_MX')  # Configuración para datos en español
        
        self.id_usuario = id_usuario or self._generar_id_unico()
        self.nombre = nombre or quitar_acentos(fake.name())
        self.contrasena = contrasena or self._generar_contrasena()
        self.num_telefono = num_telefono or fake.phone_number()
        self.tarjetas = tarjetas or self._generar_tarjetas()
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
        caracteres = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
        return ''.join(random.choice(caracteres) for _ in range(12))

    def _generar_tarjetas(self):
        """Genera números de tarjetas aleatorios"""
        tipos = ['VISA', 'MC', 'AMEX']
        return [
            f"{random.choice(tipos)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            for _ in range(random.randint(1, 3))
        ]

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

if _name_ == "_main_":
    cliente_aleatorio = Client()
    gestionar_clientes('agregar', cliente=cliente_aleatorio)
    gestionar_clientes('eliminar', id_usuario=9819)
  
    gestionar_clientes('generar', nuevo_data={'cantidad': 5})