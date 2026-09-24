import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.views.decorators.http import require_POST

from .models import State, Category, TouristPlace, PlaceImage, Review, TripInquiry
from .forms import ReviewForm, TripInquiryForm


def home_view(request):
    featured_states = State.objects.filter(is_featured=True)[:6]
    if not featured_states.exists():
        featured_states = State.objects.all()[:6]

    popular_places = TouristPlace.objects.filter(is_popular=True).select_related('state', 'category')[:8]
    if not popular_places.exists():
        popular_places = TouristPlace.objects.all().select_related('state', 'category')[:8]

    categories = Category.objects.annotate(places_total=Count('places')).order_by('name')
    
    total_states_count = State.objects.count()
    total_places_count = TouristPlace.objects.count()
    total_reviews_count = Review.objects.filter(is_approved=True).count()
    
    recent_reviews = Review.objects.filter(is_approved=True).select_related('place', 'place__state')[:4]
    
    inquiry_form = TripInquiryForm()

    context = {
        'featured_states': featured_states,
        'popular_places': popular_places,
        'categories': categories,
        'total_states_count': total_states_count,
        'total_places_count': total_places_count,
        'total_reviews_count': total_reviews_count,
        'recent_reviews': recent_reviews,
        'inquiry_form': inquiry_form,
    }
    return render(request, 'tourism/home.html', context)


def states_list_view(request):
    query = request.GET.get('q', '').strip()
    states = State.objects.annotate(places_count=Count('places')).order_by('name')

    if query:
        states = states.filter(
            Q(name__icontains=query) |
            Q(capital__icontains=query) |
            Q(description__icontains=query) |
            Q(tagline__icontains=query)
        )

    context = {
        'states': states,
        'query': query,
    }
    return render(request, 'tourism/states_list.html', context)


def state_detail_view(request, slug):
    state = get_object_or_404(State, slug=slug)
    category_slug = request.GET.get('category', '')
    
    places = state.places.select_related('category', 'state')
    if category_slug:
        places = places.filter(category__slug=category_slug)
        
    categories = Category.objects.filter(places__state=state).distinct()
    
    # Prepare Map JSON Data
    map_markers = []
    for place in state.places.all():
        if place.latitude and place.longitude:
            map_markers.append({
                'name': place.name,
                'city': place.city,
                'lat': place.latitude,
                'lng': place.longitude,
                'rating': str(place.rating),
                'category': place.category.name if place.category else '',
                'url': place.get_absolute_url(),
                'image': place.display_cover,
                'entry_fee': place.entry_fee,
            })
    
    inquiry_form = TripInquiryForm(initial={'destination_state': state})

    context = {
        'state': state,
        'places': places,
        'categories': categories,
        'selected_category': category_slug,
        'map_markers_json': json.dumps(map_markers),
        'inquiry_form': inquiry_form,
    }
    return render(request, 'tourism/state_detail.html', context)


def places_list_view(request):
    query = request.GET.get('q', '').strip()
    state_slug = request.GET.get('state', '').strip()
    category_slug = request.GET.get('category', '').strip()
    sort_by = request.GET.get('sort', 'rating')

    places = TouristPlace.objects.select_related('state', 'category')

    if query:
        places = places.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(state__name__icontains=query) |
            Q(short_summary__icontains=query) |
            Q(detailed_description__icontains=query) |
            Q(highlights__icontains=query)
        )

    if state_slug:
        places = places.filter(state__slug=state_slug)

    if category_slug:
        places = places.filter(category__slug=category_slug)

    if sort_by == 'name':
        places = places.order_by('name')
    elif sort_by == 'popular':
        places = places.order_by('-is_popular', '-rating')
    else:  # default top rated
        places = places.order_by('-rating', 'name')

    all_states = State.objects.all().order_by('name')
    all_categories = Category.objects.all().order_by('name')

    # Wishlist IDs for quick UI indicator
    wishlist = request.session.get('wishlist', [])

    context = {
        'places': places,
        'query': query,
        'selected_state': state_slug,
        'selected_category': category_slug,
        'sort_by': sort_by,
        'all_states': all_states,
        'all_categories': all_categories,
        'wishlist': wishlist,
    }
    return render(request, 'tourism/places_list.html', context)


def place_detail_view(request, slug):
    place = get_object_or_404(TouristPlace.objects.select_related('state', 'category'), slug=slug)
    gallery_images = place.gallery_images.all()
    approved_reviews = place.reviews.filter(is_approved=True)
    avg_rating = approved_reviews.aggregate(Avg('rating'))['rating__avg'] or place.rating
    
    similar_places = TouristPlace.objects.filter(
        Q(state=place.state) | Q(category=place.category)
    ).exclude(id=place.id).select_related('state', 'category')[:4]

    review_form = ReviewForm()
    inquiry_form = TripInquiryForm(initial={'destination_state': place.state, 'destination_place': place})
    
    wishlist = request.session.get('wishlist', [])
    is_in_wishlist = place.id in wishlist

    # Single place map pin
    place_map_json = json.dumps([{
        'name': place.name,
        'city': place.city,
        'lat': place.latitude,
        'lng': place.longitude,
        'rating': str(place.rating),
        'category': place.category.name if place.category else '',
        'url': place.get_absolute_url(),
        'image': place.display_cover,
        'entry_fee': place.entry_fee,
    }])

    context = {
        'place': place,
        'gallery_images': gallery_images,
        'reviews': approved_reviews,
        'avg_rating': round(avg_rating, 1),
        'similar_places': similar_places,
        'review_form': review_form,
        'inquiry_form': inquiry_form,
        'is_in_wishlist': is_in_wishlist,
        'place_map_json': place_map_json,
    }
    return render(request, 'tourism/place_detail.html', context)


def category_detail_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    places = category.places.select_related('state').order_by('-rating')
    wishlist = request.session.get('wishlist', [])

    context = {
        'category': category,
        'places': places,
        'wishlist': wishlist,
    }
    return render(request, 'tourism/category_detail.html', context)


@require_POST
def submit_review_view(request, place_id):
    place = get_object_or_404(TouristPlace, id=place_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.place = place
        review.is_approved = True
        review.save()
        messages.success(request, f"Thank you, {review.user_name}! Your review for {place.name} has been published.")
    else:
        messages.error(request, "There was an error in submitting your review. Please check all fields.")
    return redirect('tourism_app:place_detail', slug=place.slug)


def submit_inquiry_view(request):
    if request.method == 'POST':
        form = TripInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            dest = inquiry.destination_place.name if inquiry.destination_place else (inquiry.destination_state.name if inquiry.destination_state else 'India Tourism')
            messages.success(request, f"Thank you {inquiry.name}! Your travel inquiry for {dest} has been received. Our destination expert will contact you shortly.")
            return render(request, 'tourism/inquiry_success.html', {'inquiry': inquiry})
        else:
            messages.error(request, "Please correct the errors in the inquiry form.")
            return redirect('tourism_app:home')
    else:
        form = TripInquiryForm()
        return render(request, 'tourism/inquiry_form.html', {'form': form})


def toggle_wishlist_view(request, place_id):
    try:
        place = TouristPlace.objects.get(id=place_id)
    except TouristPlace.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Place not found'}, status=404)

    wishlist = request.session.get('wishlist', [])
    if place_id in wishlist:
        wishlist.remove(place_id)
        in_wishlist = False
        message = f"Removed '{place.name}' from your Wishlist."
    else:
        wishlist.append(place_id)
        in_wishlist = True
        message = f"Added '{place.name}' to your Travel Wishlist!"

    request.session['wishlist'] = wishlist
    request.session.modified = True

    return JsonResponse({
        'status': 'success',
        'in_wishlist': in_wishlist,
        'count': len(wishlist),
        'message': message,
        'place_name': place.name
    })


def wishlist_view(request):
    wishlist_ids = request.session.get('wishlist', [])
    saved_places = TouristPlace.objects.filter(id__in=wishlist_ids).select_related('state', 'category')
    
    # Generate Map Markers for Wishlist spots
    map_markers = []
    for place in saved_places:
        if place.latitude and place.longitude:
            map_markers.append({
                'name': place.name,
                'city': place.city,
                'lat': place.latitude,
                'lng': place.longitude,
                'rating': str(place.rating),
                'category': place.category.name if place.category else '',
                'url': place.get_absolute_url(),
                'image': place.display_cover,
                'entry_fee': place.entry_fee,
            })

    context = {
        'saved_places': saved_places,
        'map_markers_json': json.dumps(map_markers),
    }
    return render(request, 'tourism/wishlist.html', context)


def api_search_view(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'results': []})

    states = State.objects.filter(
        Q(name__icontains=query) | Q(capital__icontains=query)
    )[:5]

    places = TouristPlace.objects.filter(
        Q(name__icontains=query) | Q(city__icontains=query) | Q(state__name__icontains=query)
    ).select_related('state')[:8]

    results = []
    for s in states:
        results.append({
            'type': 'State',
            'title': s.name,
            'subtitle': f"Capital: {s.capital}",
            'url': s.get_absolute_url(),
            'image': s.display_cover,
        })

    for p in places:
        results.append({
            'type': 'Tourist Place',
            'title': p.name,
            'subtitle': f"{p.city}, {p.state.name}",
            'url': p.get_absolute_url(),
            'image': p.display_cover,
            'rating': str(p.rating),
        })

    return JsonResponse({'results': results})
