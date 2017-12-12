import os
import re
import sre_constants
import sys

game_path = 'D:\Games\EU3遊牧風雲2.51——历史轨迹'
text_file_directory = os.path.join('history', 'provinces')
text_file_output = 'provinces_new'


replace_rules = {#'\n.*fort1.*\n': '\n',
                 '\n\n(?=\d{4}\.\d\.\d)': '\n\n1111.1.1 = { add_core = HRE controller = HRE owner = HRE }\n'
                 }
compiled_rules = {}
name_except = [1771, 266, 265, 267]
name_include = [str(x) for x in
                [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
                 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 128, 129, 130, 131, 132, 133, 134,
                 165, 166, 1757, 1758, 1759, 1760, 1761, 1762, 1763, 1769, 1770, 1771, 1772, 1775, 1857, 1858, 1863,
                 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1876, 1878, 1880, 1995, 1996, 1997] if
                x not in name_except]
print(name_include)

try:
    for rule in replace_rules.keys():
        compiled_rules.update({re.compile(rule): replace_rules.get(rule)})
except sre_constants.error as e:
    print('错误：正则表达式编译故障。')
    print(e)
    sys.exit(1)

try:
    os.mkdir(text_file_output)
except FileExistsError as e:
    print('警告：输出文件夹已经存在。')
    if input('输入 n 取消处理').upper() == 'N':
        sys.exit(1)

# print(*[str(x)+'\n' for x in compiled_rules.keys()])

files = [os.path.join(game_path, os.path.join(text_file_directory, d)) for d in
         os.listdir(os.path.join(game_path, text_file_directory))]
count, failed_count = 0, 0
for f in files:
    count += 1
    print('读取文件', count, '/', len(files), f)
    if os.path.isfile(os.path.abspath(f)):
        if f.endswith('.txt'):
            if os.path.split(f)[-1].split(' ')[0] in name_include:
                print('开始处理...')
                try:
                    with open(f, mode='r+') as f_in:
                        text = f_in.read()
                except UnicodeDecodeError as e:
                    failed_count += 1
                    print('沃日，出现了一个错误:', f)
                    print(e)
                    continue
                for regex in compiled_rules.keys():
                    text = regex.subn(compiled_rules.get(regex), text)[0]
                with open(os.path.join(text_file_output, os.path.split(f)[-1]), mode='w') as f_out:
                    f_out.write(text)

print('\n处理完毕。', count - failed_count, '已处理，', failed_count, '处理失败。')
