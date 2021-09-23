import datetime
import json
 
class ProductionStateService:

    def __init__(self,file_name:str) -> None:
        with open(file_name) as f:
            self.data = json.load(f)
        self._convert_datetime()

    def _convert_datetime(self):
        for i in range(len(self.data)):
            self.data[i]['time'] = datetime.datetime.fromisoformat(self.data[i]['time'])
    
    def all_data(self):
        return self.data

    def _check_shift(self,time):

        if time.hour >= 6 and time.hour < 14:
            return 'shiftA'

        elif time.hour >= 14 and time.hour < 20:
            return 'shiftB'
            
        else:
            return 'shiftC'
  
    def calculate_shift_count_range(self,input_range):
        data = {
                "shiftA" :{ "production_A_count" :0, "production_B_count" :0},
                "shiftB" :{ "production_A_count" :0, "production_B_count" :0},
                "shiftC" :{ "production_A_count" :0, "production_B_count" :0},
                }

        for d in self.data:
            if d['time'] >= input_range['start_time'] and d['time'] <= input_range['end_time']:
                shift_name = self._check_shift(d['time'])
                if d['production_A']:
                    data[shift_name]['production_A_count'] = data[shift_name]['production_A_count'] + 1
                
                if d['production_B']:
                    data[shift_name]['production_B_count'] = data[shift_name]['production_B_count'] + 1

        return data


class RuntimeAndDowntimeService:
    def __init__(self,file_name:str) -> None:
        with open(file_name) as f:
            self.data = json.load(f)
        self._convert_datetime()

    def _convert_datetime(self):
        for i in range(len(self.data)):
            self.data[i]['time'] = datetime.datetime.fromisoformat(self.data[i]['time'])
    
    def all_data(self):
        return self.data

    def calculate_runtime_downtime(self,input_range):

        data ={
            "runtime" : 0,
            "downtime" : 0,
            "utilisation" : 0
        }

        for d in self.data:

            if d['time'] >= input_range['start_time'] and d['time'] <= input_range['end_time']:

                if d['runtime'] <= 1021 :
                    data['runtime'] = data['runtime'] + d['runtime']
                    
                elif d['runtime'] > 1021 :
                    data['runtime'] = data['runtime'] + 1021
                    data['downtime'] = data['downtime'] + d['runtime'] - 1021
                
                data['utilisation'] =(data['runtime']/(data['runtime']+data['downtime']))*100

        data['runtime'] = str(datetime.timedelta(seconds=int(data['runtime'])))
        data['downtime'] = str(datetime.timedelta(seconds= int(data['downtime'])))

        return data


class AverageBeltValueService:
    def __init__(self,file_name:str) -> None:
        with open(file_name) as f:
            self.data = json.load(f)
        self._convert_datetime()
        self._convert_string()

    def _convert_datetime(self):
        for i in range(len(self.data)):
            self.data[i]['time'] = datetime.datetime.fromisoformat(self.data[i]['time'])
    
    def _convert_string(self):
        for i in range(len(self.data)):
            self.data[i]['id'] = int("".join(filter(lambda i: i.isdigit(),self.data[i]['id'])))

    def all_data(self):
        return self.data

    def calculate_average_belt_value(self,input_range):

        data = []

        for d in self.data:

            if d['time'] >= input_range['start_time'] and d['time'] <= input_range['end_time']:

                if d['state']:
                    data.append({"id" : d['id'],"avg_belt1" : 0,"avg_belt2" : d['belt2']})

                elif not d['state']:
                    data.append({"id" : d['id'],"avg_belt1" : d['belt1'],"avg_belt2" : 0})



        sorted_data = sorted(data, key=lambda k: k['id'])
        return sorted_data




production_state_service = ProductionStateService('data/sample_1.json')
runtime_downtime_service = RuntimeAndDowntimeService('data/sample_2.json')
average_belt_value_service = AverageBeltValueService('data/sample_3.json')

