try:
    from urllib.parse import urlencode
    from urllib.request import build_opener, Request, HTTPHandler
    from urllib.error import HTTPError, URLError
except ImportError:
    from urllib import urlencode
    from urllib2 import build_opener, Request, HTTPHandler, HTTPError, URLError
import json


def checkout(amount):
    url = "https://test.oppwa.com/v1/checkouts"
    data = {
        'entityId': '8a8294174d0595bb014d05d82e5b01d2',
        'amount': f'{amount}',
        'currency': 'USD',
        'paymentType': 'DB'
    }
    try:
        opener = build_opener(HTTPHandler)
        request = Request(url, data=urlencode(data).encode('utf-8'))
        request.add_header('Authorization', 'Bearer OGE4Mjk0MTc0ZDA1OTViYjAxNGQwNWQ4MjllNzAxZDF8OVRuSlBjMm45aA==')
        request.get_method = lambda: 'POST'
        response = opener.open(request)
        return json.loads(response.read())
    except HTTPError as e:
        return json.loads(e.read())
    except URLError as e:
        return e.reason


def payment_check(checkout_id):
    url = f"https://test.oppwa.com/v1/checkouts/{checkout_id}/payment"
    url += '?entityId=8a8294174d0595bb014d05d82e5b01d2'
    try:
        opener = build_opener(HTTPHandler)
        request = Request(url, data=b'')
        request.add_header('Authorization', 'Bearer OGE4Mjk0MTc0ZDA1OTViYjAxNGQwNWQ4MjllNzAxZDF8OVRuSlBjMm45aA==')
        request.get_method = lambda: 'GET'
        response = opener.open(request)
        return json.loads(response.read())
    except HTTPError as e:
        return json.loads(e.read())
    except URLError as e:
        return e.reason
