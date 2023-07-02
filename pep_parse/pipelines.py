import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# Директория для создания папки с результатами
BASE_DIR = Path(__file__).parent.parent
# Директория с результатами
RESULTS_DIR = 'results'
# Текущая дата и время
CURRENT_DATE = "{:%Y-%m-%d_%H-%M-%S}".format(datetime.utcnow())


class PepParsePipeline:
    def open_spider(self, spider):
        # Словарь-счетчик статусов
        self.counter_status = defaultdict(int)
        # Путь до директории с результатами
        self.path_results = BASE_DIR / RESULTS_DIR
        # Создание директории
        self.path_results.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        # Подсчет количества статусов
        self.counter_status[item['status']] += 1
        return item

    def close_spider(self, spider):
        # Файл с количеством статусов
        file_name = f'{self.path_results}/status_summary_{CURRENT_DATE}.csv'
        with open(file_name, mode='w', encoding='utf-8') as f:
            # Заполнение таблицы данными из счетчика статусов
            writer = csv.writer(f, dialect='unix')
            writer.writerow(['Статус', 'Количество'])
            for status, num in self.counter_status.items():
                writer.writerow([status, num])
            # Добавление строки с общим количеством pep
            writer.writerow(['Total', sum(self.counter_status.values())])
