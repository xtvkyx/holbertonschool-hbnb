from flask_restx import Namespace, Resource

ns = Namespace("users", description="Users operations")

@ns.route("/")
class UserList(Resource):
    def get(self):
        return {"message": "Users endpoint working"}, 200
