#!/usr/bin/env python3
import os
import sys
import logging
import pandas as pd

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def convert_kraken_file(input_file, output_file):
    """将Kraken格式文件转换为compare格式"""
    try:
        logger.info(f"Converting Kraken file: {input_file}")

        # 读取kraken数据文件
        df = pd.read_csv(input_file, sep='\t', header=None,
                        names=["Abundance", "Column2", "Column3", "Category", "TaxID", "TaxonomicName"])

        # 获取Root行的Abundance值作为总reads数
        root_abundance = df[df['TaxonomicName'].str.contains('root', case=False, na=False)]['Abundance'].values[0]

        # 定义分类级别映射
        level_map = {
            'P': 'Phylum',
            'C': 'Class',
            'O': 'Order',
            'F': 'Family',
            'G': 'Genus'
        }

        # 过滤数据，只保留需要的分类级别
        df_filtered = df[df['Category'].isin(level_map.keys())]

        # 计算相对丰度
        df_filtered['RelativeAbundance'] = (df_filtered['Abundance'] / root_abundance).round(6)

        # 移除相对丰度小于0.5%的行
        df_filtered = df_filtered[df_filtered['RelativeAbundance'] >= 0.005]

        # 转换分类级别
        df_filtered['Category'] = df_filtered['Category'].map(level_map)

        # 移除空格并选择需要的列
        df_filtered = df_filtered[['RelativeAbundance', 'Category', 'TaxonomicName']]
        df_filtered['TaxonomicName'] = df_filtered['TaxonomicName'].str.strip()

        # 对结果进行排序
        sort_order = ['Phylum', 'Class', 'Order', 'Family', 'Genus']
        df_filtered['Category'] = pd.Categorical(df_filtered['Category'],
                                               categories=sort_order,
                                               ordered=True)
        df_filtered = df_filtered.sort_values(by=['Category', 'RelativeAbundance'],
                                            ascending=[True, False])

        # 输出结果到文件
        logger.info(f"Writing converted data to: {output_file}")
        df_filtered.to_csv(output_file, sep='\t', index=False, header=False)
        logger.info("File conversion completed successfully")

    except Exception as e:
        logger.error(f"Error converting Kraken file: {str(e)}")
        raise

def main():
    if len(sys.argv) != 3:
        print("Usage: python kraken_to_compare.py <input_file> <output_file>")
        sys.exit(1)

    try:
        convert_kraken_file(sys.argv[1], sys.argv[2])
    except Exception as e:
        logger.error(f"Conversion failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()