import numpy
import requests
import os
import csv
from scipy import special, constants
from numpy import arange, abs, sum
from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET
import xml.dom.minidom


# читаем CSV файл
data = requests.get('https://jenyay.net/uploads/Student/Modelling/task_02.csv')

ffile = []

with open('task_02.csv', 'wb') as file:
    file.write(data.content)

with open('task_02.csv') as File:
    reader = csv.reader(File, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        ffile.append(row)


variant = 15
D = float(ffile[variant][1])
f_min = float(ffile[variant][2])
f_max = float(ffile[variant][3])

# задаем константы для рассчетов
n_end = 10
f_step = 100000
r = D / 2
f_arange = arange(f_min, f_max, f_step)
wavelength_arange = constants.c / f_arange
k_arange = 2 * constants.pi / wavelength_arange


# h
def f4(n, x):
    return special.spherical_jn(n, x) + 1j * special.spherical_yn(n, x)


# b
def f3(n, x):
    return (x * special.spherical_jn(n - 1, x) - n * special.spherical_jn(n, x)) / (x * f4(n - 1, x) - n * f4(n, x))


# a
def f2(n, x):
    return special.spherical_jn(n, x) / f4(n, x)


# ЭПР
rcs_arange = (wavelength_arange ** 2) / numpy.pi * (abs(sum([((-1) ** n) * (n+0.5) * (f3(n, k_arange * r) - f2(n, k_arange * r)) for n in range(1, n_end)], axis=0)) ** 2)

if not os.path.isdir('result'):
    os.mkdir('result')
else:
    print('Уже есть такая директрория')

counter = 0

root = ET.Element("data")


for f, lambda1, rcs in zip(f_arange, wavelength_arange, rcs_arange):
    rows = ET.SubElement(root, "row")

    ET.SubElement(rows, "f").text = str(f) + ' Гц'
    ET.SubElement(rows, "lambda").text = str(lambda1) + ' м'
    ET.SubElement(rows, "rcs").text = str(rcs) + ' м^2'

tree = ET.ElementTree(root)

xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")
dom = xml.dom.minidom.parseString(xml_string)
formatted_xml = dom.toprettyxml(indent="  ")

with open('result/data.xml', 'w') as file:

    file.write(formatted_xml)


# Строим график
plt.plot(f_arange, rcs_arange)
plt.show()

