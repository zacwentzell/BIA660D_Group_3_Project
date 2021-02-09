import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from scipy.stats import spearmanr, pearsonr

df= pd.read_csv("C:\\Users\\soura\\Downloads\\Clean Movie Data.csv")
#print(df.head())

x1= df['critics']
x2= df['gross']
x3= df['budget']
x4= df['imdb_score']
x5= df['num_user_for_reviews']
x6= df['num_voted_users']

d= [x1, x3, x4, x5, x6]
data1= pd.DataFrame(data= d)
data2=data1.transpose()
print(data2.head())

#splitting data into training and test
y= x2
X_train, X_test, y_train, y_test = train_test_split(data2, y, test_size=0.2)
print ("X train shape=",X_train.shape)
print("Y train shape= ", y_train.shape)
print ("X test shape=", X_test.shape)
print("Y test shape=", y_test.shape)

#Random Forest Regression using sklearn.enseble
model = RandomForestRegressor(random_state=0)
fit= model.fit(X_train, y_train)
print(fit)
score= model.score(X_test, y_test)
print(score)
predicted_train = model.predict(X_train)
predicted_test = model.predict(X_test)

#Statistical evaluation of the model
test_score = r2_score(y_test, predicted_test)
mean_square_error= mean_squared_error(y_test, predicted_test)
spearman = spearmanr(y_test, predicted_test)
pearson = pearsonr(y_test, predicted_test)

print(f'Test data R-2 score: {test_score:>5.3}')
print(f'Test data Spearman correlation: {spearman[0]:.3}')
print(f'Test data Pearson correlation: {pearson[0]:.3}')

plt.scatter(y_test, predicted_test)
plt.xlabel('observed')
plt.ylabel('predicted')
plt.title("RandomForest Regression with scikit-learn")
plt.show()

#Coefficient relation
feature_import = pd.DataFrame(data=model.feature_importances_, columns=['values'])
feature_import.sort_values(['values'], ascending=False, inplace=True)
print(feature_import.transpose())

feature_import.reset_index(level=0, inplace=True)
sns.barplot(x='index', y='values', data=feature_import, palette='deep')
plt.xlabel("index feature")
plt.ylabel("Value")
plt.show()