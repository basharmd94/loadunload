from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mainapp.forms import ExpenseCategoryForm
from mainapp.models import ExpenseCategory


@login_required
def create_category(request, pk=None):
    """Create or Edit Expense Category"""
    category_instance = None
    if pk:
        try:
            category_instance = ExpenseCategory.objects.get(pk=pk)
        except ExpenseCategory.DoesNotExist:
            messages.error(request, 'Category not found.')
            return redirect('load:create-category')
    
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST, instance=category_instance)
        if form.is_valid():
            try:
                category = form.save()
                if category_instance:
                    messages.success(request, f'Category "{category.name}" updated successfully!')
                else:
                    messages.success(request, f'Category "{category.name}" created successfully!')
                return redirect('load:create-category')
            except Exception as e:
                messages.error(request, f'Error saving category: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f'{error}')
                    else:
                        field_label = form.fields[field].label or field
                        messages.error(request, f'{field_label}: {error}')
    else:
        form = ExpenseCategoryForm(instance=category_instance)
    
    categories = ExpenseCategory.objects.all().order_by('name')
    
    context = {
        'form': form,
        'page_title': 'Category Management',
        'categories': categories,
        'editing': category_instance is not None,
        'edit_category': category_instance,
    }
    return render(request, 'create_category.html', context)


@login_required
def delete_category(request, pk):
    """Delete a category"""
    try:
        category = ExpenseCategory.objects.get(pk=pk)
        cat_name = category.name
        category.delete()
        messages.success(request, f'Category "{cat_name}" deleted successfully!')
    except ExpenseCategory.DoesNotExist:
        messages.error(request, 'Category not found.')
    except Exception as e:
        messages.error(request, f'Error deleting category: {str(e)}')
    
    return redirect('load:create-category')
