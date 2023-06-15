arr <- read.table("arrivals_EightFifteen_Mon11Nov2019.txt") # this should _not_ have 0 and S
arr <- arr$V1
inter <- diff(arr)  # interarrivals

par(mfrow = c(1,1))
hist(inter, breaks = "fd", freq = FALSE, main = "Eight Fifteen Interarrivals")
curve(dexp(x, 1/mean(inter)), add=TRUE, col="red")
print(mean(inter))

readline("Press return to continue...")

plot(ecdf(inter), verticals=TRUE, do.points=FALSE, las=1, bty="n")
curve(pexp(x, rate = 1/mean(inter)), add = TRUE, col = "red")

# use ks.test to measure goodness, if desired
#x = seq(0, 1000, by = 0.5)
#ks.test(ecdf(inter)(x), pexp(x,rate=1/mean(inter)))

readline("Press return to continue...")

#*****************************************

#GETTING COUNTS DATA

numHours = 17.5
window = 1.0
print(numHours / window)  # 11.6667
numBins = ceiling(numHours / window)
counts = rep(0,numBins)
counts[1] = length(arr[arr <= window*3600])
for (i in 2:numBins) { 
    counts [i] = counts[i] + 
        length(arr[arr > window*3600*(i-1) & arr <= window*3600*i]) 
}
print(counts)
print(sum(counts))
print(length(arr))

breaks = 7.5 + (window * 0:numBins)

# plot a histogram
par(mfrow = c(1,1))
plot(breaks, c(counts[1], counts), type="S", ylim = c(0,200), bty="n", las=1, 
    xlab = "", xaxt = "n", ylab = "arrivals", lty="solid", lwd=2)
axis(1, at=seq(7.5, 26, by = window), tick = TRUE, lwd.ticks = 1, lwd = 1)
abline(v=breaks, lty="dotted",lwd=1)
text( x = breaks[1:numBins] + window/2, y = counts + 10, labels = counts )

readline("Press return to continue...")
################################

# plot an empirical cumulative event rate function
# to generate figure like 9.3.3

plot(c(7.5, breaks[1:numBins] + window/2), c(0, cumsum(counts)), ylim=c(0,1500), 
        type="l", bty="n", las=1, xlab = "", xaxt="n", ylab="arrivals")
points(breaks[1:numBins] + window/2, cumsum(counts), type="p", pch=20)
axis(1, at=seq(7.5, 26, by = window), tick = TRUE, lwd.ticks = 1, lwd = 1)
abline(v=breaks, lty="dotted",lwd=1)

readline("Press return to continue...")
################################

# Algorithm 9.3.1
alg931 = function(k = 2, breaks = NULL, counts = NULL)
{
    Lam_max = sum(counts)/k
    i = 1
    j = 1
    Lam = counts[i]/k

    times = NULL

    e = rexp(1)
    while (e <= Lam_max)
    {
        while (e > Lam)
        {
            i = i+1
            Lam = Lam + counts[i]/k
        }
        # remember our breaks ('a' in alg 9.3.3) have a "0th" component in them;
        # counts ('n' in alg 9.3.3) does not
        t = breaks[i+1] - (Lam - e) * k * (breaks[i+1] - breaks[i]) / counts[i];

        times = c(times, t)

        j = j + 1
        e = e + rexp(1)
    }
    return(times)
}


colors = c("red","blue","darkgreen","purple")
for (i in 1:4)
{
    events = alg931(1, breaks, counts)
    points(events, 1:length(events), type="l", col = colors[i])
}

readline("Press return to continue...")

######################################################

# BY HAND EXAMPLE FOR ALG 9.3.3

S = 100
n = 5

set.seed(804)  # chosen for decent cerf
times = sample(1:(S-1), size = n, replace = FALSE)
times = sort(times)

verts = (1:n) * (n/(n+1))

times = c(0,times,S)
verts = c(0, verts,n)

print(times)
print(verts)

plot(times, verts, type = "l", bty = "n", las = 1, ylab = "arrivals")
points(times, verts, pch = 20)

invert = function(e)
{
    # e is the event time generated from a unit SPP
    print(paste("e = ", e))

    # m is the index of the lowest line-segment endpoing across which to invert
    m = floor((n+1) * e / n)
    print(paste("m = ", m))

    # this is just some algebra determining where a horizontal line at e
    # intersects with the line segment between t_m and t_{m+1} using the
    # slope of that segment
    # NOTE: when indexing into an R array, need to +1 for each index relative
    #       to Alg 9.3.3
    t = times[m+1] + (times[m+1+1] - times[m+1]) * (((n+1) * e / n) - m)
    print(paste("t = ", t))

    yaxt_x = -4     # x value of y axis, by trial and error
    xaxt_y = -0.2   # y value of x axis, by trial and error
    segments(-5, e, t, e, lty = "dashed")
    segments(t, e, t, xaxt_y, lty = "dashed")
    points(yaxt_x, e, pch = 20, xpd = TRUE)
    points(t, xaxt_y, pch = 20, xpd = TRUE)
}

# chosen for good uSPP
set.seed(8675309)
e = rexp(1)
invert(e)

e = e + rexp(1)
invert(e)

e = e + rexp(1)
invert(e)

e = e + rexp(1)
invert(e)

e = e + rexp(1)
invert(e)

e = e + rexp(1)
invert(e)

e = e + rexp(1)
print(paste("Laste e:", e))

readline("Press return to continue...")
######################################################

### try an actual Eight Fifteen data
#  (k is the number of realizations of data you have,
#   i.e., the number of days of collected data)

alg933 <- function(k = 1, times = NULL, S)
{
    arrivals = NULL

    # n should not count t_(0) nor t_(n+1)
    n <- length(times)

    times <- c(0, times, S)

    i <- 1
    e <- rexp(1)
    while (e <= n / k)
    {
        m <- floor((n+1) * k * e/n)

        # don't let R's indexing fool you -- the m computed above is relative
        # to C/Java/Python-style indexing starting at 0 -- so m=0 really should
        # be indexing into times[1]...

        t <- times[m+1] + (times[m+1+1] - times[m+1]) * (((n+1) * k * e/n) - m)
        arrivals <- c(arrivals, t)
        i <- i + 1
        e <- e + rexp(1)
    }

    return(arrivals)
}


# plot the trace of arrivals...
plot(NA, NA, 
    xlab = "time", ylab = "# arrivals", las = 1, main = "Arrival Process",
    xaxt = "n", bty = "n", xlim = c(0,17.5)*3600, ylim = c(0,1400) )
labels = c("07:30","09:00","10:30","12:00","13:30","15:00","16:30","18:00","19:30","21:00","22:30","00:00")
axis(1, at = c(seq(0, 17.5, by = 1.5)*3600), labels = labels, lwd.ticks = 1, lwd = 0)
axis(1, at = c(0, 17.5)*3600, labels = FALSE, lwd = 1, lwd.ticks = 0)

# plot the empirical CERF for the arrivals data
points(arr, 1:length(arr), type = "l", col = "black", lwd = 2)

# ...with five realizations superimposed
colors <- c("gray","red","blue","darkgreen","purple")
for (i in 1:length(colors))
{
    events = alg933(k = 1, times = arr, S = 17.5*3600)
    points(events, 1:length(events), type="l", col = colors[i])
}
