import os
import sys

def setup_django_settings():
    sys.path.insert(0, os.getcwd())
    os.environ["DJANGO_SETTINGS_MODULE"] = "blognajd.tests.settings"


def run_tests():
    if not os.environ.get("DJANGO_SETTINGS_MODULE", False):
        setup_django_settings()

    import django
    from django.conf import settings
    from django.test.utils import get_runner
    from blognajd.tests import delete_tmp_dirs

    if django.VERSION[1] >= 7: # Django 1.7.x or above
        django.setup()
        runner = get_runner(settings,"django.test.runner.DiscoverRunner")
    else:
        runner = get_runner(settings,"django.test.simple.DjangoTestSuiteRunner")
    test_suite = runner(verbosity=2, interactive=True, failfast=False)
    # results = test_suite.run_tests(["blognajd"])
    results = test_suite.run_tests(["blognajd"])
    delete_tmp_dirs()
    return results


if __name__ == "__main__":
    run_tests()
