from collections import defaultdict
import re
import logging

logger = logging.getLogger(__name__)

class TaxonomyConverter:
    """统一的分类数据转换器"""

    def __init__(self):
        self.taxonomic_levels = {
            'phylum': 1,
            'class': 2,
            'order': 3,
            'family': 4,
            'genus': 5,
            'species': 6
        }

    def parse_kraken_file(self, file_path):
        """解析Kraken格式文件"""
        try:
            taxonomy_counts = defaultdict(lambda: defaultdict(float))
            total_reads = 0

            with open(file_path, 'r') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) < 6:
                        continue

                    percentage = float(parts[0].strip())
                    reads = int(parts[1])
                    total_reads += reads

                    # 解析分类路径
                    tax_path = parts[5:]
                    current_path = []

                    for level, taxon in enumerate(tax_path):
                        if level >= len(self.taxonomic_levels):
                            break

                        current_path.append(taxon)
                        level_name = list(self.taxonomic_levels.keys())[level]
                        taxonomy_counts[level_name][taxon] = percentage

            return taxonomy_counts

        except Exception as e:
            logger.error(f"Error parsing Kraken file: {str(e)}")
            raise

    def parse_krona_file(self, file_path):
        """解析Krona格式文件"""
        try:
            taxonomy_counts = defaultdict(lambda: defaultdict(float))
            total_count = 0

            with open(file_path, 'r') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) < 2:
                        continue

                    count = float(parts[0])
                    total_count += count
                    tax_path = parts[1:]

                    for level, taxon in enumerate(tax_path):
                        if level >= len(self.taxonomic_levels):
                            break

                        level_name = list(self.taxonomic_levels.keys())[level]
                        taxonomy_counts[level_name][taxon] += count

            # 转换为相对丰度
            for level in taxonomy_counts:
                for taxon in taxonomy_counts[level]:
                    taxonomy_counts[level][taxon] = (taxonomy_counts[level][taxon] / total_count) * 100

            return taxonomy_counts

        except Exception as e:
            logger.error(f"Error parsing Krona file: {str(e)}")
            raise

    def convert_to_standard_format(self, input_file, file_type):
        """转换为标准格式"""
        try:
            if file_type == 'kraken':
                taxonomy_counts = self.parse_kraken_file(input_file)
            elif file_type == 'krona':
                taxonomy_counts = self.parse_krona_file(input_file)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

            return taxonomy_counts

        except Exception as e:
            logger.error(f"Error converting file: {str(e)}")
            raise

    def save_standard_format(self, taxonomy_counts, output_file):
        """保存为标准格式"""
        try:
            with open(output_file, 'w') as f:
                for level in self.taxonomic_levels:
                    if level in taxonomy_counts:
                        for taxon, abundance in taxonomy_counts[level].items():
                            f.write(f"{abundance:.4f}\t{level.capitalize()}\t{taxon}\n")

        except Exception as e:
            logger.error(f"Error saving standard format: {str(e)}")
            raise