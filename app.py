"""Main Streamlit application for PDF comparison."""
import gc
import streamlit as st
from PIL import Image
from typing import Optional

from config import AppConfig, ProcessingConfig
from processing import process_page
from utils import (
    cleanup_temp_files,
    convert_pdf_to_images,
    normalize_page_lists,
    save_pdf_from_images,
    save_uploaded_file,
)

# Page configuration
config = AppConfig()
processing_config = ProcessingConfig()

st.set_page_config(
    page_title=config.page_title,
    page_icon=config.page_icon,
    layout=config.layout,
)
Image.MAX_IMAGE_PIXELS = None

# UI
st.title("🏗️ Comparador de pdfs")
st.markdown(
    """
    Sube dos pdfs. El sistema alineará las hojas, limpiará el ruido 
    y resaltará las diferencias:
    - **:green[VERDE]:** Elementos nuevos.
    - **:violet[MAGENTA]:** Elementos eliminados.
    """
)

col1, col2 = st.columns(2)
file1 = col1.file_uploader(
    "📂 pdf Original (Referencia)", type=["pdf"]
)
file2 = col2.file_uploader(
    "📂 pdf Nuevo (Modificado)", type=["pdf"]
)

if st.button("🔍 Iniciar Comparación") and file1 and file2:
    # Validar tamaño de archivos
    max_size_mb = 50
    max_size = max_size_mb * 1024 * 1024
    if file1.size > max_size or file2.size > max_size:
        st.error(f"❌ Los archivos no deben exceder {max_size_mb}MB")
        st.stop()

    status = st.empty()
    progress_bar = st.progress(0)
    temp_files: list[str] = []
    output_pdf_path: Optional[str] = None

    try:
        # Save uploaded files temporarily
        status.text("💾 Guardando archivos temporales...")
        path1 = save_uploaded_file(file1)
        path2 = save_uploaded_file(file2)
        temp_files.extend([path1, path2])

        # Convert PDFs to images
        status.text(
            "⏳ Rasterizando PDFs (esto puede tardar unos segundos)..."
        )
        pages_a = convert_pdf_to_images(path1, dpi=processing_config.dpi)
        pages_b = convert_pdf_to_images(path2, dpi=processing_config.dpi)

        # Normalize page lists
        pages_a, pages_b = normalize_page_lists(pages_a, pages_b)
        max_pages = len(pages_a)

        if max_pages == 0:
            st.error("❌ No se encontraron páginas en los PDFs")
            cleanup_temp_files(*temp_files)
            st.stop()

        # Limitar número de páginas
        if max_pages > 50:
            st.warning(f"⚠️ El PDF tiene {max_pages} páginas. Procesando solo las primeras 50.")
            pages_a = pages_a[:50]
            pages_b = pages_b[:50]
            max_pages = 50

        # Process each page and free memory
        result_images: list[Image.Image] = []

        for i in range(max_pages):
            status.text(f"⚙️ Procesando Hoja {i+1} de {max_pages}...")
            
            # Process page
            result = process_page(
                pages_a[i], pages_b[i], processing_config
            )

            if result is not None:
                result_images.append(result)
            
            # Free original images after processing
            pages_a[i] = None
            pages_b[i] = None

            # Clean memory every 3 pages
            if (i + 1) % 3 == 0:
                gc.collect()

            progress_bar.progress((i + 1) / max_pages)

        if not result_images:
            st.error("❌ No se generaron imágenes de resultado")
            cleanup_temp_files(*temp_files)
            st.stop()

        # Generate output PDF
        status.text("💾 Generando PDF final...")
        output_pdf_path = config.output_filename
        save_pdf_from_images(result_images, output_pdf_path)

        status.success("✅ ¡Proceso terminado!")

        # FREE MEMORY BEFORE DOWNLOAD
        # Clear image list
        del result_images
        # Clear page lists
        del pages_a, pages_b
        # Force garbage collection
        gc.collect()

        # Read PDF into memory AFTER cleanup
        with open(output_pdf_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
        
        st.download_button(
            "⬇️ Descargar Reporte PDF",
            pdf_bytes,
            file_name=config.output_filename,
            mime="application/pdf",
        )

    except FileNotFoundError as e:
        st.error(f"❌ Archivo no encontrado: {e}")
    except ValueError as e:
        st.error(f"❌ Error de validación: {e}")
    except MemoryError:
        st.error("❌ Memoria insuficiente. Intenta con PDFs más pequeños o menos páginas.")
    except Exception as e:
        st.error(f"❌ Ocurrió un error inesperado: {e}")
    finally:
        # Cleanup ALL temporary files
        cleanup_temp_files(*temp_files)
        if output_pdf_path:
            cleanup_temp_files(output_pdf_path)
        # Force final cleanup
        gc.collect()
