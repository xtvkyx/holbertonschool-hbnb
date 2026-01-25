from flask_restx import Namespace, Resource, fields
from hbnb.facade import get_facade

facade = get_facade()

reviews_ns = Namespace("reviews", description="Review operations")

review_model = reviews_ns.model(
    "Review",
    {
        "id": fields.String(readOnly=True),
        "user_id": fields.String(required=True),
        "place_id": fields.String(required=True),
        "rating": fields.Integer(required=True),
        "comment": fields.String(required=True),
    },
)

review_create_model = reviews_ns.model(
    "ReviewCreate",
    {
        "user_id": fields.String(required=True),
        "place_id": fields.String(required=True),
        "rating": fields.Integer(required=True),
        "comment": fields.String(required=True),
    },
)

review_update_model = reviews_ns.model(
    "ReviewUpdate",
    {
        "rating": fields.Integer(required=False),
        "comment": fields.String(required=False),
    },
)


@reviews_ns.route("")
class ReviewListResource(Resource):
    @reviews_ns.marshal_list_with(review_model)
    def get(self):
        return facade.get_reviews(), 200

    @reviews_ns.expect(review_create_model, validate=True)
    @reviews_ns.marshal_with(review_model, code=201)
    def post(self):
        data = reviews_ns.payload or {}
        try:
            return facade.create_review(data), 201
        except KeyError as e:
            reviews_ns.abort(404, str(e))
        except ValueError as e:
            reviews_ns.abort(400, str(e))


@reviews_ns.route("/<string:review_id>")
@reviews_ns.param("review_id", "Review identifier")
class ReviewResource(Resource):
    @reviews_ns.marshal_with(review_model)
    def get(self, review_id):
        review = facade.get_review(review_id)
        if review is None:
            reviews_ns.abort(404, "Review not found")
        return review, 200

    @reviews_ns.expect(review_update_model, validate=True)
    @reviews_ns.marshal_with(review_model)
    def put(self, review_id):
        data = reviews_ns.payload or {}
        try:
            return facade.update_review(review_id, data), 200
        except KeyError as e:
            reviews_ns.abort(404, str(e))
        except ValueError as e:
            reviews_ns.abort(400, str(e))

    def delete(self, review_id):
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted"}, 200
        except KeyError as e:
            reviews_ns.abort(404, str(e))
        except ValueError as e:
            reviews_ns.abort(400, str(e))
