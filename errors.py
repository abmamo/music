# flask blueprint
from flask import Blueprint, render_template
# csrf error
from flask_wtf.csrf import CSRFError

errors_bp = Blueprint('errors_bp',
               __name__,
               template_folder='templates',
               static_folder='static')
               

@errors_bp.app_errorhandler(400)
def bad_request(error):
    # error code
    status_code = 400
    # return error page
    return (
        render_template("error.html", message=str(error), status_code=status_code),
        400,
    )

@errors_bp.app_errorhandler(404)
def not_found(error):
    # error code
    status_code = 404
    # return error page
    return (
        render_template("error.html", message=str(error), status_code=status_code),
        404,
    )

@errors_bp.app_errorhandler(405)
def forbidden(error):
    # error code
    status_code = 405
    # return error page
    return (
        render_template("error.html", message=str(error), status_code=status_code),
        404,
    )


@errors_bp.app_errorhandler(500)
def server_error(error):
    # error code
    status_code = 500
    # return error page
    return (
        render_template("error.html", message=str(error), status_code=status_code),
        500,
    )

@errors_bp.app_errorhandler(502)
def server_error(error):
    # error code
    status_code = 502
    # return error page
    return (
        render_template("error.html", message=str(error), status_code=status_code),
        502,
    )

@errors_bp.app_errorhandler(CSRFError)
def handle_csrf_error(e):
    return (
        render_template("error.html", message=e.description, status_code=400),
        400,
    )