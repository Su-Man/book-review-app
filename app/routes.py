from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User, Review
from . import db

bp = Blueprint('routes', __name__)

@bp.route('/health')
def health():
    return jsonify({"status": "ok"})

@bp.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([{
        "id": r.id, "title": r.title, "author": r.author,
        "review": r.review, "rating": r.rating, "user_id": r.user_id
    } for r in reviews])

@bp.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    data = request.json
    user_id = get_jwt_identity()
    review = Review(
        title=data["title"],
        author=data["author"],
        review=data["review"],
        rating=data["rating"],
        user_id=user_id
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"msg": "Review added"}), 201

@bp.route('/reviews/<int:id>', methods=['PUT'])
@jwt_required()
def update_review(id):
    data = request.json
    review = Review.query.get_or_404(id)
    user_id = get_jwt_identity()
    if review.user_id != user_id:
        return jsonify({"msg": "Not allowed"}), 403
    review.title = data.get("title", review.title)
    review.author = data.get("author", review.author)
    review.review = data.get("review", review.review)
    review.rating = data.get("rating", review.rating)
    db.session.commit()
    return jsonify({"msg": "Review updated"})

@bp.route('/reviews/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_review(id):
    review = Review.query.get_or_404(id)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if review.user_id != user_id and not user.is_admin:
        return jsonify({"msg": "Not allowed"}), 403
    db.session.delete(review)
    db.session.commit()
    return jsonify({"msg": "Review deleted"})

@bp.route('/admin/users', methods=['GET'])
@jwt_required()
def list_users():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user.is_admin:
        return jsonify({"msg": "Admins only"}), 403
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "is_admin": u.is_admin} for u in users])
