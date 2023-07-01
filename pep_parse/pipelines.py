from collections import defaultdict
from datetime import datetime
# from pathlib import Path

# BASE_DIR = Path(__file__).parent.parent
# DIR_OUTPUT = 'results'


class PepParsePipeline:
    def open_spider(self, spider):
        # Создаем словарь-счетчик статусов
        self.counter_status = defaultdict(int)

    def process_item(self, item, spider):
        # Подсчитываем количество статусов
        self.counter_status[item['status']] += 1
        return item

    def close_spider(self, spider):
        # Определяем текущую дату и время
        current_date = "{:%Y-%m-%d_%H-%M-%S}".format(datetime.now())
        # Создаем файл в формате csv
        with open(
                f'results/status_summary_{current_date}.csv',
                mode='w',
                encoding='utf-8'
        ) as f:
            # Заполняем таблицу данными из счетчика статусов
            f.write('Статус,Количество\n')
            for status, num in self.counter_status.items():
                f.write(f'{status},{num}\n')
            # Добавляем строчку с общим количеством pep
            f.write(f'Total,{sum(self.counter_status.values())}\n')
