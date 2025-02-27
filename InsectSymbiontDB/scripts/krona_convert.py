import pandas as pd
import sys
from collections import defaultdict

def convert_krona_file(input_file, output_file):
    # 读取krona数据文件
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # 初始化数据结构
    data = []
    reads_sum = 0

    # 解析每一行数据
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) < 2:
            continue

        reads = int(parts[0])
        reads_sum += reads

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
        'Phylum': defaultdict(int),
        'Class': defaultdict(int),
        'Order': defaultdict(int),
        'Family': defaultdict(int),
        'Genus': defaultdict(int)
    }

    # 统计各分类级别的reads数
    for item in data:
        taxonomy = item['taxonomy']
        reads = item['reads']

        # 根据taxonomy长度确定各级别的分类名称
        for i, level_name in enumerate(['Phylum', 'Class', 'Order', 'Family', 'Genus']):
            if i + 1 < len(taxonomy):  # 确保索引在范围内
                taxon = taxonomy[i + 1]  # 第一个元素是域(Domain)，从第二个开始是门(Phylum)
                if taxon:  # 确保不是空字符串
                    level_counts[level_name][taxon] += reads

    # 转换为DataFrame格式
    result_data = []

    for level, counts in level_counts.items():
        for taxon, count in counts.items():
            relative_abundance = round(count / reads_sum, 4)
            if relative_abundance >= 0.005:  # 过滤掉相对丰度小于0.005的
                # 将分类名称中的下划线替换为空格
                taxon_formatted = taxon.replace('_', ' ')
                result_data.append({
                    'RelativeAbundance': relative_abundance,
                    'Category': level,
                    'TaxonomicName': taxon_formatted
                })

    # 创建DataFrame
    df = pd.DataFrame(result_data)

    # 对结果进行排序
    sort_order = ['Phylum', 'Class', 'Order', 'Family', 'Genus']
    df['Category'] = pd.Categorical(df['Category'], categories=sort_order, ordered=True)
    df = df.sort_values(by=['Category', 'RelativeAbundance'], ascending=[True, False])

    # 输出结果到文件
    df.to_csv(output_file, sep='\t', index=False, header=False)
    print(f"转换完成，输出文件：{output_file}")

if __name__ == "__main__":
    # 确保传入了输入文件和输出文件路径
    if len(sys.argv) != 3:
        print("用法: python krona_convert.py <输入文件> <输出文件>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        convert_krona_file(input_file, output_file)