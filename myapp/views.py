from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

from django.contrib import messages  


# Create your views here.
def search_list(request):
    if 'cname' in request.GET:
        cname = request.GET['cname']
        # print(cname)
        # resultList = students.objects.filter(cname = cname)
        resultList = students.objects.filter(cname__contains = cname)#關鍵字 查詢
    else:
        resultList = students.objects.all().order_by('cid')

    # for st in resultList:
    #     print(model_to_dict(st))
    # return HttpResponse("Hello")

    errorMsg = ""
    # resultList = []
    if not resultList:
        errorMsg = "No data found"
    # return render(request, 'search_list.html', locals())
    
    return render(request, 'search_list.html', {'resultList' : resultList, 'errorMsg' : errorMsg})

def search_name(request):
    return render(request, 'search_name.html')

def index(request):
    if 'site_search' in request.GET:
        site_search = request.GET["site_search"]
        site_search = site_search.strip() #去除前後空白
        keywords = site_search.split() #以空格分割 多個 關鍵字

        # print(keywords)
        # print(site_search)
        # resultList = students.objects.filter(cname__contains=site_search).order_by('cid')
        # resultList = students.objects.filter(Q(cid__contains = site_search)|Q(cname__contains = site_search)|Q(cbirthday__contains = site_search)|Q(cemail__contains = site_search)|Q(cphone__contains = site_search)|Q(caddr__contains = site_search))

        query = Q()
        for keyword in keywords:
            query |= Q(cid__contains = keyword)|Q(cname__contains = keyword)|Q(cbirthday__contains = keyword)|Q(cemail__contains = keyword)|Q(cphone__contains = keyword)|Q(caddr__contains = keyword)
        resultList = students.objects.filter(query).order_by('cid')

       
    else:
        resultList = students.objects.all()

    # resultList = students.objects.all().order_by('cid')
    for st in resultList:
        print(model_to_dict(st))
    data_count = len(resultList)
    print(f"Total data count : {data_count}")
    status = True
    errorMsg = ""
    if not resultList:
        status = False
        errorMsg = "No data found."

    #分頁設定
    paginator = Paginator(resultList, 3) #想要分頁的 資料 , 筆數
    page_num = request.GET.get('page') #取得當前頁碼
    page_obj = paginator.get_page(page_num) #取得當前頁面的資料
    print(page_obj)

    return render(request, 'index.html', {'resultList' : resultList, 'status' : status, 'errorMsg' : errorMsg, 'data_count' : data_count, 'page_obj' : page_obj})

def post(request):
    if request.method == 'POST':
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')
        # print(f"{cname} {csex} {cbirthday} {cemail} {cphone} {caddr}")
        add = students(
            cname = cname,
            csex = csex,
            cbirthday = cbirthday,
            cemail = cemail,
            cphone = cphone,
            caddr = caddr
        )
        add.save()

        return redirect('index')#重新導回 index
    else:
        return render(request, 'post.html')
    
def edit(request, id):
    # print(id)
    if request.method == 'POST':
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')
        # print(f"{cname} {csex} {cbirthday} {cemail} {cphone} {caddr}")

        update = students.objects.get(cid = id)
        update.cname = cname
        update.csex = csex
        update.cbirthday = cbirthday
        update.cemail = cemail
        update.cphone = cphone
        update.caddr = caddr
        update.save()

        return redirect('index')
    else:
        st = students.objects.get(cid = id)
        # model_to_dict(st)
        return render(request, 'edit.html', {"st" : st})
    
def delete(request, id):
    # print(id)
    if request.method == 'POST':
        stDel = students.objects.get(cid = id)
        name = stDel.cname
        stDel.delete()
        messages.success(request, f"學生 {name} 已成功刪除！")
        
        return redirect('index')
    else:
        st = students.objects.get(cid = id)
        # print(model_to_dict(st))
        return render(request, 'delete.html', {"st" : st})
    return HttpResponse("Hello")

def getAllItems(request):
    resultObj = students.objects.all().order_by('cid')
    # print(type(resultObj))
    # for item in resultList:
    #     # print(model_to_dict(item))
    #     print(type(item))
    resultList = list(resultObj.values()) # 把querySet 集合裡的 object  轉換成 list 元素為 dict 的型態
    # print(type(resultList))
    # for item in resultList:
    #     print(type(item))

    return JsonResponse(resultList, safe=False)
    #safe = True => 只允許傳入 dict
    #safe = False => 只允許傳入 非 dict

def getItem(request, id):
    try:
        obj = students.objects.get(cid = id)
        # print(obj)
        # print(model_to_dict(obj))
        resultDict = model_to_dict(obj)
        return JsonResponse(resultDict, safe=False)
    except:
        return JsonResponse({"Error":"Item not found"}, status = 404)

    