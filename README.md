# 📊 Аналитический инструмент для ежемесячного анализа

Мощный инструмент для автоматического анализа ежемесячных данных с поиском инсайтов и генерацией отчетов.

## 🌟 Возможности

- **Автоматический парсинг данных** из Excel и CSV файлов
- **Интеллектуальный поиск инсайтов**:
  - Отклонения от плана
  - Топ и аутсайдеры по показателям
  - Аномалии в данных
  - Тренды роста/снижения
  - Анализ эффективности
- **Комплексная аналитика**:
  - Сводная статистика
  - Выполнение плана
  - Рейтинг филиалов
  - Распределение показателей
- **Визуализация данных**:
  - График план/факт
  - Процент выполнения
  - Топ филиалов
  - Корреляции
  - Сводка по инсайтам
- **Генерация отчетов** в форматах:
  - HTML (интерактивный)
  - Excel (структурированный)
  - TXT (текстовый)
  - JSON (для интеграции)

## 📋 Требования

- Python 3.8+
- pandas
- openpyxl
- matplotlib
- seaborn
- PyYAML
- colorama

## 🚀 Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd Hgkbhk
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## 📖 Использование

### Базовое использование

```bash
# Анализ Excel файла
python src/main.py data/input/monthly_data.xlsx

# Анализ конкретного листа Excel
python src/main.py data/input/monthly_data.xlsx --sheet "Декабрь"

# Анализ CSV файла
python src/main.py data/input/monthly_data.csv
```

### Дополнительные опции

```bash
# Без генерации отчетов (только анализ)
python src/main.py data.xlsx --no-reports

# Без создания графиков
python src/main.py data.xlsx --no-charts

# Использование своего конфига
python src/main.py data.xlsx --config my_config.yaml
```

### Интерактивный режим

```bash
python src/main.py --interactive
```

## 🎯 Примеры использования

### 1. Быстрый анализ данных

```python
from src.main import AnalyticsTool

# Создаем инструмент
tool = AnalyticsTool()

# Анализируем файл
results = tool.analyze_file('data/input/monthly_data.xlsx')

# Получаем результаты
insights = results['insights']
analytics = results['analytics']
```

### 2. Программное использование отдельных модулей

```python
from src.data_parser import DataParser
from src.insights_engine import InsightsEngine
from src.analytics import MonthlyAnalytics

# Парсинг данных
parser = DataParser(config)
df = parser.read_excel('data.xlsx')

# Поиск инсайтов
insights_engine = InsightsEngine(config)
insights = insights_engine.analyze(df)

# Фильтрация критических инсайтов
critical = insights_engine.get_insights_by_severity('critical')
for insight in critical:
    print(f"⚠️ {insight['title']}: {insight['description']}")
```

### 3. Создание кастомных визуализаций

```python
from src.visualizer import DataVisualizer

visualizer = DataVisualizer(config)

# Создать график план/факт
chart = visualizer.create_plan_execution_chart(
    df,
    plan_col='GMV ПЛАН ДЕКАБРЬ',
    fact_col='Факт ДЕКАБРЬ СС',
    branch_col='филиал'
)
```

## ⚙️ Конфигурация

Настройте инструмент под свои нужды в файле `config.yaml`:

```yaml
insights:
  plan_deviation_threshold: 15  # Порог отклонения от плана (%)
  critical_deviation: 25        # Критическое отклонение (%)
  good_performance: 95          # Хорошее выполнение (%)
  growth_threshold: 20          # Порог роста (%)
  top_n: 10                     # Топ N филиалов

reports:
  format: ["html", "excel", "txt"]  # Форматы отчетов
  include_charts: true              # Включать графики
```

## 📊 Структура проекта

```
Hgkbhk/
├── src/
│   ├── __init__.py           # Инициализация модуля
│   ├── main.py               # Главный файл
│   ├── data_parser.py        # Парсинг данных
│   ├── insights_engine.py    # Поиск инсайтов
│   ├── analytics.py          # Аналитика
│   ├── report_generator.py   # Генерация отчетов
│   └── visualizer.py         # Визуализация
├── data/
│   ├── input/                # Входные данные
│   └── output/               # Обработанные данные
├── reports/                  # Сгенерированные отчеты
│   └── charts/              # Графики
├── config.yaml              # Конфигурация
├── requirements.txt         # Зависимости
└── README.md               # Документация
```

## 🔍 Типы инсайтов

Инструмент автоматически находит следующие типы инсайтов:

### 🔴 Критические
- Филиалы с критическим недовыполнением плана (< 75%)
- Серьезные аномалии в данных

### ⚠️ Предупреждения
- Филиалы с низкой эффективностью (< 80%)
- Отклонения от плана (> 15%)
- Аномальные значения

### ✅ Положительные
- Превышение плана
- Лидеры роста
- Самые эффективные филиалы

### ℹ️ Информационные
- Топ-исполнители
- Агрегированные метрики
- Общие тренды

## 📈 Пример отчета

После анализа вы получите:

1. **Текстовый отчет** с ключевыми инсайтами
2. **HTML отчет** с интерактивной визуализацией
3. **Excel файл** со структурированными данными:
   - Лист "Данные" - исходные данные
   - Лист "Инсайты" - найденные инсайты
   - Лист "Топ филиалов" - рейтинг
   - Лист "Сводка" - статистика
4. **Графики** в папке `reports/charts/`

## 🛠️ Расширение функциональности

### Добавление нового типа анализа

1. Откройте `src/insights_engine.py`
2. Добавьте новый метод:

```python
def _find_custom_insight(self, df: pd.DataFrame):
    """Ваш кастомный анализ"""
    # Ваша логика
    self._add_insight(
        category='Категория',
        severity='warning',
        title='Заголовок',
        description='Описание'
    )
```

3. Вызовите метод в `analyze()`:

```python
def analyze(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
    self.insights = []
    self._find_custom_insight(df)  # Добавьте здесь
    # ...
```

## 🐛 Решение проблем

### Ошибка при чтении Excel
- Убедитесь, что установлен `openpyxl`: `pip install openpyxl`
- Проверьте формат файла (.xlsx, не .xls)

### Графики не создаются
- Установите необходимые библиотеки: `pip install matplotlib seaborn`
- Проверьте настройку `include_charts: true` в config.yaml

### Кодировка в CSV
- Укажите правильную кодировку в config.yaml
- По умолчанию используется UTF-8

## 📝 Лицензия

MIT License

## 🤝 Вклад

Приветствуются pull requests и предложения по улучшению!

## 📧 Контакты

По вопросам и предложениям создавайте issues в репозитории.

---

**Версия**: 1.0.0
**Дата**: 2026-01-07
