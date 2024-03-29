from NewsTab.NewsSearcher import searchPresentNews
from NewsTab.KeyWordSelector import getKeyword
from NewsTab.Summarizer import summarize
import re
import html

def generateKeywords(stock_list):
    stock = {}

    for stock_name in stock_list.keys():
        news_list = searchPresentNews(stock_name)
        stock[stock_name] = news_list

    stock_keywords = {}

    for stock_name, news_list in stock.items():
        for news in news_list:
            news_keywords = getKeyword(news.title)
            for idx, keyword in enumerate(news_keywords):
                if keyword in stock_keywords:
                    stock_keywords[keyword][0] += 1
                    stock_keywords[keyword][1] += idx
                    if stock_name not in stock_keywords[keyword][2]:
                        stock_keywords[keyword][2].append(stock_name)
                    if news not in stock_keywords[keyword][3]:
                        stock_keywords[keyword][3].append(news)
                else:
                    stock_keywords[keyword] = [1, idx, [stock_name], [news]]

    stock_keywords = {k : [v[0], v[1], v[2], v[3]] for k, v in stock_keywords.items() if v[0] > 1}
    stock_keywords = {k : [v[0], v[1], v[2], v[3]] for k, v in sorted(stock_keywords.items(), key=lambda item: (-item[1][0], item[1][1]))}

    i = 0
    while i < len(stock_keywords):
        keywords_list = list(stock_keywords.keys())
        keyword = keywords_list[i]
        for keyword_entry in keyword.split():
            keywords_list = list(stock_keywords.keys())
            j = i + 1
            while j < len(keywords_list):
                if keyword_entry in keywords_list[j]:
                    del stock_keywords[keywords_list[j]]
                j += 1
        i += 1
    
    display_keyword = {}
    for keyword, info in stock_keywords.items():
        related_stock = "/".join(info[2])
        importance = 0
        for stock_name in info[2]:
            importance += stock_list[stock_name]
        for news in info[3]:
            news.generateContent()
            summarized_text = summarize(news.title, news.content)
            if summarized_text is not None:
                break
            
        if summarized_text is None:
            summarized_text = "해당 주제의 뉴스가 너무 길어 요약을 할 수 없습니다."
        display_keyword[keyword] = [importance, related_stock, summarized_text, []]
        for news in info[3][:3]:
            tmp_title = html.unescape(news.title)
            tmp_title = re.sub('<.*?>', '', tmp_title)
            display_keyword[keyword][3].append([tmp_title, news.url])
    
    return display_keyword
