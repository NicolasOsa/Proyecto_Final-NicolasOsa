from django.apps import AppConfig


class ClinicatandilConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ClinicaTandil'
    
    def ready(self):
        import ClinicaTandil.signals

