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
from colorama import init, Fore, Back, Style
from datetime import datetime
import json

# Inicializar colorama para Windows
init(autoreset=True)

# Variable global para el historial
historial_busquedas = []


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
        print(f"{Fore.RED}❌ Error en llamada SOAP {metodo}: {e}{Style.RESET_ALL}")
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
        print(f"{Fore.RED}❌ Error al parsear lista de países: {e}{Style.RESET_ALL}")
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
            print(f"{Fore.RED}❌ No se pudo encontrar la información del país en la respuesta XML{Style.RESET_ALL}")
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
            elif tag == 'sPhoneCode':
                info['codigo_telefono'] = elem.text
            elif tag == 'sContinentCode':
                info['continente'] = elem.text
            elif tag == 'sCountryFlag':
                info['bandera_url'] = elem.text
        
        # Verificar que tenemos la información mínima
        if 'nombre' in info:
            return {
                'nombre': info.get('nombre', 'No disponible'),
                'capital': info.get('capital', 'No disponible'),
                'moneda': info.get('moneda', 'No disponible'),
                'idiomas': ', '.join(idiomas) if idiomas else 'No disponible',
                'codigo_telefono': info.get('codigo_telefono', 'No disponible'),
                'continente': info.get('continente', 'No disponible'),
                'bandera_url': info.get('bandera_url', 'No disponible')
            }
        return None
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error al parsear información del país: {e}{Style.RESET_ALL}")
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
    print(f"\n{Fore.CYAN}📋 Códigos ISO de países disponibles:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    
    # Mostrar códigos en columnas con colores alternados
    for i in range(0, len(codigos), 8):
        fila = codigos[i:i+8]
        fila_coloreada = []
        for j, codigo in enumerate(fila):
            color = Fore.GREEN if j % 2 == 0 else Fore.YELLOW
            fila_coloreada.append(f"{color}{codigo:3}{Style.RESET_ALL}")
        print("  ".join(fila_coloreada))
    
    print(f"\n{Fore.MAGENTA}Total de países: {len(codigos)}{Style.RESET_ALL}")


def mostrar_info_pais(info_pais, codigo_pais):
    """
    Muestra la información del país en un formato atractivo.
    
    Args:
        info_pais (dict): Información del país
        codigo_pais (str): Código ISO del país
    """
    print(f"\n{Fore.BLUE}🌍 Información del país ({codigo_pais}):{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'=' * 50}{Style.RESET_ALL}")
    
    # Información principal
    print(f"{Fore.GREEN}🌍 País:{Style.RESET_ALL} {info_pais['nombre']}")
    print(f"{Fore.CYAN}🏙️ Capital:{Style.RESET_ALL} {info_pais['capital']}")
    print(f"{Fore.YELLOW}💰 Moneda:{Style.RESET_ALL} {info_pais['moneda']}")
    print(f"{Fore.MAGENTA}🗣️ Idiomas:{Style.RESET_ALL} {info_pais['idiomas']}")
    
    # Información adicional
    print(f"{Fore.RED}📞 Código telefónico:{Style.RESET_ALL} +{info_pais['codigo_telefono']}")
    print(f"{Fore.BLUE}🌎 Continente:{Style.RESET_ALL} {info_pais['continente']}")
    
    if info_pais['bandera_url'] != 'No disponible':
        print(f"{Fore.GREEN}🏳️ Bandera:{Style.RESET_ALL} {info_pais['bandera_url']}")


def agregar_al_historial(codigo_pais, info_pais):
    """
    Agrega una búsqueda al historial.
    
    Args:
        codigo_pais (str): Código del país buscado
        info_pais (dict): Información del país
    """
    global historial_busquedas
    
    busqueda = {
        'codigo': codigo_pais,
        'nombre': info_pais['nombre'],
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'info': info_pais
    }
    
    historial_busquedas.append(busqueda)
    
    # Mantener solo las últimas 10 búsquedas
    if len(historial_busquedas) > 10:
        historial_busquedas = historial_busquedas[-10:]


def mostrar_historial():
    """
    Muestra el historial de búsquedas recientes.
    """
    global historial_busquedas
    
    if not historial_busquedas:
        print(f"{Fore.YELLOW}📝 No hay búsquedas recientes.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}📚 Historial de búsquedas recientes:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    
    for i, busqueda in enumerate(historial_busquedas, 1):
        print(f"{Fore.GREEN}{i}.{Style.RESET_ALL} {busqueda['codigo']} - {busqueda['nombre']} ({busqueda['fecha']})")


def exportar_resultados(archivo="resultados_paises.txt"):
    """
    Exporta el historial de búsquedas a un archivo de texto.
    
    Args:
        archivo (str): Nombre del archivo de salida
    """
    global historial_busquedas
    
    if not historial_busquedas:
        print(f"{Fore.YELLOW}📝 No hay resultados para exportar.{Style.RESET_ALL}")
        return
    
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("🌍 CONSULTOR DE PAÍSES - RESULTADOS EXPORTADOS\n")
            f.write("=" * 50 + "\n")
            f.write(f"Fecha de exportación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for busqueda in historial_busquedas:
                f.write(f"📋 País: {busqueda['nombre']} ({busqueda['codigo']})\n")
                f.write(f"📅 Fecha de búsqueda: {busqueda['fecha']}\n")
                f.write(f"🏙️ Capital: {busqueda['info']['capital']}\n")
                f.write(f"💰 Moneda: {busqueda['info']['moneda']}\n")
                f.write(f"🗣️ Idiomas: {busqueda['info']['idiomas']}\n")
                f.write(f"📞 Código telefónico: +{busqueda['info']['codigo_telefono']}\n")
                f.write(f"🌎 Continente: {busqueda['info']['continente']}\n")
                f.write("-" * 40 + "\n\n")
        
        print(f"{Fore.GREEN}✅ Resultados exportados a '{archivo}'{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error al exportar resultados: {e}{Style.RESET_ALL}")


def mostrar_banner():
    """
    Muestra un banner atractivo al inicio del programa.
    """
    banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════════════════════════════╗
║                    🌍 CONSULTOR DE PAÍSES 🌍                    ║
║                                                              ║
║  Script Python que consume servicios SOAP para obtener      ║
║  información detallada sobre países del mundo.              ║
║                                                              ║
║  Desarrollado con ❤️  por AI Assistant                        ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)


def mostrar_menu_ayuda():
    """
    Muestra el menú de ayuda con comandos disponibles.
    """
    print(f"\n{Fore.YELLOW}📖 COMANDOS DISPONIBLES:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}• Código de país:{Style.RESET_ALL} Ingrese código ISO (ej: PE, US, ES)")
    print(f"{Fore.GREEN}• salir/exit/quit:{Style.RESET_ALL} Salir del programa")
    print(f"{Fore.GREEN}• ayuda/help:{Style.RESET_ALL} Mostrar esta ayuda")
    print(f"{Fore.GREEN}• lista/list:{Style.RESET_ALL} Mostrar lista de países")
    print(f"{Fore.GREEN}• historial/history:{Style.RESET_ALL} Mostrar búsquedas recientes")
    print(f"{Fore.GREEN}• exportar/export:{Style.RESET_ALL} Exportar resultados a archivo")
    print(f"{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}")


def main():
    """
    Función principal del script.
    """
    mostrar_banner()
    print(f"{Fore.YELLOW}Conectando al servicio SOAP...{Style.RESET_ALL}")
    
    # Crear sesión HTTP
    session = crear_session()
    
    # Obtener códigos de países
    print(f"\n{Fore.YELLOW}Obteniendo lista de países...{Style.RESET_ALL}")
    codigos = obtener_codigos_paises(session)
    
    if not codigos:
        print(f"{Fore.RED}❌ No se pudieron obtener los códigos de países.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Verifique su conexión a internet.{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"{Fore.GREEN}✅ Conexión exitosa al servicio SOAP{Style.RESET_ALL}")
    
    # Mostrar códigos disponibles
    mostrar_codigos_paises(codigos)
    
    # Mostrar ayuda inicial
    mostrar_menu_ayuda()
    
    # Bucle principal
    while True:
        try:
            # Solicitar código del país
            codigo_pais = input(f"\n{Fore.CYAN}📝 Ingrese código ISO del país (o 'ayuda' para comandos): {Style.RESET_ALL}").strip()
            
            if codigo_pais.lower() in ['salir', 'exit', 'quit']:
                print(f"\n{Fore.GREEN}👋 ¡Hasta luego!{Style.RESET_ALL}")
                break
            
            if codigo_pais.lower() in ['ayuda', 'help']:
                mostrar_menu_ayuda()
                continue
            
            if codigo_pais.lower() in ['lista', 'list']:
                mostrar_codigos_paises(codigos)
                continue
            
            if codigo_pais.lower() in ['historial', 'history']:
                mostrar_historial()
                continue
            
            if codigo_pais.lower() in ['exportar', 'export']:
                exportar_resultados()
                continue
            
            if not codigo_pais:
                print(f"{Fore.RED}❌ Por favor ingrese un código válido.{Style.RESET_ALL}")
                continue
            
            # Validar que el código existe en la lista
            if codigo_pais.upper() not in [c.upper() for c in codigos]:
                print(f"{Fore.RED}❌ El código '{codigo_pais}' no está en la lista de países disponibles.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}💡 Sugerencia: Use códigos de 2 letras como 'US', 'PE', 'ES', etc.{Style.RESET_ALL}")
                continue
            
            # Obtener información del país
            print(f"\n{Fore.YELLOW}🔍 Buscando información para {codigo_pais.upper()}...{Style.RESET_ALL}")
            info_pais = obtener_info_pais(session, codigo_pais)
            
            if info_pais:
                mostrar_info_pais(info_pais, codigo_pais.upper())
                # Agregar al historial
                agregar_al_historial(codigo_pais.upper(), info_pais)
            else:
                print(f"{Fore.RED}❌ No se pudo obtener información para el código '{codigo_pais}'{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n\n{Fore.GREEN}👋 ¡Hasta luego!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ Error inesperado: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    main() 