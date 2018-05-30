from setuptools import setup, find_packages

setup(
    name="instrument_history_api",
    version="1.0.0.dev",
    long_description=__doc__,
    install_requires = [
        "warcat",
        "pandas",
        "django",
        "djangorestframework",
        'django-filter',
        "lxml",
        "scrapy",
        "pytz",
        "requests",
        "service-identity"  # required to avoid errors with scrapy?
    ],
    packages=find_packages()
)