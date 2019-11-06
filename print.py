import os
f = open('tzt.txt', 'a')

for a in range(100):
    text = 'hell'
    text2 = text.encode('utf-8')
    f.write(str(text2) + os.linesep)