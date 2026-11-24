import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import flet as ft
from frontend.app import create_app_view


def _configure_logging() -> None:
    """Configura logging rotativo em reports/app.log para diagnóstico em campo."""
    os.makedirs("reports", exist_ok=True)
    handler = RotatingFileHandler(
        os.path.join("reports", "app.log"),
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[handler],
    )


_configure_logging()
logger = logging.getLogger(__name__)


async def main(page: ft.Page):
    """Ponto de entrada da aplicação desktop Flet."""
    page.title = "Scan Utility CiD"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    # Configura dimensões e comportamento da janela
    if hasattr(page, "window"):
        page.window.width = 1080
        page.window.height = 760
        page.window.min_width = 850
        page.window.min_height = 600
        try:
            res = page.window.center()
            if hasattr(res, "__await__"):
                await res
        except Exception as exc:
            logger.debug("Falha ao centralizar janela: %s", exc, exc_info=True)

    # Cria a visualização principal e anexa à página
    app_view = create_app_view(page)
    page.add(app_view)


if __name__ == "__main__":
    if hasattr(ft, "run"):
        ft.run(main)
    else:
        ft.app(target=main)
