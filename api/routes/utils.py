def json_response(response, code):
    from flask import make_response
    resp = make_response(response.to_json(), code)
    resp.headers['Content-Type'] = "application/json"
    return resp


def format_content_range(start, end, size):
    if start is None or end is None:
        range = '*'
    else:
        range = str(start) + '-' + str(end)
    _size = '*' if size is None else str(size)
    return range + '/' + _size
