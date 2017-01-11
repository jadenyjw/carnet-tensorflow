import os

f = open('train_data.txt', 'a')
c = open('cval_data.txt', 'a')


for (path, dirnames, filenames) in os.walk('data/forward'):
    i = 0.7 * len(filenames)
    for name in filenames[:int(i)]:
        f.write(os.path.join(path, name) + ' 0\n')
    for name in filenames[int(i):]:
        c.write(os.path.join(path, name) + ' 0\n')
for (path, dirnames, filenames) in os.walk('data/left'):
    i = 0.7 * len(filenames)
    for name in filenames[:int(i)]:
        f.write(os.path.join(path, name) + ' 1\n')
    for name in filenames[int(i):]:
        c.write(os.path.join(path, name) + ' 1\n')
for (path, dirnames, filenames) in os.walk('data/right'):
    i = 0.7 * len(filenames)
    for name in filenames[:int(i)]:
        f.write(os.path.join(path, name) + ' 2\n')
    for name in filenames[int(i):]:
        c.write(os.path.join(path, name) + ' 2\n')
