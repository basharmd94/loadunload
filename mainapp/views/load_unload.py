from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mainapp.forms import LoadUnloadForm
from mainapp.models import LoadUnload


@login_required
def create_load_unload(request):
    """Create new Load/Unload transaction"""
    if request.method == 'POST':
        form = LoadUnloadForm(request.POST)
        if form.is_valid():
            load_unload = form.save()
            messages.success(
                request, 
                f'{load_unload.transaction_type} transaction created successfully! Challan No: {load_unload.challan_no}'
            )
            return redirect('load:create-load-unload')
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
        form = LoadUnloadForm()
    
    context = {
        'form': form,
        'page_title': 'Create Load/Unload Transaction',
    }
    return render(request, 'create_load_unload.html', context)