import numpy as np
import xml.etree.ElementTree as ET

tree = ET.parse('cer1.hoomdxml')
root = tree.getroot()
pos = np.fromstring(root[0][1].text, sep='\n').reshape((-1, 3))
pos /= 10
text = "\n"
for i in pos:
    text += "{0:.4f}\t{1:.4f}\t{2:.4f}\n".format(i[0], i[1], i[2])
root[0][1].text = text
tree.write('new.hoomdxml')
