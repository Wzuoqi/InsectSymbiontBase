import pandas as pd
import sys
import logging

logger = logging.getLogger(__name__)

def convert_kraken_file(input_path: str, output_path: str):
    """将Kraken格式文件转换为标准格式"""
    try:
        logger.info(f"Converting Kraken file: {input_path}")

        # 读取文件并处理可能的NA值
        df = pd.read_csv(input_path, sep='\t', na_values=[''], keep_default_na=False)

        # 确保必要的列存在
        required_columns = ['Abundance', 'TaxonomicLevel', 'TaxonomicName']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Input file missing required columns")

        # 清理数据：移除NA值并确保字符串列不包含NA
        df = df.dropna(subset=['TaxonomicName', 'TaxonomicLevel'])
        df['TaxonomicName'] = df['TaxonomicName'].astype(str)

        # 标准化分类级别名称
        level_mapping = {
            'P': 'Phylum',
            'C': 'Class',
            'O': 'Order',
            'F': 'Family',
            'G': 'Genus',
            'S': 'Species'
        }

        # 转换分类级别
        df['TaxonomicLevel'] = df['TaxonomicLevel'].map(level_mapping)

        # 移除不需要的分类级别
        df = df[df['TaxonomicLevel'].notna()]

        # 标准化丰度值（确保是0-1之间的浮点数）
        df['Abundance'] = pd.to_numeric(df['Abundance'].str.rstrip('%'), errors='coerce') / 100
        df = df.dropna(subset=['Abundance'])

        # 按分类级别和丰度排序
        df = df.sort_values(['TaxonomicLevel', 'Abundance'], ascending=[True, False])

        # 写入输出文件
        logger.info(f"Writing converted data to: {output_path}")
        with open(output_path, 'w') as f:
            for _, row in df.iterrows():
                f.write(f"{row['Abundance']:.6f}\t{row['TaxonomicLevel']}\t{row['TaxonomicName']}\n")

        logger.info("File conversion completed successfully")

    except Exception as e:
        logger.error(f"Error converting Kraken file: {str(e)}")
        raise

if __name__ == "__main__":
    # 确保传入了输入文件和输出文件路径
    if len(sys.argv) != 3:
        print("用法: python script.py <输入文件> <输出文件>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        convert_kraken_file(input_file, output_file)
