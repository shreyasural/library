from django.shortcuts import render, redirect
from .models import Book
import qrcode
from django.http import HttpResponse
from .models import Book, ReadingHistory
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count, Sum
from datetime import date
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages


# ---------------- HOME ----------------

def home(request):
    books = Book.objects.all()
    return render(request, "home.html", {"books": books})


# ---------------- ADD BOOK ----------------

def add_book(request):
    if request.method == "POST":
        Book.objects.create(
            book_id=request.POST["book_id"],
            title=request.POST["title"],
            author=request.POST["author"],
            category=request.POST["category"],
            status="Available"
        )
        return redirect("viewbooks")

    return render(request, "addbook.html")


# ---------------- SEARCH BOOK ----------------
def search_book(request):
    book = None
    message = None

    if request.method == "POST":
        bid = request.POST.get("book_id")

        try:
            book = Book.objects.get(book_id=bid)
        except Book.DoesNotExist:
            message = "❌ Book not found. The requested book is not available in the library."

    return render(request, "searchbook.html", {
        "book": book,
        "message": message,
    })


# ---------------- DELETE BOOK ----------------

def delete_book(request):
    if request.method == "POST":
        bid = request.POST["book_id"]
        Book.objects.filter(book_id=bid).delete()
        return redirect("dashboard")

    return render(request, "deletebook.html")


# ---------------- ISSUE BOOK ----------------
@login_required
def issue_book(request):
    if request.method == "POST":

        book_id = request.POST["book_id"]
        student_name = request.POST["student_name"]
        student_id = request.POST["student_id"]
        issue_date = request.POST["issue_date"]

        book = Book.objects.filter(book_id=book_id).first()

        if book and book.status == "Available":

            book.status = "Issued"
            book.borrow_count += 1

            # Save manually entered details
            book.student_name = student_name
            book.student_id = student_id
            book.issue_date = issue_date

            book.save()

            ReadingHistory.objects.create(
                user=request.user,
                book=book
            )

        return redirect("dashboard")

    return render(request, "issuebook.html")


# ---------------- RETURN BOOK ----------------

def return_book(request):
    if request.method == "POST":

        book_id = request.POST["book_id"]
        book = Book.objects.filter(book_id=book_id).first()

        if book:
            book.status = "Available"
            book.student_name = None
            book.student_id = None
            book.issue_date = None

            book.save()

        return redirect("dashboard")

    return render(request, "returnbook.html")


# ---------------- VIEW BOOKS ----------------

def viewbooks(request):
    books = Book.objects.all()
    return render(request, "viewbooks.html", {"books": books})


# ---------------- SIGN UP ----------------

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "signup.html")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully")
        return redirect("/login/")

    return render(request, "signup.html")


# ---------------- LOGIN ----------------

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")


# ---------------- LOGOUT ----------------

def logout_user(request):
    logout(request)
    return redirect("/login/")
def dashboard(request):

    overdue_books = []

    books = Book.objects.filter(status="Issued")

    for book in books:

        if book.issue_date:
            days = (date.today() - book.issue_date).days

            if days > 10:
                book.fine = (days - 10) * 5
                overdue_books.append(book)

    return render(request, "dashboard.html", {
        "overdue_books": overdue_books
    })

from datetime import date
from .models import Book

def fine_calculator(request):
    books = Book.objects.filter(status="Issued")

    for book in books:

        if book.issue_date:
            days_borrowed = (date.today() - book.issue_date).days

            book.days_borrowed = days_borrowed

            if days_borrowed > 10:
                book.fine = (days_borrowed - 10) * 5   # ₹5 per extra day
            else:
                book.fine = 0

        else:
            book.days_borrowed = 0
            book.fine = 0

    return render(request, "fine.html", {"books": books})

from django.contrib.auth.decorators import login_required
def generate_qr(request, book_id):
    book = Book.objects.get(book_id=book_id)

    qr = qrcode.make(book.book_id)

    response = HttpResponse(content_type="image/png")
    qr.save(response, "PNG")

    return response
@login_required
def recommend_books(request):

    history = ReadingHistory.objects.filter(user=request.user)

    categories = history.values_list(
        "book__category",
        flat=True
    )

    recommendations = Book.objects.filter(
        category__in=categories,
        status="Available"
    ).exclude(
        id__in=history.values_list("book_id", flat=True)
    )

    return render(
        request,
        "recommend.html",
        {
            "books": recommendations
        }
    )

    return redirect('view_books')
def popular_books(request):

    books = Book.objects.order_by('-borrow_count')[:10]

    return render(request, 'popular_books.html', {'books': books})

def trending_categories(request):

    categories = Book.objects.values('category').annotate(
        total_borrows=Sum('borrow_count')
    ).order_by('-total_borrows')

    return render(request, 'trending_categories.html',
                  {'categories': categories}) 