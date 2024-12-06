import argparse
import os

def convert_network_data(input_file, output_file):
    """
    将网络数据从文本格式转换为echarts格式，支持symbiont分类

    Args:
        input_file (str): 输入文件路径，包含宿主-共生菌-分类关系数据
        output_file (str): 输出文件路径，用于保存生成的JavaScript代码
    """
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"输入文件不存在: {input_file}")

    # 用集合来存储唯一的宿主、共生菌和分类
    hosts = set()
    symbionts = {}  # 使用字典存储共生菌及其分类
    symbiont_categories = set()  # 存储共生菌的分类
    relationships = set()

    # 读取数据文件
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            # 跳过空行
            if not line.strip():
                continue

            # 分割数据并进行错误检查
            parts = line.strip().split('\t')
            if len(parts) != 3:
                print(f"警告: 第{line_number}行格式错误，跳过此行: {line.strip()}")
                continue

            host, symbiont, category = parts
            # 跳过空值
            if not host or not symbiont or not category:
                print(f"警告: 第{line_number}行包含空值，跳过此行: {line.strip()}")
                continue

            hosts.add(host)
            symbionts[symbiont] = category
            symbiont_categories.add(category)
            relationships.add((symbiont, host))

    # 检查是否有有效数据
    if not relationships:
        raise ValueError("没有找到有效的宿主-共生菌关系数据")

    # 生成categories数组的字符串
    categories_str = "var categories = [\n"
    # 添加宿主类别
    categories_str += "    { name: 'host', itemStyle: { color: '#ff7f0e' }, symbol: 'circle' },\n"
    # 为每个共生菌分类添加一个类别
    colors = ['#1f77b4', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    for i, category in enumerate(sorted(symbiont_categories)):
        color = colors[i % len(colors)]  # 循环使用颜色
        categories_str += f"    {{ name: '{category}', itemStyle: {{ color: '{color}' }}, symbol: 'circle' }},\n"
    categories_str = categories_str.rstrip(',\n') + '\n];\n\n'

    # 生成data数组的字符串
    data_str = "var data = [\n"
    # 添加共生菌，按分类
    for symbiont, category in sorted(symbionts.items()):
        data_str += f"    {{ name: '{symbiont}', type: 'symbiont', category: '{category}' }},\n"
    # 添加宿主
    for host in sorted(hosts):
        data_str += f"    {{ name: '{host}', type: 'host', category: 'host' }},\n"
    data_str = data_str.rstrip(',\n') + '\n];\n\n'

    # 生成links数组的字符串
    links_str = "var links = [\n"
    for symbiont, host in sorted(relationships):
        links_str += f"    {{ source: '{symbiont}', target: '{host}' }},\n"
    links_str = links_str.rstrip(',\n') + '\n];\n'

    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # 将结果写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(categories_str)
        f.write(data_str)
        f.write(links_str)

    print(f"转换完成！")
    print(f"节点数量: {len(hosts) + len(symbionts)}")
    print(f"关系数量: {len(relationships)}")
    print(f"共生菌分类数量: {len(symbiont_categories)}")

def main():
    parser = argparse.ArgumentParser(description='将网络数据转换为echarts格式')
    parser.add_argument('-i', '--input', required=True, help='输入文件路径 (network_data.txt)')
    parser.add_argument('-o', '--output', required=True, help='输出文件路径 (network_data.js)')
    args = parser.parse_args()

    try:
        convert_network_data(args.input, args.output)
    except Exception as e:
        print(f"错误: {str(e)}")
        return 1

    return 0

if __name__ == '__main__':
    main()
