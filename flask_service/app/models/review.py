from datetime import datetime, timezone

from app.extensions import db

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.String(16),
        nullable=False,
        default='pending',
        server_default='pending'
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=db.func.now()
    )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'text': self.text,
            'status': self.status,
            'created_at': self.created_at.isoformat() + 'Z'
            if self.created_at is not None
            else None,
        }
