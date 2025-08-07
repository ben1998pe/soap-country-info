# 🌍 Consultor de Información de Países

Script en Python que consume un servicio SOAP público para obtener información detallada sobre países.

## 📋 Características

- ✅ Consume servicio SOAP público de información de países
- ✅ Lista todos los códigos ISO de países disponibles
- ✅ Obtiene información detallada: nombre, capital, moneda e idiomas
- ✅ Manejo robusto de errores y reintentos de conexión
- ✅ Interfaz de usuario interactiva y amigable
- ✅ Validación de códigos de países

## 🚀 Instalación

1. **Clonar o descargar el proyecto**
2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Uso

### Ejecutar el script:
```bash
python country_info.py
```

### Ejemplo de uso:
```
🌍 Consultor de Información de Países
========================================
Conectando al servicio SOAP...
✅ Conexión exitosa al servicio SOAP

Obteniendo lista de países...

📋 Códigos ISO de países disponibles:
==================================================
AD   AE   AF   AG   AI   AL   AM   AO
AR   AS   AT   AU   AW   AZ   BA   BB
...

📝 Ingrese código ISO del país (o 'salir' para terminar): PE

🔍 Buscando información para PE...

🌍 Información del país (PE):
========================================
🌍 País: Peru
🏙️ Capital: Lima
💰 Moneda: PEN
🗣️ Idiomas: Spanish
```

## 🔧 Dependencias

- **zeep**: Cliente SOAP para Python
- **requests**: Cliente HTTP con manejo de reintentos
- **urllib3**: Utilidades HTTP

## 🌐 Servicio SOAP

El script utiliza el servicio público:
- **WSDL**: http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL
- **Proveedor**: Oorsprong Web Services

## ⚠️ Notas

- Requiere conexión a internet
- El servicio puede tener limitaciones de velocidad
- Algunos países pueden no tener información completa
- Los idiomas mostrados son una aproximación basada en el idioma principal

## 🛠️ Manejo de Errores

El script incluye manejo de errores para:
- ❌ Fallos de conexión al servicio SOAP
- ❌ Códigos de país inexistentes
- ❌ Errores de red y timeouts
- ❌ Interrupciones del usuario (Ctrl+C)

## 📝 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y personal. 