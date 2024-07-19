from flask import jsonify, make_response

class APIResponse:
    @classmethod
    def respond(cls, data=None, error=None):
        response_data = {}
        if data is not None:
            response_data['data'] = data
        if error is not None:
            response_data['error'] = error
        return make_response(jsonify(response_data), 200 if data else 400)
