library(rgl)
#library(plot3D)
#library(scatterplot3d)
library(viridis)
setwd("~/grid10-08/mincode")

#####READING DATA AND SCALING###################
data <- read.table('minoutput')
data <- data[-3]

colnames(data) <- c("temp", "mass", "he","h","s")

scaled_data <- as.data.frame(scale(data))
#scaled_data <- scaled_data[-5]

pairwise_dist <- dist(scaled_data)
#mds_4d <- cmdscale(pairwise_dist, 4)
mds_5d <- cmdscale(pairwise_dist, 5)

plot(mds_5d, xlab="", ylab="", main="Pairwise distances between observations", col = rgb(0,0,0.5,0.5))
#####################################################


######PICKING K VALUE######################################
k_value = c(2:100)
distortions = c(2:100)

for (k in k_value){
  fit <- kmeans(scaled_data, k)
  distortions[k - 1] <- fit$tot.withinss
}

plot(k_value, distortions,
     ylab = "Distortion", xlab = "K Value")

abline(v = 20, col = "red")

BIC <- c(2:100)
d <- 8
n <- 300

for(k in k_value){
  BIC[k-1] <- distortions[k-1] + (k - 1 + k * d) * log(n)
}

plot(k_value, BIC,
     xlab = "K Value", ylab = "BIC")
abline(v = 20, col = "red")

k_val = 20
###################################################



####MAKING K MODEL##############################################
k_model <- kmeans(scaled_data, k_val, iter.max = 400)

plot(data$temp, data$mass, col = k_model$cluster,
     xlab = "temp", ylab = "mass", pch = 19)

plot(mds_5d, xlab="", ylab="", main="Pairwise distances between observations", 
     col = k_model$cluster, pch = 19)
########################################################


##########FIND THE MINIMUMS FOR EACH CLUSTER#######################
cluster_mins = data.frame(matrix(NA, nrow = k_val, ncol = 5))
colnames(cluster_mins) <- c("temp", "mass", "he","h","s")

for(i in 1:k_val){
  min_idx <- which.min(data[k_model$cluster == i, ]$s)
  cluster_mins[i,] <- data[k_model$cluster == i,][min_idx,]
}
##########################################################


####PLOTS#################################################################
# s3d <- scatterplot3d(
#   x = data$temp, y= data$mass, z = data$h,
#   color = rainbow(k_val)[k_model$cluster],
#   xlab = "Temperature", ylab = "Mass", zlab = "Hydrogen", pch = 20
# )
# s3d$points3d(
#   x = cluster_mins$temp, y= cluster_mins$mass, z= cluster_mins$h,
#   col = "black", pch = 20, cex = 2
# )

# scatter3D(
#   x = data$temp, y = data$mass, z = data$h,
#   colvar = k_model$cluster
# )


##Moving plot
rgl.open()
plot3d(
  x = data$temp, y = data$mass, z = data$h,
  col = rainbow(k_val)[k_model$cluster],
  xlab = "Temperature", ylab = "Mass", zlab = "Hydrogen",
  size = 5, type = 1
)
spheres3d(
  x = cluster_mins[,1], y= cluster_mins[,2], z= cluster_mins[,4],
  color = "yellow", radius = 20
)
#legend3d("topright", legend=c(1:k_val), cex = .7, col = rainbow(k_val), pch = 19)
rglwidget()
writeWebGL(dir = "~/grid10-08/mincode", filename = file.path(dir, "index.html"))
# rglwidget()
# rgl.clear()
# rgl.close()
#####

# s3d <- scatterplot3d(
#   x = scaled_data$temp, y= scaled_data$mass, z = scaled_data$h,
#   color = rainbow(k_val)[k_model$cluster],
#   xlab = "Temperature", ylab = "Mass", zlab = "Hydrogen", pch = 20
# )
# s3d$points3d(
#   x = k_model$centers[,1], y= k_model$centers[,2], z= k_model$centers[,4],
#   col = "black", pch = 20, cex = 2
# )

#11 630 200  0.59 0.03


# plot3d(
#   x = scaled_data$temp, y= scaled_data$mass, z = scaled_data$h,
#   col = rainbow(k_val)[k_model$cluster],
#   xlab = "Scaled Temperature", ylab = "Scaled Mass", zlab = "Scaled H index"
# )
# spheres3d(
#   x = k_model$centers[,1], y= k_model$centers[,2], z= k_model$centers[,4],
#   col = rainbow(k_val), radius = 0.05
# )
# legend3d("topright", legend=c(1:k_val), cex = .7, col = rainbow(k_val), pch = 19)
# rglwidget()

# plotting_data <- data[k_model$cluster==3,]
# plot3d(
#   x = plotting_data$temp, y = plotting_data$mass, z = plotting_data$h,
#   col = viridis(max(plotting_data$s))[plotting_data$s]
# )
# rglwidget()






##### EXTERNAL UNCERTAINTY ##############
uncertainties <- data.frame(matrix(NA, nrow = nrow(cluster_mins), ncol = 8))
colnames(uncertainties) <- c('utemp', 'ltemp', 'umass', 'lmass', 'uhe', 'lhe', 'uh', 'lh')

for(i in 1:nrow(uncertainties)){
  utemp <- 0
  ltemp <- 0
  umass <- 0
  lmass <- 0
  uhe <- 0
  lhe <- 0
  uh <- 0
  lh <- 0
  
  
  for(j in 1:nrow(cluster_mins)){
    
    
    ######
    t_diff <- cluster_mins$temp[j] - cluster_mins$temp[i]
    if(cluster_mins$temp[j] > cluster_mins$temp[i]){
      if(t_diff < utemp | utemp == 0){
        utemp <- sqrt( (t_diff**2) / (abs(cluster_mins$s[i] - cluster_mins$s[j])) )
      }
    } else if(cluster_mins$temp[j] < cluster_mins$temp[i]){
      if(abs(t_diff) < ltemp | ltemp == 0){
        ltemp <- sqrt( (t_diff**2) / (abs(cluster_mins$s[i] - cluster_mins$s[j])) )
      }
    }
    #####
    
    #####
    m_diff <- cluster_mins$mass[j] - cluster_mins$mass[i]
    if(cluster_mins$mass[j] > cluster_mins$mass[i]){
      if(m_diff < umass | umass == 0){
        umass <- sqrt( (m_diff**2) / (abs(cluster_mins$s[i] - cluster_mins$s[j])) )
      }
    } else if(cluster_mins$mass[j] < cluster_mins$mass[i]){
      if(abs(m_diff) < lmass | lmass == 0){
        lmass <- sqrt( (m_diff**2) / (abs(cluster_mins$s[i] - cluster_mins$s[j])) )
      }
    }
    #####
    
    #####
    he_diff <- cluster_mins$he[j] - cluster_mins$he[i]
    if(cluster_mins$he[j] > cluster_mins$he[i]){
      if(he_diff < uhe | uhe == 0){
        uhe <- sqrt( (he_diff**2) / (abs(cluster_mins$s[i] - cluster_mins$s[j])) )
      }
    } else if(cluster_mins$he[j] < cluster_mins$he[i]){
      if(abs(he_diff) < lhe | lhe == 0){
        lhe <- sqrt( (he_diff**2) / (abs(cluster_mins$s[i] - cluster_mins$s[j])) )
      }
    }
    #####
    
    #####
    h_diff <- cluster_mins$h[j] - cluster_mins$h[i]
    if(cluster_mins$h[j] > cluster_mins$h[i]){
      if(h_diff < uh | uh == 0){
        uh <- sqrt( (h_diff**2) / (abs(cluster_mins$s[i] - cluster_mins$s[j])) )
      }
    } else if(cluster_mins$h[j] < cluster_mins$h[i]){
      if(abs(h_diff) < lh | lh == 0){
        lh <- sqrt( (h_diff**2) / (abs(cluster_mins$s[i] - cluster_mins$s[j])) )
      }
    }
    #####
    
    
  }
  
  uncertainties[i,] <- c(utemp, ltemp, umass, lmass, uhe, lhe, uh, lh)
}

########################################
