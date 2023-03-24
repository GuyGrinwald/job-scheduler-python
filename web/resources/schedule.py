from flask_restful import Resource

class Schedule(Resource):
    def get(self, job_id: int):
        # hours: int, minutes: int, seconds: int, url: str
        return "get"
