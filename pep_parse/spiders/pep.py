import scrapy

from pep_parse.items import PepParseItem


# Класс с созданным пауком
class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        # Селектор со сылками на все pep
        table_numerical_index = response.css(
            'table.pep-zero-table.docutils.align-default'
        )
        all_peps = table_numerical_index.css(
            'a.pep.reference.internal::attr(href)'
        )
        # Парсинг страницы каждого pep из общей таблицы
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        # Селектор для поиска всех нужных сведений о каждом pep
        title_page = response.css('title::text').get()
        title = title_page.strip('PEP | peps.python.org')
        number_and_name = title.split()
        number = number_and_name[0]
        name = ' '.join(number_and_name[2:])
        # Словарь с найденными сведениями
        data = {
            'number': number,
            'name': name,
            'status': response.css(
                'dt:contains("Status") + dd abbr::text'
            ).get()
        }
        # Возвращается экземпляр Item для конкретного pep
        yield PepParseItem(data)
