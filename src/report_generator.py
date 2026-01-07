"""
Модуль для генерации отчетов
"""

import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Генератор отчетов в различных форматах"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.report_config = config.get('reports', {})
        self.output_folder = self.report_config.get('output_folder', 'reports')

        # Создаем папку для отчетов если не существует
        os.makedirs(self.output_folder, exist_ok=True)

    def generate_full_report(self, df: pd.DataFrame, insights: List[Dict[str, Any]],
                            analytics_results: Dict[str, Any],
                            filename_prefix: str = 'monthly_report') -> Dict[str, str]:
        """
        Генерирует полный отчет во всех форматах

        Args:
            df: исходные данные
            insights: список инсайтов
            analytics_results: результаты анализа
            filename_prefix: префикс для имени файла

        Returns:
            Словарь с путями к созданным файлам
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        generated_files = {}

        formats = self.report_config.get('format', ['txt', 'html', 'excel'])

        if 'txt' in formats:
            txt_file = self._generate_text_report(
                insights, analytics_results,
                f"{filename_prefix}_{timestamp}.txt"
            )
            generated_files['text'] = txt_file

        if 'html' in formats:
            html_file = self._generate_html_report(
                df, insights, analytics_results,
                f"{filename_prefix}_{timestamp}.html"
            )
            generated_files['html'] = html_file

        if 'excel' in formats:
            excel_file = self._generate_excel_report(
                df, insights, analytics_results,
                f"{filename_prefix}_{timestamp}.xlsx"
            )
            generated_files['excel'] = excel_file

        logger.info(f"Сгенерировано {len(generated_files)} отчетов")
        return generated_files

    def _generate_text_report(self, insights: List[Dict[str, Any]],
                              analytics_results: Dict[str, Any],
                              filename: str) -> str:
        """Генерирует текстовый отчет"""
        filepath = os.path.join(self.output_folder, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("ЕЖЕМЕСЯЧНЫЙ АНАЛИТИЧЕСКИЙ ОТЧЕТ\n")
            f.write(f"Дата создания: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write("=" * 80 + "\n\n")

            # Краткая сводка
            if 'summary' in analytics_results:
                summary = analytics_results['summary']
                f.write("КРАТКАЯ СВОДКА\n")
                f.write("-" * 80 + "\n")
                f.write(f"Всего филиалов: {summary['total_branches']}\n")
                f.write(f"Проанализировано метрик: {len(summary['metrics'])}\n\n")

            # Инсайты
            f.write("\nКЛЮЧЕВЫЕ ИНСАЙТЫ\n")
            f.write("-" * 80 + "\n\n")

            # Группируем по важности
            critical = [i for i in insights if i['severity'] == 'critical']
            warnings = [i for i in insights if i['severity'] == 'warning']
            positive = [i for i in insights if i['severity'] == 'positive']
            info = [i for i in insights if i['severity'] == 'info']

            if critical:
                f.write("🔴 КРИТИЧЕСКИЕ ПРОБЛЕМЫ:\n\n")
                for i, insight in enumerate(critical, 1):
                    f.write(f"{i}. {insight['title']}\n")
                    f.write(f"   {insight['description']}\n\n")

            if warnings:
                f.write("\n⚠️  ПРЕДУПРЕЖДЕНИЯ:\n\n")
                for i, insight in enumerate(warnings, 1):
                    f.write(f"{i}. {insight['title']}\n")
                    f.write(f"   {insight['description']}\n\n")

            if positive:
                f.write("\n✅ ПОЛОЖИТЕЛЬНЫЕ ТЕНДЕНЦИИ:\n\n")
                for i, insight in enumerate(positive, 1):
                    f.write(f"{i}. {insight['title']}\n")
                    f.write(f"   {insight['description']}\n\n")

            if info:
                f.write("\nℹ️  ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:\n\n")
                for i, insight in enumerate(info[:5], 1):  # Ограничиваем количество
                    f.write(f"{i}. {insight['title']}\n")
                    f.write(f"   {insight['description']}\n\n")

            # Рейтинг филиалов
            if 'ranking' in analytics_results and analytics_results['ranking']:
                ranking = analytics_results['ranking']
                f.write("\nРЕЙТИНГ ФИЛИАЛОВ\n")
                f.write("-" * 80 + "\n")
                f.write(f"Метрика: {ranking['metric']}\n\n")

                f.write("ТОП-10:\n")
                for i, branch in enumerate(ranking['top_10'], 1):
                    f.write(f"{i:2d}. {branch['branch']:30s} {branch['value']:>15,.0f}\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("Конец отчета\n")

        logger.info(f"Текстовый отчет создан: {filepath}")
        return filepath

    def _generate_html_report(self, df: pd.DataFrame, insights: List[Dict[str, Any]],
                             analytics_results: Dict[str, Any],
                             filename: str) -> str:
        """Генерирует HTML отчет"""
        filepath = os.path.join(self.output_folder, filename)

        html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ежемесячный аналитический отчет</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        .insight {{
            margin: 15px 0;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ccc;
        }}
        .insight.critical {{
            background-color: #ffebee;
            border-left-color: #e74c3c;
        }}
        .insight.warning {{
            background-color: #fff3e0;
            border-left-color: #f39c12;
        }}
        .insight.positive {{
            background-color: #e8f5e9;
            border-left-color: #2ecc71;
        }}
        .insight.info {{
            background-color: #e3f2fd;
            border-left-color: #3498db;
        }}
        .insight-title {{
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 5px;
        }}
        .insight-description {{
            color: #555;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .metric {{
            display: inline-block;
            margin: 10px;
            padding: 15px;
            background-color: #ecf0f1;
            border-radius: 5px;
            min-width: 200px;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        .metric-label {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .timestamp {{
            color: #95a5a6;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Ежемесячный аналитический отчет</h1>
        <p class="timestamp">Создан: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
"""

        # Сводка
        if 'summary' in analytics_results:
            summary = analytics_results['summary']
            html_content += f"""
        <h2>Краткая сводка</h2>
        <div>
            <div class="metric">
                <div class="metric-label">Всего филиалов</div>
                <div class="metric-value">{summary['total_branches']}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Метрик проанализировано</div>
                <div class="metric-value">{len(summary['metrics'])}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Инсайтов найдено</div>
                <div class="metric-value">{len(insights)}</div>
            </div>
        </div>
"""

        # Инсайты
        html_content += "<h2>Ключевые инсайты</h2>"

        for severity, emoji in [('critical', '🔴'), ('warning', '⚠️'),
                               ('positive', '✅'), ('info', 'ℹ️')]:
            severity_insights = [i for i in insights if i['severity'] == severity]
            if severity_insights:
                for insight in severity_insights:
                    html_content += f"""
        <div class="insight {severity}">
            <div class="insight-title">{emoji} {insight['title']}</div>
            <div class="insight-description">{insight['description']}</div>
        </div>
"""

        # Рейтинг
        if 'ranking' in analytics_results and analytics_results['ranking']:
            ranking = analytics_results['ranking']
            html_content += f"""
        <h2>Рейтинг филиалов</h2>
        <p><strong>Метрика:</strong> {ranking['metric']}</p>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Филиал</th>
                    <th>Значение</th>
                </tr>
            </thead>
            <tbody>
"""
            for i, branch in enumerate(ranking['top_10'], 1):
                html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td>{branch['branch']}</td>
                    <td>{branch['value']:,.0f}</td>
                </tr>
"""
            html_content += """
            </tbody>
        </table>
"""

        html_content += """
    </div>
</body>
</html>
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info(f"HTML отчет создан: {filepath}")
        return filepath

    def _generate_excel_report(self, df: pd.DataFrame, insights: List[Dict[str, Any]],
                               analytics_results: Dict[str, Any],
                               filename: str) -> str:
        """Генерирует Excel отчет"""
        filepath = os.path.join(self.output_folder, filename)

        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Исходные данные
            df.to_excel(writer, sheet_name='Данные', index=False)

            # Инсайты
            if insights:
                insights_df = pd.DataFrame([
                    {
                        'Категория': i['category'],
                        'Важность': i['severity'],
                        'Заголовок': i['title'],
                        'Описание': i['description']
                    }
                    for i in insights
                ])
                insights_df.to_excel(writer, sheet_name='Инсайты', index=False)

            # Рейтинг
            if 'ranking' in analytics_results and analytics_results['ranking']:
                ranking = analytics_results['ranking']
                top_df = pd.DataFrame(ranking['top_10'])
                top_df.to_excel(writer, sheet_name='Топ филиалов', index=False)

            # Сводка
            if 'summary' in analytics_results:
                summary_data = []
                for metric, values in analytics_results['summary']['metrics'].items():
                    summary_data.append({
                        'Метрика': metric,
                        'Всего': values['total'],
                        'Среднее': values['mean'],
                        'Медиана': values['median'],
                        'Мин': values['min'],
                        'Макс': values['max']
                    })
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Сводка', index=False)

        logger.info(f"Excel отчет создан: {filepath}")
        return filepath

    def export_insights_to_json(self, insights: List[Dict[str, Any]],
                               filename: str = 'insights.json') -> str:
        """Экспортирует инсайты в JSON"""
        import json

        filepath = os.path.join(self.output_folder, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(insights, f, ensure_ascii=False, indent=2)

        logger.info(f"Инсайты экспортированы в JSON: {filepath}")
        return filepath
