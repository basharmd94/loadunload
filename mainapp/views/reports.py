from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from mainapp.models import GLDetail


@login_required
def financial_report(request):
    """Financial report with date range filtering"""
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    entries = GLDetail.objects.all().select_related('category', 'employee', 'load_unload', 'created_by')

    # Apply date filters
    filtered = False
    if from_date:
        entries = entries.filter(transaction_date__gte=from_date)
        filtered = True
    if to_date:
        entries = entries.filter(transaction_date__lte=to_date)
        filtered = True

    # Calculate totals for filtered data
    totals = entries.aggregate(
        total_income=Sum('amount', filter=Q(gl_type=GLDetail.INCOME)),
        total_expense=Sum('amount', filter=Q(gl_type=GLDetail.EXPENSE)),
    )

    total_income = totals['total_income'] or 0
    total_expense = totals['total_expense'] or 0
    net_profit = total_income - total_expense

    context = {
        'entries': entries,
        'page_title': 'Financial Report',
        'total_income': total_income,
        'total_expense': total_expense,
        'net_profit': net_profit,
        'from_date': from_date,
        'to_date': to_date,
        'filtered': filtered,
    }
    return render(request, 'financial_report.html', context)
