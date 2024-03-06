   
# from django.shortcuts import render
# from rest_framework.decorators import action
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import status
# import requests
# from bs4 import BeautifulSoup
# from django.conf import settings

# class NewsViewSet(ViewSet):
   

#     @action(detail=False, methods=['get'])
#     def list_notifications(self, request):
#         source_urls = settings.COLLEGE_NEWS_SOURCE_URLS
#         notifications = []
#         for source_name, url in source_urls.items():
#             response = requests.get(url)
#             soup = BeautifulSoup(response.text, 'html.parser')
#             table = soup.find('table', class_='tableborder')
#             if table:
#                 rows = table.find_all('tr')
#                 for row in rows:
#                     cols = row.find_all('td')
#                     for col in cols:
#                         links = col.find_all('a')
#                         for link in links:
#                             if 'href' in link.attrs:
#                                 image = col.find('img')
#                                 image_url = image['src'] if image else None
#                                 notifications.append({
#                                     'source': source_name,
#                                     'title': link.text.strip(),
#                                     'link': link['href'],
#                                     'description': '',
#                                     'media_url': None,
#                                 })
#             elif source_name == "JNTUK":
#                 cat_right_divs = soup.find_all('div', {'id': 'cat_right'})
#                 for cat_right_div in cat_right_divs:
#                     links = cat_right_div.find_all('a')
#                     for link in links:
#                         if 'href' in link.attrs:
#                             notifications.append({
#                                 'source': source_name,
#                                 'title': link.text.strip(),
#                                 'link': link['href'],
#                                 'description': '',
#                                 'media_url': None,
#                             })

#         return Response(notifications, status=status.HTTP_200_OK)


#     @action(detail=False, methods=['get'])
#     def list_news(self, request):
#         rss_feed_urls = settings.EDUCATION_RSS_FEED_URLS
#         news_data = []
#         for source_name, rss_feed_url in rss_feed_urls.items():
#             response = requests.get(rss_feed_url)
#             if response.status_code == 200:
#                 soup = BeautifulSoup(response.content, 'xml')
#                 items = soup.find_all('item')

#                 for item in items:
#                     title = item.find('title').get_text()
#                     link = item.find('link').get_text()
#                     description_html = item.find('description').get_text()
#                     media_url = None

#                     description_soup = BeautifulSoup(description_html, 'html.parser')
#                     image = description_soup.find('img')
#                     if image:
#                         media_url = image['src']

#                     news_data.append({
#                         'source': source_name,
#                         'title': title,
#                         'media_url': media_url,
#                         'link': link,
#                         'description': description_html
#                     })
    
#         return Response(news_data, status=status.HTTP_200_OK)
    

#     @action(detail=False, methods=['get'])

#     def list_tspsc_notifications(self, request):
#         url = settings.TSPSC_NOTIFICATIONS_URL
#         response = requests.get(url)
#         news_data = []

#         if response.status_code == 200:
#             html_content = response.text
#             soup = BeautifulSoup(html_content, "html.parser")
#             table = soup.find("table", {"class": ["table", "_table-hover", "table-light", "table-striped", "table-responsive"]})
            
#             if table:
#                 for row in table.find_all("tr"):
#                     cols = row.find_all("td")
#                     if cols:  # If the row contains columns
#                         title = cols[0].text.strip()  # Example: assuming first column is title
#                         link = cols[0].find('a')['href'] if cols[0].find('a') else '#'
                        
#                         # Ensure the link is absolute
#                         if not link.startswith('http'):
#                             link = url.rsplit('/', 1)[0] + '/' + link.lstrip('/')
                        
#                         news_data.append({
#                             "title": title,
#                             "link": link,
#                             "source": "tspsc.gov.in",
#                         })

#         return Response(news_data, status=status.HTTP_200_OK)


   
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup
from django.conf import settings

class NewsViewSet(ViewSet):
    def fetch_notifications(self, source_name, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup  # Return the soup object for further processing

   

    # @action(detail=False, methods=['get'])
    # def list_notifications(self, request):
    #     source_urls = settings.COLLEGE_NEWS_SOURCE_URLS
    #     notifications = []
    #     for source_name, url in source_urls.items():
    #         response = requests.get(url)
    #         soup = BeautifulSoup(response.text, 'html.parser')
    #         table = soup.find('table', class_='tableborder')
    #         if table:
    #             rows = table.find_all('tr')
    #             for row in rows:
    #                 cols = row.find_all('td')
    #                 for col in cols:
    #                     links = col.find_all('a')
    #                     for link in links:
    #                         if 'href' in link.attrs:
    #                             image = col.find('img')
    #                             image_url = image['src'] if image else None
    #                             notifications.append({
    #                                 'source': source_name,
    #                                 'title': link.text.strip(),
    #                                 'link': link['href'],
    #                                 'description': '',
    #                                 'media_url': None,
    #                             })
    @action(detail=False, methods=['get'])
    def jntuh_notifications(self, request):
        url = settings.COLLEGE_NEWS_SOURCE_URLS.get("JNTUH", "")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        notifications = []
        table = soup.find('table', class_='tableborder')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                for col in cols:
                    links = col.find_all('a')
                    for link in links:
                        if 'href' in link.attrs:
                            image = col.find('img')
                            image_url = image['src'] if image else None
                            notifications.append({
                                'source': "JNTUH",
                                'title': link.text.strip(),
                                'link': link['href'],
                                'description': '',
                                # 'media_url': image_url if image_url else None,
                            })
        
        return Response(notifications, status=status.HTTP_200_OK)

        #     elif source_name == "JNTUK":
        #         cat_right_divs = soup.find_all('div', {'id': 'cat_right'})
        #         for cat_right_div in cat_right_divs:
        #             links = cat_right_div.find_all('a')
        #             for link in links:
        #                 if 'href' in link.attrs:
        #                     notifications.append({
        #                         'source': source_name,
        #                         'title': link.text.strip(),
        #                         'link': link['href'],
        #                         'description': '',
        #                         'media_url': None,
        #                     })

        # return Response(notifications, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'])
    def jntuk_notifications(self, request):
        url = settings.COLLEGE_NEWS_SOURCE_URLS.get("JNTUK", "")
        soup = self.fetch_notifications("JNTUK", url)  # Adjusted to receive only the soup object
        notifications = []  # Initialize the notifications list here
        
        # Specific parsing logic for JNTUK
        cat_right_divs = soup.find_all('div', {'id': 'cat_right'})
        for cat_right_div in cat_right_divs:
            links = cat_right_div.find_all('a')
            for link in links:
                if 'href' in link.attrs:
                    notifications.append({
                        'source': "JNTUK",
                        'title': link.text.strip(),
                        'link': link['href'],
                        'description': '',
                        'media_url': None,
                    })

        return Response(notifications, status=status.HTTP_200_OK)


    


    
    @action(detail=False, methods=['get'])
    def list_news(self, request):
        rss_feed_urls = settings.EDUCATION_RSS_FEED_URLS
        news_data = []
        for source_name, rss_feed_url in rss_feed_urls.items():
            response = requests.get(rss_feed_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                items = soup.find_all('item')

                for item in items:
                    title = item.find('title').get_text()
                    link = item.find('link').get_text()
                    description_html = item.find('description').get_text()
                    media_url = None

                    description_soup = BeautifulSoup(description_html, 'html.parser')
                    image = description_soup.find('img')
                    if image:
                        media_url = image['src']

                    news_data.append({
                        'source': source_name,
                        'title': title,
                        'media_url': media_url,
                        'link': link,
                        'description': description_html
                    })
    
        return Response(news_data, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'])

    def list_tspsc_notifications(self, request):
        url = settings.TSPSC_NOTIFICATIONS_URL
        response = requests.get(url)
        news_data = []

        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            table = soup.find("table", {"class": ["table", "_table-hover", "table-light", "table-striped", "table-responsive"]})
            
            if table:
                for row in table.find_all("tr"):
                    cols = row.find_all("td")
                    if cols:  # If the row contains columns
                        title = cols[0].text.strip()  # Example: assuming first column is title
                        link = cols[0].find('a')['href'] if cols[0].find('a') else '#'
                        
                        # Ensure the link is absolute
                        if not link.startswith('http'):
                            link = url.rsplit('/', 1)[0] + '/' + link.lstrip('/')
                        
                        news_data.append({
                            "title": title,
                            "link": link,
                            "source": "tspsc.gov.in",
                        })

        return Response(news_data, status=status.HTTP_200_OK)
