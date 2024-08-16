###clustermins
### Written by Weston Hall
### 07-18-2022
### Makes cluster_mins using k-means

#library(rgl)
#library(plot3D)
#library(scatterplot3d)
library(viridisLite)
library(ggplot2)
library(viridis)
library(cluster)
library(stringr)
#library(factoextra)
#library(NbClust)
#library(dplyr)
#setwd("~/grid05-24/mincode/cluster")

data <- read.table('../minoutput2', sep=';', colClasses=c("integer","integer", "integer", "integer", "numeric","character"))
#data <- data[-3]
k_data <- data[-5]

colnames(data) <- c("temp", "mass", "he","h","s", "modes")

test<- data$modes[1]
test_split <- strsplit(test,"  ")[[1]]
test_split <- test_split[test_split!=""]
# str_sub(test_split[1],-4, -3)
mode_mat<-matrix(NA,nrow = nrow(data), ncol=length(test_split),byrow=TRUE)

for(i in 1:nrow(data)){
  test <- data$modes[i]
  test_split <- strsplit(test, "  ")[[1]]
  test_split <- test_split[test_split!=""]
  for(n in 1:length(test_split)-1){
    test_split[n] = str_sub(test_split[n],-4,-3)
  }
  test_split[length(test_split)] = str_sub(test_split[length(test_split)], -3,-2)
  mode_mat[i,] = test_split
}

scaled_data <- as.data.frame(mode_mat)
########################################


hydrogen = 600
helium=200

temp_modes <- as.data.frame(scaled_data[data$he==helium & data$h==hydrogen,])
while(nrow(temp_modes) <= 2){
  hydrogen = hydrogen + 25
  temp_modes <- scaled_data[data$he==helium & data$h==hydrogen,]
  if(hydrogen > 950){
	  temp_modes <- data.frame(matrix(ncol = 1, nrow = 3))
  }
}
maximum <- nrow(as.data.frame(temp_modes[!duplicated(temp_modes), ]))

if(maximum > 2 & ncol(temp_modes) > 1){
  k_value = c(2:maximum)
  distortions = c(2:maximum)
  BIC <- c(2:maximum)
  d <- ncol(scaled_data)
  n <- 300
  
  
  for (k in k_value){
    fit <- suppressWarnings(kmeans(temp_modes, k))
    distortions[k - 1] <- fit$tot.withinss
    BIC[k-1] <- distortions[k-1] + (k - 1 + k * d) * log(n)
  }
  
  x11(width=15, height=5)
  
  par(mfrow = c(1,3), xpd = TRUE)
  
  plot(k_value, distortions,
       ylab = "WSS Score", xlab = "K Value")
  #abline(v = k_val, col = "red")
  
  plot(k_value, BIC,
       xlab = "K Value", ylab = "BIC")
  
  col_pallete <- rainbow(10)
  shape <- c(19,17,15, 8,23,19,17,15, 8,23)
  
  plot(data[data$h == hydrogen & data$he == helium,]$temp, data[data$h == hydrogen & data$he==helium,]$mass*0.001, col = 'red',
       xaxt = 'n', yaxt= 'n', 
       xlab ='Temperature (K)', ylab = expression("Mass (M"["\u2609"]*")"),
       xlim = c(12600,10600), ylim=c(0.47,1.0),
       pch = 19)
  cat("Number of clusters: ")
  args <- readLines(con = "stdin", n = 1)
  
  k_val = as.numeric(args)
} else{
  cat("No clusters\n")
  if(ncol(temp_modes) ==1){
	  cat("1 period :/\n")
  }
  k_val = 1
}

if(k_val > 1){
  data$familyn <- NA
  if(!("ID" %in% colnames(data) )){
    data <- cbind(ID = 1:nrow(data), data)
  }
  
  for(hydrogen in seq(400,950,25)){
    #print(hydrogen)
    for(helium in seq(150,400,25)){
      fam <- 0
      #temp <- data[data$h==hydrogen & data$he == helium,]
      temp <- scaled_data[which(data$h==hydrogen & data$he == helium),]
      use_k <- k_val
      if(use_k > nrow(temp[!duplicated(temp), ])){
        use_k <- nrow(temp[!duplicated(temp),])
      }
      k_model <- kmeans(scaled_data[which(data$h==hydrogen & data$he == helium),], use_k, iter.max = 400)
      #k_model <- kmeanspp(scaled_data[which(data$h==hydrogen & data$he == helium),], k_val)
      data[data$h == hydrogen & data$he == helium,]$familyn = k_model$cluster
    }
  }
  
  
  new_cluster_mins = data.frame(matrix(NA, nrow = 60, ncol = 6))
  colnames(new_cluster_mins) <- c("temp", "mass", "he","h","s", "members")
  
  minimums <- rep(0, 60)
  
  g <- 1
  legendlabels <- data.frame(matrix(NA, nrow = 53, ncol = 2))
  i=1
  for(hydrogen in seq(400,950,25)){
    #print(hydrogen)
    for(helium in seq(150,400,25)){
      for(j in 1:max(data$familyn)){
        test_data = data[data$h == hydrogen & data$he == helium & data$familyn == j, ]
        test_data = test_data[c(-1,-7,-8,-9)]
        if(nrow(test_data) > 0){
          min_idx <- which.min(test_data$s)
          new_cluster_mins[i,] <- c(test_data[min_idx,1:5], nrow(test_data))
          #suppressWarnings(data[rownames(test_data),]$group <- g)
          legendlabels[g,] <- c(toString(hydrogen * 0.01), toString(helium * 0.01))
          g <- g+1
        }
        i = i+1
      }
    }
  }
  #print(nrow(new_cluster_mins))
  new_cluster_mins <- new_cluster_mins[is.na(new_cluster_mins$temp) == FALSE,]
  new_cluster_mins <- new_cluster_mins[order(new_cluster_mins$s),]
  #print(nrow(new_cluster_mins))
  
  write.csv(new_cluster_mins, file="cluster_mins.csv")
} else {
  
  cluster_mins = data.frame(matrix(NA, nrow = 60, ncol = 6))
  colnames(cluster_mins) <- c("temp", "mass", "he","h","s", "members")
  
  minimums <- rep(0, 60)
  
  # group <- rep(0,nrow(data))
  # data <- cbind(data, group)
  g <- 1
  legendlabels <- data.frame(matrix(NA, nrow = 53, ncol = 2))
  i=1
  for(hydrogen in seq(400,950,25)){
    for(helium in seq(150,400,25)){
      test_data = data[data$h == hydrogen & data$he == helium, ]
      if(nrow(test_data) > 0){
        min_idx <- which.min(test_data$s)
        cluster_mins[i,] <- c(test_data[min_idx,1:5], nrow(test_data))
        #suppressWarnings(data[rownames(test_data),]$group <- g)
        legendlabels[g,] <- c(toString(hydrogen * 0.01), toString(helium * 0.01))
        g <- g+1
      }
      i = i+1
    }
  }
  cluster_mins <- cluster_mins[is.na(cluster_mins$temp) == FALSE,]
  cluster_mins <- cluster_mins[order(cluster_mins$s),]
  write.csv(cluster_mins, file="cluster_mins.csv")
}



