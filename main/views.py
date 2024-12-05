
import re
from django.shortcuts import render, redirect,get_object_or_404



from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login,logout # as auth_login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import ProfileUpdateForm,ReviewForm
from django.contrib.auth.decorators import login_required
from cart.cart import Cart


# Create your views here.
def index(request):
    

    cate = Category.objects.all()

    catid = request.GET.get("category")
    if catid:
        product = Product.objects.filter(subcategory = catid)
    else:
        product = Product.objects.all()

    paginator =Paginator(product,2)
    num_page = request.GET.get('page')
    data = paginator.get_page(num_page)
    total = data.paginator.num_pages

    contex = {
        "product":product,
        "cate":cate,
        "data":data,
        "num":[i+1 for i in range(total)]
        
    }
    return render(request,'main/index.html',contex)

def blog_single(request):
    return render(request,'main/blog-single.html')
def blog(request):
    return render(request,'main/blog.html')
def cart(request):
    return render(request,'main/cart.html')
def checkout(request):
    return render(request,'main/checkout.html')
def contact(request):
    return render(request,'main/contact-us.html')

def product_details(request,id):
    product =get_object_or_404(Product, id=id)
    products = Product.objects.filter(categoroy = product.categoroy).exclude(id = id)

    cmt_all = request.GET.get("cmt_all")
    if cmt_all:
        reviews = product.reviews.all()
    else:
        reviews = product.reviews.filter()

    reviews = product.reviews.all()
    form =ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted successfully")
            return redirect('product_details', id=product.id)
    context={


        
        'product':product,
        'products':products,
        'form':form,
        'reviews':reviews
    }

    return render(request,'main/product-details.html',context)
def shop(request):
    return render(request,'main/shop.html')

        
    return render(request, 'main/login.html')
'''================================================================================
===================================================================================
                            authenticate start
================================================================================
===================================================================================

'''



def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        
        
        try:
            if username.lower() in password.lower():
                messages.error(request, "Your password is too similar to username")
                return redirect('register')
            
            if not re.search(r"[A-Z]", password):
                messages.error(request, "Your password must contain at least one uppercase letter")
                return redirect('register')
            
            if not re.search(r"\d", password):
                messages.error(request, "Your password must contain at least one digit")
                return redirect('register')
            
            
            if password == password1:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'username already exists')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'email already exists')
                    return redirect('register')
                else:
                    User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    return redirect('index')
                    
            else:
                messages.error(request, "Password does not match !!!")
                return redirect('register')   
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
    return render(request, 'auth/register.html')

def log_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.info(request, "username is not match !!!")
            return redirect('log_in')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        
    return render(request, 'auth/login.html')

def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url="log_in")
def customer_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_form = ProfileUpdateForm(instance=profile)
    
    if request.method == "POST":
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect("profile")
    
    context = {
        'profile_form': profile_form,
        'user': request.user,
        'profile':request.user.profile
    }
    return render(request, 'main/customer_profile.html',context)



# ----------------------------------------------------------------
                    #  cart section
# ----------------------------------------------------------------


@login_required(login_url="/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_detail(request):
    return render(request, 'main/cart_detail.html')




