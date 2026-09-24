from django.contrib import admin
from django.utils.html import format_html
from .models import State, Category, TouristPlace, PlaceImage, Review, TripInquiry

admin.site.site_header = "🌍 TourVista Tourism Management"
admin.site.site_title = "TourVista Admin"
admin.site.index_title = "Tourism Portal Control & Management Dashboard"


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 2
    readonly_fields = ['image_preview']
    fields = ['image', 'image_url', 'caption', 'image_preview']

    def image_preview(self, obj):
        if obj.display_image:
            return format_html('<img src="{}" style="width: 80px; height: 55px; object-fit: cover; border-radius: 6px;" />', obj.display_image)
        return "No Image"
    image_preview.short_description = "Preview"


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ['user_name', 'user_email', 'rating', 'title', 'is_approved', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['icon_badge', 'name', 'slug', 'places_count', 'image_preview', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

    def icon_badge(self, obj):
        return format_html('<i class="fas {}" style="font-size: 1.2rem; color: #3b82f6;"></i> <b style="margin-left: 6px;">{}</b>', obj.icon, obj.name)
    icon_badge.short_description = "Category"

    def places_count(self, obj):
        return obj.places.count()
    places_count.short_description = "Attractions Count"

    def image_preview(self, obj):
        if obj.display_image:
            return format_html('<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;" />', obj.display_image)
        return "None"
    image_preview.short_description = "Image"


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['cover_preview', 'name', 'capital', 'best_time_to_visit', 'climate', 'places_count', 'is_featured']
    list_filter = ['is_featured', 'climate']
    search_fields = ['name', 'capital', 'description', 'tagline']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured']

    def cover_preview(self, obj):
        if obj.display_cover:
            return format_html('<img src="{}" style="width: 70px; height: 45px; object-fit: cover; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />', obj.display_cover)
        return "No Image"
    cover_preview.short_description = "Cover"

    def places_count(self, obj):
        return obj.places.count()
    places_count.short_description = "Places"


@admin.register(TouristPlace)
class TouristPlaceAdmin(admin.ModelAdmin):
    list_display = ['thumbnail_preview', 'name', 'city', 'state', 'category', 'rating_badge', 'entry_fee', 'is_popular', 'is_featured']
    list_filter = ['state', 'category', 'is_popular', 'is_featured', 'rating']
    search_fields = ['name', 'city', 'short_summary', 'detailed_description', 'address']
    prepopulated_fields = {'slug': ('name', 'city')}
    list_editable = ['is_popular', 'is_featured']
    inlines = [PlaceImageInline, ReviewInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'state', 'category', 'city', 'short_summary', 'rating')
        }),
        ('Detailed Descriptions & Highlights', {
            'fields': ('detailed_description', 'highlights')
        }),
        ('Location & Coordinates', {
            'fields': ('address', 'latitude', 'longitude'),
            'description': 'Latitude and Longitude are used to render interactive pins on the map.'
        }),
        ('Travel Practicalities', {
            'fields': ('timings', 'entry_fee', 'best_season', 'how_to_reach_air', 'how_to_reach_train', 'how_to_reach_road')
        }),
        ('Media & Visibility', {
            'fields': ('cover_image', 'cover_image_url', 'is_popular', 'is_featured')
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.display_cover:
            return format_html('<img src="{}" style="width: 75px; height: 50px; object-fit: cover; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.15);" />', obj.display_cover)
        return "No Image"
    thumbnail_preview.short_description = "Photo"

    def rating_badge(self, obj):
        return format_html('<span style="background: #fef08a; color: #854d0e; padding: 3px 8px; border-radius: 12px; font-weight: bold;">★ {}</span>', obj.rating)
    rating_badge.short_description = "Rating"


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ['place', 'caption', 'image_preview', 'created_at']
    list_filter = ['place__state', 'place']
    search_fields = ['place__name', 'caption']

    def image_preview(self, obj):
        if obj.display_image:
            return format_html('<img src="{}" style="width: 90px; height: 60px; object-fit: cover; border-radius: 6px;" />', obj.display_image)
        return "No Image"
    image_preview.short_description = "Preview"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['place', 'user_name', 'rating', 'title', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at', 'place__state']
    search_fields = ['user_name', 'user_email', 'comment', 'title', 'place__name']
    list_editable = ['is_approved']


@admin.register(TripInquiry)
class TripInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'destination_state', 'destination_place', 'travel_date', 'travelers_count', 'status_badge', 'created_at']
    list_filter = ['status', 'destination_state', 'travel_date', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message']
    list_editable = []

    def status_badge(self, obj):
        colors = {
            'Pending': '#f59e0b',
            'Contacted': '#3b82f6',
            'Confirmed': '#10b981',
            'Closed': '#6b7280',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html('<span style="background: {}; color: #fff; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;">{}</span>', color, obj.status)
    status_badge.short_description = "Status"
