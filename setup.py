from setuptools import setup

setup(
    name = "django-limehouse",
    url = "http://github.com/sebleier/django-limehouse/",
    author = "Sean Bleier",
    author_email = "sebleier@gmail.com",
    version = "0.0.1",
    packages = ["limehouse"],
    description = "Client-side template rendering with a pjaxy flavor for django.",
    install_requires=['django>=1.3'],
    classifiers = [
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
)
