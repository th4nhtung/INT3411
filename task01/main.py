import os
from nltk.tokenize import sent_tokenize

data_path = 'audio'
dirs = os.listdir(data_path)

for file in dirs:
    inp_path = file + '.txt'
    with open(os.path.join(data_path, file, inp_path), 'r') as f:
        lines = ' '.join(f.readlines())
    lines = sent_tokenize(lines)

    out_path = file + 'out.txt'
    with open(os.path.join(data_path, file, out_path), 'w') as f:
        for line in lines:
            f.write(line + '\n')