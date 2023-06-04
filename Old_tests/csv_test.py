from lib.csv import CSV

header = ['test1', 'test2', 'test3']

data = [1, 2, 3]

data2 = [4, 5, 6, 7]

csv = CSV('test.csv', header)

csv.csv_write(data + data2)

csv.csv_write(data + data2)

csv.close()

print(type(data[0]), type(data), type([data+data2]))