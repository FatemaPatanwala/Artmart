from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class ArtistProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    social_media_handle = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user_profile.user.username
    
class Artwork(models.Model):
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE)
    artist_profile = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='artworks',null=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='artwork_images/')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    def total_price(self):
        return sum(item.price for item in self.items.all())
    
    def __str__(self):
        return f'Order {self.id} by {self.buyer.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    @property
    def price(self):
        return self.artwork.price * self.quantity
    # price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.artwork.title} (x{self.quantity})'

class Review(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.artwork.title} by {self.user.user.username}'
