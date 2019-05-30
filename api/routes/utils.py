def json_response(response, code):
    from flask import make_response
    resp = make_response(response.to_json(), code)
    resp.headers['Content-Type'] = "application/json"
    return resp
