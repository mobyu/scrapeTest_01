from mitmproxy import ctx


def response(flow):
    # flow.request.headers['User-Agent'] = 'MitmProxy'
    print(flow.request.url)
    print(flow.response.text)
