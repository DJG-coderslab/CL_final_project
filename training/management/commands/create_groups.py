"""
Command to creating groups for employees and operators
"""

from django.core.management.base import BaseCommand

from ._groups import create_groups


class Command(BaseCommand):
    """Filling relations Answer and Question"""
    help = "Create groups for employees and operators"
    
    def handle(self, *args, **kwargs):
        create_groups()
        self.stdout.write(self.style.SUCCESS("Groups was successfully created"))
