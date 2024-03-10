'''
    Clean Up unused accounts by
    sending reminders and 
    deleting not yet r longtime unused users
'''
from datetime import datetime, timedelta
import os, logging

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings

from django.conf import settings

logger = logging.getLogger(__name__)

backups_dir = os.path.join(settings.BASE_DIR, 'backups/')

class Command(BaseCommand):
    '''
        Command containg housekeeping activities 
        and sending statictis for MyWebsite
        * data base backup using dumpdate
        * sending number of users logged in in the last 7 days
    '''

    help = 'Cleans up user accounts by sending reminders and cleaning up not activated users'

    def handle(self, *args, **options):
        '''
            Actual execution of housekeeping job
        '''
        now = datetime.now()        
        last_week = datetime.today() - timedelta(days=7)
        last_weeks_users = User.objects.filter(last_login__gte=last_week)
        no_last_weeks_users = len(last_weeks_users)

        send_mail('Account Clean Up Execution',\
                  'Account clean up task was executed on '+now.strftime("%Y-%m-%d %H:%M:%S")+\
                    '\n\nNumber of users logged in the last 7 days: '+str(no_last_weeks_users),\
                    settings.EMAIL_HOST_USER,[settings.EMAIL_HOST_USER],\
                    fail_silently=False)
        
        logger.info('account cleanup executed')      
        