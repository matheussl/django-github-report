django-github-report
====================

An app for report Django exceptions on Github issues.


Install
========

pip install:

    pip install django-github-report

Add this app to django installed apps:

    INSTALLED_APPS = (
        ...
        'github_report',
    )

Add GITHUB_USER, GITHUB_TOKEN and GITHUB_REPOSITORY_NAME settings:

    GITHUB_USER = 'matheussl'                       # set you github user
    GITUB_TOKEN = 'token here'                      # set your github token
    GITHUB_REPOSITORY_NAME = 'django-github-report' # set your repository name

Add the GithubIssueHandler to logging:

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'github_report': {              # <\-----------------------
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'github_report.log.GithubIssueHandler'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins', 'github_report'], # <\-------
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }
