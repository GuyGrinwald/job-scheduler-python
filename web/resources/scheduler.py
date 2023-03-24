from flask_restful import Resource

class Scheduler(Resource):
    def post(self):
        # hours: int, minutes: int, seconds: int, url: str
        return "post"
