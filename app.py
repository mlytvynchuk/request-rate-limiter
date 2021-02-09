from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, request, Response, jsonify, make_response

rate_limits = {}


def limit_rate_request(rate_limit=100):
    def _limit_rate_request(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            global rate_limits
            endpoint = request.endpoint
            if endpoint not in rate_limits \
                    or ('expiration_date' in rate_limits[endpoint] and rate_limits[endpoint]['expiration_date']
                        < datetime.now()):
                rate_limits[endpoint] = {}
                rate_limits[endpoint]['remaining'] = rate_limit - 1
                rate_limits[endpoint]['expiration_date'] = datetime.now() + timedelta(hours=1)

            if rate_limits[endpoint]['remaining'] == 0:
                result = make_response(jsonify({'message': f'You used all {rate_limit} requests per hours'}), 403)
            else:
                result = f(*args, **kwargs)
            result.headers.add_header('X-RateLimit-Limit', rate_limit)
            result.headers.add_header('X-RateLimit-Remaining', rate_limits[endpoint]['remaining'])
            if rate_limits[endpoint]['remaining'] > 0:
                rate_limits[endpoint]['remaining'] -= 1
            return result

        return wrapper

    return _limit_rate_request


app = Flask(__name__)


@app.route('/')
@limit_rate_request()
def first_route() -> Response:
    return make_response(jsonify({
        'message': 'First route'
    }), 200)


@app.route('/second')
@limit_rate_request(rate_limit=50)
def second_route() -> Response:
    return make_response(jsonify({
        'message': 'Second route'
    }), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
