from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from urllib.parse import urljoin

class NewsViewSet(ViewSet):
    def fetch_notifications(self, source_name, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup  # Return the soup object for further processing

   

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
                          
                          
                            notifications.append({
                                'source': "JNTUH",
                                'title': link.text.strip(),
                                'link': link['href'],
                                
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
    
    @action(detail=False, methods=['get'])
    def jee_notifications(self, request):
        notifications = []
        # List of titles or links to exclude
        exclude_titles = ["Contact US", "Ministry Of Education"]
        exclude_links = ["https://jeemain.nta.nic.in/contact-us/", "https://www.education.gov.in/en"]

        # Iterate over each entry in the JEE_NOTIFICATIONS_URL dictionary
        for source_name, url in settings.JEE_NOTIFICATIONS_URL.items():
            soup = self.fetch_notifications(source_name, url)

            if soup:
                # CSS selectors for both class combinations, separated by a comma
                selectors = ".gen-list.yes-bg.padding-20.border-radius-medium.default-list,.gen-list.no-border.no-bg.padding-20.border-radius-medium.default-list"
                elements = soup.select(selectors)
                for element in elements:
                    items = element.find_all('li')
                    for item in items:
                        title = item.get_text(strip=True)
                        link_element = item.find('a')
                        link = link_element['href'] if link_element else None

                        # Ensure the link is absolute
                        link = urljoin(url, link)

                        # Skip adding the notification if its title or link matches the exclusion list
                        if title not in exclude_titles and link not in exclude_links:
                            notifications.append({
                                'source': source_name,
                                'title': title,
                                'link': link,
                            })

        return Response(notifications, status=status.HTTP_200_OK)



    @action(detail=False, methods=['get'])
    def upsc_notifications(self, request):
        notifications = []
        

        # URL of the UPSC What's New page to scrape
        UPSC_URL = "https://upsc.gov.in/whats-new"
        response = requests.get(UPSC_URL)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Example CSS selector, adjust based on actual content structure
            selectors = ".view-content .views-row"
            elements = soup.select(selectors)

            for element in elements:
                title = element.get_text(strip=True)
                link_element = element.find('a')
                link = link_element['href'] if link_element else None

                # Ensure the link is absolute
                link = urljoin(UPSC_URL, link)

                
                notifications.append({
                        'title': title,
                        'link': link,
                    })
            return Response(notifications, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to retrieve UPSC notifications"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# =========


# import aiohttp
# import asyncio
# from django.shortcuts import render
# from rest_framework.decorators import action
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import status
# from bs4 import BeautifulSoup
# from django.conf import settings
# from urllib.parse import urljoin

# class NewsViewSet(ViewSet):
#     async def fetch_notifications(self, session, url):
#         async with session.get(url) as response:
#             if response.status == 200:
#                 return await response.text()
#             return None

#     @action(detail=False, methods=['get'])
#     async def jntuk_notifications(self, request):
#         url = settings.COLLEGE_NEWS_SOURCE_URLS.get("JNTUK", "")
#         async with aiohttp.ClientSession() as session:
#             html_content = await self.fetch_notifications(session, url)
#             if html_content:
#                 soup = BeautifulSoup(html_content, 'html.parser')
#                 notifications = []
#                 # Specific parsing logic for JNTUK
#                 cat_right_divs = soup.find_all('div', {'id': 'cat_right'})
#                 for cat_right_div in cat_right_divs:
#                     links = cat_right_div.find_all('a')
#                     for link in links:
#                         if 'href' in link.attrs:
#                             notifications.append({
#                                 'source': "JNTUK",
#                                 'title': link.text.strip(),
#                                 'link': link['href'],
#                                 'description': '',
#                                 'media_url': None,
#                             })
#                 return Response(notifications, status=status.HTTP_200_OK)
#             else:
#                 return Response("Failed to fetch data from JNTUK", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     @action(detail=False, methods=['get'])
#     async def jntuh_notifications(self, request):
#         url = settings.COLLEGE_NEWS_SOURCE_URLS.get("JNTUH", "")
#         async with aiohttp.ClientSession() as session:
#             html_content = await self.fetch_notifications(session, url)
#             if html_content:
#                 soup = BeautifulSoup(html_content, 'html.parser')
#                 notifications = []
#                 # Parsing logic for JNTUH notifications
#                 table = soup.find('table', class_='tableborder')
#                 if table:
#                     rows = table.find_all('tr')
#                     for row in rows:
#                         cols = row.find_all('td')
#                         for col in cols:
#                             links = col.find_all('a')
#                             for link in links:
#                                 if 'href' in link.attrs:
#                                     notifications.append({
#                                         'source': "JNTUH",
#                                         'title': link.text.strip(),
#                                         'link': link['href'],
#                                     })
#                     return Response(notifications, status=status.HTTP_200_OK)
#             else:
#                 return Response("Failed to fetch data from JNTUH", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     @action(detail=False, methods=['get'])
#     async def list_news(self, request):
#         rss_feed_urls = settings.EDUCATION_RSS_FEED_URLS
#         news_data = []

#         async def fetch_news(session, url, source_name):
#             async with session.get(url) as response:
#                 if response.status == 200:
#                     html_content = await response.text()
#                     soup = BeautifulSoup(html_content, 'xml')
#                     items = soup.find_all('item')
#                     for item in items:
#                         title = item.find('title').get_text()
#                         link = item.find('link').get_text()
#                         description_html = item.find('description').get_text()
#                         media_url = None
#                         description_soup = BeautifulSoup(description_html, 'html.parser')
#                         image = description_soup.find('img')
#                         if image:
#                             media_url = image['src']
#                         news_data.append({
#                             'source': source_name,
#                             'title': title,
#                             'media_url': media_url,
#                             'link': link,
#                             'description': description_html
#                         })

#         async with aiohttp.ClientSession() as session:
#             tasks = [fetch_news(session, rss_feed_urls[source_name], source_name) for source_name in rss_feed_urls]
#             await asyncio.gather(*tasks)

#         return Response(news_data, status=status.HTTP_200_OK)

#     @action(detail=False, methods=['get'])
#     async def list_tspsc_notifications(self, request):
#         url = settings.TSPSC_NOTIFICATIONS_URL
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url) as response:
#                 if response.status == 200:
#                     html_content = await response.text()
#                     soup = BeautifulSoup(html_content, "html.parser")
#                     table = soup.find("table", {"class": ["table", "_table-hover", "table-light", "table-striped", "table-responsive"]})
#                     if table:
#                         news_data = []
#                         for row in table.find_all("tr"):
#                             cols = row.find_all("td")
#                             if cols:  # If the row contains columns
#                                 title = cols[0].text.strip()  # Example: assuming first column is title
#                                 link = cols[0].find('a')['href'] if cols[0].find('a') else '#'
#                                 if not link.startswith('http'):
#                                     link = url.rsplit('/', 1)[0] + '/' + link.lstrip('/')
#                                 news_data.append({
#                                     "title": title,
#                                     "link": link,
#                                     "source": "tspsc.gov.in",
#                                 })
#                         return Response(news_data, status=status.HTTP_200_OK)
#         return Response("Failed to fetch data from TSPSC", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     @action(detail=False, methods=['get'])
#     async def jee_notifications(self, request):
#         notifications = []
#         exclude_titles = ["Contact US", "Ministry Of Education"]
#         exclude_links = ["https://jeemain.nta.nic.in/contact-us/", "https://www.education.gov.in/en"]

#         async def fetch_jee_notifications(session, url, source_name):
#             async with session.get(url) as response:
#                 if response.status == 200:
#                     html_content = await response.text()
#                     soup = BeautifulSoup(html_content, 'html.parser')
#                     selectors = ".gen-list.yes-bg.padding-20.border-radius-medium.default-list,.gen-list.no-border.no-bg.padding-20.border-radius-medium.default-list"
#                     elements = soup.select(selectors)
#                     for element in elements:
#                         items = element.find_all('li')
#                         for item in items:
#                             title = item.get_text(strip=True)
#                             link_element = item.find('a')
#                             link = link_element['href'] if link_element else None
#                             link = urljoin(url, link)
#                             if title not in exclude_titles and link not in exclude_links:
#                                 notifications.append({
#                                     'source': source_name,
#                                     'title': title,
#                                     'link': link,
#                                 })

#         async with aiohttp.ClientSession() as session:
#             tasks = [fetch_jee_notifications(session, url, source_name) for source_name, url in settings.JEE_NOTIFICATIONS_URL.items()]
#             await asyncio.gather(*tasks)

#         return Response(notifications, status=status.HTTP_200_OK)
