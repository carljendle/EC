#https://www.r-bloggers.com/2020/06/penguins-dataset-overview-iris-alternative-in-r/
#install.packages("remotes")
#remotes::install_github("allisonhorst/palmerpenguins")

#
library(tidyverse)
library(palmerpenguins)

print(names(penguins))

df <- as.tibble(penguins)

print(head(df))

#Ger binär representation av dataframen med TRUE där vi har NA
print(any(is.na(df)))
#Kan också slicea istället för att använda head
nr_of_rows <- 6
binary_df <- is.na(df)
print(sum(binary_df))
print(rowSums(binary_df))

print(binary_df[1:nr_of_rows, 1:length(names(penguins))])



non_na_df <- na.omit(df)

#Har vi verkligen hanterat alla NA-värden?
print(any(is.na(non_na_df)))

#Ja!



