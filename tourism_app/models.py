from pickle import TRUE
import os
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(
        max_length=50, 
        default='fa-map-pin',
        help_text='FontAwesome icon class name (e.g., fa-mountain, fa-umbrella-beach, fa-monument, fa-leaf)'
    )
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, help_text='External image link if no file is uploaded')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&auto=format&fit=crop'


class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    capital = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200, blank=True, help_text="e.g. God's Own Country, Land of Kings")
    description = models.TextField(help_text='Detailed overview of the state tourism')
    history_culture = models.TextField(blank=True, help_text='Cultural significance and historical background')
    best_time_to_visit = models.CharField(max_length=150, default='October to March')
    climate = models.CharField(max_length=150, default='Tropical / Subtropical')
    languages = models.CharField(max_length=150, default='Hindi, English')
    cover_image = models.ImageField(upload_to='states/covers/', blank=True, null=True)
    cover_image_url = models.URLField(max_length=500, blank=True, help_text='External cover image URL')
    banner_image = models.ImageField(upload_to='states/banners/', blank=True, null=True)
    banner_image_url = models.URLField(max_length=500, blank=True, help_text='External wide banner image URL')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tourism_app:state_detail', kwargs={'slug': self.slug})

    @property
    def display_cover(self):
        if self.cover_image:
            return self.cover_image.url
        if self.cover_image_url:
            return self.cover_image_url
        return 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=800&auto=format&fit=crop'

    @property
    def display_banner(self):
        if self.banner_image:
            return self.banner_image.url
        if self.banner_image_url:
            return self.banner_image_url
        return self.display_cover


class TouristPlace(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='places')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='places')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    city = models.CharField(max_length=100)
    short_summary = models.CharField(max_length=350, help_text='One or two punchy sentences describing the place')
    detailed_description = models.TextField()
    highlights = models.TextField(blank=True, help_text='Comma or line separated key attractions & activities')
    address = models.CharField(max_length=300)
    latitude = models.FloatField(default=20.5937, help_text='GPS Latitude (for interactive maps)')
    longitude = models.FloatField(default=78.9629, help_text='GPS Longitude (for interactive maps)')
    entry_fee = models.CharField(max_length=120, default='Free / ₹50 - ₹200')
    timings = models.CharField(max_length=150, default='06:00 AM - 06:00 PM')
    best_season = models.CharField(max_length=120, default='October - March')
    how_to_reach_air = models.CharField(max_length=255, blank=True, help_text='Nearest airport and distance')
    how_to_reach_train = models.CharField(max_length=255, blank=True, help_text='Nearest railway station')
    how_to_reach_road = models.CharField(max_length=255, blank=True, help_text='Highway and bus connectivity')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8, validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    cover_image = models.ImageField(upload_to='places/covers/', blank=True, null=True)
    cover_image_url = models.URLField(max_length=500, blank=True, help_text='External cover image URL')
    is_popular = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rating', 'name']

    def __str__(self):
        return f"{self.name} ({self.city}, {self.state.name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.city}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tourism_app:place_detail', kwargs={'slug': self.slug})

    @property
    def display_cover(self):
        if self.cover_image:
            return self.cover_image.url
        if self.cover_image_url:
            return self.cover_image_url
        return 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&auto=format&fit=crop'

    @property
    def google_map_search_url(self):
        query = f"{self.name}, {self.city}, {self.state.name}".replace(" ", "+")
        return f"https://www.google.com/maps/search/?api=1&query={query}"


class PlaceImage(models.Model):
    place = models.ForeignKey(TouristPlace, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='places/gallery/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, help_text='External photo URL')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"Image for {self.place.name} - {self.caption or 'Photo'}"

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&auto=format&fit=crop'


class Review(models.Model):
    place = models.ForeignKey(TouristPlace, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    rating = models.IntegerField(default=5, choices=[(i, f"{i} Stars") for i in range(1, 6)])
    title = models.CharField(max_length=150, blank=True)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user_name} on {self.place.name} ({self.rating}★)"


class TripInquiry(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending Review'),
        ('Contacted', 'Contacted Traveler'),
        ('Confirmed', 'Booking Confirmed'),
        ('Closed', 'Closed / Completed'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    destination_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries')
    destination_place = models.ForeignKey(TouristPlace, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries')
    travel_date = models.DateField(null=True, blank=True)
    travelers_count = models.PositiveIntegerField(default=2)
    budget_range = models.CharField(max_length=100, blank=True, default='Moderate (₹10k - ₹25k)')
    message = models.TextField(help_text='Travel preferences, questions, special requests')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Trip Inquiries'
        ordering = ['-created_at']

    def __str__(self):
        dest = self.destination_place.name if self.destination_place else (self.destination_state.name if self.destination_state else 'General')
        return f"Inquiry from {self.name} for {dest} ({self.status})"
