import logging

import requests

LOG = logging.getLogger(__name__)


def resp_to_string(resp):
    # format the request
    msg = '\n-------------------- REQUEST --------------------'
    msg += "\n{0} {1}".format(resp.request.method, resp.request.url)
    for k, v in resp.request.headers.items():
        msg += "\n{0}: {1}".format(k, v)
    if resp.request.body:
        msg += "\n{0}".format(resp.request.body)
    else:
        msg += "\n<empty-body>"

    msg += "\n"

    # format the response
    msg += '\n-------------------- RESPONSE --------------------'
    msg += "\n{0} {1}".format(resp.status_code, resp.reason)
    for k, v in resp.headers.items():
        msg += "\n{0}: {1}".format(k, v)

    CHAR_LIMIT = 2000
    clean_text = resp.text.strip()
    if len(clean_text) > CHAR_LIMIT:
        clean_text = clean_text[:CHAR_LIMIT] + '... <TRUNCATED>'

    msg += "\n\n{0}".format(clean_text)
    return msg


def do_request(method, url, data=None, params=None, headers=None,
               allow_redirects=False):
    resp = requests.request(method, url, data=data, params=params,
                            headers=headers, allow_redirects=allow_redirects)
    LOG.debug(resp_to_string(resp))
    return resp


