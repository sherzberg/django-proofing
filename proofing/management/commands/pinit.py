from django.core.management.base import BaseCommand, CommandError
from proofing.management.commands import get_response, create_photosize


class Command(BaseCommand):
    help = ('Prompts the user to set up the default photo sizes required by Proofing.')
    requires_model_validation = True
    can_import_settings = True

    def handle(self, *args, **kwargs):
        return init(*args, **kwargs)

def init(*args, **kwargs):
    msg = '\nproofing requires a specific photo size to display thumbnail previews in the Django admin application.\nWould you like to generate this size now? (yes, no):'
    if get_response(msg, lambda inp: inp == 'yes', False):
        admin_thumbnail = create_photosize('admin_thumbnail', width=100, height=75, crop=True, pre_cache=False)

    msg = '\nproofing comes with a set of templates for setting up a complete photo gallery. These templates require you to define both a "thumbnail" and "display" size.\nWould you like to define them now? (yes, no):'
    if get_response(msg, lambda inp: inp == 'yes', False):
        thumbnail = create_photosize('thumbnail', width=200, height=150, crop=True)
        display = create_photosize('display', width=600, increment_count=True)
