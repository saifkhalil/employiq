import environ
env = environ.Env()

try:
    from urllib.parse import urlencode
    from urllib.request import build_opener, Request, HTTPHandler
    from urllib.error import HTTPError, URLError
except ImportError:
    from urllib import urlencode
    from urllib2 import build_opener, Request, HTTPHandler, HTTPError, URLError
import json


def checkout(amount):
    env_url = env('APP_ENV')
    url = f"{env(f'{env_url}_PAYMENT_URL')}/v1/checkouts"
    data = {
        'entityId': env(f'{env_url}_ENTITY_ID'),
        'amount': f"{amount}",
        'currency': env(f'{env_url}_CURRENCY'),
        'paymentType': 'DB'
    }
    try:
        opener = build_opener(HTTPHandler)
        request = Request(url, data=urlencode(data).encode('utf-8'))
        request.add_header('Authorization', f"Bearer {env(f'{env_url}_CHECKOUT_TOKEN')}")
        request.get_method = lambda: 'POST'
        response = opener.open(request)
        return json.loads(response.read())
    except HTTPError as e:
        return json.loads(e.read())
    except URLError as e:
        return e.reason


def payment_check(checkout_id):
    env_url = env('APP_ENV')
    url = f"{env(f'{env_url}_PAYMENT_URL')}/v1/checkouts/{checkout_id}/payment?entityId={env(f'{env_url}_ENTITY_ID')}"
    try:
        opener = build_opener(HTTPHandler)
        request = Request(url, data=b'')
        request.add_header('Authorization', f"Bearer {env(f'{env_url}_CHECKOUT_TOKEN')}")
        request.get_method = lambda: 'GET'
        response = opener.open(request)
        return json.loads(response.read())
    except HTTPError as e:
        return json.loads(e.read())
    except URLError as e:
        return e.reason
