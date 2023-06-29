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
        title_page = response.css('title::text').get()
        title = title_page.strip('PEP | peps.python.org')
        number_and_name = title.split()
        number = number_and_name[0]
        name = ' '.join(number_and_name[2:])

        data = {
            'number': number,
            'name': name,
            'status': response.css(
                'dt:contains("Status") + dd abbr::text'
            ).get()
        }
        yield PepParseItem(data)
