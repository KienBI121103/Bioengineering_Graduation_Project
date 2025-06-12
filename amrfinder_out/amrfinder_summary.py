import os
import pandas as pd
import argparse

# Tạo parser để nhận tham số từ dòng lệnh
parser = argparse.ArgumentParser(description='Tổng hợp Class/Subclass từ các file *_amrfinder.txt')

parser.add_argument('--input', '-i', required=True, help='Đường dẫn tới folder chứa các file *_amrfinder.txt')
parser.add_argument('--output', '-o', required=True, help='Đường dẫn và tên file xuất kết quả (.csv)')

args = parser.parse_args()

folder_path = os.path.abspath(args.input)
output_file = os.path.abspath(args.output)

# Kiểm tra thư mục tồn tại
if not os.path.isdir(folder_path):
    print(f"❌ Thư mục không tồn tại: {folder_path}")
    exit(1)

# Tìm file *_amrfinder.txt
file_list = sorted([f for f in os.listdir(folder_path) if f.endswith('_amrfinder.txt')])

if not file_list:
    print("⚠️ Không tìm thấy file nào có hậu tố '_amrfinder.txt' trong thư mục.")
    exit(1)

print(f"📁 Tìm thấy {len(file_list)} file cần xử lý.")

# Xử lý dữ liệu
all_classes = set()
results = {}

for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    print(f"🔍 Đang xử lý file: {file_name}")

    try:
        df = pd.read_csv(file_path, sep='\t')
    except Exception as e:
        print(f"❌ Lỗi đọc file {file_name}: {e}")
        continue

    # Kiểm tra cột cần thiết
    if 'Class' not in df.columns or 'Subclass' not in df.columns:
        print(f"⚠️ Bỏ qua file {file_name} do thiếu cột Class/Subclass.")
        continue

    # Ghép Class/Subclass
    df['Class_Subclass'] = df['Class'].fillna('NA') + ' / ' + df['Subclass'].fillna('NA')
    classes_in_file = set(df['Class_Subclass'].unique())

    results[file_name] = classes_in_file
    all_classes.update(classes_in_file)

# Tạo bảng kết quả
all_classes = sorted(all_classes)
final_table = []

for file_name in file_list:
    row = {'File': file_name}
    if file_name in results:
        row.update({cls: '1' if cls in results[file_name] else '0' for cls in all_classes})
    else:
        row.update({cls: '-' for cls in all_classes})
    final_table.append(row)

final_df = pd.DataFrame(final_table, columns=['File'] + all_classes)

# Xuất file CSV
try:
    final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ Hoàn tất! Đã tạo file output: {output_file}"
          )
except Exception as e:
    print(f"❌ Lỗi khi lưu file output {output_file}: {e}")

    