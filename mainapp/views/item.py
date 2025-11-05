from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from mainapp.forms import ItemForm
from mainapp.models import Item


@transaction.atomic
def generate_and_save_item(form_instance):
    """Generate code and save item atomically - prevents race conditions"""
    last_item = Item.objects.select_for_update().order_by('-code').first()
    if last_item:
        last_number = int(last_item.code.split('-')[1])
        new_code = f'IT-{(last_number + 1):04d}'
    else:
        new_code = 'IT-0001'
    
    form_instance.code = new_code
    form_instance.save()
    return form_instance


@login_required
def create_item(request, code=None):
    """Create or Edit Item"""
    # Check if editing
    item_instance = None
    if code:
        try:
            item_instance = Item.objects.get(code=code)
        except Item.DoesNotExist:
            messages.error(request, f'Item with code {code} not found.')
            return redirect('load:create-item')
    
    # Get last code for display (without lock)
    last_item = Item.objects.order_by('-code').first()
    last_code = last_item.code if last_item else 'None'
    
    # Calculate next code for display
    if last_item:
        last_number = int(last_item.code.split('-')[1])
        next_code = f'IT-{(last_number + 1):04d}'
    else:
        next_code = 'IT-0001'
    
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item_instance)
        if form.is_valid():
            try:
                if item_instance:
                    # Editing existing item
                    item = form.save()
                    messages.success(request, f'Item "{item.name}" updated successfully!')
                else:
                    # Creating new item
                    item = form.save(commit=False)
                    item = generate_and_save_item(item)
                    messages.success(request, f'Item "{item.name}" created successfully with code {item.code}!')
                return redirect('load:create-item')
            except Exception as e:
                messages.error(request, f'Error saving item: {str(e)}')
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
        form = ItemForm(instance=item_instance)
    
    # Get all items for the list
    items = Item.objects.all().order_by('-code')
    
    context = {
        'form': form,
        'page_title': 'Item Management',
        'last_code': last_code,
        'next_code': next_code,
        'items': items,
        'editing': item_instance is not None,
        'edit_item': item_instance,
    }
    return render(request, 'create_item.html', context)


@login_required
def list_item(request):
    """List all items"""
    items = Item.objects.all().order_by('code')
    context = {
        'items': items,
        'page_title': 'Item List',
    }
    return render(request, 'list_item.html', context)


@login_required
def delete_item(request, code):
    """Delete an item"""
    try:
        item = Item.objects.get(code=code)
        item_name = item.name
        item.delete()
        messages.success(request, f'Item "{item_name}" ({code}) deleted successfully!')
    except Item.DoesNotExist:
        messages.error(request, f'Item with code {code} not found.')
    except Exception as e:
        messages.error(request, f'Error deleting item: {str(e)}')
    
    return redirect('load:create-item')