import sys

def generate_echarts_data(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # 去掉表头
    lines = lines[1:]

    symbionts = set()
    hosts = set()
    links = []

    for line in lines:
        host, symbiont = line.strip().split('\t')
        symbionts.add(symbiont)
        hosts.add(host)
        links.append({ "source": symbiont, "target": host })

    # 构建data列表
    data = []
    for symbiont in symbionts:
        data.append({ "name": symbiont, "type": "symbiont" })
    for host in hosts:
        data.append({ "name": host, "type": "host" })

    # 打印结果
    print("var data = [")
    for item in data:
        print(f"    {{ name: '{item['name']}', type: '{item['type']}' }},")
    print("];\n")

    print("var links = [")
    for link in links:
        print(f"    {{ source: '{link['source']}', target: '{link['target']}' }},")
    print("];")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    generate_echarts_data(input_file)
