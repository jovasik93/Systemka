from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
import pandas as pd
from .forms import UploadFileForm, ItemEditForm, PasswordConfirmationForm
from django.contrib.auth import authenticate
from .models import Item
def home(request):
    if request.user.is_authenticated:
        return redirect('item_list')  # Перенаправление на item_list, если пользователь авторизован
    else:
        return redirect('login')  # Перенаправление на login, если пользователь не авторизован

def custom_404_view(request, exception):
    """Вывод кастомной страницы 404"""
    return render(request, 'myapp/404.html', status=404)
@login_required
def item_list(request):
    # Обработка загрузки файла
    if request.method == 'POST' and 'upload_file' in request.POST:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                # Чтение Excel-файла
                df = pd.read_excel(file)
                for index, row in df.iterrows():
                    Item.objects.create(
                        serial_number=row.iloc[0],  # Серийный номер
                        owner=row.iloc[1],          # Владелец
                        description=row.iloc[2],    # Описание
                        start_date=row.iloc[3],     # Дата начала
                        end_date=row.iloc[4]        # Дата окончания
                    )
                return redirect('item_list')  # Перенаправление после успешной загрузки
            except Exception as e:
                # Обработка ошибок
                return render(request, 'myapp/item_list.html', {
                    'error': f"Error processing file: {str(e)}",
                    'form': UploadFileForm(),
                    'items': Item.objects.all(),
                    'expiring_items': Item.objects.filter(end_date__gte=timezone.now().date(), end_date__lte=timezone.now().date() + timedelta(days=90))
                })
        else:
            # Если форма не валидна, вернуть страницу с ошибкой
            return render(request, 'myapp/item_list.html', {
                'error': "Invalid file format.",
                'form': form,
                'items': Item.objects.all(),
                'expiring_items': Item.objects.filter(end_date__gte=timezone.now().date(), end_date__lte=timezone.now().date() + timedelta(days=90))
            })
    else:
        form = UploadFileForm()

    # Фильтрация и отображение данных
    serial_number = request.GET.get('serial_number', None)
    owner = request.GET.get('owner', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    items = Item.objects.all()

    if serial_number:
        items = items.filter(serial_number__icontains=serial_number)
    if owner:
        items = items.filter(owner__icontains=owner)
    if start_date:
        items = items.filter(start_date__gte=start_date)
    if end_date:
        items = items.filter(end_date__lte=end_date)

    # Фильтрация сертификатов, у которых до даты окончания осталось 3 или меньше месяцев
    today = timezone.now().date()
    three_months_later = today + timedelta(days=90)
    expiring_items = Item.objects.filter(end_date__gte=today, end_date__lte=three_months_later)

    # Всегда возвращаем HttpResponse
    return render(request, 'myapp/item_list.html', {
        'items': items,
        'expiring_items': expiring_items,
        'form': form,
    })
@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'myapp/add_item.html', {'form': form})

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'myapp/confirm_delete.html', {'item': item})

@login_required
def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'myapp/item_detail.html', {'item': item})



@login_required
def expired_items(request):
    # Фильтрация сертификатов с истекшим сроком действия
    today = timezone.now().date()
    expired_items = Item.objects.filter(end_date__lt=today)  # end_date < today

    return render(request, 'myapp/expired_items.html', {'expired_items': expired_items})

@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        if 'confirm_password' in request.POST:
            # Форма подтверждения пароля
            password_form = PasswordConfirmationForm(request.POST)
            if password_form.is_valid():
                password = password_form.cleaned_data['password']
                user = authenticate(username=request.user.username, password=password)
                if user is not None:
                    # Пароль верный, показываем форму редактирования
                    form = ItemEditForm(instance=item)
                    return render(request, 'myapp/edit_item.html', {
                        'item': item,
                        'form': form,
                        'show_edit_form': True,  # Показываем форму редактирования
                    })
                else:
                    # Пароль неверный
                    password_form.add_error('password', 'Неверный пароль')
                    return render(request, 'myapp/edit_item.html', {
                        'item': item,
                        'password_form': password_form,
                        'show_edit_form': False,
                    })
        elif 'edit_item' in request.POST:
            # Форма редактирования записи
            form = ItemEditForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                messages.success(request, 'Изменения успешно сохранены!')
                return redirect('item_detail', item_id=item.id)
    else:
        # Первоначальный запрос, показываем форму подтверждения пароля
        password_form = PasswordConfirmationForm()
        return render(request, 'myapp/edit_item.html', {
            'item': item,
            'password_form': password_form,
            'show_edit_form': False,
        })

    # Если что-то пошло не так, показываем форму подтверждения пароля
    password_form = PasswordConfirmationForm()
    return render(request, 'myapp/edit_item.html', {
        'item': item,
        'password_form': password_form,
        'show_edit_form': False,
    })

