library('Matrix')
library('tictoc')
library('tidyverse')
library('igraph')
library("ggplot2")
library("dplyr")
library("RMySQL")


source('./R/functions/importDataFunctions.R')
source('./R/functions/networkFunctions.R')
source('./R/functions/similarityFunctions.R')

conn <- dbConnect(MySQL(),
                  user="root",
                  password="20020909LMC",
                  host="localhost",
                  port=3306,
                  dbname="free association")

# Load the data 
dataFile.SWOWEN     = './data/2018/processed/SWOW-EN.R100.csv'
SWOW.R123             = importDataSWOW(dataFile.SWOWEN,'R123') %>% arrange(cue, response)
# Edges = computeEdgeTable(SWOW.R123) %>% select(source, target) 

G = constructSimilarityMatrix(SWOW.R123, 'PPMI')

data = read.csv("F://project/free association/results-R123-0.5-0.95.csv")
colnames(data) = c("WordA", "WordB", "similarity", "p")


v = lookupSimilarityMatrix(S, data)
v = as.data.frame(v)

corr = data %>% select(similarity) %>% cbind(v)
ggplot(corr, aes(similarity, v)) + geom_point() + geom_smooth()
ggplot(corr, aes(x = v)) + geom_histogram(bins = 10, color = '#88ada6', fill = '#fffbf0', alpha = .25, center = 0)

