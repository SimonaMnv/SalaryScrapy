# https://devcenter.heroku.com/articles/runtime-principles#web-servers
# The port to bind to is assigned by Heroku as the PORT environment variable.
import io
import os

PORT = os.environ['PORT']
with io.open("scrapyd.conf", 'r+', encoding='utf-8') as f:
    f.read()
    f.write(u'\nhttp_port = %s\n' % PORT)
