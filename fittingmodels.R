library(tidyverse)
library(nnet)
library(VGAM)

dat = read_csv("createddata/2020s_points.csv")

common_scores = unique(dat$Pts)[1:18]
fit_data = dat %>% filter(Pts %in% common_scores,
                          First_Result != "None") %>%
  mutate(First_Result = as_factor(First_Result)) %>%
  select(Pts, Pt, First_Result)

fit = multinom(First_Result ~ Pts, fit_data)
fit = vglm(First_Result ~ Pts, fit_data, family = multinomial)



fit_data = dat %>% filter(Pts %in% common_scores) %>%
  mutate(isAce = (First_Result == "Ace"),
                          Pts = as_factor(Pts)) %>%
  select(Pts, Pt, isAce)


glm(isAce ~ Pt + Pts, fit_data, family = "binomial")



exp(0.44)
exp(0.0002538 )

