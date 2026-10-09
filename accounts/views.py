from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from books.models import BorrowRecord

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('books:book_list')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'books:book_list'

@login_required
def profile_view(request):
    borrow_records = BorrowRecord.objects.filter(user=request.user).order_by('-borrow_date')
    
    context = {
        'borrow_records': borrow_records
    }
    return render(request, 'accounts/profile.html', context)