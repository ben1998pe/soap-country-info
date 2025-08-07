#!/usr/bin/env python3
"""
Script para obtener información de países usando un servicio SOAP público.
Utiliza el servicio: http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL

Autor: AI Assistant
Fecha: 2024
"""

import sys
import requests
import xml.etree.ElementTree as ET
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def crear_session():
    """
    Crea una sesión HTTP con manejo de reintentos.
    
    Returns:
        Session: Sesión HTTP configurada
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def hacer_llamada_soap(session, metodo, parametros=None):
    """
    Realiza una llamada SOAP al servicio.
    
    Args:
        session: Sesión HTTP configurada
        metodo (str): Nombre del método SOAP
        parametros (dict): Parámetros para la llamada
        
    Returns:
        dict: Respuesta parseada o None si hay error
    """
    url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso"
    
    # Construir el XML SOAP
    soap_body = f"""
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <{metodo} xmlns="http://www.oorsprong.org/websamples.countryinfo">
                {parametros or ''}
            </{metodo}>
        </soap:Body>
    </soap:Envelope>
    """
    
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': f'http://www.oorsprong.org/websamples.countryinfo/{metodo}'
    }
    
    try:
        response = session.post(url, data=soap_body, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ Error en llamada SOAP {metodo}: {e}")
        return None


def parsear_lista_paises(xml_response):
    """
    Parsea la respuesta XML de la lista de países.
    
    Args:
        xml_response (str): Respuesta XML del servicio
        
    Returns:
        list: Lista de códigos de países
    """
    try:
        root = ET.fromstring(xml_response)
        # Buscar los códigos de países en el XML
        codigos = []
        for elem in root.iter():
            if 'sISOCode' in elem.tag:
                codigos.append(elem.text)
        return sorted(codigos)
    except Exception as e:
        print(f"❌ Error al parsear lista de países: {e}")
        return []


def parsear_info_pais(xml_response):
    """
    Parsea la respuesta XML de información de país.
    
    Args:
        xml_response (str): Respuesta XML del servicio
        
    Returns:
        dict: Información del país o None si hay error
    """
    try:
        root = ET.fromstring(xml_response)
        
        # Extraer información del XML usando namespaces
        namespaces = {
            'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
            'ns': 'http://www.oorsprong.org/websamples.countryinfo'
        }
        
        # Buscar la respuesta dentro del XML SOAP
        response_elem = root.find('.//ns:FullCountryInfoResult', namespaces)
        if response_elem is None:
            # Intentar sin namespace
            response_elem = root.find('.//FullCountryInfoResult')
        
        if response_elem is None:
            print("❌ No se pudo encontrar la información del país en la respuesta XML")
            return None
        
        info = {}
        idiomas = []
        
        # Extraer campos específicos
        for elem in response_elem.iter():
            tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            
            if tag == 'sName':
                # El primer sName es el país, los siguientes son idiomas
                if 'nombre' not in info:
                    info['nombre'] = elem.text
                else:
                    # Es un idioma
                    idiomas.append(elem.text)
            elif tag == 'sCapitalCity':
                info['capital'] = elem.text
            elif tag == 'sCurrencyISOCode':
                info['moneda'] = elem.text
        
        # Verificar que tenemos la información mínima
        if 'nombre' in info:
            return {
                'nombre': info.get('nombre', 'No disponible'),
                'capital': info.get('capital', 'No disponible'),
                'moneda': info.get('moneda', 'No disponible'),
                'idiomas': ', '.join(idiomas) if idiomas else 'No disponible'
            }
        return None
        
    except Exception as e:
        print(f"❌ Error al parsear información del país: {e}")
        return None


def obtener_codigos_paises(session):
    """
    Obtiene la lista de códigos ISO de países disponibles.
    
    Args:
        session: Sesión HTTP configurada
        
    Returns:
        list: Lista de códigos de países
    """
    xml_response = hacer_llamada_soap(session, "ListOfCountryNamesByCode")
    if xml_response:
        return parsear_lista_paises(xml_response)
    return []


def obtener_info_pais(session, codigo_pais):
    """
    Obtiene información detallada de un país por su código ISO.
    
    Args:
        session: Sesión HTTP configurada
        codigo_pais (str): Código ISO del país
        
    Returns:
        dict: Diccionario con la información del país o None si hay error
    """
    parametros = f"<sCountryISOCode>{codigo_pais}</sCountryISOCode>"
    xml_response = hacer_llamada_soap(session, "FullCountryInfo", parametros)
    if xml_response:
        return parsear_info_pais(xml_response)
    return None


def mostrar_codigos_paises(codigos):
    """
    Muestra los códigos de países en un formato legible.
    
    Args:
        codigos (list): Lista de códigos de países
    """
    print("\n📋 Códigos ISO de países disponibles:")
    print("=" * 50)
    
    # Mostrar códigos en columnas
    for i in range(0, len(codigos), 8):
        fila = codigos[i:i+8]
        print("  ".join(f"{codigo:3}" for codigo in fila))
    
    print(f"\nTotal de países: {len(codigos)}")


def mostrar_info_pais(info_pais, codigo_pais):
    """
    Muestra la información del país en un formato atractivo.
    
    Args:
        info_pais (dict): Información del país
        codigo_pais (str): Código ISO del país
    """
    print(f"\n🌍 Información del país ({codigo_pais}):")
    print("=" * 40)
    print(f"🌍 País: {info_pais['nombre']}")
    print(f"🏙️ Capital: {info_pais['capital']}")
    print(f"💰 Moneda: {info_pais['moneda']}")
    print(f"🗣️ Idiomas: {info_pais['idiomas']}")


def main():
    """
    Función principal del script.
    """
    print("🌍 Consultor de Información de Países")
    print("=" * 40)
    print("Conectando al servicio SOAP...")
    
    # Crear sesión HTTP
    session = crear_session()
    
    # Obtener códigos de países
    print("\nObteniendo lista de países...")
    codigos = obtener_codigos_paises(session)
    
    if not codigos:
        print("❌ No se pudieron obtener los códigos de países.")
        print("💡 Verifique su conexión a internet.")
        sys.exit(1)
    
    print("✅ Conexión exitosa al servicio SOAP")
    
    # Mostrar códigos disponibles
    mostrar_codigos_paises(codigos)
    
    # Bucle principal
    while True:
        try:
            # Solicitar código del país
            codigo_pais = input("\n📝 Ingrese código ISO del país (o 'salir' para terminar): ").strip()
            
            if codigo_pais.lower() in ['salir', 'exit', 'quit']:
                print("👋 ¡Hasta luego!")
                break
            
            if not codigo_pais:
                print("❌ Por favor ingrese un código válido.")
                continue
            
            # Validar que el código existe en la lista
            if codigo_pais.upper() not in [c.upper() for c in codigos]:
                print(f"❌ El código '{codigo_pais}' no está en la lista de países disponibles.")
                print("💡 Sugerencia: Use códigos de 2 letras como 'US', 'PE', 'ES', etc.")
                continue
            
            # Obtener información del país
            print(f"\n🔍 Buscando información para {codigo_pais.upper()}...")
            info_pais = obtener_info_pais(session, codigo_pais)
            
            if info_pais:
                mostrar_info_pais(info_pais, codigo_pais.upper())
            else:
                print(f"❌ No se pudo obtener información para el código '{codigo_pais}'")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main() 