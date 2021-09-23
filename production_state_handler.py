
from flask_restful import Resource,reqparse
from datetime import datetime
from service.production_state_service import production_state_service,runtime_downtime_service,average_belt_value_service


class ProductionStateHandler(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start_time', type=str)
        parser.add_argument('end_time', type=str)

        query_param = parser.parse_args()
        query_param['start_time'] = datetime.strptime(query_param['start_time'],"%Y-%m-%dT%H:%M:%SZ")
        query_param['end_time'] = datetime.strptime(query_param['end_time'],"%Y-%m-%dT%H:%M:%SZ")
        
        return production_state_service.calculate_shift_count_range(query_param)


class RuntimeAndDowntimeHandler(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start_time', type=str)
        parser.add_argument('end_time', type=str)

        query_param = parser.parse_args()
        query_param['start_time'] = datetime.strptime(query_param['start_time'],"%Y-%m-%dT%H:%M:%SZ")
        query_param['end_time'] = datetime.strptime(query_param['end_time'],"%Y-%m-%dT%H:%M:%SZ")
        
        return runtime_downtime_service.calculate_runtime_downtime(query_param)

class AverageBeltValueHandler(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start_time', type=str)
        parser.add_argument('end_time', type=str)

        query_param = parser.parse_args()
        query_param['start_time'] = datetime.strptime(query_param['start_time'],"%Y-%m-%dT%H:%M:%SZ")
        query_param['end_time'] = datetime.strptime(query_param['end_time'],"%Y-%m-%dT%H:%M:%SZ")
        
        return average_belt_value_service.calculate_average_belt_value(query_param)