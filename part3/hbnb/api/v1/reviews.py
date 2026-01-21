from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from hbnb.extensions import db
from hbnb.models.review import Review
from hbnb.models.place import Place

reviews_bp = Blueprint("reviews", __name__)

@reviews_bp.get("/reviews")
def list_reviews():
    reviews = Review.query.all()
    return [r.to_dict() for r in reviews], 200

@reviews_bp.get("/reviews/<review_id>")
def get_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return {"error": "not found"}, 404
    return review.to_dict(), 200

@reviews_bp.post("/places/<place_id>/reviews")
@jwt_required()
def create_review(place_id):
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    place = Place.query.get(place_id)
    if not place:
        return {"error": "place not found"}, 404

    if place.owner_id == user_id:
        return {"error": "cannot review your own place"}, 400

    existing = Review.query.filter_by(place_id=place_id, user_id=user_id).first()
    if existing:
        return {"error": "you already reviewed this place"}, 400

    text = data.get("text")
    rating = data.get("rating")
    if not text or rating is None:
        return {"error": "text and rating required"}, 400

    review = Review(text=text, rating=rating, place_id=place_id, user_id=user_id)
    db.session.add(review)
    db.session.commit()
    return review.to_dict(), 201

@reviews_bp.put("/reviews/<review_id>")
@jwt_required()
def update_review(review_id):
    user_id = get_jwt_identity()
    review = Review.query.get(review_id)
    if not review:
        return {"error": "not found"}, 404

    if review.user_id != user_id:
        return {"error": "forbidden"}, 403

    data = request.get_json() or {}
    data.pop("user_id", None)
    data.pop("place_id", None)

    if "text" in data:
        review.text = data["text"]
    if "rating" in data:
        review.rating = data["rating"]

    db.session.commit()
    return review.to_dict(), 200

@reviews_bp.delete("/reviews/<review_id>")
@jwt_required()
def delete_review(review_id):
    user_id = get_jwt_identity()
    review = Review.query.get(review_id)
    if not review:
        return {"error": "not found"}, 404

    if review.user_id != user_id:
        return {"error": "forbidden"}, 403

    db.session.delete(review)
    db.session.commit()
    return {"message": "deleted"}, 200
