"""
count how many lines of python code for a repo 
"""
import os
import subprocess

def line_count_linux(filename):
    return int(subprocess.check_output(['wc', '-l', filename]).split()[0])

def line_count_windows(filename):
    with open(filename, 'r', encoding='utf8') as f :
        n= len(f.readlines())
    return n

def stat_repo(folder, ext='.*'):
    stat_files = {}
    for dir, _, files in os.walk(folder):
        matched_files = [f for f in files if os.path.splitext(f)[1] == ext or ext == '.*']
        for f in matched_files:
            file_path = os.path.join(dir, f)
            stat_files[file_path] = {
                'rows' : line_count_windows(file_path),  #line_count_linux (file_path)
                'stat': os.stat(file_path)
            }
    print_file_info(stat_files)

def print_file_info(files):
    total_rows = 0
    for file_path, info in files.items():
        row_count , stat = info['rows'], info['stat']
        total_rows += row_count
        #print(f'---{file_path} --- {row_count} rows , {stat}')
    print(f'total files : {len(files)} , rows : {total_rows}')


if __name__ == "__main__":
    stat_repo('C:\\NewStart\\Java', '.java')
