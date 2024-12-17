import sys

def read_symbiont_db(file_path):
    """读取共生菌数据库文件"""
    symbiont_db = []
    with open(file_path, 'r', encoding='utf-8') as f:
        # 跳过中文标题和英文标题
        next(f)
        next(f)

        for line in f:
            if line.strip():  # 跳过空行
                fields = line.strip().split('\t')
                if len(fields) >= 6:  # 确保有足够的字段
                    symbiont_db.append({
                        'full_record': fields,
                        'id': fields[0],          # RISB ID
                        'order': fields[1],       # Order (分类目)
                        'insect': fields[2],      # Insect Species (昆虫名称)
                        'genus': fields[3],       # Symbiont Genus (共生体分类属)
                        'species': fields[4],     # Symbiont Name (共生体名称)
                        'function': fields[5]     # Function (功能)
                    })
    return symbiont_db

def get_first_valid_word(name):
    """获取物种或属名的第一个有效词（忽略 Candidatus）"""
    words = name.strip().split()
    if words[0].lower() == "candidatus":
        return words[1].lower() if len(words) > 1 else ""
    return words[0].lower()

def get_species_name(name):
    """获取完整的物种名（两个词）"""
    words = name.strip().split()
    if words[0].lower() == "candidatus":
        return " ".join(words[1:3]).lower() if len(words) > 2 else ""
    return " ".join(words[:2]).lower()

def calculate_function_score(function_text):
    """根据功能描述的长度计算分数
    分数 = (字符长度 / 300) * 5，最高5分
    返回保留两位小数的分数
    """
    if not function_text or function_text.lower() == 'none':
        return 0.0

    # 计算有效字符长度（去除空格）
    text_length = len(function_text.strip())

    # 计算分数：(长度/300) * 5，最高5分
    score = min((text_length / 500) * 10, 5.0)

    # 保留两位小数
    return round(score, 2)

def match_species_level(kraken_file, symbiont_db):
    """进行物种级别的比对"""
    species_matches = []

    with open(kraken_file, 'r') as f:
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) >= 5:
                percentage = float(fields[0])
                taxon_type = fields[3].strip()
                name = fields[-1].strip()

                if taxon_type == 'S':
                    for db_entry in symbiont_db:
                        kraken_species = get_species_name(name)
                        db_species = get_species_name(db_entry['species'])
                        if kraken_species == db_species:
                            # 基础分为占比
                            score = percentage
                            # 物种级别匹配加5分
                            score += 10
                            # 添加功能描述分数（保留两位小数）
                            score += calculate_function_score(db_entry['function'])

                            species_matches.append({
                                'percentage': percentage,
                                'kraken_name': name,
                                'db_record': db_entry['full_record'],
                                'order': db_entry['order'],
                                'species_match': True,
                                'total_score': round(score, 2)  # 确保总分也保留两位小数
                            })
    return species_matches

def match_genus_level(kraken_file, symbiont_db):
    """进行属级别的比对"""
    genus_matches = []

    with open(kraken_file, 'r') as f:
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) >= 5:
                percentage = float(fields[0])
                taxon_type = fields[3].strip()
                name = fields[-1].strip()

                if taxon_type == 'G':
                    for db_entry in symbiont_db:
                        if name.lower() in db_entry['genus'].lower():
                            # 基础分为占比
                            score = percentage
                            # 添加功能描述分数（保留两位小数）
                            score += calculate_function_score(db_entry['function'])

                            genus_matches.append({
                                'percentage': percentage,
                                'kraken_name': name,
                                'db_record': db_entry['full_record'],
                                'order': db_entry['order'],
                                'species_match': False,
                                'total_score': round(score, 2)  # 确保总分也保留两位小数
                            })
    return genus_matches

def filter_genus_matches(species_matches, genus_matches):
    """基于物种匹配结果过滤属级别的匹配结果"""
    # 获取所有已匹配物种的属名
    matched_genera = set()
    for match in species_matches:
        species_name = match['kraken_name']
        matched_genera.add(get_first_valid_word(species_name))

    # 过滤属匹配结果
    filtered_genus_matches = []
    for match in genus_matches:
        genus_name = match['kraken_name']
        if get_first_valid_word(genus_name) not in matched_genera:
            filtered_genus_matches.append(match)

    return filtered_genus_matches

def add_order_matching(matches, target_order):
    """为所有匹配结果添加目匹配信息并更新评分"""
    for match in matches:
        db_order = match['order'].strip().lower()
        target = target_order.strip().lower()

        order_match = (db_order == target)
        match['order_match'] = order_match

        if order_match:
            match['total_score'] += 10

    return matches

def filter_matches(matches, max_records=3):
    """根据内部竞争规则筛选匹配结果

    规则：
    1. 每个共生菌最多保留3条最高分记录
    2. 分数完全相同的记录只保留1条

    Args:
        matches (list): 所有匹配结果的列表
        max_records (int): 每个共生菌保留的最大记录数

    Returns:
        list: 筛选后的匹配结果
    """
    # 按共生菌名称分组
    symbiont_groups = {}
    for match in matches:
        symbiont_name = get_first_valid_word(match['kraken_name'])
        if symbiont_name not in symbiont_groups:
            symbiont_groups[symbiont_name] = []
        symbiont_groups[symbiont_name].append(match)

    # 处理每个共生菌组
    filtered_matches = []
    for symbiont_name, group in symbiont_groups.items():
        # 按分数降序排序
        sorted_group = sorted(group, key=lambda x: x['total_score'], reverse=True)

        # 处理相同分数的情况
        current_score = None
        count = 0
        selected = []

        for match in sorted_group:
            if count >= max_records:
                break

            score = match['total_score']
            if score != current_score:
                # 新的分数，添加记录
                selected.append(match)
                current_score = score
                count += 1
            # 如果分数相同，跳过（只保留第一条）

        filtered_matches.extend(selected)

    # 按总分降序排序最终结果
    return sorted(filtered_matches, key=lambda x: x['total_score'], reverse=True)

def main():
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("Usage: python script.py <target_order>")
        sys.exit(1)

    # 从命令行获取目标目
    target_order = sys.argv[1]

    symbiont_db_file = "symbiontsDB.txt"
    kraken_file = "test.kraken.txt"

    # 读取数据库
    symbiont_db = read_symbiont_db(symbiont_db_file)

    # 1. 进行物种级别的比对
    species_matches = match_species_level(kraken_file, symbiont_db)

    # 2. 进行属级别的比对
    genus_matches = match_genus_level(kraken_file, symbiont_db)

    # 3. 过滤属级别的匹配结果
    filtered_genus_matches = filter_genus_matches(species_matches, genus_matches)

    # 4. 合并所有匹配结果
    all_matches = species_matches + filtered_genus_matches

    # 5. 添加目匹配信息
    all_matches = add_order_matching(all_matches, target_order)

    # 6. 按评分排序
    sorted_matches = sorted(all_matches, key=lambda x: x['total_score'], reverse=True)

    # 7. 最终筛选（每个共生菌最多保留3条记录）
    final_matches = filter_matches(sorted_matches, max_records=3)

    # 输出结果
    print("Percentage", "Kraken_Name", "DB_ID", "Order", "Insect_Species", "Symbiont_Genus",
          "Symbiont_Species", "Function", "Species_Match", "Order_Match", "Total_Score", sep='\t')

    for match in final_matches:
        print(match['percentage'], match['kraken_name'], *match['db_record'],
              str(match['species_match']), str(match['order_match']), match['total_score'], sep='\t')

if __name__ == "__main__":
    main()