from granian import Granian

from delivery_s3_temporary_links.core.settings import settings


def run() -> None:
    """Функция для запуска приложения"""

    target = 'delivery_s3_temporary_links.run_app:app'

    Granian(
        target=target,
        address=settings.settings_app.ip,
        port=settings.settings_app.port_app,
        interface=settings.settings_app.interface,
        workers=settings.settings_app.workers
    ).serve()


if __name__ == '__main__':
    run()
