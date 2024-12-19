import os
import pandas as pd
import shutil

raw_path = "processed/raw"
cal_path = "processed/cal"
directories = [raw_path, cal_path]

for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)


# 查詢目錄下的所有 CSV 檔案
csv_files = [file for file in os.listdir("./") if file.endswith(".csv")]

# 列出篩選結果
for file in csv_files:

    print(f'processing: {file}')

    df = pd.read_csv(file)

    column_data = df.iloc[:, 3]

    result = {
        '平均值': column_data.mean(),
        '中位數': column_data.median(),
        '90th Percentile': column_data.quantile(0.90),
        '95th Percentile': column_data.quantile(0.95),
        'Min': column_data.min(),
        'Max': column_data.max()
    }

    result_df = pd.DataFrame(result, index=[0])
    new_csv_file = f'{cal_path}/{file}'
    result_df.to_csv(new_csv_file, index=False)

    shutil.move(file, f'{raw_path}/{file}')



