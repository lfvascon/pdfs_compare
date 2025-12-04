# 📄 Comparador de PDFs (Multi-página)
# Readme generado con IA

Una aplicación web sencilla y potente para comparar **dos archivos PDF completos** y detectar visualmente cualquier cambio entre ellos.

> **💡 El Problema:**
> Herramientas actuales como el comparador de versiones de **Autodesk Construction Cloud (ACC)** o BIM 360, a fecha de hoy (04/12/2025), solo permiten comparar documentos **página por página**. Si tienes un documento de 50 páginas, tienes que hacer 50 comparaciones manuales.
>
> **✅ La Solución:**
> Esta herramienta automatiza el proceso, comparando **todas las páginas de una sola vez** y generando un único archivo PDF descargable con todas las diferencias resaltadas.

## 🔒 Seguridad y Privacidad

### Almacenamiento de archivos

- **Temporales**: Los PDFs subidos se guardan en `/tmp/` del servidor (filesystem efímero)
- **Eliminación automática**: Todos los archivos se eliminan inmediatamente después del procesamiento
- **Sin persistencia**: Nada se guarda permanentemente
- **Aislamiento**: Cada sesión de usuario está completamente aislada

### Recomendaciones de seguridad

- ✅ **Archivos confidenciales**: La app elimina archivos inmediatamente
- ✅ **Sesiones aisladas**: Otros usuarios no pueden acceder a tus archivos
- ⚠️ **Datos sensibles**: Si trabajas con información clasificada, considera deployar en tu propia infraestructura
- ⚠️ **Sin encriptación**: Los archivos temporales no están encriptados en reposo
## 📋 ¿Qué hace?

Toma dos versiones de un archivo PDF (Versión A y Versión B) y genera un **nuevo PDF** donde se superponen ambas versiones.

- **Alinea las páginas:** Si el documento se movió o escaneó un poco chueco, el sistema intenta corregirlo automáticamente.
- **Detecta cambios:** Compara el contenido visualmente.
- **Resalta las diferencias:**
  - 🟢 **Verde**: Texto o gráficos nuevos (añadidos en la Versión B).
  - 🟣 **Magenta**: Texto o gráficos borrados (estaban en la A, pero no en la B).
  - ⚪ **Gris Tenue**: Todo lo que no cambió (para dar contexto).

## ✨ Características Principales

- **Comparación Total:** Procesa documentos enteros, no importa cuántas páginas tengan.
- **Alineación Inteligente:** Usa algoritmos de visión (ORB) para encuadrar las páginas antes de comparar.
- **Ignora "Ruido":** Configurado para ignorar pequeños defectos de escaneo o vibraciones de píxeles (< 5px).
- **Alta Precisión:** Capaz de detectar cambios sutiles en texto (letras cambiadas, comas, números).
- **Privacidad:** Procesamiento local o en tu propia instancia de nube; los archivos no se guardan permanentemente.

## 🚀 Cómo Usarlo (Versión Web)

Si has desplegado la herramienta en Streamlit Cloud:

1.  **Sube el archivo original** (Referencia) en la columna izquierda.
2.  **Sube el archivo nuevo** (Modificado) en la columna derecha.
3.  Haz clic en el botón **"🔍 Iniciar Comparación"**.
4.  Espera unos segundos/minutos (dependiendo del tamaño del PDF).
5.  Descarga el archivo `Reporte_Diferencias.pdf`.

## 🛠️ Instalación en tu PC (Local)

Si prefieres ejecutarlo en tu propia computadora:

### Requisitos
- Tener instalado **Python 3.10+**
- Tener instalado **Poppler** (herramienta necesaria para leer PDFs).

#### 1. Instalar Poppler
- **Windows:** Descarga los binarios [aquí](https://github.com/oschwartz10612/poppler-windows/releases/), descomprime y añade la carpeta `bin` a tu PATH de Windows.
- **Mac:** `brew install poppler`
- **Linux:** `sudo apt-get install poppler-utils`

#### 2. Instalar Librerías
Abre tu terminal en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt

- **Alinear automáticamente** las hojas, incluso si tienen escalas o rotaciones ligeramente diferentes
- **Detectar diferencias** con precisión submilimétrica
- **Filtrar ruido** para evitar falsos positivos
- **Visualizar cambios** con un sistema de colores intuitivo:
  - 🟢 **Verde**: Elementos nuevos añadidos
  - 🟣 **Magenta**: Elementos eliminados
  - ⚪ **Fondo fantasma**: Referencia en escala de grises

## ✨ Características

- ✅ **Alineación automática** mediante detección de características (ORB)
- ✅ **Comparación multipágina** - procesa PDFs completos
- ✅ **Tolerancia configurable** - ajusta la sensibilidad de detección
- ✅ **Filtrado de ruido** - elimina diferencias irrelevantes (< 5px²)
- ✅ **Exportación PDF** - descarga el reporte completo
- ✅ **Interfaz moderna** - diseño limpio con Streamlit
- ✅ **Optimizado para web** - 200 DPI para balance memoria/calidad

## 🚀 Instalación Local

### Requisitos previos

- Python 3.11+
- Poppler (para conversión PDF)

#### Instalar Poppler:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
Descarga binarios desde: http://blog.alivate.com.au/poppler-windows/

### Instalación

```bash
# Clonar o descargar el repositorio
cd pdf-compare

# Instalar dependencias Python
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

## ☁️ Despliegue en Streamlit Cloud

### Opción 1: Deploy directo

1. Sube el proyecto a un repositorio GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio
4. Selecciona `app.py` como archivo principal
5. Deploy automático

### Opción 2: Fork y deploy

1. Haz fork de este repositorio
2. Conecta tu fork en Streamlit Cloud
3. Listo

Los archivos `requirements.txt` y `packages.txt` se procesarán automáticamente.

## 📁 Estructura del Proyecto

```
pdf-compare/
├── app.py              # Aplicación principal Streamlit
├── config.py           # Configuración centralizada
├── processing.py       # Lógica de procesamiento de imágenes
├── utils.py            # Utilidades (archivos, PDFs)
├── requirements.txt    # Dependencias Python
├── packages.txt        # Dependencias del sistema (Poppler)
└── README.md          # Este archivo
```

## 🎯 Uso

1. **Cargar archivos**:
   - Sube el plano original (referencia) en el panel izquierdo
   - Sube el plano modificado en el panel derecho

2. **Iniciar comparación**:
   - Clic en "🔍 Iniciar Comparación"
   - Espera mientras se procesan las páginas

3. **Descargar resultado**:
   - Una vez procesado, descarga el PDF con las diferencias resaltadas
   - El archivo se llama `Reporte_Diferencias.pdf`

## ⚙️ Configuración

Puedes ajustar los parámetros en `config.py`:

```python
@dataclass(frozen=True)
class ProcessingConfig:
    dpi: int = 200                          # Resolución (↑ = más calidad, más RAM)
    min_area_noise: int = 5                 # Área mínima para considerar diferencia
    tolerance_kernel_size: tuple = (2, 2)   # Tolerancia de alineación
    orb_features: int = 10000               # Características para alineación
    green_color: tuple = (0, 200, 0)        # Color elementos nuevos
    magenta_color: tuple = (255, 0, 180)    # Color elementos eliminados
```

### Ajustes comunes:

- **Más sensible**: `min_area_noise = 1` (detecta cambios más pequeños)
- **Menos sensible**: `min_area_noise = 20` (ignora cambios menores)
- **Mayor calidad**: `dpi = 300` (requiere más RAM)
- **Menor uso de memoria**: `dpi = 150` (calidad reducida)

## 🛠️ Tecnologías

- **[Streamlit](https://streamlit.io/)** - Framework web
- **[OpenCV](https://opencv.org/)** - Procesamiento de imágenes
- **[pdf2image](https://github.com/Belval/pdf2image)** - Conversión PDF
- **[NumPy](https://numpy.org/)** - Operaciones numéricas
- **[Pillow](https://python-pillow.org/)** - Manipulación de imágenes
- **[Poppler](https://poppler.freedesktop.org/)** - Motor de renderizado PDF

## 📊 Algoritmo de Comparación

1. **Conversión**: PDF → Imágenes (200 DPI)
2. **Detección de características**: ORB con 10,000 puntos
3. **Matching**: Emparejamiento de características (top 20%)
4. **Alineación**: Homografía RANSAC para warp perspectivo
5. **Binarización**: Umbral adaptativo con inversión
6. **Dilatación**: Kernel 2x2 para tolerancia
7. **Diferenciación**: Resta de máscaras binarias
8. **Limpieza**: Filtrado de contornos < 5px²
9. **Visualización**: Overlay con colores distintivos

## 🔧 Solución de Problemas

### Error: "Unable to get page count"
- **Causa**: Poppler no instalado
- **Solución**: Instala `poppler-utils` (ver sección Instalación)

### Error: "Out of memory"
- **Causa**: DPI muy alto o PDFs muy grandes
- **Solución**: Reduce `dpi` en `config.py` (ej: 150)

### Las diferencias no se detectan bien
- **Causa**: Desalineación extrema o escalas muy diferentes
- **Solución**: Aumenta `orb_features` a 20000 en `config.py`

### Muchos falsos positivos
- **Causa**: Ruido o artefactos de escaneo
- **Solución**: Aumenta `min_area_noise` a 10-20

## 📝 Limitaciones

- **Memoria**: PDFs muy grandes (>100 páginas) pueden requerir mucha RAM
- **Resolución**: 200 DPI es un compromiso calidad/rendimiento
- **Rotación**: Solo funciona bien con rotaciones < 30°
- **Color**: Optimizado para planos B/N, colores pueden generar ruido

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Abre un issue primero para discutir el cambio
2. Fork el proyecto
3. Crea una rama feature (`git checkout -b feature/AmazingFeature`)
4. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
5. Push a la rama (`git push origin feature/AmazingFeature`)
6. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la [MIT License](LICENSE).

## 👤 Autor

**LFVASCON GEMINIPRO DEEPSEEK CURSOR CHAT AGENT**

---

⭐ Si encuentras útil este proyecto, considera darle una estrella en GitHub




