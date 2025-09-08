# Generador de Tests Interactivos

Una aplicación web Flask que genera tests interactivos de opción múltiple a partir de documentos PDF y PPTX utilizando inteligencia artificial (Google Gemini).

## Características

- 📄 Soporte para archivos PDF y PPTX
- 🤖 Generación automática de preguntas usando Google Gemini AI
- 🎯 Tests personalizables de 1 a 5 preguntas con 4 opciones cada una
- 🖼️ Imagen de fondo personalizable para los quizzes
- 🌙 Modo claro/oscuro con persistencia automática
- 📱 Interfaz web responsive
- 💾 Genera archivos HTML autocontenidos (funcionan offline)
- ✅ Retroalimentación inmediata con justificaciones
- 📊 Resumen final de resultados

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/albert1t0/cgr-preguntas.git
cd cgr-preguntas
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura tu API key de Google Gemini:
```bash
# Crea un archivo .env en la raíz del proyecto
echo "GOOGLE_API_KEY=tu_api_key_aqui" > .env
```

## Uso

1. Ejecuta la aplicación:
```bash
python app.py
```

2. Abre tu navegador en `http://localhost:5001`

3. Configura tu test:
   - Selecciona un archivo PDF o PPTX
   - Elige el número de preguntas (1-5) usando el slider
   - Opcionalmente, añade una imagen de fondo

4. La aplicación generará y descargará automáticamente un archivo HTML con el test interactivo personalizado

## Estructura del Proyecto

```
├── app.py              # Aplicación Flask principal
├── requirements.txt    # Dependencias Python
├── .env               # Variables de entorno (no incluido en repo)
├── templates/
│   ├── index.html     # Formulario de carga
│   └── quiz.html      # Template del test interactivo
├── uploads/           # Directorio para archivos subidos
└── .gitignore        # Archivos excluidos de git
```

## Tecnologías Utilizadas

- **Flask**: Framework web
- **Google Gemini AI**: Generación de preguntas
- **PyPDF2**: Extracción de texto de PDFs
- **python-pptx**: Extracción de texto de PowerPoint
- **HTML/CSS/JavaScript**: Frontend interactivo

## Funcionalidades del Test Generado

- Tests autocontenidos que funcionan sin conexión a internet
- Navegación por pestañas entre preguntas (dinámicamente generadas)
- Validación de respuestas con retroalimentación visual
- Justificaciones detalladas para cada respuesta
- Modo claro/oscuro con toggle integrado
- Imagen de fondo personalizada (opcional)
- Resumen final con puntuación

## Versiones

### v1.2 - Mejoras de Personalización
- ✨ **Selector de preguntas**: Elige entre 1-5 preguntas con slider interactivo
- 🎨 **Imagen de fondo**: Personaliza tus quizzes con imágenes de fondo
- 🌗 **Modo oscuro**: Toggle entre tema claro y oscuro con persistencia automática
- 🔄 **Detección automática**: Respeta la preferencia del sistema del usuario

### v1.0 - Versión Base
- Generación básica de 2 preguntas por documento
- Templates HTML autocontenidos
- Integración con Google Gemini AI

## Requisitos

- Python 3.10+
- API key válida de Google Gemini
- Archivos PDF legibles (no encriptados) o PPTX estándar

## Licencia

Este proyecto está bajo la Licencia MIT.