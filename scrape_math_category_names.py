from bs4 import BeautifulSoup
from pprint import pprint
import urllib.request
import urllib
import pandas as pd
import os

link_path = 'https://arxiv.org/archive/math'
link = urllib.request.urlopen(link_path).read()
soup = BeautifulSoup(link)

pprint(soup)

cat_dict = {}
for element in soup.findAll('li'):
    for cat in element.findAll('b'):
        category = cat.get_text()
        category = category.split(' - ')
        ## Ignore the first few elements which are not math categories
        if (len(category) == 2):
            cat_dict[category[0]] = category[1]

# os.chdir('/Users/jedchou/PycharmProjects/UIUC_math_network')
# df.to_csv('math_category_dictionary.csv',sep=',',index=False)


