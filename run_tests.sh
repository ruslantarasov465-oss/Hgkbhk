#!/bin/bash

# Скрипт для запуска тестов

echo "=========================================="
echo "Запуск тестов аналитического инструмента"
echo "=========================================="
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "Ошибка: Python 3 не найден"
    exit 1
fi

echo "Python версия:"
python3 --version
echo ""

# Проверка зависимостей
echo "Проверка зависимостей..."
python3 -c "import pandas, openpyxl, matplotlib, seaborn, yaml" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Некоторые зависимости не установлены"
    echo "Запустите: pip install -r requirements.txt"
    echo ""
fi

# Запуск тестов
echo "Запуск тестов..."
echo ""
python3 tests/test_basic.py

exit $?
