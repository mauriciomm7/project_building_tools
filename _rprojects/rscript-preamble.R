library(quanteda)
library(eurlex)
library(ggplot2)
library(forcats)
library(marginaleffects)
library(modelsummary)
library(tinytable)
library(stargazer)
library(tidyverse)
library(tidyr)
library(lubridate)
library(stringr)
library(janitor)
library(dplyr)
library(rvest)
library(readr)
library(haven)
library(sf)
library(sandwich)
library(MASS)
library(conflicted)
conflict_prefer("select", "dplyr")
conflict_prefer("filter", "dplyr")
conflicts_prefer(dplyr::select, dplyr::filter)

sapply(X = c("dplyr", "tidyr", "rvest", "purrr", "stringr", "zoo", "ggplot2", "janitor"),
       FUN = library,
       character.only = TRUE)

sapply(X = c("dplyr",  "readr", "haven", "sf", "ggplot2", "stringr", "tinytable", "tidyr",
             "modelsummary", "sandwich", "MASS", "marginaleffects", "conflicted"),
       FUN = library,
       character.only = TRUE)
