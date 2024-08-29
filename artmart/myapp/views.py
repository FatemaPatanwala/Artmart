from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login as auth_login, logout
from myapp.forms import *
from django.contrib.auth.forms import AuthenticationForm
from myapp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

#USER REGISTRATION
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            user_profile=UserProfile.objects.create(user=user)
            ArtistProfile.objects.create(user_profile=user_profile)
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

#ARTIST LOGIN
def artist_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.groups.filter(name='Artists').exists():
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'artist_login.html', {'error': 'You are not an artist!'})
    return render(request, 'artist_login.html')

#USER LOGIN
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.groups.filter(name='Users').exists():
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'user_login.html', {'error': 'You are not a regular user!'})
    return render(request, 'user_login.html')

#LOGOUT
def user_logout(request):
    logout(request)
    return redirect('home')

#HOME PAGE
def home(request):
    artworks = Artwork.objects.all()
    is_artist = request.user.groups.filter(name='Artists').exists()

    return render(request, 'home.html', {'artworks': artworks,'is_artist': is_artist})





#LIST OF ARTISTS
def artist(request):
   
   artists=ArtistProfile.objects.all()
   context= {'artists' : artists}
   return render(request,'artist.html',context)

#VIEW ARTIST PROFILE 
def view_artist_profile(request, artist_id):
    artist_profile = get_object_or_404(ArtistProfile, id=artist_id)
    artworks = artist_profile.artworks.all()
    context = {
        'artist_profile': artist_profile,
        'artworks': artworks,
    } 
    return render(request, 'artist_profile.html', context)
  




#LIST OF ARTWORK
def artwork(request):
   artworks=Artwork.objects.all()
   is_artist = request.user.groups.filter(name='Artists').exists()
   context= {'artworks' : artworks, 'is_artist': is_artist}
   return render(request,'artwork.html',context)

#CREATE ARTWORK 
@login_required
def create_artwork(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.artist = request.user.userprofile.artistprofile
            artwork.save()
            return redirect('artwork')
    else:
        form = ArtworkForm()
    return render(request, 'artwork_create.html', {'form': form})

#UPDATE ARTWORK
@login_required
def edit_artwork(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    user=request.user   
    if artwork.artist.user_profile.user != user:
        return redirect('artwork_detail', artwork_id=artwork.id)

    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid():
            form.save()
            return redirect('artwork_detail', artwork_id=artwork.id)
    else:
        form = ArtworkForm(instance=artwork)

    return render(request, 'artwork_update.html', {'form': form, 'artwork': artwork})

#ARTWORK DETAILS
def artwork_detail(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    return render(request, 'artwork_detail.html', {'artwork': artwork})

#DELETE ARTWORK
def artwork_delete(request,artwork_id):
    artwork=Artwork.objects.get(id=artwork_id)
    if request.method=='POST':
        artwork.delete()
        return redirect('artist_artworks')
    return render(request,"artwork_delete.html",{'artwork': artwork})

#ARTIST'S ARTWORK
def artist_artworks(request):
    artist_profile = get_object_or_404(ArtistProfile, user_profile__user=request.user)
    artworks = artist_profile.artworks.all()
    context = {
        'artist_profile': artist_profile,
        'artworks': artworks,
    } 
    return render(request, 'artist_artworks.html', context)





#SHOPPING CART
@login_required
def add_to_cart(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    order, created = Order.objects.get_or_create(buyer=request.user.userprofile, is_paid=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, artwork=artwork)
    if not created:
        order_item.quantity += 1
        order_item.save()
    return redirect('cart')

@login_required
def cart(request):
    try:
        order = Order.objects.get(buyer=request.user.userprofile, is_paid=False)
    except Order.DoesNotExist:
        order = None
    return render(request, 'cart.html', {'order': order})

@login_required
def remove_from_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        order_item.delete()
    return redirect('cart')

#CHECKOUT
@login_required
def checkout(request):
    order = get_object_or_404(Order, buyer=request.user.userprofile, is_paid=False)
    if request.method == 'POST':
        order.is_paid = True
        order.save()
        return redirect('order_history')
    return render(request, 'checkout.html', {'order': order})




#REVIEW
@login_required
def leave_review(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.artwork = artwork
            review.user = request.user.userprofile
            review.save()
            return redirect('artwork_detail', artwork_id=artwork.id)
    else:
        form = ReviewForm()
    return render(request, 'leave_review.html', {'form': form, 'artwork': artwork})

def view_reviews(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    reviews = Review.objects.filter(artwork=artwork)
    return render(request, 'view_reviews.html', {'artwork': artwork, 'reviews': reviews})




    
    