"""
Модуль для автоматического поиска инсайтов в данных
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class InsightsEngine:
    """Движок для поиска инсайтов в аналитических данных"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.insights_config = config.get('insights', {})
        self.insights = []

    def analyze(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Выполняет комплексный анализ данных и находит инсайты

        Args:
            df: DataFrame с данными

        Returns:
            Список найденных инсайтов
        """
        self.insights = []

        # Различные типы анализа
        self._find_plan_deviations(df)
        self._find_top_performers(df)
        self._find_underperformers(df)
        self._find_growth_leaders(df)
        self._find_anomalies(df)
        self._find_efficiency_insights(df)
        self._calculate_aggregated_metrics(df)

        logger.info(f"Найдено {len(self.insights)} инсайтов")

        return self.insights

    def _add_insight(self, category: str, severity: str, title: str,
                     description: str, data: Dict[str, Any] = None):
        """Добавляет инсайт в список"""
        insight = {
            'category': category,
            'severity': severity,  # 'critical', 'warning', 'info', 'positive'
            'title': title,
            'description': description,
            'data': data or {}
        }
        self.insights.append(insight)

    def _find_plan_deviations(self, df: pd.DataFrame):
        """Находит отклонения от плана"""
        try:
            # Ищем колонки с планом и фактом
            plan_cols = [col for col in df.columns if 'ПЛАН' in str(col).upper()]
            fact_cols = [col for col in df.columns if 'ФАКТ' in str(col).upper()]

            for plan_col in plan_cols:
                # Пытаемся найти соответствующую фактическую колонку
                for fact_col in fact_cols:
                    if not df[plan_col].empty and not df[fact_col].empty:
                        # Вычисляем процент выполнения
                        df_temp = df.copy()
                        df_temp['execution_%'] = (df_temp[fact_col] / df_temp[plan_col] * 100)

                        # Критические отклонения
                        critical_threshold = self.insights_config.get('critical_deviation', 25)
                        critical_under = df_temp[
                            df_temp['execution_%'] < (100 - critical_threshold)
                        ]

                        if not critical_under.empty:
                            branch_col = self._find_branch_column(df)
                            if branch_col:
                                branches = critical_under[branch_col].tolist()[:5]
                                self._add_insight(
                                    category='План/Факт',
                                    severity='critical',
                                    title=f'Критическое недовыполнение плана',
                                    description=f'Обнаружено {len(critical_under)} филиалов '
                                                f'с выполнением плана менее {100 - critical_threshold}%. '
                                                f'Филиалы: {", ".join(map(str, branches))}',
                                    data={
                                        'count': len(critical_under),
                                        'branches': branches,
                                        'metric': plan_col
                                    }
                                )

                        # Превышение плана
                        over_performers = df_temp[df_temp['execution_%'] > 110]
                        if not over_performers.empty:
                            branch_col = self._find_branch_column(df)
                            if branch_col:
                                branches = over_performers[branch_col].tolist()[:5]
                                self._add_insight(
                                    category='План/Факт',
                                    severity='positive',
                                    title=f'Превышение плана',
                                    description=f'{len(over_performers)} филиалов превысили план. '
                                                f'Лидеры: {", ".join(map(str, branches))}',
                                    data={
                                        'count': len(over_performers),
                                        'branches': branches,
                                        'metric': plan_col
                                    }
                                )

        except Exception as e:
            logger.warning(f"Ошибка при анализе отклонений от плана: {e}")

    def _find_top_performers(self, df: pd.DataFrame):
        """Находит топ-исполнителей по различным метрикам"""
        try:
            branch_col = self._find_branch_column(df)
            if not branch_col:
                return

            # Находим числовые колонки
            numeric_cols = df.select_dtypes(include=[np.number]).columns

            for col in numeric_cols:
                if col != branch_col and not df[col].empty:
                    top_n = self.insights_config.get('top_n', 10)
                    top_branches = df.nlargest(top_n, col)

                    if not top_branches.empty:
                        total = df[col].sum()
                        top_total = top_branches[col].sum()
                        percentage = (top_total / total * 100) if total > 0 else 0

                        self._add_insight(
                            category='Топ-исполнители',
                            severity='info',
                            title=f'Топ-{top_n} по метрике {col}',
                            description=f'Топ-{top_n} филиалов обеспечивают {percentage:.1f}% '
                                        f'от общего показателя. '
                                        f'Лидер: {top_branches.iloc[0][branch_col]}',
                            data={
                                'top_branches': top_branches[branch_col].tolist(),
                                'values': top_branches[col].tolist(),
                                'metric': col,
                                'percentage': round(percentage, 2)
                            }
                        )
                        break  # Один инсайт для основной метрики

        except Exception as e:
            logger.warning(f"Ошибка при поиске топ-исполнителей: {e}")

    def _find_underperformers(self, df: pd.DataFrame):
        """Находит филиалы с низкими показателями"""
        try:
            branch_col = self._find_branch_column(df)
            if not branch_col:
                return

            # Ищем процентные показатели выполнения
            percent_cols = [col for col in df.columns if '%' in str(col)]

            for col in percent_cols:
                if not df[col].empty:
                    # Конвертируем в числа если нужно
                    df_temp = df.copy()
                    df_temp[col] = pd.to_numeric(df_temp[col], errors='coerce')

                    # Находим филиалы с выполнением менее 80%
                    low_performers = df_temp[df_temp[col] < 80]

                    if not low_performers.empty and len(low_performers) > 2:
                        branches = low_performers[branch_col].tolist()[:5]
                        avg_performance = low_performers[col].mean()

                        self._add_insight(
                            category='Низкая эффективность',
                            severity='warning',
                            title=f'Филиалы с низким выполнением по {col}',
                            description=f'Обнаружено {len(low_performers)} филиалов '
                                        f'с показателем менее 80%. '
                                        f'Средний показатель: {avg_performance:.1f}%. '
                                        f'Филиалы: {", ".join(map(str, branches))}',
                            data={
                                'count': len(low_performers),
                                'branches': branches,
                                'metric': col,
                                'avg_value': round(avg_performance, 2)
                            }
                        )
                        break

        except Exception as e:
            logger.warning(f"Ошибка при поиске низкоэффективных филиалов: {e}")

    def _find_growth_leaders(self, df: pd.DataFrame):
        """Находит лидеров роста"""
        try:
            # Ищем колонки с процентами роста
            growth_cols = [col for col in df.columns
                           if any(x in str(col).lower() for x in ['рост', 'growth', '%'])]

            branch_col = self._find_branch_column(df)
            if not branch_col:
                return

            for col in growth_cols:
                if not df[col].empty:
                    df_temp = df.copy()
                    df_temp[col] = pd.to_numeric(df_temp[col], errors='coerce')

                    growth_threshold = self.insights_config.get('growth_threshold', 20)
                    high_growth = df_temp[df_temp[col] > growth_threshold]

                    if not high_growth.empty:
                        branches = high_growth.nlargest(5, col)
                        self._add_insight(
                            category='Рост',
                            severity='positive',
                            title=f'Лидеры роста по {col}',
                            description=f'{len(high_growth)} филиалов показывают рост более {growth_threshold}%. '
                                        f'Максимальный рост: {branches[col].max():.1f}% '
                                        f'({branches.iloc[0][branch_col]})',
                            data={
                                'count': len(high_growth),
                                'top_branches': branches[branch_col].tolist(),
                                'growth_values': branches[col].tolist(),
                                'metric': col
                            }
                        )
                        break

        except Exception as e:
            logger.warning(f"Ошибка при поиске лидеров роста: {e}")

    def _find_anomalies(self, df: pd.DataFrame):
        """Находит аномальные значения в данных"""
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            branch_col = self._find_branch_column(df)

            for col in numeric_cols[:5]:  # Ограничиваем количество проверяемых колонок
                if col != branch_col and len(df[col].dropna()) > 10:
                    # Используем IQR для поиска выбросов
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1

                    outliers = df[
                        (df[col] < (Q1 - 1.5 * IQR)) |
                        (df[col] > (Q3 + 1.5 * IQR))
                    ]

                    if not outliers.empty and len(outliers) <= 10:
                        if branch_col:
                            branches = outliers[branch_col].tolist()
                            self._add_insight(
                                category='Аномалии',
                                severity='warning',
                                title=f'Аномальные значения в {col}',
                                description=f'Обнаружено {len(outliers)} аномальных значений. '
                                            f'Филиалы: {", ".join(map(str, branches[:3]))}',
                                data={
                                    'count': len(outliers),
                                    'branches': branches,
                                    'metric': col
                                }
                            )
                            break

        except Exception as e:
            logger.warning(f"Ошибка при поиске аномалий: {e}")

    def _find_efficiency_insights(self, df: pd.DataFrame):
        """Находит инсайты по эффективности"""
        try:
            # Ищем колонки с расходами и доходами
            expense_cols = [col for col in df.columns
                            if any(x in str(col).lower() for x in ['расход', 'expense', 'опер'])]
            revenue_cols = [col for col in df.columns
                            if any(x in str(col).upper() for x in ['GMV', 'ВЫРУЧКА', 'REVENUE'])]

            if expense_cols and revenue_cols:
                expense_col = expense_cols[0]
                revenue_col = revenue_cols[0]

                df_temp = df.copy()
                df_temp['efficiency'] = (
                    pd.to_numeric(df_temp[expense_col], errors='coerce') /
                    pd.to_numeric(df_temp[revenue_col], errors='coerce') * 100
                )

                # Находим самые эффективные филиалы
                efficient = df_temp.nsmallest(5, 'efficiency')
                branch_col = self._find_branch_column(df)

                if not efficient.empty and branch_col:
                    self._add_insight(
                        category='Эффективность',
                        severity='positive',
                        title='Самые эффективные филиалы',
                        description=f'Топ-5 филиалов с наименьшим соотношением расходов к доходам. '
                                    f'Лидер: {efficient.iloc[0][branch_col]} '
                                    f'({efficient.iloc[0]["efficiency"]:.2f}%)',
                        data={
                            'branches': efficient[branch_col].tolist(),
                            'efficiency_values': efficient['efficiency'].tolist()
                        }
                    )

        except Exception as e:
            logger.warning(f"Ошибка при анализе эффективности: {e}")

    def _calculate_aggregated_metrics(self, df: pd.DataFrame):
        """Вычисляет агрегированные метрики"""
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns

            if len(numeric_cols) > 0:
                total_metrics = {}
                for col in numeric_cols:
                    total_metrics[col] = {
                        'total': df[col].sum(),
                        'average': df[col].mean(),
                        'median': df[col].median(),
                        'std': df[col].std()
                    }

                self._add_insight(
                    category='Общие метрики',
                    severity='info',
                    title='Агрегированные показатели',
                    description=f'Общее количество филиалов: {len(df)}. '
                                f'Проанализировано {len(numeric_cols)} метрик.',
                    data=total_metrics
                )

        except Exception as e:
            logger.warning(f"Ошибка при расчете агрегированных метрик: {e}")

    def _find_branch_column(self, df: pd.DataFrame) -> str:
        """Находит колонку с названиями филиалов"""
        possible_names = ['филиал', 'branch', 'название', 'name', 'region', 'регион']

        for col in df.columns:
            if any(name in str(col).lower() for name in possible_names):
                return col

        # Если не нашли, возвращаем первую текстовую колонку
        text_cols = df.select_dtypes(include=['object']).columns
        if len(text_cols) > 0:
            return text_cols[0]

        return None

    def get_insights_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        """Возвращает инсайты по уровню важности"""
        return [i for i in self.insights if i['severity'] == severity]

    def get_insights_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Возвращает инсайты по категории"""
        return [i for i in self.insights if i['category'] == category]
