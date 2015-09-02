from django.test import TestCase as DjangoTestCase


class ContextPreprocessorTestCase(DjangoTestCase):
    fixtures = ['sitesettings_tests.json']

    def test_context_has_settings(self):
        response = self.client.get('/')
        for context in response.context:
            self.assertTrue('settings' in context)
