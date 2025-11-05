from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import ProtectedError
from mainapp.forms import PartyForm
from mainapp.models import Party


@transaction.atomic
def generate_and_save_party(form_instance):
    """Generate code and save party atomically - prevents race conditions"""
    last_party = Party.objects.select_for_update().order_by('-code').first()
    if last_party:
        last_number = int(last_party.code.split('-')[1])
        new_code = f'PR-{(last_number + 1):04d}'
    else:
        new_code = 'PR-0001'
    
    form_instance.code = new_code
    form_instance.save()
    return form_instance


@login_required
def create_party(request, code=None):
    """Create or Edit Party"""
    # Check if editing
    party_instance = None
    if code:
        try:
            party_instance = Party.objects.get(code=code)
        except Party.DoesNotExist:
            messages.error(request, f'Party with code {code} not found.')
            return redirect('load:create-party')
    
    # Get last code for display (without lock)
    last_party = Party.objects.order_by('-code').first()
    last_code = last_party.code if last_party else 'None'
    
    # Calculate next code for display
    if last_party:
        last_number = int(last_party.code.split('-')[1])
        next_code = f'PR-{(last_number + 1):04d}'
    else:
        next_code = 'PR-0001'
    
    if request.method == 'POST':
        form = PartyForm(request.POST, instance=party_instance)
        if form.is_valid():
            try:
                if party_instance:
                    # Editing existing party
                    party = form.save()
                    messages.success(request, f'Party "{party.name}" updated successfully!')
                else:
                    # Creating new party
                    party = form.save(commit=False)
                    party = generate_and_save_party(party)
                    messages.success(request, f'Party "{party.name}" created successfully with code {party.code}!')
                return redirect('load:create-party')
            except Exception as e:
                messages.error(request, f'Error saving party: {str(e)}')
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
        form = PartyForm(instance=party_instance)
    
    # Get all parties for the list
    parties = Party.objects.all().order_by('-code')
    
    context = {
        'form': form,
        'page_title': 'Party Management',
        'last_code': last_code,
        'next_code': next_code,
        'parties': parties,
        'editing': party_instance is not None,
        'edit_party': party_instance,
    }
    return render(request, 'create_party.html', context)


@login_required
def list_party(request):
    """List all parties"""
    parties = Party.objects.all().order_by('code')
    context = {
        'parties': parties,
        'page_title': 'Party List',
    }
    return render(request, 'list_party.html', context)


@login_required
def delete_party(request, code):
    """Delete a party"""
    try:
        party = Party.objects.get(code=code)
        party_name = party.name
        party.delete()
        messages.success(request, f'Party "{party_name}" ({code}) deleted successfully!')
    except Party.DoesNotExist:
        messages.error(request, f'Party with code {code} not found.')
    except ProtectedError:
        messages.error(request, 'Cannot delete party because it is referenced by existing transactions.')
    except Exception as e:
        messages.error(request, f'Error deleting party: {str(e)}')
    
    return redirect('load:create-party')