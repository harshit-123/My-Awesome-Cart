from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt

from .Paytm import Checksum
# MERCHANT_KEY = 'Your-Merchant-Key-Here'
MERCHANT_KEY = 'gCzx&KxdxXX4eaFa'
# Create your views here.
def index(request):
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category = cat)
        n = len(prod) #get the length of the products
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {"allProds": allProds}
    return render(request, "shop/index.html", params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prodtemp = Product.objects.filter(category = cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod) #get the length of the products
        nSlides = n//4 + ceil((n/4) - (n//4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {"allProds": allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<5:
        params = {"msg": "Please make sure to search relevant search query"}
    return render(request, "shop/search.html", params)



def about(request):
    return render(request, "shop/about.html")
    # return HttpResponse("We are at About")

def contact(request):
    if request.method == "POST":
        name  = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc  = request.POST.get('desc','')
        contact = Contact(name = name, email = email , phone = phone, desc = desc)
        contact.save()
        msg = True
        return render(request, "shop/contact.html", {"msg": msg})
    return render(request, "shop/contact.html")

def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get('orderid','')
        email    = request.POST.get('email','')
        try:
            order = Order.objects.filter(order_id= order_id, email= email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id= order_id)
                updates = []
                for item in update:
                    updates.append({"text": item.update_desc, "time": item.timestamp})
                    response = json.dumps({"status": "success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status"; "No Item"}')
        except Exception as e:
            return HttpResponse('{"success": "Error"}')
    return render(request, "shop/tracker.html")

def products(request, id):
    #Fetch product by Id
    product = Product.objects.filter(id=id)
    return render(request, "shop/prodview.html", {"product": product[0]})

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson','')
        amount     = request.POST.get('totalprice',default=0)
        name       = request.POST.get('name','')
        email      = request.POST.get('email','')
        phone      = request.POST.get('phone','')
        address    = request.POST.get('address','') + " " + request.POST.get('address2','')
        city       = request.POST.get('city','')
        state      = request.POST.get('state','')
        zip        = request.POST.get('zip','')
        order      = Order(name = name, email = email , phone = phone, address = address, city = city, state = state , zip = zip, items_json = items_json, amount= amount)
        order.save()

        update = OrderUpdate(order_id = order.order_id, update_desc= "Order has been placed successfully")
        update.save()
        thank = True
        id = order.order_id
        #request paytm to transfer the Amount to your amount the paytm User
        # return render(request, "shop/checkout.html", {"thank": thank, "id": id})
        param_dict = {
                'MID': 'DqqseX70406154784323',
                'ORDER_ID': str(id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {"param_dict": param_dict})
    return render(request, "shop/checkout.html")

@csrf_exempt
def handlerequest(request):
    #Paytm will send you POST request
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        response_dict['RESPONSE'] == '01' if print("Order Successful") else print("Order Not successfull BECAUSE"+ response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})