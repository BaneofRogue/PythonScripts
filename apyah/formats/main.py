from machine.util import *

cleaner = Cleaner('investing.json', 'investing')
cleaner.load()

organized_data = cleaner.organize("data.json")

parser = Parser('data.json')
parser.load()

data = parser.generate_candles()

for index in range(1, 20):
    print(data[index])