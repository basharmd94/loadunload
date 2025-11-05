from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mainapp.forms import LoadUnloadForm
from mainapp.models import LoadUnload


@login_required
def create_load_unload(request, pk=None):
    """Create or Edit Load/Unload transaction"""
    # Check if editing
    transaction_instance = None
    if pk:
        transaction_instance = get_object_or_404(LoadUnload, pk=pk)
    
    if request.method == 'POST':
        form = LoadUnloadForm(request.POST, instance=transaction_instance)
        if form.is_valid():
            load_unload = form.save()
            if transaction_instance:
                messages.success(
                    request, 
                    f'{load_unload.transaction_type} transaction updated successfully! Challan No: {load_unload.challan_no}'
                )
            else:
                messages.success(
                    request, 
                    f'{load_unload.transaction_type} transaction created successfully! Challan No: {load_unload.challan_no}'
                )
            return redirect('load:list-load-unload')
        else:
            # Show specific errors
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f'{error}')
                    else:
                        field_label = form.fields[field].label or field
                        messages.error(request, f'{field_label}: {error}')
    else:
        form = LoadUnloadForm(instance=transaction_instance)
    
    context = {
        'form': form,
        'page_title': 'Edit Transaction' if transaction_instance else 'Create Load/Unload Transaction',
        'editing': transaction_instance is not None,
        'transaction': transaction_instance,
    }
    return render(request, 'create_load_unload.html', context)


@login_required
def list_load_unload(request):
    """List all Load/Unload transactions"""
    transactions = LoadUnload.objects.all().order_by('-transaction_date', '-created_at')
    context = {
        'transactions': transactions,
        'page_title': 'Load/Unload Transactions',
    }
    return render(request, 'load_unload_list.html', context)


@login_required
def delete_load_unload(request, pk):
    """Delete a Load/Unload transaction"""
    try:
        transaction = LoadUnload.objects.get(pk=pk)
        challan_no = transaction.challan_no
        transaction_type = transaction.transaction_type
        transaction.delete()
        messages.success(request, f'{transaction_type} transaction (Challan: {challan_no}) deleted successfully!')
    except LoadUnload.DoesNotExist:
        messages.error(request, 'Transaction not found.')
    except Exception as e:
        messages.error(request, f'Error deleting transaction: {str(e)}')
    
    return redirect('load:list-load-unload')


@login_required
def recent_loads(request):
    """Show recent Load transactions (latest 6)"""
    transactions = LoadUnload.objects.filter(transaction_type='Load').order_by('-transaction_date', '-created_at')[:6]
    context = {
        'transactions': transactions,
        'page_title': 'Recent Loads',
    }
    return render(request, 'load_unload_list.html', context)


@login_required
def recent_unloads(request):
    """Show recent Unload transactions (latest 6)"""
    transactions = LoadUnload.objects.filter(transaction_type='Unload').order_by('-transaction_date', '-created_at')[:6]
    context = {
        'transactions': transactions,
        'page_title': 'Recent Unloads',
    }
    return render(request, 'load_unload_list.html', context)