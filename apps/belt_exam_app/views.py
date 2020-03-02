from django.shortcuts import render, HttpResponse, redirect
from django.contrib.messages import get_messages
from django.contrib import messages
import re
from .models import *

# Create your views here.

def index(request):
    return render(request, "belt_exam_app/index.html")
    
    
def users(request, user_id):
    author = User.objects.get(id=user_id)
    context = {
        'quotes': Quote.objects.filter(author = author),
        'author': author 
    }
    return render(request, "belt_exam_app/users.html", context)

def quotes(request):
    registered_users = User.objects.all()
    current_user = User.objects.get(id = request.session['id']) 
    allquotes = Quote.objects.all().order_by('-id')
    context = {
        "registered_users": registered_users,
        "current_user": current_user,
        "quotes": allquotes,
    }

    return render(request, "belt_exam_app/quotes.html", context)

def register(request):
    # if get request; redirect to index
    if request.method == "GET":
        return redirect ('/')
    # if validation successful (User.objects.register should return True),
    # store id in req.session
    new_user = User.objects.register(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['confirm_password'])
    if new_user['status'] == True:
        # Register: validation_result = {'status': True, 'created_user': created_user}
        request.session['id'] = new_user['created_user'].id
        return redirect('/quotes')
    else:
        messages.error(request, new_user['errors'], extra_tags = "register")
        return redirect ('/')

def login(request):
    # if get request; redirect to index
    if request.method == "GET":
        return redirect ('/')
    current_user = User.objects.login_validate(request.POST['email'], request.POST['password'])
    if current_user['status'] == True:
        request.session['id'] = current_user['found_user'].id
        return redirect('/quotes')
    else:
        messages.error(request, current_user['errors'], extra_tags = "login")
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')


# result = {'status' : True, 'errors' : errors}
# quote_text, user_id, quoted_by

def quote_post(request):
    if request.method == "GET":
        return redirect ('/')
    if request.method == "POST":
        quote_text = request.POST['quote']
        user_id = request.session['id']
        quoted_by = request.POST['quote_author']
        print (quoted_by)
        # Validate secret before creating, pass arguments to validate function
        result = Quote.objects.validate_quote(quote_text, user_id, quoted_by)
        if result['status'] == True:
            messages.info(request, result['errors'])
            return redirect ('/quotes')
        messages.error(request, result['errors'], extra_tags = "quote_post")
        return redirect('/quotes')

def favorite_quote(request, quote_id):
    quote_faved = Quote.objects.get(id=quote_id)
    user_faved = User.objects.get(id=request.session['id'])
    quote_faved.favorites.add(user_faved)
    return redirect('/quotes')

def dashboard(request):
    return redirect('/quotes')

def edit(request, id): #goes to the edit page
    context = {
        'user_data': User.objects.filter(id=id)
    }
    return render(request, 'belt_exam_app/edit_user.html', context)

def edit_users(request):
    if request.method == "GET":
        return redirect ('/')
    #user = User.objects.get(id = request.session['id'])
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        result = User.objects.validate_edit(first_name, last_name, email)
        if result['status'] == True:
            messages.info(request, result['errors'])
            return render(request, 'belt_exam_app/edit_user.html')
        messages.error(request, result['errors'], extra_tags = "edit_user")
        return render(request, 'belt_exam_app/edit_user.html')
    


# Create your views here.
