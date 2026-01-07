# 🚀 Инструкция по установке и запуску

## Быстрый запуск (3 шага)

### Шаг 1: Установка зависимостей

```bash
pip install -r requirements.txt
```

### Шаг 2: Подготовка данных

Скопируйте ваш Excel или CSV файл в папку `data/input/`:

```bash
cp /path/to/your/monthly_data.xlsx data/input/
```

### Шаг 3: Запуск

**Вариант A: Используйте удобный скрипт**
```bash
./run.sh
```

**Вариант B: Запуск напрямую**
```bash
python3 src/main.py data/input/your_file.xlsx
```

---

## 📋 Способы запуска

### 1️⃣ Автоматический скрипт (Рекомендуется)

```bash
./run.sh
```

**Что делает:**
- Проверяет наличие Python и зависимостей
- Показывает доступные файлы
- Позволяет выбрать файл для анализа
- Автоматически предлагает открыть отчет

### 2️⃣ Интерактивный режим

```bash
python3 src/main.py --interactive
```

или

```bash
./run.sh
# Выберите "Интерактивный режим"
```

**Возможности:**
- Выбор файла через меню
- Выбор листа Excel
- Пошаговые подсказки

### 3️⃣ Командная строка

```bash
# Базовый анализ
python3 src/main.py data/input/monthly_data.xlsx

# Анализ конкретного листа
python3 src/main.py data/input/monthly_data.xlsx --sheet "Декабрь"

# Без создания графиков (быстрее)
python3 src/main.py data/input/monthly_data.xlsx --no-charts

# Только анализ, без отчетов
python3 src/main.py data/input/monthly_data.xlsx --no-reports

# Своя конфигурация
python3 src/main.py data/input/monthly_data.xlsx --config custom_config.yaml
```

### 4️⃣ Программное использование (Python)

```python
from src.main import AnalyticsTool

# Создаем инструмент
tool = AnalyticsTool()

# Анализируем файл
results = tool.analyze_file('data/input/monthly_data.xlsx')

# Работаем с результатами
print(f"Найдено инсайтов: {len(results['insights'])}")

# Получаем критические проблемы
critical = [i for i in results['insights'] if i['severity'] == 'critical']
for insight in critical:
    print(f"⚠️ {insight['title']}: {insight['description']}")
```

---

## 🔧 Требования

### Обязательно:
- **Python 3.8+** (проверьте: `python3 --version`)
- **pip** (менеджер пакетов Python)

### Зависимости (устанавливаются автоматически):
- pandas >= 2.0.0
- openpyxl >= 3.1.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- PyYAML >= 6.0
- colorama >= 0.4.6

---

## 📦 Установка зависимостей

### Через pip (рекомендуется):

```bash
pip install -r requirements.txt
```

### Через pip3 (если pip не работает):

```bash
pip3 install -r requirements.txt
```

### Через виртуальное окружение (для изоляции):

```bash
# Создаем виртуальное окружение
python3 -m venv venv

# Активируем
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Устанавливаем зависимости
pip install -r requirements.txt

# Запускаем
python src/main.py data/input/your_file.xlsx
```

---

## 📁 Структура файлов данных

### Поддерживаемые форматы:
- Excel: `.xlsx`, `.xls`
- CSV: `.csv`

### Требования к структуре:

1. **Первая строка = заголовки колонок**

2. **Колонка с названиями филиалов:**
   - "филиал", "branch", "название", "name", "регион", "region"

3. **Колонки с планом:**
   - Должны содержать слово "ПЛАН" или "план"
   - Например: "GMV ПЛАН ДЕКАБРЬ", "План продаж"

4. **Колонки с фактом:**
   - Должны содержать слово "ФАКТ" или "факт"
   - Например: "GMV ФАКТ ДЕКАБРЬ", "Факт продаж"

5. **Числовые колонки:**
   - Могут содержать пробелы в числах (автоматически удаляются)
   - Могут использовать запятую как разделитель (автоматически конвертируется)

### Пример структуры:

| филиал | GMV ПЛАН | GMV ФАКТ | Расход план | Расход факт | Рост % |
|--------|----------|----------|-------------|-------------|--------|
| Филиал А | 1000000 | 1100000 | 100000 | 95000 | 10% |
| Филиал Б | 800000 | 600000 | 80000 | 85000 | -5% |

---

## 📊 Что получите после запуска

### В папке `reports/`:

1. **HTML отчет** (`monthly_report_YYYYMMDD_HHMMSS.html`)
   - Интерактивный отчет с визуализацией
   - Откройте в любом браузере

2. **Excel отчет** (`monthly_report_YYYYMMDD_HHMMSS.xlsx`)
   - Лист "Данные" - исходные данные
   - Лист "Инсайты" - найденные проблемы и возможности
   - Лист "Топ филиалов" - рейтинг
   - Лист "Сводка" - статистика

3. **Текстовый отчет** (`monthly_report_YYYYMMDD_HHMMSS.txt`)
   - Краткая сводка
   - Ключевые инсайты
   - Рейтинг филиалов

### В папке `reports/charts/`:

1. `plan_vs_fact.png` - Сравнение плана и факта
2. `execution_percentage.png` - Процент выполнения плана
3. `top_branches.png` - Топ филиалов
4. `insights_summary.png` - Сводка по инсайтам

---

## ⚙️ Настройка

Отредактируйте `config.yaml` для настройки под ваши нужды:

```yaml
# Пороги для поиска инсайтов
insights:
  plan_deviation_threshold: 15    # Порог отклонения от плана (%)
  critical_deviation: 25          # Критическое отклонение (%)
  good_performance: 95            # Хорошее выполнение (%)
  growth_threshold: 20            # Порог роста (%)
  top_n: 10                       # Топ N филиалов

# Настройки отчетов
reports:
  output_folder: "reports"
  format: ["html", "excel", "txt"]  # Форматы отчетов
  include_charts: true              # Создавать ли графики
  language: "ru"

# Настройки визуализации
visualization:
  chart_style: "seaborn"
  figure_size: [14, 8]
  dpi: 100
```

---

## 🐛 Решение проблем

### Проблема: "command not found: python3"

**Решение:**
```bash
# Проверьте установлен ли Python
python --version

# Если показывает версию, используйте python вместо python3
python src/main.py data/input/your_file.xlsx
```

### Проблема: "No module named 'pandas'" или другие модули

**Решение:**
```bash
# Установите зависимости
pip install -r requirements.txt

# Или через pip3
pip3 install -r requirements.txt

# Или конкретный модуль
pip install pandas openpyxl matplotlib
```

### Проблема: "Permission denied: ./run.sh"

**Решение:**
```bash
# Дайте права на выполнение
chmod +x run.sh

# Теперь запустите
./run.sh
```

### Проблема: "File not found" или "No such file"

**Решение:**
```bash
# Проверьте путь к файлу
ls data/input/

# Используйте полный путь
python3 src/main.py /full/path/to/file.xlsx

# Или скопируйте файл в правильную папку
cp /path/to/your/file.xlsx data/input/
```

### Проблема: Ошибки с кодировкой в CSV

**Решение:**
В `config.yaml` измените кодировку:
```yaml
data:
  file_encoding: "cp1251"  # Для Windows
  # или
  file_encoding: "utf-8"   # Для Unix/Mac
```

### Проблема: Графики не создаются

**Решение:**
```bash
# Установите библиотеки визуализации
pip install matplotlib seaborn

# Проверьте настройку в config.yaml
# include_charts: true
```

---

## 📚 Дополнительные ресурсы

- **README.md** - Полная документация
- **QUICKSTART.md** - Быстрый старт за 5 минут
- **example_usage.py** - Примеры использования
- **config.yaml** - Файл конфигурации

### Запуск примеров:

```bash
python3 example_usage.py
```

### Запуск тестов:

```bash
./run_tests.sh
# или
python3 tests/test_basic.py
```

---

## 💡 Советы по использованию

1. **Для первого запуска** используйте `./run.sh` - он все проверит и настроит

2. **Для регулярного анализа** создайте алиас:
   ```bash
   alias analyze='python3 /path/to/Hgkbhk/src/main.py'

   # Теперь можно запускать так:
   analyze data/input/new_data.xlsx
   ```

3. **Для пакетной обработки** нескольких файлов:
   ```bash
   for file in data/input/*.xlsx; do
       python3 src/main.py "$file"
   done
   ```

4. **Для автоматизации** добавьте в cron:
   ```bash
   # Каждый день в 9:00
   0 9 * * * cd /path/to/Hgkbhk && python3 src/main.py data/input/daily_report.xlsx
   ```

---

## 🎯 Готово к работе!

Теперь просто запустите:

```bash
./run.sh
```

и следуйте подсказкам на экране! 🚀
