from flask import current_app
import json
import codecs
import os
import twitter
import pytz
from datetime import datetime

try:
    from instagram_private_api import (
        Client, ClientError, ClientCompatPatch, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientCompatPatch, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)


def ig_login(currentUser):

    device_id = None
    try:
        settings_file = os.path.join(
            current_app.root_path, 'cookies', currentUser['username'])
        if not os.path.isfile(settings_file):
            # settings file does not exist

            # login new
            api = Client(
                currentUser['ig-username'], currentUser['ig-password'],
                on_login=lambda x: onlogin_callback(x, settings_file))
        else:
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data, object_hook=from_json)

            device_id = cached_settings.get('device_id')
            # reuse auth settings
            api = Client(
                currentUser['ig-username'], currentUser['ig-password'],
                settings=cached_settings)

    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print(
            'ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

        # Login expired
        # Do relogin but use default ua, keys and such
        api = Client(
            currentUser['ig-username'], currentUser['ig-password'],
            device_id=device_id,
            on_login=lambda x: onlogin_callback(x, settings_file))

    except ClientLoginError as e:
        print('ClientLoginError {0!s}'.format(e))
        exit(9)
    except ClientError as e:
        print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(
            e.msg, e.code, e.error_response))
        exit(9)
    except Exception as e:
        print('Unexpected Exception: {0!s}'.format(e))
        exit(99)

    # Call the api
    lst = []
    posts = api.feed_timeline()
    items = [item for item in posts.get('feed_items', [])
             if item.get('media_or_ad')]
    tz = pytz.timezone('America/New_York')
    for item in items:
        ClientCompatPatch.media(item['media_or_ad'])
        ig_post = {'Platform': 'Instagram',
                   'Date': convert_time(tz, item['media_or_ad']['taken_at']),
                   'Link': 'https://www.instagram.com/p/' + str(item['media_or_ad']['code'])}
        ig_post_copy = ig_post.copy()
        lst.append(ig_post_copy)
    return lst


def login_twitter(currentUser):
    lst = []
    api = twitter.Api(consumer_key=currentUser['twitter-consumer_key'],
                      consumer_secret=currentUser['twitter-consumer_secret'],
                      access_token_key=currentUser['twitter-access_token_key'],
                      access_token_secret=currentUser['twitter-access_token_secret'])
    tz = pytz.timezone('America/New_York')
    statuses = api.GetHomeTimeline()
    for s in statuses:
        tweets = {'Platform': 'Twitter',
                  'Date': convert_time(tz, s.created_at_in_seconds),
                  'Link': 'https://twitter.com/placeholder/status/' + s.id_str}
        tweets_copy = tweets.copy()
        lst.append(tweets_copy)
    return lst


def convert_time(tz, post_time):
    return datetime.fromtimestamp(post_time, tz).isoformat()
