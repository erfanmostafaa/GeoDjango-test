from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        self.stdout.write("waiting for databse ...")
        db_connection = False
        while not db_connection:
            try:
                db_connection = connections["default"].ensure_connection()
                db_connection = True
            except OperationalError:
                self.stdout.write("Database is unavailable, waiting 1 second")
                time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS("Database is available!"))

