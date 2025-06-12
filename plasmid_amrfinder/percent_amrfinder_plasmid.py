import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Thư mục chứa các thư mục SRR con, trong đó có file amrfinder.txt
base_dir = "C:/Users/hoahoa/Documents/DSA_study/Thesis_project/plasmid_amrfinder"

# FIX: Sử dụng pattern đúng để tìm file trong tất cả thư mục con
# Thay vì: pattern = os.path.join(base_dir, "_amrfinder.txt")
# Sử dụng: pattern với ** để tìm đệ quy trong tất cả thư mục con
pattern = os.path.join(base_dir, "**", "*_amrfinder.txt")

print(f"Đang tìm kiếm với pattern: {pattern}")

# Tìm tất cả file amrfinder.txt với tìm kiếm đệ quy
amrfinder_files = glob.glob(pattern, recursive=True)
num_files = len(amrfinder_files)
print(f"Đã tìm thấy {num_files} file amrfinder.txt")

# Debug: Hiển thị danh sách file tìm được
if num_files > 0:
    print("Các file tìm được:")
    for i, filepath in enumerate(amrfinder_files[:10], 1):  # Hiển thị 10 file đầu
        print(f"  {i}. {filepath}")
    if num_files > 10:
        print(f"  ... và {num_files - 10} file khác")

if num_files == 0:
    print("⚠️ Không tìm thấy file nào. Đang kiểm tra thư mục...")
    
    # Debug: Kiểm tra cấu trúc thư mục
    if os.path.exists(base_dir):
        print(f"✅ Thư mục base tồn tại: {base_dir}")
        subdirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
        print(f"Các thư mục con: {subdirs[:5]}..." if len(subdirs) > 5 else f"Các thư mục con: {subdirs}")
        
        # Thử tìm với pattern khác
        alternative_patterns = [
            os.path.join(base_dir, "**", "amrfinder.txt"),
            os.path.join(base_dir, "**", "*amrfinder*"),
            os.path.join(base_dir, "*", "*_amrfinder.txt"),
            os.path.join(base_dir, "*", "amrfinder.txt")
        ]
        
        print("\nThử các pattern khác:")
        for alt_pattern in alternative_patterns:
            alt_files = glob.glob(alt_pattern, recursive=True)
            print(f"  Pattern: {alt_pattern}")
            print(f"  Tìm được: {len(alt_files)} file")
            if len(alt_files) > 0:
                for f in alt_files[:3]:
                    print(f"    - {f}")
                if len(alt_files) > 3:
                    print(f"    ... và {len(alt_files) - 3} file khác")
    else:
        print(f"❌ Thư mục base không tồn tại: {base_dir}")
    
    exit()

gene_file_counter = Counter()
success_files = 0
failed_files = 0

print(f"\nĐang xử lý {num_files} file...")

for i, filepath in enumerate(amrfinder_files, 1):
    try:
        # Hiển thị tiến trình
        if i % 10 == 0 or i == num_files:
            print(f"  Đang xử lý file {i}/{num_files}...")
            
        df = pd.read_csv(filepath, sep="\t", comment='#')
        
        # Kiểm tra cột tồn tại
        if "Element symbol" in df.columns:
            genes_in_file = set(df["Element symbol"].dropna())
            gene_file_counter.update(genes_in_file)  # Đếm 1 lần cho gene xuất hiện trong file này
            success_files += 1
        else:
            print(f"⚠️ Không tìm thấy cột 'Element symbol' trong {filepath}")
            # Hiển thị các cột có sẵn
            print(f"   Các cột có sẵn: {list(df.columns)}")
            failed_files += 1
            
    except Exception as e:
        print(f"❌ Lỗi đọc file {filepath}: {e}")
        failed_files += 1

print(f"✅ Đọc thành công {success_files} file, lỗi {failed_files} file")

if success_files == 0:
    print("⚠️ Không đọc được file nào thành công.")
    exit()

# Tính tỉ lệ phần trăm file có gene đó
gene_file_percentages = {gene: (count / success_files) * 100 for gene, count in gene_file_counter.items()}

print(f"Tổng số gene duy nhất tìm được: {len(gene_file_percentages)}")

df_plot = pd.DataFrame(list(gene_file_percentages.items()), columns=["Gene", "Percent of Strains"])
df_plot = df_plot.sort_values(by="Percent of Strains", ascending=False)

# Hiển thị top 10 gene phổ biến nhất
print("\nTop 10 gene phổ biến nhất:")
for i, (_, row) in enumerate(df_plot.head(10).iterrows(), 1):
    print(f"  {i}. {row['Gene']}: {row['Percent of Strains']:.1f}%")

# Lưu dữ liệu ra file CSV
csv_output = "amr_gene_file_frequency_plasmid.csv"
df_plot.to_csv(csv_output, index=False)
print(f"✅ Đã lưu bảng thống kê (tỉ lệ file có gene): {csv_output}")

# Vẽ biểu đồ
plt.figure(figsize=(24, 6))
plt.bar(df_plot["Gene"], df_plot["Percent of Strains"], color='skyblue')
plt.ylabel('Percent(%)')
plt.xlabel('Gene')
plt.title(f'Percent Antibiotics Resistance Gene in Plasmid (n={success_files} samples)')
plt.xticks(rotation=45, ha='right', fontsize=4)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Lưu biểu đồ
plot_output = "amr_gene_file_frequency_plasmid.png"
plt.savefig(plot_output, dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Đã lưu biểu đồ: {plot_output}")

print(f"\n🎉 Hoàn thành! Đã phân tích {success_files} file và tìm được {len(gene_file_percentages)} gene duy nhất.")