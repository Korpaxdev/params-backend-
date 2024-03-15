import json
from pathlib import Path

from django.core.management import BaseCommand, CommandParser

from backend.models import ParameterModel


class Command(BaseCommand):
    help = "Создает параметры из JSON файла"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("json_file", type=str, help="JSON файл для парсинга")

    def handle(self, *args, **options):
        json_path = Path(options["json_file"])
        if not json_path.exists():
            raise FileNotFoundError("JSON файл не найден")

        blocks = json.loads(json_path.read_text())

        for block in blocks:
            data_length = block["data_length"]
            cat_id = block["id"]
            for param in block["params"]:
                param_info = {
                    "data_length": data_length,
                    "cat_id": cat_id,
                    "length": param["length"],
                    "name": param["name"],
                    "rus_name": param["rus_name"],
                    "scaling": param["scaling"],
                    "range": param["range"],
                    "spn": param["spn"],
                }
                ParameterModel.objects.create(**param_info)
                print(f"Создан параметр {param_info=}")
