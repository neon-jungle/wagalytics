from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Warning, register


def google_analytics_settings_check(app_configs, **kwargs):
    messages = []
    if not hasattr(settings, 'GA_KEY_FILEPATH'):
        messages.append(
            Warning('GA_KEYFILEPATH setting not set. Wagalytics will be disabled')
        )
    if not hasattr(settings, 'GA_VIEW_ID'):
        messages.append(
            Warning('GA_VIEW_ID setting not set. Wagalytics will be disabled')
        )
    return messages


class WagalyticsApp(AppConfig):
    name = 'wagalytics'

    def ready(self):
        register(google_analytics_settings_check)
