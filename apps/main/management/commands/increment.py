from __future__ import annotations

from argparse import ArgumentParser

from django.core.management.base import BaseCommand

from apps.main.models import CountData


class Command(BaseCommand):
    help = 'increment'

    def add_arguments(self, parser: ArgumentParser) -> None:
        pass


    def handle(self, *args: list, **options: dict) -> None:
        count_data, _ = CountData.objects.get_or_create()
        prev_count = count_data.count
        count_data.count = prev_count + 1
        count_data.save()
        print(f'COUNT: {prev_count} -> {count_data.count}')
