from flask import Flask
import os


def create_app():
	app = Flask(__name__)
	app.config.from_object(Config())
	
	from main import main
	app.register_blueprint(main)

	return app


class Config:
	SECRET_KEY = os.urandom(24)


app = create_app()

if __name__ == '__main__':
	app.run(debug=False)


