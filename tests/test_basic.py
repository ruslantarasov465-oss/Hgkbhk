"""
Базовые тесты для аналитического инструмента
"""

import sys
import os
import pandas as pd
import numpy as np

# Добавляем src в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_parser import DataParser
from insights_engine import InsightsEngine
from analytics import MonthlyAnalytics


def create_sample_dataframe():
    """Создает тестовый DataFrame"""
    data = {
        'филиал': ['Филиал А', 'Филиал Б', 'Филиал В', 'Филиал Г', 'Филиал Д'],
        'GMV ПЛАН ДЕКАБРЬ': [1000000, 800000, 1200000, 500000, 900000],
        'GMV ФАКТ ДЕКАБРЬ': [1100000, 600000, 1250000, 450000, 920000],
        'Опер расход план': [100000, 80000, 120000, 50000, 90000],
        'Опер расход факт': [95000, 85000, 115000, 48000, 88000],
        'Рост %': [10, -5, 8, 15, 2]
    }
    return pd.DataFrame(data)


def test_data_parser():
    """Тест парсера данных"""
    print("Тест 1: DataParser")

    config = {
        'data': {
            'input_folder': 'data/input',
            'output_folder': 'data/output'
        }
    }

    parser = DataParser(config)

    # Тест с тестовым DataFrame
    df = create_sample_dataframe()

    # Очистка данных
    df_clean = parser.clean_data(df)

    assert len(df_clean) > 0, "DataFrame не должен быть пустым"
    print(f"✓ DataFrame содержит {len(df_clean)} строк")

    # Тест конвертации числовых колонок
    numeric_cols = ['GMV ПЛАН ДЕКАБРЬ', 'GMV ФАКТ ДЕКАБРЬ']
    df_converted = parser.convert_numeric_columns(df, numeric_cols)

    assert pd.api.types.is_numeric_dtype(df_converted[numeric_cols[0]]), \
        "Колонка должна быть числовой"
    print("✓ Числовые колонки сконвертированы корректно")

    print("✓ DataParser: ВСЕ ТЕСТЫ ПРОЙДЕНЫ\n")
    return True


def test_insights_engine():
    """Тест движка инсайтов"""
    print("Тест 2: InsightsEngine")

    config = {
        'insights': {
            'plan_deviation_threshold': 15,
            'critical_deviation': 25,
            'good_performance': 95,
            'growth_threshold': 20,
            'top_n': 10
        }
    }

    engine = InsightsEngine(config)
    df = create_sample_dataframe()

    # Анализ
    insights = engine.analyze(df)

    assert isinstance(insights, list), "Результат должен быть списком"
    print(f"✓ Найдено {len(insights)} инсайтов")

    # Проверка структуры инсайтов
    if insights:
        insight = insights[0]
        required_keys = ['category', 'severity', 'title', 'description']
        for key in required_keys:
            assert key in insight, f"Инсайт должен содержать ключ '{key}'"
        print("✓ Структура инсайтов корректна")

    # Тест фильтрации
    critical = engine.get_insights_by_severity('critical')
    assert isinstance(critical, list), "Результат фильтрации должен быть списком"
    print(f"✓ Фильтрация работает (критических: {len(critical)})")

    print("✓ InsightsEngine: ВСЕ ТЕСТЫ ПРОЙДЕНЫ\n")
    return True


def test_analytics():
    """Тест аналитического модуля"""
    print("Тест 3: MonthlyAnalytics")

    config = {}
    analytics = MonthlyAnalytics(config)
    df = create_sample_dataframe()

    # Анализ производительности
    results = analytics.analyze_performance(df)

    assert isinstance(results, dict), "Результат должен быть словарем"
    print("✓ Анализ выполнен успешно")

    # Проверка наличия ключевых разделов
    expected_sections = ['summary', 'plan_execution', 'ranking']
    for section in expected_sections:
        assert section in results, f"Результаты должны содержать раздел '{section}'"
    print("✓ Все разделы анализа присутствуют")

    # Проверка сводной статистики
    summary = results['summary']
    assert 'total_branches' in summary, "Должно быть количество филиалов"
    assert summary['total_branches'] == len(df), "Количество филиалов должно совпадать"
    print(f"✓ Сводная статистика корректна ({summary['total_branches']} филиалов)")

    # Проверка рейтинга
    if results['ranking']:
        ranking = results['ranking']
        assert 'top_10' in ranking, "Должен быть топ-10"
        print(f"✓ Рейтинг создан")

    # Тест текстового отчета
    report = analytics.get_summary_report()
    assert isinstance(report, str), "Отчет должен быть строкой"
    assert len(report) > 0, "Отчет не должен быть пустым"
    print("✓ Текстовый отчет сгенерирован")

    print("✓ MonthlyAnalytics: ВСЕ ТЕСТЫ ПРОЙДЕНЫ\n")
    return True


def test_integration():
    """Интеграционный тест"""
    print("Тест 4: Интеграционный тест")

    # Полный цикл анализа
    config = {
        'insights': {
            'plan_deviation_threshold': 15,
            'critical_deviation': 25,
            'good_performance': 95,
            'growth_threshold': 20,
            'top_n': 10
        }
    }

    df = create_sample_dataframe()

    # Парсинг
    parser = DataParser(config)
    df_clean = parser.clean_data(df)
    print("✓ Шаг 1: Данные загружены и очищены")

    # Аналитика
    analytics = MonthlyAnalytics(config)
    results = analytics.analyze_performance(df_clean)
    print("✓ Шаг 2: Аналитика выполнена")

    # Инсайты
    engine = InsightsEngine(config)
    insights = engine.analyze(df_clean)
    print(f"✓ Шаг 3: Найдено {len(insights)} инсайтов")

    # Проверка консистентности
    assert len(df_clean) == results['summary']['total_branches'], \
        "Количество филиалов должно совпадать"
    print("✓ Данные консистентны")

    print("✓ ИНТЕГРАЦИОННЫЙ ТЕСТ ПРОЙДЕН\n")
    return True


def run_all_tests():
    """Запуск всех тестов"""
    print("=" * 80)
    print("ЗАПУСК ТЕСТОВ АНАЛИТИЧЕСКОГО ИНСТРУМЕНТА")
    print("=" * 80)
    print()

    tests = [
        ("DataParser", test_data_parser),
        ("InsightsEngine", test_insights_engine),
        ("MonthlyAnalytics", test_analytics),
        ("Integration", test_integration)
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"✗ {name}: ОШИБКА - {e}\n")
            failed += 1

    print("=" * 80)
    print(f"РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 80)
    print(f"Пройдено: {passed}/{len(tests)}")
    print(f"Провалено: {failed}/{len(tests)}")

    if failed == 0:
        print("\n✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print(f"\n✗ {failed} тестов провалено")

    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
