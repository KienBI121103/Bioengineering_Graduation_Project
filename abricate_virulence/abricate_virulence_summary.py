import os
import pandas as pd
import argparse

# Step 1: Define argument parser
parser = argparse.ArgumentParser(description="Tạo ma trận sự hiện diện/không hiện diện của gen độc lực từ các file CSV.")
parser.add_argument("input_path", type=str, help="Đường dẫn đến thư mục chứa các file CSV")
parser.add_argument("output_path", type=str, help="Đường dẫn file CSV output (bao gồm tên file và .csv)")
args = parser.parse_args()

# Check if input folder exists
if not os.path.exists(args.input_path):
    print(f"Lỗi: Thư mục input '{args.input_path}' không tồn tại.")
    exit(1)

if not os.path.isdir(args.input_path):
    print(f"Lỗi: '{args.input_path}' không phải là thư mục.")
    exit(1)

# Check if output directory exists, create if not
output_dir = os.path.dirname(args.output_path)
if output_dir and not os.path.exists(output_dir):
    try:
        os.makedirs(output_dir)
        print(f"Đã tạo thư mục output: {output_dir}")
    except Exception as e:
        print(f"Lỗi khi tạo thư mục output: {e}")
        exit(1)

# Ensure output file has .csv extension
if not args.output_path.lower().endswith('.csv'):
    args.output_path += '.csv'

print(f"Input path: {args.input_path}")
print(f"Output path: {args.output_path}")

# Step 2: Trích xuất tên gen từ tất cả các file
all_gene_names = set()  # Lưu trữ tất cả các gen độc lực
file_gene_mapping = {}  # Ánh xạ giữa tên file và danh sách gen

# Duyệt qua tất cả các file trong thư mục
csv_files_found = False
for filename in os.listdir(args.input_path):
    if filename.endswith(".csv"):  # Chỉ xử lý các file có đuôi .csv
        csv_files_found = True
        file_path = os.path.join(args.input_path, filename)
        
        try:
            df = pd.read_csv(file_path)  # Đọc file CSV
            
            # Kiểm tra xem cột 'GENE' có tồn tại không
            if 'GENE' not in df.columns:
                print(f"Cảnh báo: File '{filename}' không có cột 'GENE'. Bỏ qua file này.")
                continue
            
            # Trích xuất tên gen từ cột 'GENE' và loại bỏ NaN
            gene_names = df['GENE'].dropna().astype(str).tolist()
            gene_names = [gene.strip() for gene in gene_names if gene.strip()]  # Loại bỏ chuỗi rỗng
            
            if gene_names:  # Chỉ xử lý nếu có gen
                all_gene_names.update(gene_names)  # Thêm vào tập hợp tất cả gen
                file_gene_mapping[filename] = set(gene_names)  # Lưu ánh xạ
                print(f"Đã xử lý '{filename}': {len(gene_names)} gen")
            else:
                print(f"Cảnh báo: File '{filename}' không có gen hợp lệ.")
                
        except Exception as e:
            print(f"Lỗi khi đọc file '{filename}': {e}")

if not csv_files_found:
    print("Không tìm thấy file CSV nào trong thư mục input.")
    exit(1)

if not file_gene_mapping:
    print("Không có file nào được xử lý thành công.")
    exit(1)

# Step 3: Tạo ma trận sự hiện diện/không hiện diện
all_gene_names = sorted(all_gene_names)  # Sắp xếp tên gen
file_names = sorted(file_gene_mapping.keys())  # Sắp xếp tên file

print(f"Tạo ma trận với {len(file_names)} file và {len(all_gene_names)} gen...")

# Khởi tạo DataFrame với giá trị 0
presence_matrix = pd.DataFrame(0, index=file_names, columns=all_gene_names, dtype=int)

# Điền giá trị vào DataFrame
for file_name, genes in file_gene_mapping.items():
    for gene in genes:
        presence_matrix.at[file_name, gene] = 1

# Step 4: Xuất ra file CSV
try:
    presence_matrix.to_csv(args.output_path)
    print(f"File CSV '{args.output_path}' đã được tạo thành công.")
    print(f"Kích thước ma trận: {presence_matrix.shape[0]} file x {presence_matrix.shape[1]} gen")
    
    # Hiển thị thống kê tóm tắt
    if not presence_matrix.empty:
        total_genes_per_file = presence_matrix.sum(axis=1)
        total_files_per_gene = presence_matrix.sum(axis=0)
        
        print(f"Số gen trung bình mỗi file: {total_genes_per_file.mean():.1f}")
        print(f"File có nhiều gen nhất: {total_genes_per_file.max()} gen ({total_genes_per_file.idxmax()})")
        print(f"File có ít gen nhất: {total_genes_per_file.min()} gen ({total_genes_per_file.idxmin()})")
        
except Exception as e:
    print(f"Lỗi khi ghi file output: {e}")
    exit(1)