from flask import Flask
from application.blueprints.routes import web

class HTB(Flask):
    def process_response(self, response):
        response.headers['Server'] = 'FlameDrake/1.0 (Infernal Engine)'
        super(HTB, self).process_response(response)
        return response

app = HTB(__name__)
app.config.from_object('application.config.Config')

app.register_blueprint(web, url_prefix='/')