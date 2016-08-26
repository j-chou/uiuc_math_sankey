## UIUC network
require(reshape2)
require(plyr)
require(dplyr)
require(ggplot2)
require(scales)

prof_table <- read.csv('~/PycharmProjects/UIUC_math_network/UIUC_math_network.csv')

prof_table <- ddply(prof_table,.(name,category),nrow)
prof_table <- ddply(prof_table,
                    .(variable),
                    transform,
                    rescale = rescale(value))

prof_list <- 
for (i in 1:nrow(prof_table)){
  
}


names(prof_table) <- c('name','variable','value')

ggplot(prof_table,aes(variable,name))+
  geom_tile(aes(fill = rescale),colour = "white")+
  scale_fill_gradient(low = "white",high="blue")+
  labs(x='',y='Name')



