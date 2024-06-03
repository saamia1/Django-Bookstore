import os
import sys
from decouple import config, Csv
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookstore.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
