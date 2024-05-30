from django.shortcuts import render,get_object_or_404, redirect
from .models import Listing, ListingMedia
from .forms import ListingForm
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib import messages
import uuid
import os
from django.core.paginator import Paginator
from supabase import create_client, Client
from django.contrib.auth.decorators import login_required


supabase: Client = create_client(os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_SEC'))
bucket_name = os.environ.get('SUPABASE_BUCKET')

def index(request):
    base_query = Listing.objects.prefetch_related('medias').all().order_by('-created_at')
    price = request.GET.get('price')
    city = request.GET.get('city')
    subcity = request.GET.get('subcity')
    my = request.GET.get('my')

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
        },
        "user":request.user
    }

    return render(request, 'listing/index.html', context)

@login_required
def my_listings(request):
    listings = Listing.objects.filter(user_id=request.user.id).order_by('-created_at') 
    print('REQUEST USER ID ',request.user.id)
    paginator = Paginator(listings, 8)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  

    if listings.count() < 1:
        messages.info(request, "You Have No House Listing, Click Post to create one!")
    context = {
        "listings":page_obj,
        "page_obj":page_obj,
        "cities": ['Addis Ababa', 'Mekelle','Adama','Debrezeit'],
        "subcities":['Arada','Kirkos','Bole','Addis Ketema'],
        "price_ranges":{
             '5000':'<=5000',
             '10000':'<=10000',
             '20000': '<=20000'
        },
        "user":request.user
    }
    return render(request,'listing/my_listings.html', context)


def listing_retrieve(request,id):
    listing = get_object_or_404(Listing, id=id)
    context = {
        "listing":listing
    }
    print(listing)
    return render(request, 'listing/detail.html', context)

@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            form.instance.user_id = request.user.id
            form.save() 
            if request.FILES.getlist('media'):
                    
                    for media_file in request.FILES.getlist('media'):
                        # media storage upload
                        # file_name = f'listing_{form.instance.id}_{uuid.uuid4()}{os.path.splitext(media_file.name)[1]}'
                        # file_path = f'listings/{file_name}'
                        # listing_media = ListingMedia()
                        # listing_media.listing = form.instance
                        # listing_media.media_type = media_file.content_type
                        # default_storage.save(file_path, media_file)
                        # file_url = f'{settings.MEDIA_URL}{file_path}'
                        # listing_media.file_path = file_url
                        # listing_media.save()

                        # supabase upload
                        file = media_file
                        file_ext = os.path.splitext(file.name)[1]
                        file_name = f'listing_{form.instance.id}_{uuid.uuid4()}{os.path.splitext(media_file.name)[1]}'
                        listing_media = ListingMedia()
                        listing_media.listing = form.instance
                        listing_media.media_type = media_file.content_type
                        upload_response = supabase.storage.from_(bucket_name).upload(file_name, file.read(), file_options={"content-type": f"image/{file_ext}"})
                        if upload_response.status_code == 200:
                            print('Upload successful:', upload_response)
                            public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
                            print(public_url)
                            listing_media.file_path = public_url
                            listing_media.file_name = file_name
                            listing_media.save()
                        else:
                            print('Upload failed:', upload_response['error'])


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

@login_required
def set_status(request,id):
    listing = get_object_or_404(Listing, id=id,user_id=request.user.id)
    listing.status = not listing.status
    listing.save()

@login_required
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

@login_required
def listing_delete(request, id):
    listing = get_object_or_404(Listing, id=id)
    medias = listing.medias.all()
    if medias.count() > 0:
        for media in medias:
        #     file_path = media.file_path.replace(settings.MEDIA_URL, '')
        #     if default_storage.exists(file_path):
        #         default_storage.delete(file_path)
        #     media.delete()

        # supabase delete
            res = supabase.storage.from_(bucket_name).remove(media.file_name)
    listing.delete()
    return redirect("listings")