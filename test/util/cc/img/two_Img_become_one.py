from PIL import Image

# 打开两张PNG图片
image1 = Image.open(r"D:\temp\112\1.png")
image2 = Image.open(r"D:\temp\112\2.png")

# 获取两张图片的宽度和高度
width1, height1 = image1.size
width2, height2 = image2.size

# 计算新图片的总高度（两张图片高度之和）和最大宽度（两张图片中较宽的那张）
total_height = height1 + height2
max_width = max(width1, width2)

# 创建一个新的空白图片，大小为（最大宽度，总高度）
new_image = Image.new("RGB", (max_width, total_height))

# 将第一张图片粘贴到新图片的顶部
new_image.paste(image1, (0, 0))

# 将第二张图片粘贴到新图片的底部
new_image.paste(image2, (0, height1))

# 保存新图片
new_image.save(r"D:\temp\112\combined_image.png")
