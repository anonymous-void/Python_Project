fp = open('test.txt', 'w')
for i in range(1, 100):
    print(i)
    fp.write(str(i))
    fp.write('\n')

fp.close()
