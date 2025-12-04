"""Configuration settings for PDF comparison application."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessingConfig:
    """Configuration for image processing parameters."""

    dpi: int = 200
    min_area_noise: int = 5
    tolerance_kernel_size: tuple[int, int] = (2, 2)
    tolerance_iterations: int = 1
    orb_features: int = 10000
    match_percentage: float = 0.20
    min_matches: int = 4
    ghost_base_weight: float = 0.3
    ghost_bg_weight: float = 0.7
    green_color: tuple[int, int, int] = (0, 200, 0)
    magenta_color: tuple[int, int, int] = (255, 0, 180)
    threshold_value: int = 10


@dataclass(frozen=True)
class AppConfig:
    """Application-level configuration."""

    page_title: str = "Comparador de pdfs"
    page_icon: str = "📐"
    layout: str = "wide"
    output_filename: str = "Reporte_Diferencias.pdf"


