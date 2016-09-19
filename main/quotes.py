from grab import Grab
from grab.error import GrabCouldNotResolveHostError
from weblib.error import DataNotFound
import re


class BashQuotes:
    URL = 'http://bash.im/'
    g = Grab()
    try:
        g.go(URL)
    except GrabCouldNotResolveHostError:
        print('Не удалось получить список цитат, проверьте ваше подключение к интернету')
        exit()

    quote_pattern = './/div[@class="quote"]'

    def _get_current_page(self):
        bash = self.g.doc.select('.//input[@class="page"]').html()
        page = re.findall('max="\d*"', bash)
        page = re.sub('\D', '', str(page))
        return int(page)

    def _get_quotes_from_specified_page(self, page):
        if re.match('http://bash\.im/index/\d+', self.g.doc.url):
            self.g.go(str(page))
        elif self.g.doc.url == self.URL:
            self.g.go('index/' + str(page))
        else:
            self.g.go(self.URL + 'index/' + str(page))
        bash = self.g.doc.select(self.quote_pattern)
        return dict(sorted(self._get_quotes(bash).items(), reverse=True)), self.current_page

    @staticmethod
    def _get_quotes(bash):
        quotes_dict = {}
        for k in range(bash.count()):
            try:
                quote_id = bash[k].select('.//a[@class="id"]').text()
                quote_text = bash[k].html()

                result = re.split(r'(<div class="text">|</div>)', quote_text)[4]
                result = re.sub(r'&lt;', '<', result)
                result = re.sub(r'&gt;', '>', result)
                result = re.sub(r'<br>', '\n', result)

                quotes_dict[str(quote_id).split('#')[1]] = result
            except DataNotFound:
                pass
        return quotes_dict

    def __init__(self):
        self.last_page = self._get_current_page()
        self.current_page = self.last_page
        self.pages_list = [k for k in range(self.last_page + 1)]

    def get_new_quotes(self):
        return self._get_quotes_from_specified_page(self.last_page)

    def get_next_page(self):
        if self.current_page != self.last_page:
            self.current_page += 1
        return self._get_quotes_from_specified_page(self.current_page)

    def get_prev_page(self):
        if self.current_page != 1:
            self.current_page -= 1
        return self._get_quotes_from_specified_page(self.current_page)

    def get_random_quotes(self):
        self.g.go(self.URL + 'random')
        bash = self.g.doc.select(self.quote_pattern)
        return self._get_quotes(bash)
