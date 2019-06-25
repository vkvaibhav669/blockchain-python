# python 3 module
import barcode
import random

#n = random.randint(100000,999999)
n = random.randint(100000000000,999999999999)
N = str(n)
#barcode.PROVIDED_BARCODES
#print(H)
EAN = barcode.get_barcode_class('ean13') 
#ean  
#code = b(n)
#from barcode.writer import ImageWriter
ean = EAN(N)
#code = ean(N, writer=ImageWriter)
#code = ean(N)
bar_code = ean.save('asset_barcode')
#f = open('/asset_barcode.png')