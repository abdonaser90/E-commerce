from django.contrib import messages
from django.shortcuts import render

from reviews.models import Reviews

# Create your views here.
def addReview(request):
    if request.method == 'POST' and 'btnsave' in request.POST:
        if request.user is not None and request.user.id != None:
            reviews = Reviews.objects.get(product=request.GET['pro_id'])
            if request.POST['review']:
                reviews.content = request.POST['content']
                reviews.state = False
                reviews.save()
                messages.success("Your Feedback Is Under Reviewing")

