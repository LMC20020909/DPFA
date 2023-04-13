library("RMySQL")
library("ggplot2")
library("dplyr")
library('tidyverse')
library('igraph')
library('Matrix')

source('./R/functions/similarityFunctions.R')
source('./R/functions/importDataFunctions.R')
source('./R/functions/networkFunctions.R')

conn <- dbConnect(MySQL(),
                  user="root",
                  password="20020909LMC",
                  host="localhost",
                  port=3306,
                  dbname="free association")
# associate_strength = './output/similarity/SWOW-associative strength.csv'
# score = read.csv(associate_strength)
# score = as.matrix(score)
alpha = 0.75
dataFile.SWOWEN     = './data/2018/processed/SWOW-EN.R100.csv'
SWOW.R123             = importDataSWOW(dataFile.SWOWEN,'R123') %>% arrange(cue, response)
G = constructSimilarityMatrix(SWOW.R123, 'PPMI')
num = data.frame(index=1:1000)
word = "computer"
data = dbGetQuery(conn, sprintf("SELECT * FROM nearby WHERE word = '%s';", word))
data = cbind(data, num)
colnames(data) = c("WordA", "WordB", "similarity", "index")
s = lookupSimilarityMatrix(G, data)
s =  as.data.frame(s)
data = cbind(data, s)
data = filter(data, complete.cases(s))
colnames(data) = c("WordA", "WordB", "word2vec", "percentile", "PPMI")
data$diff <- abs(data$word2vec - data$PPMI)
data = arrange(data, diff)
title = sprintf("pointwise mutual information (%s)", word)
fig_data = gather(data, method, similarity, word2vec, PPMI)
# fig_data = filter(fig_data, similarity < 0.99)
ggplot(fig_data, aes(x = percentile, y = similarity, colour = method)) + 
  geom_point() + geom_smooth() +
  labs(title = title)
  # geom_smooth(aes(y=similarity)) + 
  # geom_smooth(aes(y=s), color = "black") +
  # guides(size = guide_legend(), shape = guide_legend())
