"""
Примеры использования аналитического инструмента
"""

import sys
import os

# Добавляем src в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import AnalyticsTool
from data_parser import DataParser
from insights_engine import InsightsEngine
from analytics import MonthlyAnalytics
from visualizer import DataVisualizer
import yaml


def example_1_basic_analysis():
    """
    Пример 1: Базовый анализ файла
    """
    print("=" * 80)
    print("ПРИМЕР 1: Базовый анализ файла")
    print("=" * 80)

    # Создаем инструмент
    tool = AnalyticsTool(config_path='config.yaml')

    # Анализируем файл (замените на свой путь)
    # results = tool.analyze_file('data/input/monthly_data.xlsx')

    print("\nДля запуска этого примера:")
    print("1. Поместите ваш Excel файл в data/input/")
    print("2. Раскомментируйте строку с analyze_file и укажите путь к файлу")
    print("3. Запустите: python example_usage.py")


def example_2_custom_config():
    """
    Пример 2: Использование кастомной конфигурации
    """
    print("\n" + "=" * 80)
    print("ПРИМЕР 2: Кастомная конфигурация")
    print("=" * 80)

    # Создаем свою конфигурацию
    custom_config = {
        'insights': {
            'plan_deviation_threshold': 10,  # Более строгий порог
            'critical_deviation': 20,
            'good_performance': 98,
            'growth_threshold': 15,
            'top_n': 5
        },
        'reports': {
            'output_folder': 'custom_reports',
            'format': ['html', 'excel'],
            'include_charts': True
        },
        'visualization': {
            'chart_style': 'seaborn',
            'figure_size': [16, 10]
        }
    }

    # Сохраняем в файл
    with open('custom_config.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(custom_config, f, allow_unicode=True)

    print("✓ Кастомная конфигурация создана: custom_config.yaml")
    print("\nТеперь вы можете использовать:")
    print("python src/main.py data.xlsx --config custom_config.yaml")


def example_3_programmatic_usage():
    """
    Пример 3: Программное использование модулей
    """
    print("\n" + "=" * 80)
    print("ПРИМЕР 3: Программное использование")
    print("=" * 80)

    # Загружаем конфигурацию
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # Создаем модули
    parser = DataParser(config)
    insights_engine = InsightsEngine(config)
    analytics = MonthlyAnalytics(config)

    print("\n✓ Модули созданы:")
    print("  - DataParser: для чтения файлов")
    print("  - InsightsEngine: для поиска инсайтов")
    print("  - MonthlyAnalytics: для аналитики")

    print("\nПример кода:")
    print("""
    # Читаем данные
    df = parser.read_excel('data.xlsx')

    # Ищем инсайты
    insights = insights_engine.analyze(df)

    # Получаем критические инсайты
    critical = insights_engine.get_insights_by_severity('critical')
    for insight in critical:
        print(f"⚠️ {insight['title']}")

    # Выполняем аналитику
    results = analytics.analyze_performance(df)
    print(analytics.get_summary_report())
    """)


def example_4_insights_filtering():
    """
    Пример 4: Фильтрация и работа с инсайтами
    """
    print("\n" + "=" * 80)
    print("ПРИМЕР 4: Работа с инсайтами")
    print("=" * 80)

    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    insights_engine = InsightsEngine(config)

    # Пример инсайтов (в реальности получаются из analyze())
    example_insights = [
        {
            'category': 'План/Факт',
            'severity': 'critical',
            'title': 'Критическое недовыполнение',
            'description': '5 филиалов с выполнением < 75%'
        },
        {
            'category': 'Рост',
            'severity': 'positive',
            'title': 'Лидеры роста',
            'description': '3 филиала показывают рост > 20%'
        }
    ]

    # Симулируем результаты
    insights_engine.insights = example_insights

    print("\nДоступные методы фильтрации:")
    print("\n1. По уровню важности:")
    print("   critical_insights = insights_engine.get_insights_by_severity('critical')")

    print("\n2. По категории:")
    print("   plan_insights = insights_engine.get_insights_by_category('План/Факт')")

    print("\n3. Кастомная фильтрация:")
    print("""
    positive_insights = [
        i for i in insights
        if i['severity'] == 'positive'
    ]
    """)


def example_5_custom_visualization():
    """
    Пример 5: Создание кастомных визуализаций
    """
    print("\n" + "=" * 80)
    print("ПРИМЕР 5: Кастомные визуализации")
    print("=" * 80)

    print("\nПример создания графиков:")
    print("""
from visualizer import DataVisualizer
import pandas as pd

# Загружаем конфигурацию
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Создаем визуализатор
viz = DataVisualizer(config)

# Ваши данные
df = pd.read_excel('data.xlsx')

# Создаем график план/факт
chart = viz.create_plan_execution_chart(
    df,
    plan_col='GMV ПЛАН ДЕКАБРЬ',
    fact_col='Факт ДЕКАБРЬ СС',
    branch_col='филиал',
    top_n=20
)
print(f"График создан: {chart}")

# Создаем график процента выполнения
chart = viz.create_execution_percentage_chart(
    df,
    plan_col='GMV ПЛАН ДЕКАБРЬ',
    fact_col='Факт ДЕКАБРЬ СС',
    branch_col='филиал'
)

# Создаем топ филиалов
chart = viz.create_top_branches_chart(
    df,
    branch_col='филиал',
    metric_col='GMV ФАКТ М-1 (Ноябрь)',
    top_n=15,
    title='Топ-15 филиалов по GMV'
)
    """)


def example_6_batch_processing():
    """
    Пример 6: Пакетная обработка нескольких файлов
    """
    print("\n" + "=" * 80)
    print("ПРИМЕР 6: Пакетная обработка")
    print("=" * 80)

    print("\nПример кода для обработки нескольких файлов:")
    print("""
from main import AnalyticsTool
import os
from pathlib import Path

# Создаем инструмент
tool = AnalyticsTool()

# Папка с файлами
input_folder = Path('data/input')

# Обрабатываем все Excel файлы
for file_path in input_folder.glob('*.xlsx'):
    print(f"Обработка: {file_path.name}")

    results = tool.analyze_file(
        str(file_path),
        generate_reports=True,
        create_charts=True
    )

    # Сохраняем результаты
    print(f"  ✓ Найдено инсайтов: {len(results['insights'])}")
    print(f"  ✓ Создано отчетов: {len(results['reports'])}")
    print()
    """)


def main():
    """Запуск всех примеров"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ АНАЛИТИЧЕСКОГО ИНСТРУМЕНТА" + " " * 15 + "║")
    print("╚" + "=" * 78 + "╝")

    examples = [
        ("Базовый анализ", example_1_basic_analysis),
        ("Кастомная конфигурация", example_2_custom_config),
        ("Программное использование", example_3_programmatic_usage),
        ("Работа с инсайтами", example_4_insights_filtering),
        ("Кастомные визуализации", example_5_custom_visualization),
        ("Пакетная обработка", example_6_batch_processing),
    ]

    try:
        for i, (name, func) in enumerate(examples, 1):
            func()

        print("\n" + "=" * 80)
        print("ВСЕ ПРИМЕРЫ ЗАВЕРШЕНЫ")
        print("=" * 80)
        print("\nДополнительная информация:")
        print("- README.md - полная документация")
        print("- config.yaml - настройки инструмента")
        print("- src/main.py --help - справка по командам")
        print("\nБыстрый старт:")
        print("  python src/main.py data/input/your_file.xlsx")
        print()

    except Exception as e:
        print(f"\nОшибка при выполнении примеров: {e}")


if __name__ == '__main__':
    main()
