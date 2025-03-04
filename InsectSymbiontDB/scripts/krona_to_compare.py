#!/usr/bin/env python3
import os
import sys
import logging
import pandas as pd
from collections import defaultdict

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def convert_krona_file(input_file, output_file):
    """将 Krona 格式文件转换为 compare 格式"""
    try:
        logger.info(f"Converting Krona file: {input_file}")

        # 读取 krona 数据文件
        with open(input_file, 'r') as f:
            lines = f.readlines()

        # 初始化数据结构
        data = []

        # 解析每一行数据
        for line in lines:
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue

            # 读取reads数
            reads = float(parts[0].strip('%'))

            # 提取分类级别信息
            taxonomy = parts[1:]

            # 确保至少有一个分类级别
            if len(taxonomy) >= 1:
                data.append({
                    'reads': reads,
                    'taxonomy': taxonomy
                })

        # 初始化各分类级别的计数器
        level_counts = {
            'Phylum': defaultdict(float),
            'Class': defaultdict(float),
            'Order': defaultdict(float),
            'Family': defaultdict(float),
            'Genus': defaultdict(float)
        }

        # 初始化各级别的总reads计数
        level_totals = {
            'Phylum': 0,
            'Class': 0,
            'Order': 0,
            'Family': 0,
            'Genus': 0
        }

        # 统计各分类级别的reads数和总数
        for item in data:
            taxonomy = item['taxonomy']
            reads = item['reads']

            # 根据 taxonomy 长度确定各级别的分类名称
            for i, level_name in enumerate(['Phylum', 'Class', 'Order', 'Family', 'Genus']):
                if i + 1 < len(taxonomy):  # 确保索引在范围内
                    taxon = taxonomy[i + 1]  # 第一个元素是域(Domain)，从第二个开始是门(Phylum)
                    if taxon and taxon not in ['unknown', 'unclassified', 'NA']:
                        level_counts[level_name][taxon] += reads
                        level_totals[level_name] += reads

        # 转换为 DataFrame 格式
        result_data = []

        # 计算每个分类级别的相对丰度
        for level, counts in level_counts.items():
            level_total = level_totals[level]
            if level_total > 0:  # 避免除以零
                for taxon, count in counts.items():
                    relative_abundance = round(count / level_total, 4)  # 使用该级别的总reads计算相对丰度并保留4位小数
                    if relative_abundance >= 0.005:  # 过滤掉相对丰度小于0.5%的
                        # 将分类名称中的下划线替换为空格
                        taxon_formatted = taxon.replace('_', ' ')
                        result_data.append({
                            'RelativeAbundance': relative_abundance,
                            'Category': level,
                            'TaxonomicName': taxon_formatted
                        })

        # 创建 DataFrame
        df = pd.DataFrame(result_data)

        # 对结果进行排序
        sort_order = ['Phylum', 'Class', 'Order', 'Family', 'Genus']
        df['Category'] = pd.Categorical(df['Category'],
                                      categories=sort_order,
                                      ordered=True)
        df = df.sort_values(by=['Category', 'RelativeAbundance'],
                           ascending=[True, False])

        # 输出结果到文件
        logger.info(f"Writing converted data to: {output_file}")
        df.to_csv(output_file, sep='\t', index=False, header=False)
        logger.info("File conversion completed successfully")

    except Exception as e:
        logger.error(f"Error converting Krona file: {str(e)}")
        raise

def main():
    if len(sys.argv) != 3:
        print("Usage: python krona_to_compare.py <input_file> <output_file>")
        sys.exit(1)

    try:
        convert_krona_file(sys.argv[1], sys.argv[2])
    except Exception as e:
        logger.error(f"Conversion failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()