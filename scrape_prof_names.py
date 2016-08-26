from bs4 import BeautifulSoup
from pprint import pprint
import urllib.request
import urllib
import pandas as pd
import os

## Get UIUC math prof names from UIUC website
link_path = 'http://www.math.illinois.edu/People/faculty.html'
link = urllib.request.urlopen(link_path).read()
soup = BeautifulSoup(link)

prof_names = []
for element in soup.findAll('table')[0].findAll('a'):
    if (element.get_text() != ''):
        prof_names.append(element.get_text())
#
# prof_names = [x.replace('.','').replace('-','_').replace('\'','') for x in prof_names]
# prof_names = [' '.join(x.split()) for x in prof_names]
# prof_names_query_format = [x.replace(', ','_').replace(' ','_') for x in prof_names]
# #prof_names_query_format = [prof.split(', ')[0]+'_'+prof.split(', ')[1].split()[0][0] for prof in prof_names]
#
# file_name = open('/Users/jedchou/PycharmProjects/UIUC_math_network/prof_names_query.txt','w')
# for item in prof_names_query_format:
#     file_name.write('\'%s\',\n' % item)
prof_names_query_format = []
with open('/Users/jedchou/PycharmProjects/UIUC_math_network/prof_names_query.txt','r') as file:
    for line in file:
        prof_names_query_format.append(line.replace('\n',''))

## Create dictionary of professor names
keys = prof_names_query_format
values = prof_names
prof_names_dict = dict(zip(keys,values))

## Dataframe storing prof names, coauthors, and
df_header = ['name','authors','category']
df = pd.DataFrame([],df_header)

## For each UIUC math prof, search for all arxiv papers and
## get paper category, co-authors
for prof in prof_names_query_format:
    url = 'http://export.arxiv.org/api/query?search_query=au:'+prof+'&start=0&max_results=200'
    data = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(data,'lxml')

    num_papers = len(soup.findAll('entry'))

    author_list = ['']*num_papers
    category_list = ['']*num_papers
    index = 0
    for entry in soup.findAll('entry'):

        # title = entry.findAll()

        ## Get all authors on paper
        authors = [name.get_text() for name in entry.findAll('name')]
        authors = ';'.join(authors)

        ## Get paper category
        category = entry.findAll('arxiv:primary_category')[0]['term']

        author_list[index] = authors
        category_list[index] = category

        index += 1

    ## Append papers for this prof to df
    df = df.append(pd.DataFrame({'name':[prof]*num_papers,
                                 'authors':author_list,
                                 'category':category_list}))

## Get dictionary of arxiv math categories
link_path = 'https://arxiv.org/archive/math'
link = urllib.request.urlopen(link_path).read()
soup = BeautifulSoup(link)

# pprint(soup)

cat_dict = {}
for element in soup.findAll('li'):
    for cat in element.findAll('b'):
        category = cat.get_text()
        category = category.split(' - ')
        ## Ignore the first few elements which are not math categories
        if (len(category) == 2):
            cat_dict[category[0]] = category[1]

## Convert abbreviated category names to full names
full_cat_names = [cat_dict[str(x)] if str(x) in cat_dict else 'Non-Math' for x in df.category]
df.category = full_cat_names

## CHECK WHY JAMES PASCALEFF CLASSIFIED AS NON-MATH!!!
## GET BETTER D3 COLORSCHEME

df_table = pd.DataFrame(df.groupby(['name','category']).agg(['count']))
df_table = df_table.reset_index()

## Convert abbreviated prof names to full names
df_table.name = [prof_names_dict[x] if x in prof_names_dict else x for x in df_table.name]

num_profs = len(prof_names)
prof_list = [0]*df_table.shape[0]

for index,row in df_table.iterrows():
    prof_list[index] = [str(row['name'].item()), str(row['category'].item()), int(row['authors'])]

file_name = open('/Users/jedchou/PycharmProjects/UIUC_math_network/test_prof_list.txt','w')
for item in prof_list:
    file_name.write('%s,\n' % item)

os.chdir('/Users/jedchou/PycharmProjects/UIUC_math_network')
df.to_csv('test_UIUC_math_network.csv',sep=',',index=False)
df_table.to_csv('prof_table_by_group_count.csv',sep=',',index=False)
