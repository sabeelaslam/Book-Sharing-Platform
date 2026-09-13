from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import User, Book, BorrowRequest

# Create a blueprint named 'admin'
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required 
def admin_dashboard():
    total_users = User.query.filter(User.role != 'Admin').count()
    total_books = Book.query.count()
    return render_template('admin/admin_dashboard.html', total_users=total_users, total_books=total_books)

@admin_bp.route('/users')
@login_required
def view_users():
    active_users = User.query.filter_by(is_blocked=False).filter(User.role != 'Admin').all()
    blocked_users = User.query.filter_by(is_blocked=True).filter(User.role != 'Admin').all()
    return render_template('admin/view_users.html', active_users=active_users, blocked_users=blocked_users)

@admin_bp.route('/books')
@login_required
def view_books():
    available_books = Book.query.filter(Book.book_status != 'Borrowed').all()
    borrowed_books = Book.query.filter_by(book_status='Borrowed').all()
    return render_template('admin/view_books.html', available_books=available_books, borrowed_books=borrowed_books)

@admin_bp.route('/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    # delete requests associated with this book first
    BorrowRequest.query.filter_by(book_id=book.book_id).delete()
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully.', 'success')
    return redirect(url_for('admin.view_books'))

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'Admin':
        flash('Cannot delete an admin.', 'danger')
        return redirect(url_for('admin.view_users'))
    
    # 1. Delete all requests made by user
    BorrowRequest.query.filter_by(borrower_id=user.id).delete()

    # 2. Delete all requests made for the books owned by user
    books = Book.query.filter_by(owner_id=user.id).all()
    for book in books:
        BorrowRequest.query.filter_by(book_id=book.book_id).delete()

    # 3. Delete all books owned by this user
    Book.query.filter_by(owner_id=user.id).delete()

    # 4. Finally, delete the user
    db.session.delete(user)
    db.session.commit()
    
    flash('User and their associated books/requests deleted successfully.', 'success')
    return redirect(url_for('admin.view_users'))

@admin_bp.route('/toggle_user_block/<int:user_id>', methods=['POST'])
@login_required
def toggle_user_block(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'Admin':
        flash('Cannot block an admin.', 'danger')
    else:
        user.is_blocked = not user.is_blocked
        db.session.commit()
        status = 'blocked' if user.is_blocked else 'unblocked'
        flash(f'User successfully {status}.', 'success')
    return redirect(url_for('admin.view_users'))