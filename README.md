# 🌍 Consultor de Información de Países

Script en Python que consume un servicio SOAP público para obtener información detallada sobre países.

## 📋 Características

- ✅ **Interfaz colorida y atractiva** con colores y emojis
- ✅ **Consume servicio SOAP público** de información de países
- ✅ **Lista todos los códigos ISO** de países disponibles (246 países)
- ✅ **Información detallada**: nombre, capital, moneda, idiomas, código telefónico, continente
- ✅ **Historial de búsquedas** - Mantiene las últimas 10 consultas
- ✅ **Exportar resultados** a archivo de texto
- ✅ **Manejo robusto de errores** y reintentos de conexión
- ✅ **Interfaz de usuario interactiva** con comandos adicionales
- ✅ **Validación de códigos** de países
- ✅ **Banner atractivo** al inicio del programa

## 🚀 Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone https://github.com/ben1998pe/soap-country-info.git
   cd soap-country-info
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Uso

### Ejecutar el script:
```bash
python country_info.py
```

### Comandos disponibles:
- **Código de país**: Ingrese código ISO (ej: PE, US, ES)
- **`salir/exit/quit`**: Salir del programa
- **`ayuda/help`**: Mostrar ayuda
- **`lista/list`**: Mostrar lista de países
- **`historial/history`**: Mostrar búsquedas recientes
- **`exportar/export`**: Exportar resultados a archivo

### Ejemplo de uso:
```
╔══════════════════════════════════════════════════════════════╗
║                    🌍 CONSULTOR DE PAÍSES 🌍                    ║
║                                                              ║
║  Script Python que consume servicios SOAP para obtener      ║
║  información detallada sobre países del mundo.              ║
║                                                              ║
║  Desarrollado con ❤️  por AI Assistant                        ║
╚══════════════════════════════════════════════════════════════╝

📋 Códigos ISO de países disponibles:
==================================================
AD   AE   AF   AG   AI   AL   AM   AN
AO   AQ   AR   AS   AT   AU   AW   AX
...

📝 Ingrese código ISO del país (o 'ayuda' para comandos): PE

🔍 Buscando información para PE...

🌍 Información del país (PE):
==================================================
🌍 País: Peru
🏙️ Capital: Lima
💰 Moneda: PEN
🗣️ Idiomas: Spanish
📞 Código telefónico: +51
🌎 Continente: AM
🏳️ Bandera: http://www.oorsprong.org/WebSamples.CountryInfo/Flags/Peru.jpg
```

## 🔧 Dependencias

- **requests**: Cliente HTTP con manejo de reintentos
- **urllib3**: Utilidades HTTP
- **colorama**: Colores en terminal para Windows

## 🌐 Servicio SOAP

El script utiliza el servicio público:
- **WSDL**: http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL
- **Proveedor**: Oorsprong Web Services

## ✨ Nuevas Características

### 🎨 **Interfaz Mejorada**
- Colores atractivos en terminal
- Banner informativo al inicio
- Emojis para mejor experiencia visual

### 📚 **Historial de Búsquedas**
- Mantiene las últimas 10 consultas
- Comando `historial` para ver búsquedas recientes
- Información con fecha y hora

### 📄 **Exportar Resultados**
- Comando `exportar` para guardar en archivo
- Formato legible con toda la información
- Archivo: `resultados_paises.txt`

### 📞 **Información Adicional**
- Código telefónico del país
- Código de continente
- URL de la bandera del país

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
- ❌ Errores al exportar archivos

## 📝 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y personal.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Puedes:
- Reportar bugs
- Sugerir nuevas características
- Mejorar la documentación
- Agregar más funcionalidades 