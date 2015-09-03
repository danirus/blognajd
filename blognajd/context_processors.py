from django.contrib.sites.models import Site
from blognajd.conf import settings as _settings
from blognajd.models import DefaultSiteSettings


def settings(request):
    """
    Adds configuration information to the context.

    To employ, add the conf method reference to your project
    settings TEMPLATE_CONTEXT_PROCESSORS.

    Example:
        TEMPLATE_CONTEXT_PROCESSORS = (
            ...
            "blognajd.context_processors.settings",
        )
    """
    return {
        'settings': _settings,
        'usersettings': DefaultSiteSettings(),
        'baseurl': '{0}://{1}'.format(
            request.META.get('wsgi.url_scheme', 'http'),
            Site.objects.get_current().domain)
    }
