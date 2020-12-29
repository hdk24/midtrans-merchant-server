from flask import jsonify

from app.routes.response import make_response


def register_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return not_found()

    @app.errorhandler(400)
    def bad_request_error(error):
        return bad_request()

    @app.errorhandler(405)
    def method_not_allowed(error):
        return make_response(code=405, message='method not allowed')

    if app.config.get('E500_ACTIVATED', True):
        @app.errorhandler(Exception)
        def internal_server_error(error):
            app.log_exception(error)
            return internal_error()


def bad_request(message=None, errors=None, code=400):
    msg = message if message is not None else 'Bad Request'
    data = {} if not errors else {'errors': errors}
    return make_response(code=code, message=msg, data=data)


def unauthorized(message=None):
    msg = message if message is not None else 'Unauthorized'
    return make_response(code=401, message=msg)


def forbidden(message=None):
    msg = message if message is not None else 'Forbidden'
    return make_response(code=403, message=msg)


def not_found(message=None):
    msg = message if message is not None else 'Not Found'
    return make_response(code=404, message=msg)


def internal_error(message=None):
    msg = message if message is not None else 'Internal Server Error'
    return make_response(code=500, message=msg)
