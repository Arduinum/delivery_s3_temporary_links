from pathlib import Path


def get_file_path(file_name: str) -> Path | None:
    """Вернёт путь до файла"""

    paths = Path(__file__).resolve()

    for path_db in paths.parents:
        target_db_path = path_db / file_name

        if target_db_path.exists():
            return target_db_path

    return None
