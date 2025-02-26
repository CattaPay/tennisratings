library(tidyverse)
library(nnet)
library(VGAM)


dat = read_csv("createddata/2020s_points.csv")

common_scores = unique(dat$Pts)[1:18]
fit_data = dat %>% filter(Pts %in% common_scores,
                          First_Result != "None") %>%
  mutate(First_Result = as_factor(First_Result)) %>%
  select(Pts, Pt, First_Result)

## multinomial regression ##

fit = multinom(First_Result ~ Pts, fit_data)
fit = vglm(First_Result ~ Pts, fit_data, family = multinomial)

fit$fitted.values

fit_data = dat %>% filter(Pts %in% common_scores) %>%
  mutate(isAce = (First_Result == "Ace"),
                          Pts = as_factor(Pts)) %>%
  select(Pts, Pt, isAce)


glm(isAce ~ Pt + Pts, fit_data, family = "binomial")

# naive Bayes
library(e1071)
nb_model = naiveBayes(First_Result ~ Pts + Pt, data = fit_data)
nb_model$tables

?naiveBayes
predictions <- predict(nb_model, fit_data, type = "raw")

conf_matrix <- table(Predicted = predictions, Actual = fit_data$First_Result)
print(conf_matrix)

# Accuracy
accuracy <- sum(diag(conf_matrix)) / sum(conf_matrix)
print(paste("Accuracy:", round(accuracy, 3)))


