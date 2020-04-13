import os
from nltk.tokenize import sent_tokenize

data_path = 'data'
dirs = os.listdir(data_path)

for file in dirs:
    inp = 'content.txt'
    with open(os.path.join(data_path, file, inp), 'r', encoding="utf-8") as f:
        lines = '\n' . join(line.strip(' \t\n\r') for line in f.readlines())
    lines = sent_tokenize(lines)
    lines = [sentence for line in lines for sentence in line.split('\n')]

    out = 'info.txt'
    with open(os.path.join(data_path, file, out), 'w', encoding="utf-8") as f:
        line_no = -1
        for line in lines:
            line = ('Link: ' if (line_no < 0) else '{:03d}.wav\n'.format(line_no)) + line
            f.write(line + '\n')
            line_no += 1