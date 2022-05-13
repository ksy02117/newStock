from django.shortcuts import render
from django.http import JsonResponse
from db.models import Keywords, Stocks, AnnualPrice
from NewsTab.NewsSearcher import searchPastNews
from datetime import datetime

# Create your views here.
def getKeywordDatabaseJson(request):
    keyword_datas = Keywords.objects.order_by('-importance')[:10]
    data = []
    for keyword_data in keyword_datas:
        single_data = {}
        single_data['keyword'] = keyword_data.keywords_text
        single_data['importance'] = keyword_data.importance
        single_data['stocks'] = keyword_data.related_stocks.split('/')
        single_data['summary'] = keyword_data.summarized_text
        single_data['news'] = []
        if keyword_data.news_title_1 != None and keyword_data.news_url_1 != None:
            single_data['news'].append({'title' : keyword_data.news_title_1, 'url' : keyword_data.news_url_1})
        if keyword_data.news_title_2 != None and keyword_data.news_url_2 != None:
            single_data['news'].append({'title' : keyword_data.news_title_1, 'url' : keyword_data.news_url_2})
        if keyword_data.news_title_3 != None and keyword_data.news_url_3 != None:
            single_data['news'].append({'title' : keyword_data.news_title_1, 'url' : keyword_data.news_url_3})
        data.append(single_data)
    
    return JsonResponse({'data': data}, json_dumps_params={'ensure_ascii':False})



def getStockDatabaseJson(request):
    stock_datas = Stocks.objects.all()
    data = []
    for stock_data in stock_datas:
        single_data = {}
        single_data['name'] = stock_data.stock_name
        single_data['code'] = stock_data.stock_code
        data.append(single_data)
    
    return JsonResponse({'data': data}, json_dumps_params={'ensure_ascii':False})



def getAnnualDatabaseJson(request, stock_name):
    Annual_datas = AnnualPrice.objects.filter(stock_name = stock_name)
    data = []
    for Annual_data in Annual_datas:
        single_data = {}
        single_data['name'] = Annual_data.stock_name
        single_data['date'] = Annual_data.date
        single_data['start'] = Annual_data.start_price
        single_data['end'] = Annual_data.end_price
        data.append(single_data)
    
    return JsonResponse({'data': data}, json_dumps_params={'ensure_ascii':False})


# TODO:
def getDailyDatabaseJson(request, stock_name):

    return JsonResponse({'data' : 'TODO'}, json_dumps_params={'ensure_ascii':False})



def getPastNewsJson(request, query, date):
    date = datetime.strptime(date, '%y%m%d')
    news_list = searchPastNews(query, date)
    
    data = []
    for news in news_list:
        data.append({'title':news.title, 'url':news.url})

    return JsonResponse({'data': data}, json_dumps_params={'ensure_ascii':False})