import os
import logging
import pandas as pd
from typing import Dict, List, Tuple

# 设置日志记录
logger = logging.getLogger(__name__)

class TaxonomyConverter:
    """处理不同格式的分类数据文件的转换器"""

    def __init__(self):
        self.supported_levels = ['phylum', 'class', 'order', 'family', 'genus', 'species']

    def _validate_abundance(self, value: float) -> float:
        """验证并标准化丰度值"""
        try:
            value = float(value)
            # 如果丰度值大于1，假设它是百分比格式
            if value > 1:
                value = value / 100
            return max(0.0, min(1.0, value))  # 确保值在0-1之间
        except ValueError as e:
            logger.error(f"Invalid abundance value: {value}")
            raise ValueError(f"Invalid abundance value: {value}")

    def _parse_kraken(self, file_path: str) -> Dict[str, Dict[str, float]]:
        """解析Kraken格式文件
        Kraken格式示例：
        percentage\tnum_reads\ttaxon_level\ttaxon_id\tscientific_name
        """
        logger.info(f"Parsing Kraken file: {file_path}")
        try:
            results = {level: {} for level in self.supported_levels}

            with open(file_path, 'r') as f:
                for line in f:
                    try:
                        parts = line.strip().split('\t')
                        if len(parts) < 5:
                            continue

                        percentage = self._validate_abundance(parts[0].strip('%'))
                        level = parts[2].lower()
                        taxon_name = parts[4]

                        if level in self.supported_levels:
                            results[level][taxon_name] = percentage

                    except Exception as e:
                        logger.warning(f"Error parsing line in Kraken file: {line.strip()}, Error: {str(e)}")
                        continue

            return results

        except Exception as e:
            logger.error(f"Error reading Kraken file: {str(e)}")
            raise

    def _parse_krona(self, file_path: str) -> Dict[str, Dict[str, float]]:
        """解析Krona格式文件
        Krona格式示例：
        abundance\tphylum\tclass\torder\tfamily\tgenus\tspecies
        """
        logger.info(f"Parsing Krona file: {file_path}")
        try:
            results = {level: {} for level in self.supported_levels}

            with open(file_path, 'r') as f:
                header = f.readline().strip().split('\t')
                if len(header) < 2:
                    raise ValueError("Invalid Krona file format")

                for line in f:
                    try:
                        parts = line.strip().split('\t')
                        if len(parts) < 2:
                            continue

                        abundance = self._validate_abundance(parts[0])

                        # 处理每个分类级别
                        for i, taxon in enumerate(parts[1:], 1):
                            if i < len(header) and header[i].lower() in self.supported_levels:
                                level = header[i].lower()
                                if taxon and taxon != 'NA':
                                    results[level][taxon] = abundance

                    except Exception as e:
                        logger.warning(f"Error parsing line in Krona file: {line.strip()}, Error: {str(e)}")
                        continue

            return results

        except Exception as e:
            logger.error(f"Error reading Krona file: {str(e)}")
            raise

    def convert_to_standard_format(self, file_path: str, file_type: str) -> Dict[str, Dict[str, float]]:
        """将输入文件转换为标准格式"""
        logger.info(f"Converting {file_type} file to standard format: {file_path}")

        try:
            if file_type.lower() == 'kraken':
                return self._parse_kraken(file_path)
            elif file_type.lower() == 'krona':
                return self._parse_krona(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

        except Exception as e:
            logger.error(f"Error converting file: {str(e)}")
            raise

    def save_standard_format(self, data: Dict[str, Dict[str, float]], output_path: str):
        """将标准格式数据保存为文件"""
        logger.info(f"Saving standardized data to: {output_path}")

        try:
            with open(output_path, 'w') as f:
                for level in self.supported_levels:
                    for taxon, abundance in data[level].items():
                        # 格式：abundance\tlevel\ttaxon_name
                        f.write(f"{abundance:.6f}\t{level.capitalize()}\t{taxon}\n")

            logger.info("Data saved successfully")

        except Exception as e:
            logger.error(f"Error saving standardized data: {str(e)}")
            raise