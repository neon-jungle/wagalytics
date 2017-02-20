from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from oauth2client.service_account import ServiceAccountCredentials


def get_access_token():
    # from https://ga-dev-tools.appspot.com/embed-api/server-side-authorization/
    # Defines a method to get an access token from the credentials object.
    # The access token is automatically refreshed if it has expired.

    # The scope for the OAuth2 request.
    SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'

    # Construct a credentials objects from the key data and OAuth2 scope.
    _credentials = ServiceAccountCredentials.from_json_keyfile_name(
        settings.GA_KEY_FILEPATH, SCOPE)

    return _credentials.get_access_token().access_token


def token(request):
    if hasattr(settings, 'GA_KEY_FILEPATH'):
        # return a cached access token to ajax clients
        access_token = cache.get_or_set('ga_access_token', get_access_token, 3600)
        return HttpResponse(access_token)
    return HttpResponseServerError()


def dashboard(request):
    context = {}
    if hasattr(settings, 'GA_VIEW_ID'):
        context.update({
            'ga_view_id': settings.GA_VIEW_ID,
        })
    return render(request, 'wagalytics/dashboard.html', context)
