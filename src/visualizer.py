"""
Модуль для создания визуализаций
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import os
import logging

logger = logging.getLogger(__name__)


class DataVisualizer:
    """Класс для создания визуализаций данных"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.viz_config = config.get('visualization', {})

        # Настройка стиля
        style = self.viz_config.get('chart_style', 'seaborn')
        plt.style.use('default')
        sns.set_palette("husl")

        self.figure_size = tuple(self.viz_config.get('figure_size', [14, 8]))
        self.dpi = self.viz_config.get('dpi', 100)

        # Создаем папку для графиков
        self.charts_folder = os.path.join(
            config.get('reports', {}).get('output_folder', 'reports'),
            'charts'
        )
        os.makedirs(self.charts_folder, exist_ok=True)

    def create_plan_execution_chart(self, df: pd.DataFrame,
                                   plan_col: str, fact_col: str,
                                   branch_col: str,
                                   top_n: int = 15) -> str:
        """
        Создает график выполнения плана

        Args:
            df: DataFrame с данными
            plan_col: колонка с планом
            fact_col: колонка с фактом
            branch_col: колонка с названиями филиалов
            top_n: количество топ филиалов для отображения

        Returns:
            Путь к созданному файлу
        """
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

        # Готовим данные
        df_temp = df[[branch_col, plan_col, fact_col]].copy()
        df_temp = df_temp.dropna()
        df_temp = df_temp.nlargest(top_n, fact_col)

        x = np.arange(len(df_temp))
        width = 0.35

        # Создаем столбцы
        bars1 = ax.bar(x - width/2, df_temp[plan_col], width,
                       label='План', color='#3498db', alpha=0.8)
        bars2 = ax.bar(x + width/2, df_temp[fact_col], width,
                       label='Факт', color='#2ecc71', alpha=0.8)

        # Настройка осей
        ax.set_xlabel('Филиалы', fontsize=12, fontweight='bold')
        ax.set_ylabel('Значение', fontsize=12, fontweight='bold')
        ax.set_title(f'План vs Факт - Топ {top_n} филиалов', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(df_temp[branch_col], rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        filepath = os.path.join(self.charts_folder, 'plan_vs_fact.png')
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()

        logger.info(f"График план/факт создан: {filepath}")
        return filepath

    def create_performance_distribution(self, df: pd.DataFrame,
                                       metric_col: str) -> str:
        """
        Создает график распределения показателей

        Args:
            df: DataFrame с данными
            metric_col: колонка с метрикой

        Returns:
            Путь к созданному файлу
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figure_size, dpi=self.dpi)

        data = df[metric_col].dropna()

        # Гистограмма
        ax1.hist(data, bins=30, color='#3498db', alpha=0.7, edgecolor='black')
        ax1.set_xlabel(metric_col, fontsize=12)
        ax1.set_ylabel('Количество', fontsize=12)
        ax1.set_title('Распределение', fontsize=14, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)

        # Box plot
        bp = ax2.boxplot(data, vert=True, patch_artist=True)
        bp['boxes'][0].set_facecolor('#3498db')
        bp['boxes'][0].set_alpha(0.7)
        ax2.set_ylabel(metric_col, fontsize=12)
        ax2.set_title('Box Plot', fontsize=14, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        filepath = os.path.join(self.charts_folder, 'distribution.png')
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()

        logger.info(f"График распределения создан: {filepath}")
        return filepath

    def create_top_branches_chart(self, df: pd.DataFrame,
                                  branch_col: str, metric_col: str,
                                  top_n: int = 10, title: str = None) -> str:
        """
        Создает горизонтальный bar chart топ филиалов

        Args:
            df: DataFrame с данными
            branch_col: колонка с названиями филиалов
            metric_col: колонка с метрикой
            top_n: количество филиалов
            title: заголовок графика

        Returns:
            Путь к созданному файлу
        """
        fig, ax = plt.subplots(figsize=(12, 8), dpi=self.dpi)

        # Готовим данные
        df_temp = df[[branch_col, metric_col]].copy()
        df_temp = df_temp.dropna()
        df_temp = df_temp.nlargest(top_n, metric_col)
        df_temp = df_temp.sort_values(metric_col)

        # Создаем цветовую карту
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(df_temp)))

        bars = ax.barh(df_temp[branch_col], df_temp[metric_col], color=colors)

        # Добавляем значения на столбцы
        for i, (bar, value) in enumerate(zip(bars, df_temp[metric_col])):
            ax.text(value, i, f' {value:,.0f}', va='center', fontsize=10)

        ax.set_xlabel(metric_col, fontsize=12, fontweight='bold')
        ax.set_ylabel('Филиалы', fontsize=12, fontweight='bold')
        ax.set_title(title or f'Топ-{top_n} филиалов по {metric_col}',
                    fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()

        filepath = os.path.join(self.charts_folder, 'top_branches.png')
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()

        logger.info(f"График топ филиалов создан: {filepath}")
        return filepath

    def create_execution_percentage_chart(self, df: pd.DataFrame,
                                         plan_col: str, fact_col: str,
                                         branch_col: str) -> str:
        """
        Создает график процента выполнения плана

        Args:
            df: DataFrame с данными
            plan_col: колонка с планом
            fact_col: колонка с фактом
            branch_col: колонка с названиями филиалов

        Returns:
            Путь к созданному файлу
        """
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

        # Вычисляем процент выполнения
        df_temp = df[[branch_col, plan_col, fact_col]].copy()
        df_temp['execution_%'] = (df_temp[fact_col] / df_temp[plan_col] * 100)
        df_temp = df_temp.dropna()
        df_temp = df_temp.sort_values('execution_%', ascending=False).head(20)

        # Цвета в зависимости от выполнения
        colors = ['#2ecc71' if x >= 100 else '#e74c3c' if x < 75 else '#f39c12'
                  for x in df_temp['execution_%']]

        bars = ax.barh(df_temp[branch_col], df_temp['execution_%'], color=colors, alpha=0.8)

        # Добавляем линию 100%
        ax.axvline(x=100, color='black', linestyle='--', linewidth=2, label='100% план')

        # Добавляем значения
        for i, (bar, value) in enumerate(zip(bars, df_temp['execution_%'])):
            ax.text(value, i, f' {value:.1f}%', va='center', fontsize=9)

        ax.set_xlabel('Процент выполнения плана', fontsize=12, fontweight='bold')
        ax.set_ylabel('Филиалы', fontsize=12, fontweight='bold')
        ax.set_title('Выполнение плана по филиалам', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()

        filepath = os.path.join(self.charts_folder, 'execution_percentage.png')
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()

        logger.info(f"График процента выполнения создан: {filepath}")
        return filepath

    def create_correlation_heatmap(self, df: pd.DataFrame,
                                  numeric_cols: Optional[List[str]] = None) -> str:
        """
        Создает тепловую карту корреляций

        Args:
            df: DataFrame с данными
            numeric_cols: список числовых колонок (если None, берутся все)

        Returns:
            Путь к созданному файлу
        """
        fig, ax = plt.subplots(figsize=(12, 10), dpi=self.dpi)

        if numeric_cols:
            corr_data = df[numeric_cols].corr()
        else:
            numeric_df = df.select_dtypes(include=[np.number])
            corr_data = numeric_df.corr()

        # Создаем heatmap
        sns.heatmap(corr_data, annot=True, fmt='.2f', cmap='coolwarm',
                   center=0, square=True, linewidths=1,
                   cbar_kws={"shrink": 0.8}, ax=ax)

        ax.set_title('Корреляция между метриками', fontsize=14, fontweight='bold')

        plt.tight_layout()

        filepath = os.path.join(self.charts_folder, 'correlation_heatmap.png')
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()

        logger.info(f"Тепловая карта создана: {filepath}")
        return filepath

    def create_insights_summary_chart(self, insights: List[Dict[str, Any]]) -> str:
        """
        Создает сводный график по инсайтам

        Args:
            insights: список инсайтов

        Returns:
            Путь к созданному файлу
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figure_size, dpi=self.dpi)

        # Подсчет по важности
        severity_counts = {}
        for insight in insights:
            sev = insight['severity']
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        severity_labels = {
            'critical': 'Критические',
            'warning': 'Предупреждения',
            'positive': 'Положительные',
            'info': 'Информация'
        }

        severity_colors = {
            'critical': '#e74c3c',
            'warning': '#f39c12',
            'positive': '#2ecc71',
            'info': '#3498db'
        }

        labels = [severity_labels.get(k, k) for k in severity_counts.keys()]
        sizes = list(severity_counts.values())
        colors = [severity_colors.get(k, '#95a5a6')
                 for k in severity_counts.keys()]

        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
               startangle=90, textprops={'fontsize': 10})
        ax1.set_title('Распределение инсайтов по важности', fontsize=12, fontweight='bold')

        # Подсчет по категориям
        category_counts = {}
        for insight in insights:
            cat = insight['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1

        categories = list(category_counts.keys())
        counts = list(category_counts.values())

        ax2.barh(categories, counts, color='#3498db', alpha=0.7)
        ax2.set_xlabel('Количество', fontsize=10)
        ax2.set_title('Инсайты по категориям', fontsize=12, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)

        plt.tight_layout()

        filepath = os.path.join(self.charts_folder, 'insights_summary.png')
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()

        logger.info(f"Сводный график инсайтов создан: {filepath}")
        return filepath

    def create_all_charts(self, df: pd.DataFrame,
                         insights: List[Dict[str, Any]],
                         analytics_results: Dict[str, Any]) -> List[str]:
        """
        Создает все доступные графики

        Args:
            df: DataFrame с данными
            insights: список инсайтов
            analytics_results: результаты анализа

        Returns:
            Список путей к созданным файлам
        """
        created_files = []

        try:
            # Находим основные колонки
            branch_col = self._find_branch_column(df)

            # План/факт графики
            plan_cols = [col for col in df.columns if 'ПЛАН' in str(col).upper()]
            fact_cols = [col for col in df.columns if 'ФАКТ' in str(col).upper()]

            if plan_cols and fact_cols and branch_col:
                try:
                    chart = self.create_plan_execution_chart(
                        df, plan_cols[0], fact_cols[0], branch_col
                    )
                    created_files.append(chart)
                except Exception as e:
                    logger.warning(f"Не удалось создать график план/факт: {e}")

                try:
                    chart = self.create_execution_percentage_chart(
                        df, plan_cols[0], fact_cols[0], branch_col
                    )
                    created_files.append(chart)
                except Exception as e:
                    logger.warning(f"Не удалось создать график процента выполнения: {e}")

            # Топ филиалов
            if branch_col and fact_cols:
                try:
                    chart = self.create_top_branches_chart(
                        df, branch_col, fact_cols[0]
                    )
                    created_files.append(chart)
                except Exception as e:
                    logger.warning(f"Не удалось создать график топ филиалов: {e}")

            # Сводка инсайтов
            if insights:
                try:
                    chart = self.create_insights_summary_chart(insights)
                    created_files.append(chart)
                except Exception as e:
                    logger.warning(f"Не удалось создать сводку инсайтов: {e}")

            logger.info(f"Создано {len(created_files)} графиков")

        except Exception as e:
            logger.error(f"Ошибка при создании графиков: {e}")

        return created_files

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
