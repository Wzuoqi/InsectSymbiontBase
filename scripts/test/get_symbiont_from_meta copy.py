import sys
import argparse

def read_symbiont_db(file_path):
    """读取共生菌数据库文件"""
    symbiont_db = []
    with open(file_path, 'r') as f:
        # 跳过标题行
        next(f)
        for line in f:
            if line.strip():  # 跳过空行
                fields = line.strip().split('\t')
                if len(fields) >= 5:  # 确保有足够的字段（包括新增的功能列）
                    # 如果功能不为None，则添加到数据库中
                    if fields[-1].lower() != 'none':
                        symbiont_db.append({
                            'full_record': fields,
                            'genus': fields[-3],  # 由于新增了一列，需要调整索引
                            'species': fields[-2],  # 由于新增了一列，需要调整索引
                            'order': fields[2],    # 目
                            'insect': fields[3]    # 昆虫物种
                        })
    return symbiont_db

def get_first_two_words(species_name):
    """获取物种名称的前两个词"""
    words = species_name.split()
    return ' '.join(words[:2]) if len(words) >= 2 else species_name

def process_kraken_file(kraken_file, symbiont_db, target_order):
    """处理kraken文件并进行比对"""
    matches = {}  # 使用字典来按kraken名称组织匹配结果
    matched_genera = set()  # 用于记录已经在种级别匹配过的属

    with open(kraken_file, 'r') as f:
        # 首先处理所有种级别的记录
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) >= 5:
                percentage = float(fields[0])
                taxon_type = fields[3].strip()
                name = fields[-1].strip()

                if taxon_type == 'S':
                    if name not in matches:
                        matches[name] = []

                    for db_entry in symbiont_db:
                        kraken_species = get_first_two_words(name)
                        db_species = get_first_two_words(db_entry['species'])
                        if kraken_species.lower() == db_species.lower():
                            order_match = db_entry['order'].lower() == target_order.lower()
                            matches[name].append({
                                'percentage': percentage,
                                'kraken_name': name,
                                'db_record': db_entry['full_record'],
                                'taxon_type': 'S',
                                'genus': db_entry['genus'],
                                'order': db_entry['order'],
                                'insect': db_entry['insect'],
                                'order_match': order_match,
                                'species_match': True
                            })
                            matched_genera.add(db_entry['genus'].lower())

        # 重新读取文件，处理属级别的记录
        f.seek(0)
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) >= 5:
                percentage = float(fields[0])
                taxon_type = fields[3].strip()
                name = fields[-1].strip()

                if taxon_type == 'G':
                    if name.lower() not in matched_genera:
                        if name not in matches:
                            matches[name] = []

                        for db_entry in symbiont_db:
                            if name.lower() in db_entry['genus'].lower():
                                order_match = db_entry['order'].lower() == target_order.lower()
                                matches[name].append({
                                    'percentage': percentage,
                                    'kraken_name': name,
                                    'db_record': db_entry['full_record'],
                                    'taxon_type': 'G',
                                    'genus': db_entry['genus'],
                                    'order': db_entry['order'],
                                    'insect': db_entry['insect'],
                                    'order_match': order_match,
                                    'species_match': False
                                })

    # 对每个kraken记录选择最多3条不同目和昆虫物种的记录
    diverse_matches = []
    for name, match_list in matches.items():
        selected = select_diverse_records(match_list, 3)
        diverse_matches.extend(selected)

    return diverse_matches

def select_diverse_records(records, max_count=3):
    """为每个kraken记录选择不同目和昆虫物种的记录"""
    if not records:
        return []

    # 按百分比排序
    sorted_records = sorted(records, key=lambda x: x['percentage'], reverse=True)

    selected = [sorted_records[0]]  # 始终选择百分比最高的记录
    seen_orders = {sorted_records[0]['order']}
    seen_insects = {sorted_records[0]['insect']}

    # 遍历剩余记录
    for record in sorted_records[1:]:
        if len(selected) >= max_count:
            break

        # 如果目或昆虫物种都不同，则选择该记录
        if (record['order'] not in seen_orders or record['insect'] not in seen_insects):
            selected.append(record)
            seen_orders.add(record['order'])
            seen_insects.add(record['insect'])

    # 如果还没选够，添加剩余的高分记录
    while len(selected) < max_count and len(selected) < len(sorted_records):
        next_record = sorted_records[len(selected)]
        if next_record not in selected:
            selected.append(next_record)

    return selected

def select_diverse_matches(matches, max_results=200):
    """选择多样的匹配结果并按评分排序"""
    # 计算每个匹配的评分
    for match in matches:
        base_score = match['percentage']
        bonus_score = 0
        if match['order_match']:
            bonus_score += 5
        if match['species_match']:
            bonus_score += 3
        match['total_score'] = base_score + bonus_score

    # 直接按总评分排序
    sorted_matches = sorted(matches, key=lambda x: x['total_score'], reverse=True)
    return sorted_matches[:max_results]

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='Process Kraken output and match with symbiont database.')
    parser.add_argument('--order', type=str, required=True, help='Target insect order for matching')
    args = parser.parse_args()

    # 文件路径
    symbiont_db_file = "symbiontsDB.txt"
    kraken_file = "test.kraken.txt"

    # 读取数据库
    symbiont_db = read_symbiont_db(symbiont_db_file)

    # 处理kraken文件并获取匹配结果
    matches = process_kraken_file(kraken_file, symbiont_db, args.order)

    # 选择多样的匹配结果
    selected_matches = select_diverse_matches(matches)

    # 输出结果
    print("Percentage", "Kraken_Name", "DB_ID", "Order", "Insect_Species", "Symbiont_Genus",
          "Symbiont_Species", "Function", "Order_Match", "Species_Match", "Total_Score", sep='\t')
    for match in selected_matches:
        print(match['percentage'], match['kraken_name'], *match['db_record'],
              str(match['order_match']), str(match['species_match']), match['total_score'], sep='\t')

if __name__ == "__main__":
    main()