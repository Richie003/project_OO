import json
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import Product, Review, Order, CheckOut
from account.models import User
from .forms import ReviewForm, ProductForm, CheckOutForm
from account.decorators import allowed_user, unauthenticated_user, noCategory
from django.contrib.auth.decorators import login_required


# Create your views here.

# @noCategory
def shop_items(request):
    items = Product.objects.all()
    context = {
        'items': items
    }
    return render(request, 'products.html', context)


# @noCategory
@login_required(login_url='login')
def product_detail(request, pk, Id):
    item = Product.objects.get(id=Id, pr_name=pk)
    related = Product.objects.filter(seller=item.seller).exclude(id=item.pk)
    size = item.size.all()
    # for the comments
    comments = Review.objects.all().filter(product=item.id)
    # print(comments.product)
    form = ReviewForm
    if request.method == "POST":
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.name = request.user
            form.product = item
            form.save()
            return redirect('prod_detail', Id=Id, pk=item.pr_name)
    context = {
        'item': item,
        'related': related,
        'comments': comments,
        'form': form,
        'size': size
    }
    return render(request, 'product_view.html', context)


# @noCategory
@login_required(login_url='login')
def upload_product(request):
    from random import randint
    fst = randint(100, 300)
    snd = randint(400, 600)
    trd = randint(700, 900)
    reduced = '%s%s%s' % (fst, snd, trd)
    form = ProductForm
    user = request.user
    if request.method == "POST":
        form = ProductForm(request.POST or None, request.FILES)
        images = request.FILES.getlist('image')
        if form.is_valid():
            form.image = (image for image in images)
            instance = form.save(commit=False)
            instance.seller = user
            instance.code = reduced
            instance.save()
            messages.success(request, f'successfully added')
            return redirect('prod_detail', Id=instance.pk, pk=instance.pr_name)
    context = {
        "form": form
    }
    return render(request, "upload.html", context)


# @noCategory
@login_required(login_url='login')
def update_product(request, pk):
    item = Product.objects.get(id=pk)
    form = ProductForm(instance=item)
    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('pr_name')
            messages.success(request, f'{name} successfully updated ')
            return redirect('prod_detail', Id=item.pk, pk=name)
    context = {
        'form': form
    }
    return render(request, 'update.html', context)


# @noCategory
def add_to_cart(request):
    data = json.loads(request.body)
    seller = data['seller']
    productId = data['productId']
    action = data['action']
    priceNum = data['priceNum']
    size = int(data['size'])
    print('Action:', action)
    print('product', productId)
    print(type(size))

    customer = request.user
    product = Product.objects.get(id=productId)
    user = User.objects.get(username=seller)
    order, created = Order.objects.get_or_create(seller=user, customer=customer, product=product, size=size)
    item = Order.objects.filter(customer=customer, product=product, price=priceNum)

    if action == 'add':
        order.quantity = order.quantity + 1
        order.price = order.price + int(priceNum)
    elif action == 'remove':
        order.quantity = order.quantity - 1
        order.price = order.price - int(priceNum)

    order.save()

    if order.quantity <= 0:
        order.delete()
    return JsonResponse('Item was Added', safe=False)


# @noCategory
@login_required(login_url='login')
def cart(request):
    item = Order.objects.filter(customer=request.user)
    total = sum([i.price for i in item])
    context = {
        'item': item,
        'total': total
    }

    return render(request, 'order.html', context)


def remove_item(request, pk):
    item = Order.objects.get(pk=pk)
    item.delete()

    return HttpResponse('success', content_type='text/plain')


# @noCategory
@login_required(login_url='login')
def checkout(request, pk):
    order = Order.objects.get(id=pk)
    form = CheckOutForm
    if request.method == 'POST':
        form = CheckOutForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.customer = request.user
            instance.seller = order.seller
            instance.product = order.product
            instance.ordered = True
            print(order.product)
            instance.save()
            return redirect('cart')

    context = {
        'form': form,
        'order':order
    }
    return render(request, 'checkout.html', context)


def search_res(request):
    if request.is_ajax():
        res= None
        body =request.body.decode("utf-8")
        # print(body)
        anon = request.META['REMOTE_ADDR']
        products = request.POST.get('products')
        qs= Product.objects.filter(
            Q(pr_name__icontains=products) |
            Q(price__icontains=products) |
            Q(seller__username__icontains=products)
            ).distinct()
        # print(qs)
        # print(f'{anon} Input: {products} \nInput_length: {len(products)}\nResults_num: {qs.count()}')
        if len(qs)>0 and len(products)>0:
            data = []
            for pos in qs:
                itemize = {
                    'pk': pos.pk,
                    'price': pos.price,
                    'pr_name': pos.pr_name,
                    'seller': pos.seller.username,
                    'image': pos.image.url
                }
                data.append(itemize)
            res= data
        else:
            res = 'No results found!'
        return JsonResponse({'data': res})
    return JsonResponse({})