import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['http://peps.python.org/']

    def parse(self, response):
        table_numerical_index = response.css(
            'table.pep-zero-table.docutils.align-default'
        )
        all_peps = table_numerical_index.css(
            'a.pep.reference.internal::attr(href)'
        )
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title_pep = (response.css('h1.page-title::text').get()).split(' – ')
        name = title_pep[1]
        for element in title_pep[0].split():
            if element.isdigit():
                break

        data = {
            'number': element,
            'name': name,
            'status': response.css(
                'dt:contains("Status") + dd abbr::text'
            ).get()
        }
        yield PepParseItem(data)
