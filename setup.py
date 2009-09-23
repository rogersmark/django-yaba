from setuptools import setup, find_packages
 
setup(
    name = "django-yaba",
    version = "0.2",
    author = "Mark Rogers",
    author_email = "f4nt@f4ntasmic.com",
    url = "http://www.f4ntasmic.com",
    
    packages = find_packages('src'),
    package_dir = {'':'src'},
    package_data = {
        '': ['*.html']
    },
    include_package_data=True,
    license = "BSD License",
    keywords = "django yaba blog",
    description = "Yet Another Blog Application",
    install_requires=[
        'setuptools',
        'python-twitter',
        'twitter',
        'simplejson',
        'Django',
        'South',
        'feedparser',
        'django_test_extensions',
        'django-disqus',
        'django-tagging',
    ],
    classifiers = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        'Programming Language :: Python',
    ]
)
