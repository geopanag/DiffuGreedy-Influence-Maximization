library(ggplot2)
library(reshape2)

setwd("path/to/Data/to_plot")

df  = data.frame(matrix(ncol=10,nrow=0))

nam = c()
for(f in dir(pattern  = "spreading*")){
  dat = read.csv(f)
  dat = dat[order(dat[,2]),]
  df = rbind(df,dat[,1])
  nam = c(nam,f)
}

names(df) = seq(10,100,10)

dni_means  = apply(df,1,mean)
nam = c("K-core decomposition","IMM on Follower","PMIA on Diffusion","Diffusion Greedy","Diffusion CELF","SIMPATH on Databased")
df$Method = factor(nam,nam[order(dni_means ,decreasing=T)])
reshaped = melt(df,id=c("Method"))

reshaped$variable = as.numeric(as.character(reshaped$variable))
ggplot(reshaped,aes(x=variable,y=value,color=Method))+geom_line(size=2)+geom_point(size=4,aes(shape = Method))+
  xlab("Seed Set Size")+ylab("Number of Distinct Nodes Influenced in the Test set")+
  scale_x_continuous(breaks = seq(10,100,10),limits = c(10, 100))+ 
  theme(text = element_text(size=14),legend.text= element_text(size=12),axis.text = element_text(size=14))+
  scale_color_manual(values=c("blue","steelblue","red","brown","orange","magenta"))


ggsave("../../../Figures/spreading.pdf")


#---------------------------------------------------------------------- Time

library(xtable)
time = c(
  632, #k-cores
  16504, #diffusion greedy
  16, #diffusion celf
  103898+180, #IMM
  999 + 26398 + 569,  #PMIA on diffusion
  2981+93898+29) # SIMPATH on databased


dat = cbind(nam,dni_means,time)
dat = data.frame(dat)
names(dat) = c("Method","DNI","Time (sec)")
xtable(dat)

