def run(o):
    """
    Inspired by Craig Addyman (http://www.craigaddyman.com/parse-an-xml-sitemap-with-python/)
    Enhanced by Viktor Petersson (http://viktorpetersson.com) / @vpetersson
    Enhanced by Jari Turkia (https://blog.hqcodeshop.fi/) / @HQJaTu

    - stolen by me

    # to use in ur own pypal do this...
    from core.PyPal import PyPal
    pal = PyPal({'name':'pypal'})
    common = pal.nlp.processSentence( 'common sitemap' )
    get_site_urls = common['get_site_urls']
    get_site_urls('somesite.com')
    """

    from bs4 import BeautifulSoup
    import requests
    from urllib.parse import urlparse
    from typing import List

    def get_sitemap(url: str):
        get_url = requests.get(url, timeout=2) # you may want to make this bigger for large sites
        if get_url.status_code == 200:
            return get_url.text
        else:
            print('Unable to fetch sitemap: %s.' % url)

    def process_sitemap(s: str) -> List:
        soup = BeautifulSoup(s, 'lxml')
        result = []
        for loc in soup.findAll('loc'):
            result.append(loc.text)

        return result

    def is_sub_sitemap(url: str) -> bool:
        parts = urlparse(url)
        if parts.path.endswith('.xml') and 'sitemap' in parts.path:
            return True
        else:
            return False

    def parse_sitemap(s: str) -> List:
        sitemap = process_sitemap(s)
        result = []
        while sitemap:
            candidate = sitemap.pop()
            if is_sub_sitemap(candidate):
                sub_sitemap = get_sitemap(candidate)
                for i in process_sitemap(sub_sitemap):
                    sitemap.append(i)
            else:
                result.append(candidate)

        return result

    # def main():
    #     sitemap = get_sitemap('https://www.cloudsigma.com/sitemap.xml')
    #     url_count = 0
    #     for url in parse_sitemap(sitemap):
    #         url_count += 1
    #         print("%5d) %s" % (url_count, url))
    #     print("-end-of-list-")

    def get_site_urls(url: str) -> List:

        # https://stackoverflow.com/questions/25027122/break-the-function-after-certain-time
        
        # import signal
        # class TimeoutException(Exception):   # Custom exception class
        #     pass

        # def timeout_handler(signum, frame):   # Custom signal handler
        #     raise TimeoutException

        # signal.signal(signal.SIGALRM, timeout_handler)
        # signal.alarm(5) 


        try:

            s = url.rstrip('/')  # strip any existing last slashes

            data = get_sitemap(s + "/sitemap.xml")
            urls = parse_sitemap(data)
            return urls

        # except TimeoutException:
                # continue # continue the for loop if function A takes more than 5 second
            # else:
                # Reset the alarm
                # signal.alarm(0)

        except Exception as e:
            print('get_site_urls fail::', url)
            print(e)
            return []


    return {"get_site_urls": get_site_urls, "parse_sitemap": parse_sitemap, "is_sub_sitemap": is_sub_sitemap, "get_sitemap": get_sitemap, "process_sitemap": process_sitemap}
