from flask_restful import Resource


class Health(Resource):
    """
    Health check endpoint to test the responsivness of the API
    """

    def get(self):
        return {"status": 200}
