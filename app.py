from flask import Flask

from config import Config
from db import init_db
from routes.sms import sms_bp
from routes.web import web_bp

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(sms_bp)
app.register_blueprint(web_bp)
init_db(app)

if __name__ == "__main__":
    app.run(debug=True)