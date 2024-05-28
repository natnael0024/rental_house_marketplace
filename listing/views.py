from django.shortcuts import render,get_object_or_404, redirect
from .models import Listing, ListingMedia
from .forms import ListingForm
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib import messages
import uuid
import os
from django.core.paginator import Paginator



def index(request):
    base_query = Listing.objects.prefetch_related('medias').all().order_by('-created_at')
    price = request.GET.get('price')
    city = request.GET.get('city')
    subcity = request.GET.get('subcity')

    if price:
        base_query = base_query.filter(price__lte=price)
    if city:
        base_query = base_query.filter(city__icontains=city)
    if subcity:
        base_query = base_query.filter(sub_city__icontains=subcity)
    listings = base_query

    paginator = Paginator(listings, 8)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if listings.count() < 1:
        messages.info(request, "No House Found")
    context = {
        "listings":page_obj,
        "page_obj":page_obj,
        "cities": ['Addis Ababa', 'Mekelle','Adama','Debrezeit'],
        "subcities":['Arada','Kirkos','Bole','Addis Ketema'],
        "price_ranges":{
             '5000':'<=5000',
             '10000':'<=10000',
             '20000': '<=20000'
        }
    }

    return render(request, 'listing/index.html', context)


def listing_retrieve(request,id):
    listing = get_object_or_404(Listing, id=id)
    context = {
        "listing":listing
    }
    print(listing)
    return render(request, 'listing/detail.html', context)


def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            form.instance.user_id = request.user.id
            form.save() 
            if request.FILES.getlist('media'):
                    print("!@@@@@@@@@@@@@@@@!@@@@@@@@@@@@@@!@@@@@@@@@@@@!")
                    for media_file in request.FILES.getlist('media'):
                        file_name = f'listing_{form.instance.id}_{uuid.uuid4()}{os.path.splitext(media_file.name)[1]}'
                        file_path = f'listings/{file_name}'
                        listing_media = ListingMedia()
                        listing_media.listing = form.instance
                        listing_media.media_type = media_file.content_type
                        default_storage.save(file_path, media_file)
                        file_url = f'{settings.MEDIA_URL}{file_path}'
                        listing_media.file_path = file_url
                        listing_media.save()

            listings = Listing.objects.all()
            context = {
                "listings":listings
            }
            return redirect("home")
        return 
    form = ListingForm()
    context = {
        'form':form
    }
    return render(request, "listing/create.html",context)

def set_status(request,id):
    listing = get_object_or_404(Listing, id=id,user_id=request.user.id)
    listing.status = not listing.status
    listing.save()



def listing_update(request, id):
    listing = get_object_or_404(Listing, id=id)

    if request.method == 'POST':
        form = ListingForm(request.POST,instance=listing)
        if form.is_valid():
            form.save()
            return redirect("listings")
        
    else:
        form = ListingForm(instance=listing)

    context = {
        'form':form
    }
    return render(request, "listing/edit.html",context)

# def listing_delete(request, id):
#     listing = get_object_or_404(Listing, id=id)
#     listing.delete()
#     return redirect("listings")