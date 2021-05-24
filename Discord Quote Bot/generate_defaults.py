import os

arr = os.listdir('Audio_recordings')
print(arr)

i = 1
while str(i) in arr:
    ass = os.listdir('Audio_recordings/' + str(i))
    print(str(i) + ': ' + str(ass))
    f = open('Audio_recordings/' + str(i) + '/record.txt', 'w')
    f.write('1')
    f.close()
    i += 1

