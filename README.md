#**Readme generado con IA**
# 🏗️ Comparador de pdfs

Aplicación web para comparar dos versiones de planos técnicos en formato PDF, detectando y visualizando diferencias automáticamente mediante procesamiento de imágenes.

## 📋 Descripción

Esta herramienta profesional permite comparar planos arquitectónicos, de ingeniería o cualquier tipo de documentación técnica en PDF. Utiliza algoritmos avanzados de visión por computadora para:

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


