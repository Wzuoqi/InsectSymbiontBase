import os

def split_file(input_file, output_dir, lines_per_file):
    # 创建输出目录，如果不存在
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, 'r') as file:
        file_count = 0
        current_lines = []

        for line_number, line in enumerate(file, start=1):
            current_lines.append(line)

            # 每达到指定行数，就写入一个新文件
            if line_number % lines_per_file == 0:
                output_file = os.path.join(output_dir, f'split_file_{file_count}.tab')
                with open(output_file, 'w') as out_file:
                    out_file.writelines(current_lines)  # 写入当前行
                print(f"创建文件: {output_file}")
                file_count += 1
                current_lines = []  # 清空当前行列表

        # 处理剩余的行
        if current_lines:
            output_file = os.path.join(output_dir, f'split_file_{file_count}.tab')
            with open(output_file, 'w') as out_file:
                out_file.writelines(current_lines)  # 写入剩余行
            print(f"创建文件: {output_file}")

if __name__ == "__main__":
    input_file_path = './data/gene250212.tab'  # 输入文件路径
    output_directory = './split'  # 输出目录
    lines_per_file = 500000  # 每个文件的行数

    split_file(input_file_path, output_directory, lines_per_file)