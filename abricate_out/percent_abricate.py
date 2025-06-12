import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Thư mục chứa các thư mục SRR con, trong đó có file _vfdb.csv
base_dir = "C:/Users/hoahoa/Documents/DSA_study/Thesis_project/abricate_out"

# Pattern để tìm file
pattern = os.path.join(base_dir, "**", "*_vfdb.csv")

print(f"Đang tìm kiếm với pattern: {pattern}")

# Tìm tất cả file vfdb.csv với tìm kiếm đệ quy
vfdb_files = glob.glob(pattern, recursive=True)
num_files = len(vfdb_files)
print(f"Đã tìm thấy {num_files} file vfdb.csv")

# Debug: Hiển thị danh sách file tìm được
if num_files > 0:
    print("Các file tìm được:")
    for i, filepath in enumerate(vfdb_files[:10], 1):  # Hiển thị 10 file đầu
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
            os.path.join(base_dir, "**", "vfdb.csv"),
            os.path.join(base_dir, "**", "*vfdb*"),
            os.path.join(base_dir, "*", "*_vfdb.csv"),
            os.path.join(base_dir, "*", "vfdb.csv")
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

# Define proper column names for abricate VFDB output
# Based on the error output, the columns appear to be:
column_names = [
    'FILE', 'SEQUENCE', 'START', 'END', 'STRAND', 'GENE', 
    'COVERAGE', 'COVERAGE_MAP', 'GAPS', 'PERCENT_COVERAGE', 
    'PERCENT_IDENTITY', 'DATABASE', 'ACCESSION', 'PRODUCT', 'RESISTANCE'
]

gene_file_counter = Counter()
success_files = 0
failed_files = 0

print(f"\nĐang xử lý {num_files} file...")

for i, filepath in enumerate(vfdb_files, 1):
    try:
        # Hiển thị tiến trình
        if i % 10 == 0 or i == num_files:
            print(f"  Đang xử lý file {i}/{num_files}...")
        
        # Read CSV with header, but handle the # symbol and separator detection properly
        # First, read the file and process the header line to detect separator
        with open(filepath, 'r') as f:
            first_line = f.readline().strip()
            
        # Detect separator by checking which one gives more columns
        separator = '\t'  # default
        if '\t' in first_line:
            separator = '\t'
        elif ',' in first_line:
            separator = ','
        else:
            # Try both and see which gives more columns
            try:
                df_tab = pd.read_csv(filepath, sep='\t', nrows=1)
                df_comma = pd.read_csv(filepath, sep=',', nrows=1)
                if len(df_comma.columns) > len(df_tab.columns):
                    separator = ','
            except:
                pass
                
        # Check if first line starts with # (header line)
        if first_line.startswith('#'):
            # Read with header, but skip the # symbol
            df = pd.read_csv(filepath, sep=separator, header=0, comment=None)
            # Clean the column names by removing the # symbol
            df.columns = [col.replace('#', '') for col in df.columns]
        else:
            # Read without header and assign column names
            df = pd.read_csv(filepath, sep=separator, header=None)
            df.columns = column_names[:len(df.columns)]
            
        # Debug: Check if we have proper column separation
        if len(df.columns) == 1 and ',' in df.columns[0]:
            # The single column contains comma-separated values, try splitting
            print(f"  🔄 Phát hiện columns không được tách đúng, thử lại với comma separator...")
            df = pd.read_csv(filepath, sep=',', header=0, comment=None)
            if first_line.startswith('#'):
                df.columns = [col.replace('#', '') for col in df.columns]
        
        if df.empty:
            print(f"⚠️ File rỗng: {filepath}")
            failed_files += 1
            continue
            
        if 'GENE' in df.columns:
            genes_in_file = set(df['GENE'].dropna().astype(str))
            # Filter out empty strings and very long strings
            genes_in_file = {gene.strip() for gene in genes_in_file if gene.strip() and len(gene.strip()) < 50}
            
            if genes_in_file:
                gene_file_counter.update(genes_in_file)
                success_files += 1
                print(f"  ✅ File {i}: Tìm được {len(genes_in_file)} gene: {list(genes_in_file)[:5]}...")
            else:
                failed_files += 1
                print(f"  ⚠️ File {i}: Không tìm được gene nào sau khi lọc")
        else:
            print(f"⚠️ File {i}: Không có cột GENE. Các cột có sẵn: {list(df.columns)}")
            failed_files += 1
            
    except pd.errors.EmptyDataError:
        print(f"⚠️ File {i}: File rỗng hoặc chỉ có comment - {os.path.basename(filepath)}")
        failed_files += 1
    except Exception as e:
        print(f"❌ Lỗi đọc file {filepath}: {e}")
        # If still having issues, try more aggressive parsing
        if len(df.columns) == 1 or 'GENE' not in df.columns:
            try:
                print(f"  🔄 Thử phương pháp parsing khác...")
                # Try reading as text and parsing manually
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                
                if len(lines) > 0:
                    header_line = lines[0].strip()
                    if header_line.startswith('#'):
                        header_line = header_line[1:]  # Remove #
                    
                    # Try different separators
                    for sep in ['\t', ',', ';', '|']:
                        headers = header_line.split(sep)
                        if 'GENE' in headers and len(headers) > 10:
                            print(f"  ✅ Tìm thấy separator phù hợp: '{sep}' với {len(headers)} cột")
                            df = pd.read_csv(filepath, sep=sep, header=0, comment=None)
                            if header_line.startswith('#'):
                                df.columns = [col.replace('#', '') for col in df.columns]
                            break
                    
                if 'GENE' not in df.columns:
                    print(f"  ❌ Vẫn không tìm được cột GENE sau khi thử tất cả separator")
                    failed_files += 1
                    continue
                    
            except Exception as parse_error:
                print(f"  ❌ Lỗi parsing thủ công: {parse_error}")
                failed_files += 1
                continue
            failed_files += 1

print(f"✅ Đọc thành công {success_files} file, lỗi {failed_files} file")

if success_files == 0:
    print("⚠️ Không đọc được file nào thành công.")
    print("💡 Gợi ý: Kiểm tra format của file CSV hoặc thử mở một file để xem cấu trúc")
    exit()

# Tính tỉ lệ phần trăm file có gene đó
gene_file_percentages = {gene: (count / success_files) * 100 for gene, count in gene_file_counter.items()}

print(f"Tổng số gene duy nhất tìm được: {len(gene_file_percentages)}")

if len(gene_file_percentages) == 0:
    print("⚠️ Không tìm được gene nào.")
    exit()

df_plot = pd.DataFrame(list(gene_file_percentages.items()), columns=["Gene", "Percent of Strains"])
df_plot = df_plot.sort_values(by="Percent of Strains", ascending=False)

# Hiển thị top 10 gene phổ biến nhất
print("\nTop 10 gene phổ biến nhất:")
for i, (_, row) in enumerate(df_plot.head(10).iterrows(), 1):
    print(f"  {i}. {row['Gene']}: {row['Percent of Strains']:.1f}%")

# Lưu dữ liệu ra file CSV
csv_output = "vfdb_gene_file_frequency.csv"
df_plot.to_csv(csv_output, index=False)
print(f"✅ Đã lưu bảng thống kê (tỉ lệ file có gene): {csv_output}")

# Vẽ biểu đồ cho top 20 gene
plt.figure(figsize=(24, 8))
top_genes = df_plot.head(100)
plt.bar(range(len(top_genes)), top_genes["Percent of Strains"], color='skyblue')
plt.xticks(range(len(top_genes)), top_genes["Gene"], rotation=45, ha='right')
plt.ylabel('Percent of Strains (%)')
plt.xlabel('Virulence Factor Genes')
plt.title('Top 100 Most Common Virulence Factor Genes')
plt.tight_layout()

# Lưu biểu đồ
plot_output = "vfdb_gene_frequency_plot.png"
plt.savefig(plot_output, dpi=300, bbox_inches='tight')
print(f"✅ Đã lưu biểu đồ: {plot_output}")

plt.show()

print(f"\n📊 Tóm tắt kết quả:")
print(f"  - Số file xử lý thành công: {success_files}")
print(f"  - Số gene duy nhất tìm được: {len(gene_file_percentages)}")
print(f"  - Gene phổ biến nhất: {df_plot.iloc[0]['Gene']} ({df_plot.iloc[0]['Percent of Strains']:.1f}%)")
print(f"  - File kết quả: {csv_output}")
print(f"  - Biểu đồ: {plot_output}")
