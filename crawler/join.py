from urllib.request import urlopen
from crawler.link import LinkFinder
from crawler.main1 import *

class Join:

    # Class variables (Shared among all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()


    def __init__(self, project_name, base_url, domain_name):
        Join.project_name = project_name
        Join.base_url = base_url
        Join.domain_name = domain_name
        Join.queue_file = Join.project_name + '/queue.txt'
        Join.crawled_file = Join.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First Join', Join.base_url)


    @staticmethod
    def boot():
        crawl_project(Join.project_name)
        create_file(Join.project_name, Join.base_url)
        Join.queue = file_to_set(Join.queue_file)
        Join.crawled = file_to_set(Join.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Join.crawled:
            print(thread_name + " now crawling" + page_url)
            print('Queue' + str(len(Join.queue)) + ' | crawled' + str(len(Join.crawled)))
            Join.add_links_to_queue(Join.gather_links(page_url))
            Join.queue.remove(page_url)
            Join.crawled.add(page_url)
            Join.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Join.base_url, page_url)
            finder.feed(html_string)
        except:
            print('Error: Cannot crawl the page')
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Join.queue:
                continue
            if url in Join.crawled:
                continue
            if Join.domain_name not in url:
                continue
            Join.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Join.queue, Join.queue_file)
        set_to_file(Join.crawled, Join.crawled_file)

