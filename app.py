import webScrap
from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask_jsonpify import jsonify
from flask_cors import CORS, cross_origin
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

db_connect = create_engine('mysql+mysqlconnector://root@localhost/cannabistock')
app = Flask(__name__)
cors = CORS(app)
api = Api(app)


class Employees(Resource):
    @staticmethod
    def get():
        conn = db_connect.connect()
        query = conn.execute("select * from company ")
        return {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class Quarterly_dataPL(Resource):
    @staticmethod
    def get():
        conn = db_connect.connect()
        query = conn.execute("select * from quarterly_dataPL  ")
        return {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class Quarterly_dataBS(Resource):
    @staticmethod
    def get():
        conn = db_connect.connect()
        query = conn.execute("select * from quarterly_dataBS  ")
        return {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

class Quarterly_dataCF(Resource):
    @staticmethod
    def get():
        conn = db_connect.connect()
        query = conn.execute("select * from quarterly_dataCF  ")
        return {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from company where id =%d " % int(employee_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Employees, '/api')
api.add_resource(Quarterly_dataPL, '/api_pl')
api.add_resource(Quarterly_dataBS, '/api_bs')
api.add_resource(Quarterly_dataCF, '/api_cf')
api.add_resource(Employees_Name, '/api/<employee_id>')

executors = {
    'default': ThreadPoolExecutor(16),
    'processpool': ProcessPoolExecutor(4)
}

sched = BackgroundScheduler(timezone='Asia/Seoul', executors=executors)

def job():
    webScrap.web_scraping()

sched.add_job(job, 'interval', minutes=60)

if __name__ == '__main__':
    sched.start()
    app.run(debug=True) 
    app.run()

 
