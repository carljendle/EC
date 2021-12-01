#https://www.r-bloggers.com/2020/06/penguins-dataset-overview-iris-alternative-in-r/
#install.packages("remotes")
#remotes::install_github("allisonhorst/palmerpenguins")

#
library(tidyverse)
library(palmerpenguins)
library(psych)
library(gclus)
library(recipes)

#install.packages("GGally")

library("ggplot2")                     
library("GGally")

library(cluster)



######################
# Snabbanalys av datan
######################
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

print(summary(non_na_df))
print(describe(non_na_df))




######################
# Visualisering
######################

non_na_df %>%
  select(species, where(is.numeric)) %>% 
  GGally::ggpairs(aes(color = species),
                  columns = c("flipper_length_mm", "body_mass_g", 
                              "bill_length_mm", "bill_depth_mm")) +
  scale_colour_manual(values = c("darkorange","purple","cyan4")) +
  scale_fill_manual(values = c("darkorange","purple","cyan4"))


######################
# Principal Component Analysis
######################
penguin_recipe <-
  recipe(~., data = non_na_df) %>% 
  update_role(species, island, sex, new_role = "id") %>% 
  step_normalize(all_predictors()) %>%
  step_pca(all_predictors(), id = "pca") %>% 
  prep()

penguin_pca <- 
  penguin_recipe %>% 
  tidy(id = "pca") 

penguin_pca


non_na_df %>% 
  dplyr::select(where(is.numeric)) %>% 
  tidyr::drop_na() %>% 
  scale() %>% 
  prcomp() %>%  
  .$rotation



penguin_recipe %>% 
  tidy(id = "pca", type = "variance") %>% 
  dplyr::filter(terms == "percent variance") %>% 
  ggplot(aes(x = component, y = value)) + 
  geom_col(fill = "#b6dfe2") + 
  xlim(c(0, 5)) + 
  ylab("% of total variance")


##############################
#Klustring - innan normalisering
#############################

labels <- non_na_df$species

kmeans_data <- non_na_df %>% select(where(is.numeric))

min_val <- 2
max_val <- 10
results <- as.tibble(cbind("Measure" = 0, "Clusters" = 0))


for( i in min_val:max_val){
  kmeans_results <- kmeans(kmeans_data, centers = i, nstart = 20)
  
  measure <- kmeans_results$betweenss/kmeans.re$totss
  
  results <- rbind(results, list(measure, i))
  
}


print(kmeans_results)
#För att inspektera vad vi har i vår kmeans.re - använd str()
print(str(kmeans_results))

#Plocka bort startvärde för 0 kluster - inte superspännande!
results <- results[-1, ]
ggplot(data=results[-1, ], aes(x=Clusters, y=Measure)) +
  geom_line()+
  geom_point()




