
from django.contrib.auth.models import Group

def create_groups():
    Group.objects.create(name="employees")
    Group.objects.create(name="operators")


