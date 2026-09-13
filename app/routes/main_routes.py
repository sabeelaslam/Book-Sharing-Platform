from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from app.models import Book, BorrowRequest, User
from app import db
from datetime import datetime, timedelta, timezone

bp = Blueprint('main', __name__)

@bp.before_request
def auto_return_digital_books():
    # Find all accepted digital book requests where 7 days have passed since acceptance
    if current_user.is_authenticated:
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        expired_requests = BorrowRequest.query.join(Book).filter(
            Book.type == 'Digital',
            BorrowRequest.request_status == 'Accepted',
            BorrowRequest.accepted_at <= seven_days_ago
        ).all()
        
        if expired_requests:
            for req in expired_requests:
                req.request_status = 'Returned'
                req.returned_at = datetime.now(timezone.utc)
            db.session.commit()

@bp.route('/home', methods=['GET'])
def home():
    search_by = request.args.get('search_by', '')
    search_query = request.args.get('search_query', '')
    
    query = Book.query.filter(Book.book_status == 'Available')
    
    if search_query:
        if search_by == 'title':
            query = query.filter(Book.title.ilike(f'%{search_query}%'))
        elif search_by == 'author':
            query = query.filter(Book.author.ilike(f'%{search_query}%'))
        elif search_by == 'category':
            query = query.filter(Book.category.ilike(f'%{search_query}%'))
        else:
            query = query.filter(
                (Book.title.ilike(f'%{search_query}%')) | 
                (Book.author.ilike(f'%{search_query}%')) | 
                (Book.category.ilike(f'%{search_query}%'))
            )
            
    books = query.order_by(Book.created_at.desc()).all()
    return render_template('main/home.html', user=current_user, books=books, search_by=search_by, search_query=search_query)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username:
            current_user.username = username
        if password:
            current_user.password = generate_password_hash(password)

        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('main.profile'))

    return render_template('main/profile.html', user=current_user)

@bp.route('/add_book', methods=['GET','POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        category = request.form.get('category')
        book_type = request.form.get('type')
        owner_notes = request.form.get('availability_notes')
        cover_url = request.form.get('cover_url')
        if book_type == 'Digital':
            link = request.form.get('digital_link')
            if link:
                digital_link = link
            else:
                file = request.files.get('digital_file')
                if file and file.filename != '':
                    # Save the uploaded file to a secure location
                    filename = f"{current_user.id}_{file.filename}"
                    file_path = f"static/books/{filename}"
                    file.save(file_path)
                    digital_link = url_for('static', filename=f'books/{filename}', _external=True)
                else:
                    flash('Please provide a digital link or upload a file for digital books.', 'danger')
                    return redirect(url_for('main.add_book'))
        else:
            digital_link = None

        new_book = Book(
            owner_id=current_user.id,
            title=title,
            author=author,
            category=category,
            type=book_type,
            owner_notes=owner_notes,
            digital_link=digital_link,
            cover_url=cover_url,
            book_status='Available'
        )
        db.session.add(new_book)
        db.session.commit()
        flash(f'Book "{title}" has been added to your collection!', 'success')
        return redirect(url_for('main.my_books'))

    return render_template('main/add_book.html')

@bp.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    if book.owner_id != current_user.id:
        flash('Permission denied.', 'danger')
        return redirect(url_for('main.my_books'))
        
    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.category = request.form.get('category')
        book.type = request.form.get('type')
        book.cover_url = request.form.get('cover_url')
        
        if book.type == 'Physical':
            book.owner_notes = request.form.get('availability_notes')
            book.digital_link = None
        else:
            book.owner_notes = None
            link = request.form.get('digital_link')
            file = request.files.get('digital_file')
            
            if link:
                book.digital_link = link
            elif file and file.filename != '':
                filename = f"{current_user.id}_edit_{file.filename}"
                file_path = f"static/books/{filename}"
                file.save(file_path)
                book.digital_link = url_for('static', filename=f'books/{filename}', _external=True)
                
            elif not book.digital_link:
                flash('Please provide a digital link or upload a file for digital books.', 'danger')
                return redirect(url_for('main.edit_book', book_id=book.book_id))

        db.session.commit()
        flash(f'Book "{book.title}" updated successfully!', 'success')
        return redirect(url_for('main.my_books'))

    return render_template('main/edit_book.html', book=book)

@bp.errorhandler(413)
def too_large(e):
    flash('File size exceeds the 30MB limit.', 'danger')
    return redirect(url_for('main.add_book'))

@bp.route('/my_books')
@login_required
def my_books():
    books = Book.query.filter_by(owner_id=current_user.id).order_by(Book.created_at.desc()).all()
    return render_template('main/my_books.html', books=books)

@bp.route('/update_book_status/<int:book_id>', methods=['POST'])
@login_required
def update_book_status(book_id):
    book = Book.query.get_or_404(book_id)
    if book.owner_id != current_user.id:
        flash('Permission denied.', 'danger')
        return redirect(url_for('main.my_books'))
    
    new_status = request.form.get('status')
    if new_status in ['Available', 'Borrowed', 'Lost/Damaged']:
        book.book_status = new_status
        db.session.commit()
        flash(f'Status updated for "{book.title}"', 'success')
    return redirect(url_for('main.my_books'))

@bp.route('/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.owner_id != current_user.id:
        flash('Permission denied.', 'danger')
        return redirect(url_for('main.my_books'))
    
    # Delete all requests associated with this book first to avoid foreign key constraint errors
    BorrowRequest.query.filter_by(book_id=book.book_id).delete()
    
    db.session.delete(book)
    db.session.commit()
    flash(f'Book "{book.title}" was deleted.', 'info')
    return redirect(url_for('main.my_books'))

@bp.route('/borrow_request/<int:book_id>', methods=['GET', 'POST'])
@login_required
def borrow_request(book_id):
    book = Book.query.get_or_404(book_id)
    if book.owner_id == current_user.id:
        flash('You cannot request to borrow your own book.', 'danger')
        return redirect(url_for('main.home'))
    
    exists = BorrowRequest.query.filter(
        BorrowRequest.book_id == book.book_id,
        BorrowRequest.borrower_id == current_user.id,
        BorrowRequest.request_status.in_(['Pending', 'Accepted'])
    ).first()
    if exists:
        flash('You have already requested to borrow this book.', 'info')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        proposed_date = request.form.get('proposed_date')
        proposed_time = request.form.get('proposed_time')
        location = request.form.get('location')
        message = request.form.get('message')

        # Create a new borrow request
        borrow_request = BorrowRequest(
            book_id=book.book_id,
            borrower_id=current_user.id,
            proposed_date=proposed_date,
            proposed_time=proposed_time,
            location=location,
            request_status='Pending',
            message=message
        )
        db.session.add(borrow_request)
        db.session.commit()
        flash('Your borrow request has been submitted.', 'success')
        return redirect(url_for('main.home'))

    return render_template('main/borrow_request.html', book=book)

@bp.route('/download_request/<int:book_id>', methods=['GET','POST'])
@login_required
def download_request(book_id):
    book = Book.query.get_or_404(book_id)
    if book.owner_id == current_user.id:
        flash('You cannot request to borrow your own book.', 'danger')
        return redirect(url_for('main.home'))
    exists = BorrowRequest.query.filter(
        BorrowRequest.book_id == book.book_id,
        BorrowRequest.borrower_id == current_user.id,
        BorrowRequest.request_status.in_(['Pending', 'Accepted'])
    ).first()
    if exists:
        flash('You have already requested to download this book.', 'info')
        return redirect(url_for('main.home'))

    # Create a new borrow request for digital download
    borrow_request = BorrowRequest(
        book_id=book.book_id,
        borrower_id=current_user.id,
        proposed_date=None,
        proposed_time=None,
        location=None,
        request_status='Pending',
        message='Requesting to download the digital copy.'
    )
    db.session.add(borrow_request)
    db.session.commit()
    flash('Your download request has been submitted.', 'success')
    return redirect(url_for('main.home'))

@bp.route('/borrowed_books')
@login_required
def borrowed_books():
    borrowed_requests = BorrowRequest.query.filter_by(
        borrower_id=current_user.id, 
        request_status='Accepted'
    ).order_by(BorrowRequest.created_at.desc()).all()
    
    exchange_requests = BorrowRequest.query.join(Book).filter(
        (Book.owner_id == current_user.id) | (BorrowRequest.borrower_id == current_user.id),
        Book.type == 'Physical',
        BorrowRequest.request_status == 'Accepted'
    ).order_by(BorrowRequest.created_at.desc()).all()

    return render_template('main/borrowed_books.html', 
                           borrowed_requests=borrowed_requests, 
                           exchange_requests=exchange_requests)

@bp.route('/view_requests', methods=['GET', 'POST'])
@login_required
def view_requests():
    incoming_requests = BorrowRequest.query.filter(
    BorrowRequest.book.has(owner_id=current_user.id), 
    BorrowRequest.request_status == 'Pending').order_by(BorrowRequest.created_at.desc()).all()
    outgoing_requests = BorrowRequest.query.filter_by(borrower_id=current_user.id, request_status='Pending').order_by(BorrowRequest.created_at.desc()).all()
    return render_template('main/view_requests.html', incoming_requests=incoming_requests, outgoing_requests=outgoing_requests)

@bp.route('/request_action/<int:request_id>', methods=['GET', 'POST'])
@login_required
def request_action(request_id):
    action = request.form.get('action')
    borrow_request = BorrowRequest.query.get_or_404(request_id)

    if action == 'accept':
        borrow_request.request_status = 'Accepted'
        borrow_request.accepted_at = datetime.now(timezone.utc)
        
        # Digital books remain Available so multiple users can borrow them simultaneously
        if borrow_request.book.type != 'Digital':
            borrow_request.book.book_status = 'Borrowed'
            
        db.session.commit()
        flash('You have accepted the request.', 'success')
    elif action == 'reject':
        borrow_request.request_status = 'Rejected'
        db.session.commit()
        flash('You have rejected the request.', 'info')
    elif action == 'delete':
        db.session.delete(borrow_request)
        db.session.commit()
        flash('The request has been deleted.', 'info')
    else:
        flash('Invalid action or permission denied.', 'danger')

    return redirect(url_for('main.view_requests'))

@bp.route('/suggest_alternative/<int:request_id>', methods=['GET', 'POST'])
@login_required
def suggest_alternative(request_id):
    borrow_request = BorrowRequest.query.get_or_404(request_id)
    if request.method == 'POST':
        proposed_date = request.form.get('proposed_date')
        proposed_time = request.form.get('proposed_time')
        location = request.form.get('location')
        message = request.form.get('message')

        borrow_request.proposed_date = proposed_date
        borrow_request.proposed_time = proposed_time
        borrow_request.location = location
        borrow_request.message = message
        borrow_request.is_proposed = True

        db.session.commit()
        flash('Alternative proposal has been sent to the borrower.', 'success')
        return redirect(url_for('main.view_requests'))

    return render_template('main/suggest_alternative.html', req=borrow_request)

@bp.route('/return_book/<int:request_id>', methods=['POST'])
@login_required
def return_book(request_id):
    borrow_request = BorrowRequest.query.get_or_404(request_id)

    if borrow_request.book.type == 'Digital' and borrow_request.request_status == 'Accepted':
        # Mark request as removed/returned
        db.session.delete(borrow_request)
        
        # Change book status back to available
        borrow_request.book.book_status = 'Available'
        
        db.session.commit()
        flash(f'You have successfully returned "{borrow_request.book.title}".', 'success')
    else:
        flash('Cannot return this book or invalid request state.', 'warning')
        
    return redirect(url_for('main.borrowed_books'))

@bp.route('/delete_exchange_record/<int:request_id>', methods=['POST'])
@login_required
def delete_exchange_record(request_id):
    borrow_request = BorrowRequest.query.get_or_404(request_id)

    db.session.delete(borrow_request)
    db.session.commit()

    flash('Physical book exchange record deleted successfully.', 'info')
    
    return redirect(url_for('main.borrowed_books'))