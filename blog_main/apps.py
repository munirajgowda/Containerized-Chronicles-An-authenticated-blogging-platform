from django.apps import AppConfig


class OtpAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_main'
    
    def ready(self):
        import blog_main.signals
