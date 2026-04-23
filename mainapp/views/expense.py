from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from mainapp.forms import ExpenseForm
from mainapp.models import GLDetail


@login_required
def create_expense(request):
    """Create a new expense entry in GLDetail"""
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            try:
                expense = form.save(commit=False)
                expense.gl_type = GLDetail.EXPENSE
                expense.created_by = request.user
                expense.save()
                messages.success(request, f'Expense "{expense.description}" of ৳{expense.amount} added successfully!')
                return redirect('load:create-expense')
            except Exception as e:
                messages.error(request, f'Error saving expense: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f'{error}')
                    else:
                        field_label = form.fields[field].label or field
                        messages.error(request, f'{field_label}: {error}')
    else:
        form = ExpenseForm()
    
    # Recent expenses for quick reference
    recent_expenses = GLDetail.objects.filter(gl_type=GLDetail.EXPENSE).order_by('-transaction_date', '-created_at')[:10]
    
    context = {
        'form': form,
        'page_title': 'Add Expense',
        'recent_expenses': recent_expenses,
    }
    return render(request, 'create_expense.html', context)


@login_required
def list_gl(request):
    """List all GL entries (income + expense) with summary"""
    entries = GLDetail.objects.all().select_related('category', 'employee', 'load_unload', 'created_by')
    
    # Calculate totals
    totals = entries.aggregate(
        total_income=Sum('amount', filter=Q(gl_type=GLDetail.INCOME)),
        total_expense=Sum('amount', filter=Q(gl_type=GLDetail.EXPENSE)),
    )
    
    total_income = totals['total_income'] or 0
    total_expense = totals['total_expense'] or 0
    net_profit = total_income - total_expense
    
    context = {
        'entries': entries,
        'page_title': 'General Ledger',
        'total_income': total_income,
        'total_expense': total_expense,
        'net_profit': net_profit,
    }
    return render(request, 'list_gl.html', context)


@login_required
def delete_expense(request, pk):
    """Delete an expense GL entry (only manual expenses, not auto-posted income)"""
    try:
        entry = GLDetail.objects.get(pk=pk)
        if entry.load_unload:
            messages.error(request, 'Cannot delete auto-posted income entries. Delete the Load/Unload transaction instead.')
        else:
            desc = entry.description
            entry.delete()
            messages.success(request, f'Expense "{desc}" deleted successfully!')
    except GLDetail.DoesNotExist:
        messages.error(request, 'Entry not found.')
    except Exception as e:
        messages.error(request, f'Error deleting entry: {str(e)}')
    
    return redirect('load:list-gl')
