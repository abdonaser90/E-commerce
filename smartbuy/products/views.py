from django.shortcuts import get_object_or_404, render
from .models import Product
from django.contrib import messages
from reviews.models import Reviews

# Create your views here.

def products(request):
    pro = Product.objects.all()

    name = None
    descr = None
    priceFrom = None
    priceTo = None

    if 'searchName' in request.GET:
        name = request.GET['searchName']
        if name:
            pro = pro.filter(name__icontains=name)

    if 'searchDesc' in request.GET:
        descr = request.GET['searchDesc']
        if descr:
            pro = pro.filter(description__icontains=descr)

    if 'searchPriceFrom' in request.GET and 'searchPriceTo' in request.GET:
        priceFrom = request.GET['searchPriceFrom']
        priceTo = request.GET['searchPriceTo']
        if priceFrom and priceTo:
            if priceFrom.isdigit() and priceTo.isdigit():
                pro = pro.filter(price__gte=priceFrom, price__lte=priceTo)



    context = {
        'products': pro
    }
    return render(request, 'products/products.html', context)


def product(request, pro_id):
    context = {
        'pro': get_object_or_404(Product, pk=pro_id)
    }
    return render(request, 'products/product.html', context)


def search(request):
    return render(request, 'products/search.html')

def addReview(request):
    if request.method == 'POST' and 'btnsave' in request.POST:
        if request.user is not None and request.user.id != None:
            reviews = Reviews.objects.get(product=request.GET['pro_id'])
            if request.POST['review']:
                reviews.review = request.POST['content']
                reviews.state = False
                reviews.save()
                messages.success("Your Feedback Is Under Reviewing")