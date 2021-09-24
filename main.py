from flask import Flask
from flask_restful import Resource, Api
from production_state_handler import ProductionStateHandler,RuntimeAndDowntimeHandler,AverageBeltValueHandler


app = Flask(__name__)
api = Api(app)

api.add_resource(ProductionStateHandler, '/api/machine/production-count')
api.add_resource(RuntimeAndDowntimeHandler, '/api/machine/runtime-downtime')
api.add_resource(AverageBeltValueHandler, '/api/machine/average-beltvalue')


if __name__ == '__main__':
    app.run(debug=True,port=8080)
 