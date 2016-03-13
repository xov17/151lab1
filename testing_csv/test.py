import csv


a = [[1.2,'abc',3],[1.2,'werew',4]]
with open("output.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(a)