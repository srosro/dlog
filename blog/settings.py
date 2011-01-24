#Blog settings
PING_DIRECTORIES = ()
SAVE_PING_DIRECTORIES = bool(PING_DIRECTORIES)

COPYRIGHT = 'Your Name'

PAGINATION = 10
ALLOW_EMPTY = True
ALLOW_FUTURE = True

MAIL_COMMENT = True
AKISMET_COMMENT = True
UPLOAD_TO = 'uploads'

PINGBACK_CONTENT_LENGTH = 300

F_MIN = 0.1
F_MAX = 1.0
USE_BITLY = False

try:
    import twitter
    USE_TWITTER = True
except ImportError:
    USE_TWITTER = False

TWITTER_USER = ''
TWITTER_PASSWORD = ''

#Disqus (optional)
DISQUS_SHORTNAME = ''

STATUS_CHOICES = {
                'Draft': 0,
                'Hidden': 1,
                'Published': 2}