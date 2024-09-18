from flask import Flask

from config import Config
from db import init_db
from routes.sms import sms_bp

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(sms_bp)

init_db(app)

if __name__ == "__main__":
    app.run(debug=True)