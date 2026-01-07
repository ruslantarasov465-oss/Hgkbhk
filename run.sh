#!/bin/bash

# Скрипт быстрого запуска аналитического инструмента

echo "=========================================="
echo "   Аналитический инструмент - Запуск"
echo "=========================================="
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Ошибка: Python 3 не найден"
    echo "Установите Python 3.8+ и попробуйте снова"
    exit 1
fi

echo "✓ Python версия: $(python3 --version)"
echo ""

# Переход в директорию скрипта
cd "$(dirname "$0")"

# Проверка зависимостей
echo "Проверка зависимостей..."
python3 -c "import pandas, openpyxl, matplotlib, seaborn, yaml, colorama" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Зависимости не установлены"
    echo ""
    read -p "Установить зависимости сейчас? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Установка зависимостей..."
        pip3 install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "❌ Ошибка при установке зависимостей"
            exit 1
        fi
        echo "✓ Зависимости установлены"
    else
        echo "Запустите: pip3 install -r requirements.txt"
        exit 1
    fi
else
    echo "✓ Все зависимости установлены"
fi

echo ""
echo "=========================================="
echo ""

# Проверка наличия файлов в data/input
if [ -z "$(ls -A data/input/*.xlsx data/input/*.xls data/input/*.csv 2>/dev/null)" ]; then
    echo "⚠️  В папке data/input/ нет файлов для анализа"
    echo ""
    echo "Скопируйте ваш Excel или CSV файл в data/input/"
    echo "Например: cp /path/to/your/file.xlsx data/input/"
    echo ""
    read -p "Запустить в интерактивном режиме? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 src/main.py --interactive
        exit 0
    else
        echo "До свидания!"
        exit 0
    fi
fi

# Показываем доступные файлы
echo "Доступные файлы для анализа:"
echo ""
select file in data/input/*.{xlsx,xls,csv} "Интерактивный режим" "Выход"; do
    case $file in
        "Интерактивный режим")
            echo ""
            python3 src/main.py --interactive
            break
            ;;
        "Выход")
            echo "До свидания!"
            exit 0
            ;;
        *)
            if [ -f "$file" ]; then
                echo ""
                echo "Анализ файла: $file"
                echo ""
                python3 src/main.py "$file"

                if [ $? -eq 0 ]; then
                    echo ""
                    echo "✓ Анализ завершен успешно!"
                    echo ""
                    echo "Отчеты созданы в папке: reports/"
                    echo "Графики созданы в папке: reports/charts/"
                    echo ""

                    # Предлагаем открыть HTML отчет
                    HTML_REPORT=$(ls -t reports/*.html 2>/dev/null | head -n1)
                    if [ -n "$HTML_REPORT" ]; then
                        echo "Последний HTML отчет: $HTML_REPORT"
                        read -p "Открыть HTML отчет в браузере? (y/n): " -n 1 -r
                        echo ""
                        if [[ $REPLY =~ ^[Yy]$ ]]; then
                            # Попытка открыть в браузере
                            if command -v xdg-open &> /dev/null; then
                                xdg-open "$HTML_REPORT"
                            elif command -v open &> /dev/null; then
                                open "$HTML_REPORT"
                            else
                                echo "Откройте файл вручную: $HTML_REPORT"
                            fi
                        fi
                    fi
                else
                    echo ""
                    echo "❌ Произошла ошибка при анализе"
                    echo "Проверьте формат файла и структуру данных"
                fi
                break
            else
                echo "Неверный выбор, попробуйте снова"
            fi
            ;;
    esac
done

echo ""
echo "=========================================="
echo "Спасибо за использование!"
echo "=========================================="
