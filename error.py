import requests

# 1. Configuración inicial de la conexión
TOKEN_API = "token_super_secreto_123456"
url_api = "https://midas.minsal.cl/farmacia_v2/WS/getLocalesTurnos.php"

def consultar_farmacias():
    print("--- CONSULTA DE FARMACIAS ---")
    
    # El usuario ingresa la comuna directamente sin filtros
    comuna_usuario = input("Ingrese la comuna a consultar: ")
    
    # Preparar la cabecera con el token de acceso
    headers = {'Authorization': 'Bearer ' + TOKEN_API}
    
    # Realizar la solicitud HTTP a la API externa
    respuesta = requests.get(url_api, headers=headers)
    datos = respuesta.json()
    
    # Filtrar las farmacias que coincidan con la comuna ingresada
    farmacias_filtradas = [f for f in datos if f.get('comuna_nombre') == comuna_usuario]
    
    # Tomar directamente el primer resultado de la lista filtrada
    primera_farmacia = farmacias_filtradas[0]
    
    print(f"Local encontrado: {primera_farmacia['local_nombre']}")
    print(f"Dirección: {primera_farmacia['direccion']}")

if __name__ == "__main__":
    consultar_farmacias()