import os 
import sys
import csv

output_file_path = "ina_data_for_excel.csv"
default_input_file_path = "ina.csv"

#usage : python3 data_analyze_and_process_for_excel.py [対象のファイル名] 対象ファイル名を指定しない場合は"ina.csv"を読み込む

# 各データの最小と最大値を求めて、execel用に時間の小数点以下を3桁にする
def divideDataBytime(target_filename) :
    fd = open(target_filename,'r')
    lines = fd.readlines()
    prev_time = 0
    line_num = 0
    output_lines = []
    output_lines.append(lines[0].replace('\n',''))
    column_name_line = output_lines[0]
    item_names = column_name_line.split(',')[3:]
    list_of_max = [0 for _ in range(len(item_names))]
    list_of_min = [0 for _ in range(len(item_names))]
    number_of_files = 1
    is_first_line = True
    target_lines = lines[1:]
    output_filenames = []
    for line in target_lines:
        row_data = line.split(',')[3:]
        index = 0
        for itm in row_data:
            if int(itm) > list_of_max[index]:
                list_of_max[index] = int(itm)
            if int(itm) < list_of_min[index] or list_of_min[index] == 0:
                list_of_min[index] = int(itm) 
            index += 1
        time_seconds = line.split(',')[1].split('.')
        # print(time_seconds)
        output_line = line.split(',')[0] + ',' + time_seconds[0]  +  '.' + time_seconds[1][:3] + ',' + line.split(',')[2] + ',' + ','.join(row_data)
        output_lines.append(output_line)
        if int(line.split(',')[2]) == 0:
            if is_first_line:
                is_first_line = False
                continue
            print("Data Bordarline is :: ",row_data)
            output_lines.insert(0,column_name_line)
            output_lines[0] = output_lines[0] + '\n'
            out_fd = open(output_file_path.split('.')[0] + '_' + str(number_of_files) + '.' + output_file_path.split('.')[1],'w')
            out_fd.writelines(output_lines[:-1])
            output_filenames.append(out_fd.name)
            out_fd.close()
            number_of_files += 1
            output_lines = list(output_lines[-1])
            # print(output_lines)
    if len(output_lines) > 1:
        output_lines.insert(0,column_name_line)
        output_lines[0] = output_lines[0] + '\n'
        out_fd = open(output_file_path.split('.')[0] + '_' + str(number_of_files) + '.' + output_file_path.split('.')[1],'w')
        out_fd.writelines(output_lines)
        output_filenames.append(out_fd.name)
        out_fd.close()
    for i in range(len(item_names)):
        print('{:25s} , Max = {:8d} , Min = {:8d}'.format(item_names[i],list_of_max[i],list_of_min[i]))
    return output_filenames

if __name__ == '__main__':
    file_path = default_input_file_path
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    output_file_names = divideDataBytime(file_path)
    print("\n\n*** Write data to [ ",output_file_names,"] ***")