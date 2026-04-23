from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Q
from mainapp.models import LoadUnload, GLDetail, Employee


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

    # Accounting KPIs from GLDetail
    gl_entries = GLDetail.objects.all()
    gl_totals = gl_entries.aggregate(
        total_income=Sum('amount', filter=Q(gl_type=GLDetail.INCOME)),
        total_expense=Sum('amount', filter=Q(gl_type=GLDetail.EXPENSE)),
        today_income=Sum('amount', filter=Q(gl_type=GLDetail.INCOME, transaction_date=today)),
        today_expense=Sum('amount', filter=Q(gl_type=GLDetail.EXPENSE, transaction_date=today)),
    )

    total_income = gl_totals['total_income'] or 0
    total_expense = gl_totals['total_expense'] or 0
    net_profit = total_income - total_expense
    today_income = gl_totals['today_income'] or 0
    today_expense = gl_totals['today_expense'] or 0

    total_employees = Employee.objects.filter(is_active=True).count()

    # Recent expenses for dashboard
    recent_expenses = GLDetail.objects.filter(gl_type=GLDetail.EXPENSE).order_by('-transaction_date', '-created_at')[:6]

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
        # Accounting KPIs
        'total_income': total_income,
        'total_expense': total_expense,
        'net_profit': net_profit,
        'today_income': today_income,
        'today_expense': today_expense,
        'total_employees': total_employees,
        'recent_expenses': recent_expenses,
    }
    return render(request, 'index.html', context)