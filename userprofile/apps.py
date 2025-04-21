from django.apps import AppConfig

class UserprofileConfig(AppConfig):
    name = 'userprofile'

    def ready(self):
        import userprofile.signals  # Import the signals
