import pandas as pd
import sys

def convert_kraken_file(input_file, output_file):
    # 读取kraken数据文件
    df = pd.read_csv(input_file, sep='\t', header=None, names=["Abundance", "Column2", "Column3", "Category", "TaxID", "TaxonomicName"])

    # 获取Root行的Abundance值
    root_abundance = df[df['TaxonomicName'].str.contains('root')]['Abundance'].values[0]

    # 定义级别缩写映射
    level_map = {
        'P': 'Phylum',
        'C': 'Class',
        'O': 'Order',
        'F': 'Family',
        'G': 'Genus',
    }

    # 过滤数据，只保留需要的分类级别
    df_filtered = df[df['Category'].isin(level_map.keys())]

    # 计算相对丰度
    df_filtered['RelativeAbundance'] = (df_filtered['Abundance'] / root_abundance).round(4)

    # 移除相对丰度小于0.01的行
    df_filtered = df_filtered[df_filtered['RelativeAbundance'] >= 0.005]

    # 转换分类级别
    df_filtered['Category'] = df_filtered['Category'].map(level_map)

    # 移除空格并选择需要的列
    df_filtered = df_filtered[['RelativeAbundance', 'Category', 'TaxonomicName']]
    df_filtered['TaxonomicName'] = df_filtered['TaxonomicName'].str.strip()

    # 对结果进行排序
    sort_order = ['Phylum', 'Class', 'Order', 'Family', 'Genus']
    df_filtered['Category'] = pd.Categorical(df_filtered['Category'], categories=sort_order, ordered=True)
    df_filtered = df_filtered.sort_values(by=['Category', 'RelativeAbundance'], ascending=[True, False])

    # 输出结果到文件
    df_filtered.to_csv(output_file, sep='\t', index=False, header=False)
    print(f"转换完成，输出文件：{output_file}")

if __name__ == "__main__":
    # 确保传入了输入文件和输出文件路径
    if len(sys.argv) != 3:
        print("用法: python script.py <输入文件> <输出文件>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        convert_kraken_file(input_file, output_file)
