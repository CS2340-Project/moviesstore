from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone  # Add this import

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    RATING_CHOICES = [
        ('G', 'General Audience'),
        ('PG', 'Parental Guidance'),
        ('PG-13', 'Parental Guidance for children under 13'),
        ('R', 'Restricted'),
        ('NC-17', 'Adults Only'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    
    # New fields with null=True or default values
    genres = models.ManyToManyField(Genre, blank=True)
    duration = models.IntegerField(help_text="Duration in minutes", null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    director = models.CharField(max_length=255, null=True, blank=True)
    cast = models.TextField(help_text="Enter main cast members", null=True, blank=True)
    rating = models.CharField(max_length=5, choices=RATING_CHOICES, default='PG')
    user_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        default=0.0
    )
    trailer_url = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=100, default='English')
    country = models.CharField(max_length=100, default='United States')
    
    is_featured = models.BooleanField(default=False)
    availability_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)  # Changed this line
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name}"
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5  # Adding default value
    )
    data = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    is_spoiler = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.movie.name} - {self.rating}/10 - {self.comment[:50]}"