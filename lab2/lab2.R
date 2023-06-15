#load simEd package
library(simEd)

#using ssq to build a convergence function which
#returns the convergence to steady state figure
convergence<- function(num_jobs, iseed, serviceFcn=NULL){
  average_sojo<-rep(0, num_jobs)
  sojourn_times<-ssq(maxDepartures = num_jobs, showOutput = FALSE, seed=iseed, serviceFcn = serviceFcn, saveSojournTimes = TRUE)$sojournTimes
  for(i in seq(100, num_jobs, by=100)){
    
    average_sojo[i]<-mean(sojourn_times[1:i])
     
  }
  return (average_sojo)
}

#using  built function convergence to generate three sequences of average sojourn time
#and plot the convergence-to-steady-state graph with avgSojourn time every 100 jobs
Dottedline<- function(num_jobs, serviceFcn=NULL, solid_so=9){
  
  all_avgSojourn1<- convergence(num_jobs, 111111, serviceFcn)
  
  all_avgSojourn2<- convergence(num_jobs, 021031, serviceFcn)
  
  all_avgSojourn3<- convergence(num_jobs, 020131, serviceFcn)
  plot(all_avgSojourn1, pch=1, xlim=c(0, num_jobs), ylim=c(0, solid_so*2+7), xlab="jobs", ylab="average sojourn", frame.plot=FALSE)
  points(all_avgSojourn2, pch=5)
  points(all_avgSojourn3, pch=16)
  abline(h=solid_so, col = "black", lwd = 2)
  legend("topleft", c("111111","021031","020131"),cex=0.8,title = "Initial Seed", pch=c(1, 5, 16))
}

#Write R functions for three different gamma service processes:
getSvc1 = function() { rgamma(1, shape = 1.0, scale = 0.9) }
getSvc2 = function() { rgamma(1, shape = 1.05, scale = 0.9) }
getSvc3 = function() { rgamma(1, shape = 1.1, scale = 0.9) }

par(mfrow=c(4,1),pin=c(5,1))
#1 experiment with default service process M/M/1
Dottedline(5000)

#2 experiment with first gamma service process M/G/1
Dottedline(5000,serviceFcn = getSvc1, solid_so = 1/(1/0.9-1))

#3 experiment with second gamma service process M/G/1
Dottedline(5000, serviceFcn = getSvc2, solid_so = 1/(1/0.945-1))
           
#4 experiment with third gamme service process M/G/1
#par(pin=c(5,2))
Dottedline(500000, serviceFcn = getSvc3, solid_so = 1/(1/0.99-1))

