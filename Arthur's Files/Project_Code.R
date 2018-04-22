
library(MASS)

#Data retrieved 
MovieData = read.csv("C:/Users/Class2018/Desktop/BIA 660/Movie Data.csv", header = TRUE)
MovieData
#Dependent Variable
Revenue = MovieData$gross

#Independent Variables
Critics = MovieData$X.critics
Length = MovieData$time
FBlikes_director = MovieData$director.fb.like
FBlikes_actor3 = MovieData$actor_3_facebook_likes
FBlikes_actor2 = MovieData$actor_2_facebook_likes
FBlikes_actor1 = MovieData$actor_1_facebook_likes
FBlikes_cast = MovieData$cast_total_facebook_likes
FBlikes_movie = MovieData$movie_facebook_likes
Score = MovieData$imdb_score
Voted_Users = MovieData$num_voted_users
Year = MovieData$title_year
Screen = MovieData$aspect_ratio

#Aggregating the independent variables
numeric_data = data.frame(Length, Critics, FBlikes_director, FBlikes_actor3, FBlikes_actor2, FBlikes_actor1, FBlikes_cast, FBlikes_movie, Score, Voted_Users, Year, Screen)

#Dimension Reduction - Principal Component Analysis (PCA)
PCA = prcomp(numeric_data, center = TRUE, scale. = TRUE)
summary = summary(PCA)
summary

PCA_df = data.frame(t(summary$importance))
barplot(PCA_df$Proportion.of.Variance, main = "Proportion of Variance of PCA", xlab = "Components", ylab = "Proportion of Variance", xlim = c(0,15), ylim = c(0,0.3))
barplot(PCA_df$Cumulative.Proportion, main = "Cumulative Proportion of Variance of PCA", xlab = "Components", ylab = "Cumulative Variance")

#Logistic Regression
Reg = glm(Revenue ~ Length, data = numeric_data)
summary(plot(x = Revenue, y = Length))
?abline

PCA_Regression = glm(Revenue ~ Critics + Length + FBlikes_director + FBlikes_actor3 + FBlikes_actor2 + FBlikes_actor1 + FBlikes_cast + FBlikes_movie, data = numeric_data)
summary(PCA_Regression)
plot(PCA_Regression)

#Anova
PCA_anova = aov(Revenue ~ Critics + Length + FBlikes_director + FBlikes_actor3 + FBlikes_actor2 + FBlikes_actor1 + FBlikes_cast + FBlikes_movie, data = numeric_data)
summary(PCA_anova)
plot(PCA_anova$residuals, main = "Residual Plot of ANOVA")

#Stepwise Regression
PCA_stepwise = lm(Revenue ~ Critics + Length + FBlikes_director + FBlikes_actor3 + FBlikes_actor2 + FBlikes_actor1 + FBlikes_cast + FBlikes_movie, data = numeric_data)
step = stepAIC(PCA_stepwise)
step$anova
summary(step)

#Random Forest
library(randomForest)
rf = randomForest(Revenue ~ ., data = numeric_data, ntree=100, mtry=2, importance=TRUE)
rf
varImpPlot(rf)
plot(rf, type="simple")
