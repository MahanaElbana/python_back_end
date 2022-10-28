from django.apps import AppConfig


class AuthUserAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_user_app'
    
    
    # 3- call signal function to execute when listening for the creation of a User model.
    def ready(self):
        # i added it for signals
        '''
        If you provide an AppConfig instance as the sender argument,
        please ensure that the signal is registered in ready().
        AppConfigs are recreated for tests that run with a modified 
        set of INSTALLED_APPS (such as when settings are overridden)
        and such signals should be connected for each new AppConfig instance.
        '''
        import auth_user_app.signals