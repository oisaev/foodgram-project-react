import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = 'Загрузка инициализационных данных из .csv'

    def handle(self, *args, **options):
        data_to_load = (
            (Ingredient, 'ingredients.csv'),
            (Tag, 'tags.csv')
        )
        for model, file in data_to_load:
            file_full_path = os.path.join(
                settings.BASE_DIR,
                'data',
                file
            )
            with open(file_full_path) as f:
                reader = csv.DictReader(f)
                for line in reader:
                    model.objects.get_or_create(**line)
        self.stdout.write(self.style.SUCCESS('Данные загружены успешно'))
