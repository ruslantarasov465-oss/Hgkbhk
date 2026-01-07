"""
Главный модуль для запуска аналитического инструмента
"""

import yaml
import argparse
import logging
import sys
from pathlib import Path
from colorama import init, Fore, Style

from data_parser import DataParser
from insights_engine import InsightsEngine
from analytics import MonthlyAnalytics
from report_generator import ReportGenerator
from visualizer import DataVisualizer

# Инициализация colorama для цветного вывода
init(autoreset=True)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analytics.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class AnalyticsTool:
    """Главный класс аналитического инструмента"""

    def __init__(self, config_path: str = 'config.yaml'):
        """
        Инициализация инструмента

        Args:
            config_path: путь к файлу конфигурации
        """
        self.config = self._load_config(config_path)
        self.parser = DataParser(self.config)
        self.insights_engine = InsightsEngine(self.config)
        self.analytics = MonthlyAnalytics(self.config)
        self.report_generator = ReportGenerator(self.config)
        self.visualizer = DataVisualizer(self.config)

    def _load_config(self, config_path: str) -> dict:
        """Загружает конфигурацию"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Ошибка при загрузке конфигурации: {e}")
            return {}

    def analyze_file(self, file_path: str, sheet_name: str = None,
                    generate_reports: bool = True,
                    create_charts: bool = True) -> dict:
        """
        Анализирует файл и генерирует отчеты

        Args:
            file_path: путь к файлу
            sheet_name: название листа Excel (опционально)
            generate_reports: генерировать ли отчеты
            create_charts: создавать ли графики

        Returns:
            Результаты анализа
        """
        print(f"\n{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.CYAN}АНАЛИТИЧЕСКИЙ ИНСТРУМЕНТ - ЕЖЕМЕСЯЧНЫЙ АНАЛИЗ")
        print(f"{Fore.CYAN}{'=' * 80}\n")

        # Шаг 1: Загрузка данных
        print(f"{Fore.YELLOW}[1/5] Загрузка данных...")
        try:
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = self.parser.read_excel(file_path, sheet_name)
            elif file_path.endswith('.csv'):
                df = self.parser.read_csv(file_path)
            else:
                raise ValueError("Неподдерживаемый формат файла")

            df = self.parser.clean_data(df)
            print(f"{Fore.GREEN}✓ Загружено {len(df)} строк, {len(df.columns)} колонок")

        except Exception as e:
            print(f"{Fore.RED}✗ Ошибка при загрузке данных: {e}")
            return {}

        # Шаг 2: Анализ данных
        print(f"\n{Fore.YELLOW}[2/5] Выполнение аналитики...")
        try:
            analytics_results = self.analytics.analyze_performance(df)
            print(f"{Fore.GREEN}✓ Анализ выполнен")
        except Exception as e:
            print(f"{Fore.RED}✗ Ошибка при анализе: {e}")
            analytics_results = {}

        # Шаг 3: Поиск инсайтов
        print(f"\n{Fore.YELLOW}[3/5] Поиск инсайтов...")
        try:
            insights = self.insights_engine.analyze(df)
            print(f"{Fore.GREEN}✓ Найдено {len(insights)} инсайтов")

            # Вывод критических инсайтов
            critical = [i for i in insights if i['severity'] == 'critical']
            if critical:
                print(f"\n{Fore.RED}⚠️  Обнаружено {len(critical)} критических проблем:")
                for i in critical[:3]:
                    print(f"  • {i['title']}")

            positive = [i for i in insights if i['severity'] == 'positive']
            if positive:
                print(f"\n{Fore.GREEN}✓ Положительных тенденций: {len(positive)}")

        except Exception as e:
            print(f"{Fore.RED}✗ Ошибка при поиске инсайтов: {e}")
            insights = []

        # Шаг 4: Создание графиков
        chart_files = []
        if create_charts and self.config.get('reports', {}).get('include_charts', True):
            print(f"\n{Fore.YELLOW}[4/5] Создание визуализаций...")
            try:
                chart_files = self.visualizer.create_all_charts(
                    df, insights, analytics_results
                )
                print(f"{Fore.GREEN}✓ Создано {len(chart_files)} графиков")
            except Exception as e:
                print(f"{Fore.RED}✗ Ошибка при создании графиков: {e}")

        # Шаг 5: Генерация отчетов
        report_files = {}
        if generate_reports:
            print(f"\n{Fore.YELLOW}[5/5] Генерация отчетов...")
            try:
                report_files = self.report_generator.generate_full_report(
                    df, insights, analytics_results
                )
                print(f"{Fore.GREEN}✓ Создано {len(report_files)} отчетов")
                print(f"\n{Fore.CYAN}Созданные отчеты:")
                for report_type, filepath in report_files.items():
                    print(f"  • {report_type}: {filepath}")
            except Exception as e:
                print(f"{Fore.RED}✗ Ошибка при генерации отчетов: {e}")

        # Итоговая сводка
        print(f"\n{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.GREEN}АНАЛИЗ ЗАВЕРШЕН!")
        print(f"{Fore.CYAN}{'=' * 80}\n")

        if analytics_results:
            print(self.analytics.get_summary_report())

        return {
            'data': df,
            'analytics': analytics_results,
            'insights': insights,
            'reports': report_files,
            'charts': chart_files
        }

    def interactive_mode(self):
        """Интерактивный режим работы"""
        print(f"\n{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.CYAN}ИНТЕРАКТИВНЫЙ РЕЖИМ")
        print(f"{Fore.CYAN}{'=' * 80}\n")

        print("Выберите действие:")
        print("1. Анализировать Excel файл")
        print("2. Анализировать CSV файл")
        print("3. Выход")

        choice = input("\nВаш выбор: ")

        if choice == '1':
            file_path = input("Путь к Excel файлу: ")
            sheet_name = input("Название листа (Enter для первого листа): ")
            sheet_name = sheet_name if sheet_name else None
            self.analyze_file(file_path, sheet_name)

        elif choice == '2':
            file_path = input("Путь к CSV файлу: ")
            self.analyze_file(file_path)

        elif choice == '3':
            print("До свидания!")
            sys.exit(0)

        else:
            print(f"{Fore.RED}Неверный выбор")


def main():
    """Точка входа в программу"""
    parser = argparse.ArgumentParser(
        description='Аналитический инструмент для ежемесячного анализа'
    )

    parser.add_argument(
        'file',
        nargs='?',
        help='Путь к файлу для анализа (Excel или CSV)'
    )

    parser.add_argument(
        '-s', '--sheet',
        help='Название листа Excel',
        default=None
    )

    parser.add_argument(
        '-c', '--config',
        help='Путь к файлу конфигурации',
        default='config.yaml'
    )

    parser.add_argument(
        '--no-reports',
        action='store_true',
        help='Не генерировать отчеты'
    )

    parser.add_argument(
        '--no-charts',
        action='store_true',
        help='Не создавать графики'
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Интерактивный режим'
    )

    args = parser.parse_args()

    # Создаем инструмент
    tool = AnalyticsTool(config_path=args.config)

    # Запускаем анализ
    if args.interactive:
        tool.interactive_mode()
    elif args.file:
        tool.analyze_file(
            args.file,
            sheet_name=args.sheet,
            generate_reports=not args.no_reports,
            create_charts=not args.no_charts
        )
    else:
        # Если файл не указан, запускаем интерактивный режим
        tool.interactive_mode()


if __name__ == '__main__':
    main()
