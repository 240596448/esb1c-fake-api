from flask import Flask
from app.routes import bp


srv = Flask(__name__)
srv.register_blueprint(bp)


if __name__ == '__main__':
    srv.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False,
        )
