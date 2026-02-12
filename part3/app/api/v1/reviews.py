from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.hbnb_facade import HBnBFacade

reviews_api = Namespace("reviews", description="Reviews operations")
facade = HBnBFacade()

review_model = reviews_api.model("Review", {
    "id": fields.String(readonly=True),
    "text": fields.String(required=True),
    "rating": fields.Integer,
    "user_id": fields.String,
    "place_id": fields.String,
})

@reviews_api.route("/")
class ReviewList(Resource):
    @reviews_api.marshal_list_with(review_model)
    def get(self):
        place_id = request.args.get("place_id")
        if place_id:
            return facade.get_reviews_by_place(place_id)
        return facade.get_reviews()

    @reviews_api.expect(review_model, validate=True)
    @reviews_api.marshal_with(review_model, code=201)
    @jwt_required()
    def post(self):
        data = request.get_json() or {}
        user_id = get_jwt_identity()
        review = facade.create_review(
            text=data.get("text"),
            rating=data.get("rating"),
            user_id=user_id,
            place_id=data.get("place_id"),
        )
        return review, 201

@reviews_api.route("/<string:review_id>")
class ReviewItem(Resource):
    @reviews_api.marshal_with(review_model)
    def get(self, review_id):
        review = facade.get_review(review_id)
        if review is None:
            reviews_api.abort(404, "Review not found")
        return review

    @reviews_api.expect(review_model, validate=True)
    @reviews_api.marshal_with(review_model)
    def put(self, review_id):
        data = request.get_json() or {}
        review = facade.update_review(review_id, **data)
        if review is None:
            reviews_api.abort(404, "Review not found")
        return review

    def delete(self, review_id):
        ok = facade.delete_review(review_id)
        if not ok:
            reviews_api.abort(404, "Review not found")
        return {"message": "Review deleted"}, 200
