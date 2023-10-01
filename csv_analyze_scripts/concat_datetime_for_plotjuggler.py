import os
import sys

# 時間が飛んでいる行を探し出し、その次に一行空白を挿入する事で、データを時間ごとに分割する。
# コマンドライン引数が無ければina.csvを読み込んで、output.csvに出力する。ある場合は渡したものを読み込む。


output_file_path = "data_concat.csv"
default_input_file_path = "ina.csv"

# 時間が飛んでいる行を探し、その次に一行空白行を挿入する
def divideDataBytime(target_filename) :
    fd = open(target_filename,'r')
    lines = fd.readlines()
    prev_time = 0
    line_num = 0
    output_lines = []
    for line in lines:
        data = line.split(',')
        if 'timestamp_date' in line:
            output_line = 'timestamp'  #headerの場合はtimestampの名前を統合する
        else:
            output_line = data[0] + '/' +  data[1] #dateとtimeを結合
            output_line = output_line[:-3]
        for itm in data[3:]:    #dtを削除
            output_line += ',' + itm
        output_lines.append(output_line)
    fd.close()
    out_fd = open(output_file_path,'w')
    out_fd.writelines(output_lines)
    out_fd.close()


if __name__ == '__main__':
    file_path = default_input_file_path
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    divideDataBytime(file_path)