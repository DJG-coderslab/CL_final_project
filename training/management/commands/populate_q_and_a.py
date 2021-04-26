"""
Command for filling database a sample data,
not for including to production version
"""


from django.core.management.base import BaseCommand

from ._priv import q_and_a, set_correct_answer


class Command(BaseCommand):
    """Filling relations Answer and Question"""
    help = "Create Questions and related answers"
    
    def handle(self, *args, **kwargs):
        q_and_a()
        set_correct_answer()
        self.stdout.write(self.style.SUCCESS("Created questions and answers"))
