import logging
import traceback

from django.conf import settings
from django.views.debug import get_exception_reporter_filter

from github import Github

from .conf import conf

getLogger = logging.getLogger
logger = getLogger('django.request')

if not logger.handlers:
    logger.addHandler(NullHandler())


class GithubIssueHandler(logging.Handler):
    """An exception log handler that create Github issues.

    If the request is passed as the first argument to the log record,
    request data will be provided in Github issue.
    """

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        try:
            request = record.request
            title = '%s (%s IP): %s' % (
                record.levelname,
                (request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS
                 and 'internal' or 'EXTERNAL'),
                record.getMessage()
            )
            filter = get_exception_reporter_filter(request)
            request_repr = filter.get_request_repr(request)
        except Exception:
            title = '%s: %s' % (
                record.levelname,
                record.getMessage()
            )
            request = None
            request_repr = "Request repr() unavailable."
        title = self.format_title(title)

        if record.exc_info:
            exc_info = record.exc_info
            stack_trace = '\n'.join(traceback.format_exception(*record.exc_info))
        else:
            exc_info = (None, record.getMessage(), None)
            stack_trace = 'No stack trace available'

        message = "%s\n\n%s" % (stack_trace, request_repr)

        # create github issue

        github = Github(conf.GITHUB_TOKEN)
        user = github.get_user(conf.GITHUB_USER)
        repository = user.get_repo(conf.GITHUB_REPOSITORY_NAME)
        issue = repository.create_issue(self, title, body=message)



    def format_title(self, title):
        """
        Escape CR and LF characters, and limit length.
        RFC 2822's hard limit is 998 characters per line. So, minus "Title: "
        the actual title must be no longer than 989 characters.
        """
        formatted_title = title.replace('\n', '\\n').replace('\r', '\\r')
        return formatted_title[:989]
