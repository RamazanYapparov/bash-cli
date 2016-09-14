from grab import Grab
from weblib.error import DataNotFound
import re


class BashQuotes:

    def get_quotes(self):
        g = Grab(log_file="bash.html", url='bash.im')
        g.go("bash.im")
        bash = g.doc.select('.//div[@class="quote"]')
        quotes_dict = {}
        for k in range(bash.count()):
            try:
                quote_id = bash[k].select('.//a[@class="id"]').text()
                quote_text = bash[k].html()

                result = re.split(r'(<div class="text">|</div>)', quote_text)[4]
                result = re.sub(r'&lt;', '<', result)
                result = re.sub(r'&gt;', '>', result)
                result = re.sub(r'<br>', '\n', result)

                quotes_dict[quote_id] = result
            except DataNotFound:
                pass
        return quotes_dict