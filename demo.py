#!/usr/bin/env python3
"""
Демонстрация работы аналитического инструмента
Создает тестовые данные и запускает анализ
"""

import pandas as pd
import numpy as np
import sys
import os

# Добавляем src в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import AnalyticsTool
from colorama import init, Fore, Style

init(autoreset=True)


def create_demo_data():
    """Создает тестовые данные для демонстрации"""

    print(f"{Fore.CYAN}Создание тестовых данных...")

    np.random.seed(42)

    # Создаем 30 филиалов
    branches = [
        "Филиал Пара", "Филиал Бепен", "Филиал Рич Гранд ду Норд",
        "Филиал Натал", "Филиал Севара", "Филиал Форталеза",
        "Филиал Серилим Африка", "Филиал Ваня Севандор",
        "Филиал Ильяус", "Филиал Федеральный", "Филиал Бразилка",
        "Филиал Естинути", "Филиал Атланты", "Филиал Гуварапари",
        "Филиал Анхета", "Филиал Парана", "Филиал Понд-Ринга",
        "Филиал Матаньюс", "Филиал Гувараба", "Филиал Сан Паулу",
        "Филиал Штат", "Филиал Санта Катарина", "Филиал Большой Набер",
        "Филиал Канена", "Филиал Канцил де Кануа", "Филиал Трамандал",
        "Филиал Грамаду", "Филиал Рич Гранд ду Сул", "Филиал Порту Алегри",
        "Филиал Камуса"
    ]

    data = []

    for branch in branches:
        # Генерируем реалистичные данные
        base_gmv = np.random.randint(300000, 5000000)
        plan_gmv = base_gmv * np.random.uniform(0.95, 1.15)

        # Некоторые филиалы недовыполняют план
        if np.random.random() < 0.3:
            fact_gmv = plan_gmv * np.random.uniform(0.60, 0.85)  # Недовыполнение
        elif np.random.random() < 0.5:
            fact_gmv = plan_gmv * np.random.uniform(0.85, 1.0)   # Близко к плану
        else:
            fact_gmv = plan_gmv * np.random.uniform(1.0, 1.25)   # Превышение

        # Операционные расходы
        expense_ratio = np.random.uniform(0.08, 0.15)
        plan_expense = plan_gmv * expense_ratio
        fact_expense = fact_gmv * expense_ratio * np.random.uniform(0.9, 1.1)

        # Процент роста
        growth = np.random.uniform(-10, 30)

        data.append({
            'филиал': branch,
            'GMV ФАКТ М-1 (Ноябрь)': int(base_gmv),
            'GMV ПЛАН ДЕКАБРЬ': int(plan_gmv),
            'Факт ДЕКАБРЬ СС': int(fact_gmv),
            'Опер расход филиала ФАКТ НОЯБРЬ': int(plan_expense),
            'Опер расход филиала ПЛАН ДЕКАБРЬ': int(fact_expense),
            'Расходы фот логистики ПЛАН': int(plan_expense * 0.6),
            'Расходы фот логистики ФАКТ': int(fact_expense * 0.6),
            'Част - ть более ФАКТ ноябрь': round(np.random.uniform(0.95, 1.10), 2),
            'Част - Ть более ПЛАН': round(np.random.uniform(0.95, 1.10), 2),
            'Дост - ть на заказ ФАКТ ноябрь': f"{int(np.random.uniform(85, 99))}%",
            'Дост - ть на заказ ПЛАН': f"{int(np.random.uniform(90, 99))}%",
            'Рост %': round(growth, 1)
        })

    df = pd.DataFrame(data)

    # Сохраняем в Excel
    demo_file = 'data/input/demo_monthly_data.xlsx'
    os.makedirs('data/input', exist_ok=True)
    df.to_excel(demo_file, index=False)

    print(f"{Fore.GREEN}✓ Тестовые данные созданы: {demo_file}")
    print(f"{Fore.GREEN}✓ Филиалов: {len(df)}")
    print(f"{Fore.GREEN}✓ Метрик: {len(df.columns)}")

    return demo_file


def run_demo():
    """Запускает демонстрацию"""

    print(f"\n{Fore.CYAN}{'=' * 80}")
    print(f"{Fore.CYAN}ДЕМОНСТРАЦИЯ АНАЛИТИЧЕСКОГО ИНСТРУМЕНТА")
    print(f"{Fore.CYAN}{'=' * 80}\n")

    # Создаем тестовые данные
    demo_file = create_demo_data()

    print(f"\n{Fore.YELLOW}Запуск анализа...\n")

    # Создаем инструмент и запускаем анализ
    tool = AnalyticsTool(config_path='config.yaml')

    results = tool.analyze_file(
        demo_file,
        generate_reports=True,
        create_charts=True
    )

    # Выводим статистику
    print(f"\n{Fore.CYAN}{'=' * 80}")
    print(f"{Fore.CYAN}РЕЗУЛЬТАТЫ ДЕМОНСТРАЦИИ")
    print(f"{Fore.CYAN}{'=' * 80}\n")

    if results:
        insights = results.get('insights', [])

        # Статистика по типам инсайтов
        critical = [i for i in insights if i['severity'] == 'critical']
        warnings = [i for i in insights if i['severity'] == 'warning']
        positive = [i for i in insights if i['severity'] == 'positive']
        info = [i for i in insights if i['severity'] == 'info']

        print(f"{Fore.GREEN}✓ Анализ завершен успешно!")
        print(f"\n{Fore.WHITE}Найдено инсайтов:")
        print(f"  {Fore.RED}🔴 Критических: {len(critical)}")
        print(f"  {Fore.YELLOW}⚠️  Предупреждений: {len(warnings)}")
        print(f"  {Fore.GREEN}✅ Положительных: {len(positive)}")
        print(f"  {Fore.BLUE}ℹ️  Информационных: {len(info)}")

        # Показываем примеры инсайтов
        if critical:
            print(f"\n{Fore.RED}Критические проблемы (примеры):")
            for insight in critical[:3]:
                print(f"  • {insight['title']}")

        if positive:
            print(f"\n{Fore.GREEN}Положительные тенденции (примеры):")
            for insight in positive[:3]:
                print(f"  • {insight['title']}")

        # Информация об отчетах
        reports = results.get('reports', {})
        if reports:
            print(f"\n{Fore.CYAN}Созданные отчеты:")
            for report_type, filepath in reports.items():
                print(f"  • {report_type}: {filepath}")

        # Информация о графиках
        charts = results.get('charts', [])
        if charts:
            print(f"\n{Fore.CYAN}Созданные графики:")
            for chart in charts:
                print(f"  • {os.path.basename(chart)}")

        print(f"\n{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.GREEN}ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!")
        print(f"{Fore.CYAN}{'=' * 80}\n")

        print(f"{Fore.WHITE}Что делать дальше:")
        print(f"  1. Откройте HTML отчет в браузере для интерактивного просмотра")
        print(f"  2. Посмотрите Excel отчет с детальными данными")
        print(f"  3. Изучите графики в папке reports/charts/")
        print(f"  4. Попробуйте со своими данными: python3 src/main.py your_file.xlsx")

        print(f"\n{Fore.YELLOW}Справка по командам:")
        print(f"  python3 src/main.py --help")
        print(f"  ./run.sh  {Fore.WHITE}# Интерактивный запуск")
        print()

    else:
        print(f"{Fore.RED}✗ Ошибка при выполнении демонстрации")


if __name__ == '__main__':
    try:
        run_demo()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Демонстрация прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
