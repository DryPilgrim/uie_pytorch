import random
import csv
# real_ratio = [0.6748, 0.0163, 0.0318, 0.0507,0.0595,0.0537,0.0977,0.0036,0.0078,0.0011,0.0017,0.0005,0.0005,0.0005]
real_ratio=[0.6718, 0.2321, 0.421, 0.0170, 0.0102, 0.0262, 0.005]

# 生成随机字符串
def generate_random_string(length):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))

# 构造表格
data = []
for i in range(4000):
    data.append({
        "host": generate_random_string(10),
        "value": random.uniform(0,10)
    })
with open('table.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["host", "value"])
    writer.writeheader()
    writer.writerows(data)

# 统计各个区间的 host 数量
value_counts = {}
num2=0
num3=0
for d in data:
    if d['value']==0.0:
        num2 += 1
    if d['value']==3.0:
        num3 += 1
value_counts[(0.0, 0.0)] = num2

for i in range(12):
    lower_bound = i * 0.25
    upper_bound = (i + 1) * 0.25
    host_count = len([d for d in data if lower_bound < d["value"] <= upper_bound])
    value_counts[(lower_bound, upper_bound)] = host_count

value_counts[(3.0, 3.0)] = value_counts[(2.75, 3.0)] - num3
print('value_counts:\n',value_counts)

# 计算 num 和逐个筛选区间
# num = len(data)
num = round((value_counts[(0.0, 0.0)]+value_counts[(0, 0.25)] )/ real_ratio[0])
for i in range(1,12):
    lower_bound = i * 0.25
    upper_bound = (i + 1) * 0.25
    ratio = real_ratio[i]
    host_count = value_counts[(lower_bound, upper_bound)]
    if host_count > num * real_ratio[i]:
        keep_count = round(num * real_ratio[i])
        # 排序并仅保留前 keep_count 个 host
        d_temp = []
        for d in data:
            # print('d["value"]:',d["value"],type(d["value"]))
            try:
                if lower_bound < d["value"] <= upper_bound:
                    d_temp.append(d)
            except:
                continue
        hosts_to_keep = d_temp[:keep_count]
        # hosts_to_keep = [d for d in data if lower_bound < d["value"] <= upper_bound][:keep_count]
        # 将其他 host 的 value 置为 None
        for d in data:
            if d in hosts_to_keep:
                continue
            try:
                if lower_bound < d["value"] <= upper_bound:
                    # print('-------')
                    d["value"] = None
            except:
                continue

# 将结果写入新的 csv 表格
with open('processed_table.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["host", "value"])
    writer.writeheader()
    writer.writerows(data)

# 检查每个区间的 host 数量占比是否符合 real_ratio

len_data = len([k for k in data if k['value'] != None])
for i in range(12):
    lower_bound = i * 0.25
    upper_bound = (i + 1) * 0.25
    ratio = real_ratio[i]
    d_tmp=[]
    for d in data:
        try:
            if lower_bound < d["value"] <= upper_bound:
                d_tmp.append(d)
        except:
            continue
    host_count = len(d_tmp)
    # host_count = len([d for d in data if lower_bound < d["value"] <= upper_bound])
    print(f"区间 ({lower_bound}, {upper_bound}]: {host_count}, 占比 {host_count / len_data}, 目标占比 {ratio}")
