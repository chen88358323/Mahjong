# 第一阶段：从起始位置到第一个坏道组之前（0-167060480s）
# mkpart primary ext4 2048s 167059456s -a optimal

# 第二阶段：跳过第一个坏道组后继续分区（261839996s-385733532s）
# mkpart primary ext4 261839996s 385732608s -a optimal

# 第三阶段：跳过第一个坏道组后继续分区（385938335s-2885660344s）
# mkpart primary ext4 385938335s 2885660344s -a optimal

# 第四阶段：跳过第二个坏道组后分配剩余空间（2885866019s-100%）
# mkpart primary ext4 2885866019s 100% -a optimal

def find_max_multiple(target, base=2048):
    """
    找到小于等于target的最大base倍数
    :param target: 目标数
    :param base: 基数(默认为2048)
    :return: 最大base倍数
    """
    multiple = (target // base) * base
    if multiple > target:
        multiple -= base
    return multiple

def find_min_multiple(N,base=2048):
    x = ((N + base - 1) // base) * base  # 等价于向上取整
    print(x)  # 输出应为261840896
    return x


# 测试用例
test_num = 2885660344
result = find_max_multiple(test_num)
print(f"小于等于{test_num}的最大2048倍数是: {result}")  # 应输出385732608

test_min_num=2885866019
res=find_min_multiple(test_min_num)
print(f"大于等于{test_min_num}的最小2048倍数是: {res}")