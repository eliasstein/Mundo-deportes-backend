from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
import requests
import jwt
import os

# URL de las claves públicas de Firebase
jwks_url = "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com"

# Función para obtener las claves públicas
def obtener_claves_publicas():
    response = requests.get(jwks_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("No se pudieron obtener las claves públicas de Firebase.")

# Función para decodificar y verificar un idToken
def decodificar_idToken(idToken, audiencia):
    try:
        # Obtener las claves públicas de Firebase
        claves_publicas = obtener_claves_publicas()
        
        # Decodificar el token sin verificar
        encabezado = jwt.get_unverified_header(idToken)
        
        # Obtener la clave pública correspondiente

        key_id = encabezado['kid']
        certificado = claves_publicas[key_id]

        # Convertir el certificado a una clave pública
        certificado_x509 = load_pem_x509_certificate(certificado.encode(), default_backend())
        public_key = certificado_x509.public_key()

        # Decodificar y verificar el token
        decoded_token = jwt.decode(idToken, public_key, algorithms=["RS256"], audience=audiencia)
        return decoded_token
    except jwt.ExpiredSignatureError:
        print("El token ha expirado.")
    except jwt.InvalidAudienceError:
        print("El token no es válido para esta audiencia.")
    except jwt.InvalidTokenError as e:
        print(f"Token inválido: {str(e)}")


def check_valid_cookie(idToken:str):
    # Ejemplo de uso
    audiencia = os.getenv("PROJECT_ID")  #IdProyecto
    token_decodificado = decodificar_idToken(idToken, audiencia)
    if token_decodificado:
        return True
    return False