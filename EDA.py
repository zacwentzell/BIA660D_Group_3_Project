import csv
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

#Creting a list of all the movie genres and their count
ret_val = list()
with open('C:\\Users\\soura\\Downloads\\Clean Movie Data.csv', 'r', encoding='utf8') as f:
    m_obj = csv.DictReader(f)
    genre_list = list()
    for m in m_obj:
        g = list()

        genre_list.extend(m['genres'].split('|'))

        m['glist'] = m['genres'].split('|')
        m['gross'] = int(m['gross'])

        ret_val.append(dict(m))

    c_obj = Counter(genre_list)


d_dict = dict()
groups = list()
uk = list()

#Obtaining the genres for each director and the total gross under each director
for ret in ret_val:
    d_dict[ret['director_name']] = {'glist': list(), 'gross_sum': 0, 'director_name': ret['director_name']}

for ret in ret_val:
    d_dict[ret['director_name']]['glist'].extend(ret['glist'])
    d_dict[ret['director_name']]['gross_sum'] += ret['gross']

# This is what you want to see
#print(c_obj)
print(d_dict)

data = list()
for ret in ret_val:
    data.append(d_dict[ret['director_name']])
    #ret['glist'] = d_dict[ret['director_name']]['glist']

dt = pd.DataFrame(data)
#print(dt)
#dt.to_csv("directors.csv")
max_val= dt.loc[dt['gross_sum'].idxmax()]
print(max_val)

#plotting a graph for the genre and sum profit against each
genres= list(c_obj)
each_genre_sum = c_obj.values()
plt.bar(genres, each_genre_sum)
plt.xlabel("Genre")
plt.ylabel("Sum of each Genre")
plt.show()

#plottting the relation between the budget and gross
df= pd.read_csv('C:\\Users\\soura\\Downloads\\Clean Movie Data.csv')
gross= df['gross']
budget= df['budget']
plt.scatter(budget, gross)
plt.xlabel("Budget")
plt.ylabel("Gross")
plt.show()

#Plotting the total number of movies made each year in incresing order
df['title_year'].value_counts().plot(kind= 'barh')
plt.xlabel("Total movies")
plt.ylabel("Year")
plt.show()
print(df['title_year'].value_counts().head())

#plotting the relation between the voter users and the review users
voting_users= df['num_voted_users']
review_users= df['num_user_for_reviews']
plt.plot(voting_users, review_users)
plt.xlabel("rating users")
plt.ylabel("review users")
plt.show()