import os
import csv
import hashlib
from datetime import datetime
import requests

class Autenticacion:
    def __init__(self):
        # Simulación de credenciales (Contraseña real: "EcoTech2026*")
        self.usuario_valido = "admin_ecotech"
        self.password_hash_almacenada = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

    def cifrar_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validar_login(self):
        print("=== ACCESO AL SISTEMA ECOTECH SOLUTIONS ===")
        usuario = input("Ingrese usuario: ").strip()
        password = input("Ingrese contraseña: ").strip()
        
        if usuario == self.usuario_valido and self.cifrar_password(password) == self.password_hash_almacenada:
            print("¡Acceso concedido con éxito!\n")
            return True
        else:
            print("Acceso denegado: Credenciales incorrectas.")
            return False


class EcoTechLogistica:
    def __init__(self, archivo_csv="seguimiento_envios.csv"):
        self.url_api = "https://midas.minsal.cl/farmacia_v2/WS/getLocalesTurnos.php"
        self.csv_file = archivo_csv

    def validar_codigo_envio(self, codigo):
        return codigo.startswith('TS-') and codigo[3:].isdigit()

    def obtener_direccion(self, farmacia):
        for k in ('direccion', 'local_direccion', 'local_dir', 'direccion_local', 'local_direccion_1'):
            v = farmacia.get(k)
            if v:
                return v
        return farmacia.get('direccion', '') or ''

    def consultar_y_guardar(self):
        entrada = input('Ingrese código de envío (formato TS-NNNNN): ').strip()
        
        if not self.validar_codigo_envio(entrada):
            print('Código inválido. Use el formato TS- seguido de números.')
            return

        codigo = entrada
        comuna_destino = input('Ingrese comuna de destino del envío: ').strip().upper()
        
        token = os.environ.get('TOKEN_LOGISTICA')
        headers = {'Authorization': f'Bearer {token}'} if token else {}

        try:
            print("Consultando servicio externo...")
            respuesta = requests.get(self.url_api, headers=headers, timeout=5)
            respuesta.raise_for_status()
            datos = respuesta.json()
            
            farmacias_comuna = [f for f in datos if f.get('comuna_nombre') == comuna_destino]
            cantidad = len(farmacias_comuna)

            if cantidad:
                print(f'Envío {codigo}: se encontraron {cantidad} resultados en {comuna_destino}.')
            else:
                print(f'No se encontraron registros en {comuna_destino}.')
                return

            is_new = not os.path.exists(self.csv_file)

            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if is_new:
                    writer.writerow(['timestamp', 'codigo_envio', 'comuna', 'local_nombre', 'direccion'])
                
                for farmacia in farmacias_comuna:
                    nombre = farmacia.get('local_nombre', '')
                    direccion = self.obtener_direccion(farmacia)
                    print(f'Envío {codigo} -> {nombre} | Dirección: {direccion}')
                    writer.writerow([datetime.now().isoformat(), codigo, comuna_destino, nombre, direccion])

            print(f'Registro guardado exitosamente en {self.csv_file}.')

        except requests.exceptions.RequestException as e:
            print(f'No fue posible completar la consulta al servicio externo: {e}')


if __name__ == '__main__':
    # Paso 1: Autenticación de seguridad
    auth = Autenticacion()
    if auth.validar_login():
        # Paso 2: Ejecución de la lógica de negocio si el login es correcto
        sistema = EcoTechLogistica()
        sistema.consultar_y_guardar()