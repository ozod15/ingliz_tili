from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from verbs.models import UserProfile


class Command(BaseCommand):
    help = 'Create default users (test and admin)'

    def handle(self, *args, **options):
        # Create test user
        if not User.objects.filter(username='test').exists():
            test_user = User.objects.create_user(
                username='test',
                password='test',
                is_staff=False
            )
            UserProfile.objects.create(user=test_user)
            self.stdout.write(self.style.SUCCESS('Created test user (username: test, password: test)'))
        else:
            self.stdout.write('Test user already exists')
        
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                password='admin',
                is_staff=True,
                is_superuser=True
            )
            UserProfile.objects.create(user=admin_user)
            self.stdout.write(self.style.SUCCESS('Created admin user (username: admin, password: admin)'))
        else:
            self.stdout.write('Admin user already exists')
