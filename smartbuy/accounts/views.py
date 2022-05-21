from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserProfile
from products.models import Product
import re

# Create your views here.

def signin(request):
    if request.method == 'POST' and 'btnlogin' in request.POST:
        username = request.POST['user']
        password = request.POST['pass']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request, user)
            # messages.success(request, 'You are now logged in')
        else:
            messages.error(request, 'UserName or Password invalid')

        return redirect('signin')
    else:
        return render(request, 'accounts/signin.html')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')


def signup(request):
    if request.method == 'POST' and 'btnsignup' in request.POST:
        # variables for fields
        fname = None
        lname = None
        address = None
        city = None
        state = None
        email = None
        username = None
        password = None
        terms = None
        is_added = None
        
        # Get values from the form
        if 'fname' in request.POST: fname = request.POST['fname']
        else: messages.error(request, 'Error in First Name') 

        if 'lname' in request.POST: lname = request.POST['lname']
        else: messages.error(request, 'Error in Last Name')

        if 'address' in request.POST: address = request.POST['address']
        else: messages.error(request, 'Error in Address')

        if 'city' in request.POST: city = request.POST['city']
        else: messages.error(request, 'Error in City')

        if 'state' in request.POST: state = request.POST['state']
        else: messages.error(request, 'Error in State')

        if 'email' in request.POST: email = request.POST['email']
        else: messages.error(request, 'Error in Email')

        if 'user' in request.POST: username = request.POST['user']
        else: messages.error(request, 'Error in UserName')

        if 'pass' in request.POST: password = request.POST['pass']
        else: messages.error(request, 'Error in Password')

        if 'terms' in request.POST: terms = request.POST['terms']

        # check the values
        if fname and lname and address and city and state and email and username and password:
            if terms == 'on':
                # check if username is taken 
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'This UserName is taken')
                else:
                    # check is email is taken 
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'This Email is taken')
                    else:
                        patt = "^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([.-]\w+)*$"
                        if re.match(patt, email):
                            # add user
                            user = User.objects.create_user(first_name=fname, last_name=lname, email=email, username=username, password= password)
                            user.save()
                            # add user profile
                            userproile = UserProfile(user=user, address=address, city=city, state=state)
                            userproile.save()
                            # clear fields
                            fname=''
                            lname=''
                            address=''
                            city=''
                            state=''
                            email=''
                            username=''
                            password=''
                            terms=None
                            # Success Message
                            messages.success(request, 'Your account is created')
                            is_added = True
                        else:
                            messages.error(request, 'Invalid email')
            else:
                messages.error(request, 'You must agree the  terms')
        else:
            messages.error(request, 'Check the empty fields')

        return render(request, 'accounts/signup.html', {
            'fname':fname,
            'lname':lname,
            'address':address,
            'city':city,
            'state':state,
            'email':email,
            'user':username,
            'pass':password,
            'is_added':is_added,
        })
    else:
        return render(request, 'accounts/signup.html')


def profile(request):
    if request.method == 'POST' and 'btnsave' in request.POST:
        
        if request.user is not None and request.user.id != None:
            userprofile = UserProfile.objects.get(user=request.user)

            if request.POST['fname'] and request.POST['lname'] and request.POST['address'] and request.POST['city'] and request.POST['state'] and request.POST['email'] and request.POST['user'] and request.POST['pass']:
                request.user.first_name = request.POST['fname']  
                request.user.last_name = request.POST['lname']
                userprofile.address = request.POST['address']  
                userprofile.city = request.POST['city']  
                userprofile.state = request.POST['state']  
                # userprofile.email = request.POST['email']  
                # userprofile.username = request.POST['user']
                if not request.POST['pass'].startswith('pbkdf2_sha256$320000$'):
                    request.user.set_password(request.POST['pass'])
                request.user.save()
                userprofile.save()
                auth.login(request, request.user)
                messages.success(request, 'Your data has been saved')
            else:
                messages.error(request, 'Check your values and elements')

        return redirect('profile')
    
    else:
        if request.user is not None:
            context = None
            if not request.user.is_anonymous:
                userprofile = UserProfile.objects.get(user=request.user)
                context = {
                    'fname': request.user.first_name,
                    'lname': request.user.last_name,
                    'email': request.user.email,
                    'user': request.user.username,
                    'pass': request.user.password,
                    'address':userprofile.address,
                    'city':userprofile.city,
                    'state':userprofile.state
                }
            return render(request, 'accounts/profile.html', context)
        else:
            return redirect('profile')


def product_favorite(request, pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav = Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter(user=request.user, product_favorites=pro_fav).exists():
            messages.success(request, 'Already product in the favorite list')
        else:
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.product_favorites.add(pro_fav)
            messages.success(request, 'Product has been added to favorite list')

    else:
        messages.error(request, 'You must be logged in')

    return redirect('/products/' + str(pro_id))


def show_product_favorite(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo = UserProfile.objects.get(user=request.user)
        pro = userInfo.product_favorites.all()
        context = { 'products':pro }
    return render(request, 'products/products.html', context)