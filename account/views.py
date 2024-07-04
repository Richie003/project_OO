from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from account.decorators import allowed_user, unauthenticated_user, noCategory
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from shop.models import Order, Product
from .models import *
from .forms import *


# User Autyhentication (Sign_Up, Sign_In, Sign_Out)
@unauthenticated_user
def register(request):
    form = UserAdminCreationForm
    if request.method == 'POST':
        form = UserAdminCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            # username = request.POST.get('username')
            # password = request.POST.get('password1')

            # user = authenticate(request, username=username, password=password)

            # login(request, user)
            # messages.success(request, f'Profile successfully updated ')
            return redirect('login')
    context = {
        'form':form
    }
    return render(request, 'sign_up.html', context)

@unauthenticated_user
@csrf_protect
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            get_user = Bio.objects.filter(user_id=request.user.pk)
            get_user.update(
                active_user=True
            )
            request.session['member_id'] = username + '45'
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                messages.info(request, f"{username} logged in successfully, you're now a verified customer :) ✔")
                return redirect('category')
        else:
            messages.info(request, 'registration number OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def log_out(request):
    user = request.user.pk
    get_user = Bio.objects.filter(user_id=user)
    get_user.update(
        active_user=False
    )
    logout(request)
    # del request.session['member_id']
    return redirect('login')

# Categorize the User under CATEGORY = ['Merchant', 'Customer', 'None']
# @noCategory
@allowed_user(allowed_roles=[''])
def sub_category(request):
    form = SubscriptionForm
    user = User.objects.all().filter(username=request.user)
    if request.method == "POST":
        form = SubscriptionForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            if request.POST.get('plan') == 'Merchant':
                user.update(
                    category='Merchant'
                )
                return redirect('/')
            else:
                user.update(
                    category='Customer'
                )
                return redirect('/')

    context = {
        'form': form
    }
    return render(request, 'category.html', context)


# Users Profile and Update
# @noCategory
@login_required(login_url='login')
def user_profile(request):
    # print(f"Referer: {request.META['HTTP_REFERER']}")
    bio = Bio.objects.get(user = request.user)
    user = User.objects.get(username=request.user)
    update_bio = BioForms(instance=bio)
    form = UserAdminCreationForm(instance=user)
    if request.method == 'POST':
        if 'bio-profile' in request.POST:
            update_bio = BioForms(request.POST or None, request.FILES, instance=bio)
            if update_bio.is_valid():
                update_bio.save()
                messages.success(request, f'Profile successfully updated ')
                return redirect('profile')
        if 'main-profile' in request.POST:
             form = UserAdminCreationForm(request.POST or None, instance=user)
             if form.is_valid():
                 form.save()
                 username = request.POST.get('username')
                 password = request.POST.get('password1')

                 user = authenticate(request, username=username, password=password)

                 login(request, user)
                 messages.success(request, f'Profile successfully updated ')
                 return redirect('profile')
    context = {
        'bio':bio,
        'form':form,
        'update_bio':update_bio
    }
    return render(request, 'profile.html', context)

# Merchant User Products and Orders Dashboard
# @noCategory
@login_required(login_url='login')
@allowed_user(allowed_roles=['Merchant'])
def user_prod_stats(request):
    items = Product.objects.filter(seller=request.user)
    orders = Order.objects.filter(seller=request.user)
    total = sum([i.price for i in orders])
    context = {
        'items': items,
        'orders':orders,
        'total': total
    }

    return render(request, 'user_admin.html', context)


def remove_product(request, pk):
    item = Product.objects.get(pk=pk)
    item.delete()

    return HttpResponse('success', content_type='text/plain')


def remove_order(request, pk):
    order = Order.objects.get(pk=pk)
    order.delete()

    return HttpResponse('success', content_type='text/plain')