from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from listing.models import Listing
from django.utils import timezone
from django.db.models import Count, Max
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth, TruncDay, TruncDate


def dashboard(request):
    # if not request.user.is_admin:
    #     return redirect('listings')
    today = timezone.now().date()
    total_users = CustomUser.objects.count()
    today_new_users = CustomUser.objects.filter(created_at=today).count()
    month_new_users = CustomUser.objects.filter(created_at__year=today.year, created_at__month=today.month).count()
    year_new_users = CustomUser.objects.filter(created_at__year=today.year).count()

    start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())

    # Count the number of active users who logged in at least once in the last week
    active_users = CustomUser.objects.filter(is_active=True).annotate(max_login_date=Max('last_login')).filter(max_login_date__gte=start_of_week).count()

    # users chart
    user_counts = CustomUser.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    labels = [user_count['month'].strftime('%b') for user_count in user_counts]
    data = [user_count['count'] for user_count in user_counts]

    # listings chart
    # listing_counts = Listing.objects.annotate(day=TruncDay('created_at')).values('day').annotate(count=Count('id')).order_by('day')
    # pr_labels = [listing_count['day'].strftime('%a') for listing_count in listing_counts]
    # pr_data = [listing_count['count'] for listing_count in listing_counts]
    # pr_labels = ['Mon','Tue','Wed','Thur','Fri','Sat','Sun']

    start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())

    # Get the end of the current week
    end_of_week = start_of_week + timedelta(days=6)

    # Create a list of all days of the week
    all_days = [start_of_week + timedelta(days=i) for i in range(7)]

    # Get the listing counts for each day of the week
    listing_counts = Listing.objects.filter(created_at__date__range=[start_of_week, end_of_week]).annotate(day=TruncDay('created_at')).values('day').annotate(count=Count('id')).order_by('day')

    # Create a dictionary to map the counts to the corresponding days
    count_dict = {listing_count['day'].date(): listing_count['count'] for listing_count in listing_counts}

    # Create the data and labels lists
    pr_data = [count_dict.get(day.date(), 0) for day in all_days]
    pr_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    # listing_counts = Listing.objects.annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).order_by('day')

    # pr_labels = [listing_count['day'].strftime('%Y-%m-%d') for listing_count in listing_counts]
    # pr_data = [listing_count['count'] for listing_count in listing_counts]
    
    total_listings_count = Listing.objects.count()
    month_new_listings = Listing.objects.filter(created_at__year=today.year, created_at__month=today.month).count()

    context = {
        'total_users':total_users,
        'today_new_users':today_new_users,
        'month_new_users':month_new_users,
        'year_new_users':year_new_users,
        'active_users':active_users,
        'labels': labels,
        'user_data': data,
        'pr_labels':pr_labels,
        'pr_data':pr_data,
        'total_listings_count':total_listings_count,
        'month_new_listings':month_new_listings
    }
    return render(request,'admin/pages/dashboard.html', context)