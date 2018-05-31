from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import Group,User
# Create your views here.
from Project.models import Book,BookInstance,Author,Language,Genre,BorrowedBook,Comment
from django.contrib.auth.decorators import login_required
from .forms import CommentForm , BookForm
import datetime

# Create your views here.

@login_required()
def home(request):
    b=Book.objects.all()
    group = Group.objects.get(name='Librarian')
    context = { 'book' : b , 'group':group }
    return render(request, 'index.html',context)



def details (request , key):
    c = Book.objects.get(id=key)
    group = Group.objects.get(name='Librarian')
    comments = Comment.objects.filter(book = c)
    commentform = CommentForm()


    bookform = BookForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if bookform.is_valid():
            c = bookform
            c.save()
            return redirect(reverse('book_detail', kwargs={'id': id}))

    try:
        borrowed_book = BorrowedBook.objects.get(book=c, borrower=request.user)

    except:
        borrowed_book = None
    context = { 'det' : c , 'borrowed_book': borrowed_book , 'commentform': commentform , 'comments': comments , 'bookform': bookform , 'group':group}
    return render(request, 'examples.html',context)


def delete (request , key):
    v=Book.objects.get(id=key)
    v.delete()
    return redirect('/')

def book_search(request):
    query = request.GET.get('q')
    print(query)
    books = Book.objects.filter(title__icontains=query)
    context = {'books': books}
    return render(request, 'search.html', context)

def book_return(request, id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=id)
        try:
            borrowed_book = BorrowedBook.objects.get(book=book, borrower=request.user)
        except:
            borrowed_book = None
        book.copies += 1
        book.save()
        borrowed_book.delete()
        return redirect('/%s' %(id))

    return redirect('/%s' %(id))


def book_borrow(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        if book.copies > 0:
            borrowed_book = BorrowedBook()
            borrowed_book.book = book
            borrowed_book.save()
            borrowed_book.borrower.add(request.user)
            borrowed_book.save()
            book.copies -= 1
            borrowed_book.due_back =  datetime.date.today() + datetime.timedelta(weeks=3)
            borrowed_book.save()
            book.save()
            return redirect('/%s' %(book.id))

    return redirect('/%s' %(book.id))


def book_comment(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.comment_author = request.user
            instance.book = book
            instance.save()
            print('comment added')
            return redirect('/%s' %(book.id))

    return redirect('/%s' %(book.id))

def book_add(request):
    form = BookForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
    context = {'form': form}
    return render(request, 'book_add.html', context)

def book_update(request, id):
    group = Group.objects.get(name='Librarian')
    book = Book.objects.get(id=id)
    form = BookForm(request.POST or None, request.FILES or None, instance=book)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/%s' % (book.pk))

    context = {'form': form , 'group':group}
    return render(request, 'book_update.html', context)


def check(request):
    ch=BorrowedBook.objects.all()
    group = Group.objects.get(name='Librarian')
    context = {'ch': ch , 'group': group}
    return render(request, 'check.html', context)