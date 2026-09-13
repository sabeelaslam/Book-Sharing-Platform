from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timezone

# Load the current logged-in user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Member')
    is_blocked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Relationships
    books = db.relationship('Book', backref='owner', lazy=True)
    requests = db.relationship('BorrowRequest', backref='borrower', lazy=True)

class Book(db.Model):
    __tablename__ = 'books'
    
    book_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    cover_url = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(50), nullable=False) 
    owner_notes = db.Column(db.Text, nullable=True) 
    digital_link = db.Column(db.Text, nullable=True) 
    book_status = db.Column(db.String(50), nullable=False, default='Available')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Relationship
    requests = db.relationship('BorrowRequest', backref='book', lazy=True)

class BorrowRequest(db.Model):
    __tablename__ = 'borrow_requests'
    
    request_id = db.Column(db.Integer, primary_key=True)
    borrower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    request_status = db.Column(db.String(50), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    accepted_at = db.Column(db.DateTime, nullable=True)
    returned_at = db.Column(db.DateTime, nullable=True)
    proposed_date = db.Column(db.String(50), nullable=True)
    proposed_time = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=True)
    is_proposed = db.Column(db.Boolean, default=False)