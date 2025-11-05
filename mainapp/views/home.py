from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from mainapp.models import LoadUnload


@login_required
def index(request):
    today = timezone.localdate()
    transactions = LoadUnload.objects.all()

    total_transactions = transactions.count()
    total_loads = transactions.filter(transaction_type='Load').count()
    total_unloads = transactions.filter(transaction_type='Unload').count()
    today_transactions = transactions.filter(transaction_date=today).count()
    today_loads = transactions.filter(transaction_type='Load', transaction_date=today).count()
    today_unloads = transactions.filter(transaction_type='Unload', transaction_date=today).count()

    aggregates = transactions.aggregate(
        total_boxes=Sum('box_qty'),
        total_quantity=Sum('quantity'),
        total_amount=Sum('total_amount'),
    )

    recent_loads = transactions.filter(transaction_type='Load').order_by('-transaction_date', '-created_at')[:6]
    recent_unloads = transactions.filter(transaction_type='Unload').order_by('-transaction_date', '-created_at')[:6]

    context = {
        'user': request.user,
        'kpi_total_transactions': total_transactions,
        'kpi_total_loads': total_loads,
        'kpi_total_unloads': total_unloads,
        'kpi_today_transactions': today_transactions,
        'kpi_today_loads': today_loads,
        'kpi_today_unloads': today_unloads,
        'kpi_total_boxes': aggregates.get('total_boxes') or 0,
        'kpi_total_quantity': aggregates.get('total_quantity') or 0,
        'kpi_total_amount': aggregates.get('total_amount') or 0,
        'today': today,
        'recent_loads': recent_loads,
        'recent_unloads': recent_unloads,
    }
    return render(request, 'index.html', context)