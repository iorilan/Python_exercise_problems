"""
Loop through all txt in folder A and output the content to file all.txt . saperate by dash 
split a large txt file into dir 5k lines per file 
"""
import os
import uuid
def merge_files(output_file, folder=None, files=None, prefix=True, suffix=True):
    def sort_files(x):
        return int(x.split('_')[0])

    if not files:
        files = [os.path.join(folder, f) for f in sorted(os.listdir(folder), key=sort_files)]

    with open(output_file, 'w') as of:
        for f in files:
            file_name=os.path.basename(f)
            #print(file_name)
            if prefix:
                of.write(f'++++++BEGIN OF [{file_name}]+++++\n')
            with open(f, 'r') as f:
                while True:
                    line = f.readline()
                    if line == '':
                        break
                    of.write(line)
            if suffix:
                of.write(f'++++++END OF [{file_name}]+++++\n')

def split_files(input_file, output_dir, lines_per_file=100):
    file_name = os.path.basename(input_file)
    idx=0
    os.makedirs(output_dir, exist_ok=True)
    stop=False
    with open(input_file, 'r') as f :
        while not stop:
            output_file = os.path.join(output_dir, f'{idx}_{file_name}')
            empty_output = True
            with open(output_file, 'w') as f2:
                for i in range(0, lines_per_file):
                    line = f.readline()
                    if line == '':
                        stop = True
                        if empty_output:
                            os.remove(output_file)
                        break
                    f2.write(line)
                    empty_output = False
            idx+=lines_per_file

def generate_test_file(output_file, lines):
    with open(output_file, 'w') as f:
        for i in range(0, lines-1):
            f.write(f'{uuid.uuid4()}\n')

def cleanup():
    for dir, _, files in os.walk('test_split'):
        try:
            for f in files:
                os.remove(os.path.join(dir, f))
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    generate_test_file("test_split\\1.txt", 5000)
    #split_files('test_split\\1.txt', 'test_split\\splited', 100)
    #merge_files('test_split\\merged.txt', folder='test_split\\splited', prefix=False)

    #cleanup() 
    
