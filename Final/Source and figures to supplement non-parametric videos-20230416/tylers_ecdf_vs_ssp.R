library(simEd)
arr = tylersGrill$arrivalTimes
plot((arr / 3600) + 7.5, 1:length(arr), type = "s", bty = "l")
len = length(arr) #[1] 1434
ia_avg = mean(diff(arr))

ssp = rep(0,len)
ssp[1] = rexp(1, 1/ia_avg)
for (i in 2:len) { 
    ssp[i] = ssp[i-1] + rexp(1, rate = 1/ia_avg) 
}
points((ssp / 3600) + 7.5, 1:length(arr), type = "s", col = "red")
