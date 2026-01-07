"""
Основной аналитический модуль
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class MonthlyAnalytics:
    """Класс для выполнения ежемесячного анализа"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data = None
        self.results = {}

    def analyze_performance(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Анализирует производительность филиалов

        Args:
            df: DataFrame с данными

        Returns:
            Словарь с результатами анализа
        """
        results = {
            'summary': self._calculate_summary_statistics(df),
            'plan_execution': self._analyze_plan_execution(df),
            'ranking': self._create_branch_ranking(df),
            'trends': self._analyze_trends(df),
            'distribution': self._analyze_distribution(df)
        }

        self.results = results
        return results

    def _calculate_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Вычисляет сводную статистику"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        summary = {
            'total_branches': len(df),
            'metrics': {}
        }

        for col in numeric_cols:
            summary['metrics'][col] = {
                'total': float(df[col].sum()),
                'mean': float(df[col].mean()),
                'median': float(df[col].median()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'std': float(df[col].std())
            }

        return summary

    def _analyze_plan_execution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Анализирует выполнение плана"""
        execution = {}

        # Ищем пары план/факт
        plan_cols = [col for col in df.columns if 'ПЛАН' in str(col).upper()]
        fact_cols = [col for col in df.columns if 'ФАКТ' in str(col).upper()]

        for plan_col in plan_cols:
            for fact_col in fact_cols:
                # Проверяем, что колонки связаны
                plan_key = str(plan_col).replace('ПЛАН', '').strip()
                fact_key = str(fact_col).replace('ФАКТ', '').strip()

                if plan_key and fact_key and plan_key.lower() in fact_key.lower():
                    df_temp = df.copy()
                    df_temp['execution_%'] = (
                        pd.to_numeric(df_temp[fact_col], errors='coerce') /
                        pd.to_numeric(df_temp[plan_col], errors='coerce') * 100
                    )

                    execution[f'{plan_col}_{fact_col}'] = {
                        'avg_execution': float(df_temp['execution_%'].mean()),
                        'above_plan': int((df_temp['execution_%'] > 100).sum()),
                        'below_plan': int((df_temp['execution_%'] < 100).sum()),
                        'critical_below': int((df_temp['execution_%'] < 75).sum())
                    }

        return execution

    def _create_branch_ranking(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Создает рейтинг филиалов"""
        branch_col = self._find_branch_column(df)
        if not branch_col:
            return {}

        # Находим основную метрику (обычно GMV)
        main_metric = None
        for col in df.columns:
            if 'GMV' in str(col).upper() and 'ФАКТ' in str(col).upper():
                main_metric = col
                break

        if not main_metric:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                main_metric = numeric_cols[0]

        if not main_metric:
            return {}

        # Создаем рейтинг
        df_sorted = df.sort_values(by=main_metric, ascending=False)

        ranking = {
            'metric': main_metric,
            'top_10': [],
            'bottom_10': []
        }

        for idx, row in df_sorted.head(10).iterrows():
            ranking['top_10'].append({
                'branch': row[branch_col],
                'value': float(row[main_metric]) if pd.notna(row[main_metric]) else 0
            })

        for idx, row in df_sorted.tail(10).iterrows():
            ranking['bottom_10'].append({
                'branch': row[branch_col],
                'value': float(row[main_metric]) if pd.notna(row[main_metric]) else 0
            })

        return ranking

    def _analyze_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Анализирует тренды"""
        trends = {}

        # Ищем колонки с процентами роста
        growth_cols = [col for col in df.columns
                       if '%' in str(col) or 'рост' in str(col).lower()]

        for col in growth_cols:
            df_temp = df.copy()
            df_temp[col] = pd.to_numeric(df_temp[col], errors='coerce')

            trends[col] = {
                'growing': int((df_temp[col] > 0).sum()),
                'declining': int((df_temp[col] < 0).sum()),
                'stable': int((df_temp[col] == 0).sum()),
                'avg_growth': float(df_temp[col].mean())
            }

        return trends

    def _analyze_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Анализирует распределение показателей"""
        distribution = {}

        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols[:10]:  # Ограничиваем количество
            values = df[col].dropna()

            if len(values) > 0:
                # Создаем квартили
                distribution[col] = {
                    'quartiles': {
                        'Q1': float(values.quantile(0.25)),
                        'Q2': float(values.quantile(0.50)),
                        'Q3': float(values.quantile(0.75))
                    },
                    'percentiles': {
                        'P10': float(values.quantile(0.10)),
                        'P90': float(values.quantile(0.90))
                    }
                }

        return distribution

    def compare_periods(self, df_current: pd.DataFrame,
                       df_previous: pd.DataFrame) -> Dict[str, Any]:
        """
        Сравнивает два периода

        Args:
            df_current: данные текущего периода
            df_previous: данные предыдущего периода

        Returns:
            Результаты сравнения
        """
        comparison = {
            'branches_change': {
                'current': len(df_current),
                'previous': len(df_previous),
                'diff': len(df_current) - len(df_previous)
            },
            'metrics_comparison': {}
        }

        # Сравниваем общие метрики
        numeric_cols = set(df_current.select_dtypes(include=[np.number]).columns) & \
                       set(df_previous.select_dtypes(include=[np.number]).columns)

        for col in numeric_cols:
            current_sum = df_current[col].sum()
            previous_sum = df_previous[col].sum()
            change = ((current_sum - previous_sum) / previous_sum * 100) if previous_sum != 0 else 0

            comparison['metrics_comparison'][col] = {
                'current': float(current_sum),
                'previous': float(previous_sum),
                'change_%': float(change)
            }

        return comparison

    def _find_branch_column(self, df: pd.DataFrame) -> Optional[str]:
        """Находит колонку с названиями филиалов"""
        possible_names = ['филиал', 'branch', 'название', 'name', 'region', 'регион']

        for col in df.columns:
            if any(name in str(col).lower() for name in possible_names):
                return col

        text_cols = df.select_dtypes(include=['object']).columns
        if len(text_cols) > 0:
            return text_cols[0]

        return None

    def get_summary_report(self) -> str:
        """Возвращает текстовый отчет"""
        if not self.results:
            return "Анализ не выполнен"

        report = []
        report.append("=" * 60)
        report.append("ЕЖЕМЕСЯЧНЫЙ АНАЛИТИЧЕСКИЙ ОТЧЕТ")
        report.append("=" * 60)

        if 'summary' in self.results:
            summary = self.results['summary']
            report.append(f"\nВсего филиалов: {summary['total_branches']}")

        if 'ranking' in self.results and self.results['ranking']:
            ranking = self.results['ranking']
            report.append(f"\n\nТОП-5 ФИЛИАЛОВ по {ranking['metric']}:")
            for i, branch in enumerate(ranking['top_10'][:5], 1):
                report.append(f"{i}. {branch['branch']}: {branch['value']:,.0f}")

        if 'plan_execution' in self.results:
            report.append("\n\nВЫПОЛНЕНИЕ ПЛАНА:")
            for key, exec_data in self.results['plan_execution'].items():
                report.append(f"  Средний % выполнения: {exec_data['avg_execution']:.1f}%")
                report.append(f"  Выше плана: {exec_data['above_plan']} филиалов")
                report.append(f"  Ниже плана: {exec_data['below_plan']} филиалов")
                break  # Показываем первую метрику

        report.append("\n" + "=" * 60)

        return "\n".join(report)
