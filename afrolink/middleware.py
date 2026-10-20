from django.utils import translation


class SubdomainLanguageMiddleware:
    """
    Force German on de.* hosts. Otherwise leave language to LocaleMiddleware
    (cookie from the nav language switcher).
    """

    SUBDOMAIN_LANGUAGE_MAP = {
        'de': 'de',
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':', 1)[0].lower()
        subdomain = host.split('.', 1)[0]
        forced = self.SUBDOMAIN_LANGUAGE_MAP.get(subdomain)

        if forced:
            translation.activate(forced)
            request.LANGUAGE_CODE = forced

        response = self.get_response(request)

        if forced:
            response['Content-Language'] = forced
        elif not response.get('Content-Language'):
            response['Content-Language'] = translation.get_language() or 'en'

        return response
