from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import ProtectedError
from mainapp.forms import EmployeeForm
from mainapp.models import Employee


@transaction.atomic
def generate_and_save_employee(form_instance):
    """Generate code and save employee atomically - prevents race conditions"""
    last_emp = Employee.objects.select_for_update().order_by('-code').first()
    if last_emp:
        last_number = int(last_emp.code.split('-')[1])
        new_code = f'EMP-{(last_number + 1):04d}'
    else:
        new_code = 'EMP-0001'
    
    form_instance.code = new_code
    form_instance.save()
    return form_instance


@login_required
def create_employee(request, code=None):
    """Create or Edit Employee"""
    employee_instance = None
    if code:
        try:
            employee_instance = Employee.objects.get(code=code)
        except Employee.DoesNotExist:
            messages.error(request, f'Employee with code {code} not found.')
            return redirect('load:create-employee')
    
    # Get last code for display
    last_emp = Employee.objects.order_by('-code').first()
    last_code = last_emp.code if last_emp else 'None'
    
    if last_emp:
        last_number = int(last_emp.code.split('-')[1])
        next_code = f'EMP-{(last_number + 1):04d}'
    else:
        next_code = 'EMP-0001'
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee_instance)
        if form.is_valid():
            try:
                if employee_instance:
                    employee = form.save()
                    messages.success(request, f'Employee "{employee.name}" updated successfully!')
                else:
                    employee = form.save(commit=False)
                    employee = generate_and_save_employee(employee)
                    messages.success(request, f'Employee "{employee.name}" created successfully with code {employee.code}!')
                return redirect('load:create-employee')
            except Exception as e:
                messages.error(request, f'Error saving employee: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f'{error}')
                    else:
                        field_label = form.fields[field].label or field
                        messages.error(request, f'{field_label}: {error}')
    else:
        form = EmployeeForm(instance=employee_instance)
    
    employees = Employee.objects.all().order_by('-code')
    
    context = {
        'form': form,
        'page_title': 'Employee Management',
        'last_code': last_code,
        'next_code': next_code,
        'employees': employees,
        'editing': employee_instance is not None,
        'edit_employee': employee_instance,
    }
    return render(request, 'create_employee.html', context)


@login_required
def delete_employee(request, code):
    """Delete an employee"""
    try:
        employee = Employee.objects.get(code=code)
        emp_name = employee.name
        employee.delete()
        messages.success(request, f'Employee "{emp_name}" ({code}) deleted successfully!')
    except Employee.DoesNotExist:
        messages.error(request, f'Employee with code {code} not found.')
    except ProtectedError:
        messages.error(request, 'Cannot delete employee because it is referenced by existing entries.')
    except Exception as e:
        messages.error(request, f'Error deleting employee: {str(e)}')
    
    return redirect('load:create-employee')
