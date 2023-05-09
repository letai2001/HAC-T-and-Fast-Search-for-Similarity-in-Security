import os
import tlsh
import json
from sklearn.neighbors import KDTree
import numpy as np
from sklearn.neighbors import DistanceMetric
import binascii
from sklearn.neighbors import BallTree
from scipy.spatial import distance

# Đường dẫn đến thư mục chứa các tệp tin
path = r'C:\\Users\\Admin\\Downloads\\tlsh_train\\data_test'

# Tạo một từ điển để lưu giá trị TLSH của các tệp tin
tlsh_dict = {}
def tlsh_distance(x, y):
    return tlsh.diff(x, y)

# Lặp qua tất cả các tệp tin trong thư mục và tính giá trị TLSH
for filename in os.listdir(path):
    # Đường dẫn đầy đủ của tệp tin
    full_path = os.path.join(path, filename)
    # Kiểm tra xem tệp tin có phải là tệp tin và không phải là thư mục
    if os.path.isfile(full_path):
        # Đọc nội dung của tệp tin
        with open(full_path, 'rb') as f:
            data = f.read()
            # Tính giá trị TLSH của tệp tin
            hash_value = tlsh.hash(data)
            # Lưu giá trị TLSH vào từ điển
            tlsh_dict[filename] = hash_value

# Ghi giá trị TLSH vào tệp JSON
with open('tlsh.json', 'w') as f:
    json.dump(tlsh_dict, f)
# Đọc giá trị TLSH từ tệp JSON và in chúng ra
# with open('tlsh.json', 'r') as f:
#     tlsh_dict = json.load(f)
#     for filename, hash_value in tlsh_dict.items():
#         print(f"Giá trị TLSH của tệp tin {filename}: {hash_value}")
