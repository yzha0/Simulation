rollD<-function(){
  # this function returns the value of rolling a fair dice
  die <- sample(1:6, 1)
  return(die)
}

oneEst <- function(num_rolls = 1000) {
  # this function returns the estimate of a sum of 10
  # when rolling three fair dice
  count <- 0
  for (i in 1:num_rolls) {
    if (rollD() + rollD()+ rollD() == 10) {
      count <- count + 1
    }
  }
  return(count / num_rolls)
}

getEsts <- function(num_estimates = 100, num_rolls = 1000)
{
  # this function creates a vector of size num_estimates and fills
  # that vector with estimates of rolling a sum of ten using
  # n_roll per computed estimate
  estimates <- rep(0, num_estimates)
  for (i in 1:num_estimates) {
    estimates[i] <- oneEst(num_rolls)
  }
  return(estimates)
}

oneHistogram <- function(num_estimates, num_rolls)
{
  # this function creates a histogram that shows
  # the probability distribution of all estimates of 
  # rolling a sum of ten from three dices using N_est & N_roll
  all_estimates <- getEsts(num_estimates, num_rolls)
  hist(all_estimates, xlim = c(0, 0.3),xlab ="P(d1+d2+d3=10)", main= paste("Histogram of rolling three dices
N_est=",num_estimates, "N_roll=",num_rolls))
  m <- mean(all_estimates)
  abline(v = m, col = "blue", lwd = 2)
  s <- sd(all_estimates)
  abline(v = c(m - 2*s, m + 2*s), col = "red", lwd = 2, lty = "dashed") 
  print(quantile(getEsts(num_estimates), probs=c(0.5, 0.75, 0.95, 0.99)))
}


par(mfrow = c(2,3)) # display graphs in 2 rows, 3 column
# Generating two sets of histograms
# fix N_est, vary N_roll 10, 100, 1000
oneHistogram(1000, 10)
oneHistogram(1000, 100)
oneHistogram(1000, 1000)
# vary N_est 10, 100, 1000, fix N_roll
oneHistogram(10,1000)
oneHistogram(100,1000)
oneHistogram(1000,1000)

