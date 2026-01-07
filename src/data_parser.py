"""
Модуль для парсинга данных из Excel/CSV файлов
"""

import pandas as pd
import os
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataParser:
    """Парсер для чтения и обработки файлов с данными"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data = None

    def read_excel(self, file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """
        Читает данные из Excel файла

        Args:
            file_path: путь к файлу
            sheet_name: название листа (если None, читает первый лист)

        Returns:
            DataFrame с данными
        """
        try:
            logger.info(f"Чтение файла: {file_path}")

            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(file_path)

            logger.info(f"Загружено {len(df)} строк и {len(df.columns)} колонок")
            self.data = df
            return df

        except Exception as e:
            logger.error(f"Ошибка при чтении файла: {e}")
            raise

    def read_csv(self, file_path: str, encoding: str = 'utf-8',
                 delimiter: str = ',') -> pd.DataFrame:
        """
        Читает данные из CSV файла

        Args:
            file_path: путь к файлу
            encoding: кодировка файла
            delimiter: разделитель

        Returns:
            DataFrame с данными
        """
        try:
            logger.info(f"Чтение CSV файла: {file_path}")

            df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)

            logger.info(f"Загружено {len(df)} строк и {len(df.columns)} колонок")
            self.data = df
            return df

        except Exception as e:
            logger.error(f"Ошибка при чтении CSV файла: {e}")
            raise

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Очищает данные от пустых строк и колонок

        Args:
            df: исходный DataFrame

        Returns:
            Очищенный DataFrame
        """
        logger.info("Очистка данных...")

        # Удаление полностью пустых строк
        df = df.dropna(how='all')

        # Удаление полностью пустых колонок
        df = df.dropna(axis=1, how='all')

        logger.info(f"После очистки: {len(df)} строк и {len(df.columns)} колонок")

        return df

    def convert_numeric_columns(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """
        Конвертирует указанные колонки в числовой формат

        Args:
            df: DataFrame
            columns: список колонок для конвертации

        Returns:
            DataFrame с конвертированными колонками
        """
        for col in columns:
            if col in df.columns:
                # Удаление пробелов и конвертация в число
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace(' ', '').str.replace(',', '.'),
                    errors='coerce'
                )

        return df

    def get_data_summary(self) -> Dict[str, Any]:
        """
        Возвращает краткую информацию о загруженных данных

        Returns:
            Словарь с информацией
        """
        if self.data is None:
            return {"error": "Данные не загружены"}

        return {
            "rows": len(self.data),
            "columns": len(self.data.columns),
            "column_names": list(self.data.columns),
            "missing_values": self.data.isnull().sum().to_dict(),
            "dtypes": self.data.dtypes.astype(str).to_dict()
        }
