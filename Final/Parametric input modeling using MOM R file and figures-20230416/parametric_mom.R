library(simEd)

# grab the arrival data and service data as collected by University of Richmond
# students for Tyler's Grill
arr <- tylersGrill$arrivalTimes
svc <- tylersGrill$serviceTimes

open_time  = 0     # 07:30
close_time = 48600 # 21:30

ten_am =  9000     # 10:00
one_pm = 19800     # 13:00

# use stripchart to create an across-time "scatterplot" of the arrivals
par(mfrow = c(2,1))  # two rows, one column
stripchart(arr, pch = "|")  # use a skinny print character
abline(v = c(ten_am, one_pm), lty = "dashed", col = "red")

# use stripchart to focus in on a subset of the arrivals
stripchart(arr[arr >= ten_am & arr <= one_pm], pch = "|")
readline('...')  # wait for return

# we will talk about modeling arrivals using a non-parameteric approach

##########################################################################

# determine whether service times are independent
acf(svc)

# determine whether service times are from a stationary process
# (i.e., rate doesn't change) -- check via fitting a linear
# model
observations = 1:length(svc)
fit <- lm(svc ~ observations)  # order: dependent variable ~ independent variable
plot(svc ~ observations)
abline(fit)

# use names(fit) to see what is availabile inside fit
slope <- fit$coefficients[2]
print(paste("slope of linear fit:", slope))
readline('...')  # wait for return

##########################################################################
# Because the service times are deemed to be independent (no 
# autocorrelation beyond lag 0) and from a stationary process
# (service times versus observation number returns a fitted
# regression line with slope 0), we now proceed to use method
# of moments (MOM) to fit both an exponential distribution and
# a gamma distribution.
#

# 1) exponential: one parameter mu
#   (a) using MOM: set sample mean to mu
#       --> x_bar = mu
#       --> mean(svc) = mu
#       and therefore the parameter estimate to exponential will
#       be mu_hat = mean(svc).

mu_hat = mean(svc)
print(paste("MOM parameter estimate when fitting exponential:", mu_hat))

#   (b) now plot an empirical cumulative distribution function (ecf)
#       for the service times, and superimpose the exponential cdf
#       using the parameter estimate
#           NB: R's dexp|pexp|qexp functions parameterize using
#               the rate, not the mean, so need to adjust below

plot.stepfun(ecdf(svc), pch = "", main = "exponential CDF fit to service ECDF")
curve(pexp(x, rate = 1/mu_hat), col = "red", lwd = 2, add = TRUE)

#   (c) and now print the fit, as determined by the Kolmogorov-Smirnov
#       goodness-of-fit test, noting the produced D value (corresponding
#       to the largest vertical line between pexp and the ecdf):

ks_fit <- ks.test(svc, "pexp", rate = 1/mu_hat)
print(paste("K-S measure for exponential goodness of fit:", ks_fit$statistic))
# add the fit statistic to the graphic
text(150, 0.3, paste("ks.test D statistic:", format(ks_fit$statistic, digits=4)))

#   (d) Note that, in general, the K-S test should not be used when there are
#       ties in the data, as a continuous distribution should not produce any
#       ties (duplicate values).  In this context, it is because the
#       data-collection software rounded the service time to the nearest 
#       second.  We can remedy this by adding a small amount of noise to each
#       service time, and noting that the produced D value is essentially the
#       same as before:

svc_with_noise <- svc + runif(length(svc), 0.001, 0.002)
mu_hat_noise <- mean(svc_with_noise)
print(paste("MOM parameter estimate when fitting exponential (with noise):", 
        mu_hat_noise))
ks_fit_check <- ks.test(svc_with_noise, "pexp", rate = 1/mu_hat_noise)
print(paste("K-S measure for exponential goodness of fit (with noise):", 
        ks_fit_check$statistic))

# 2) gamma: two parameters: shape (k) and scale (theta)
#   (a) using MOM: set sample mean to mean of gamma (k*theta), and
#                  set sample variance to variance of gamma (k*theta^2)
#                     (see https://en.wikipedia.org/wiki/Gamma_distribution)
#       --> x_bar = k * theta
#           s^2   = k * theta^2
#       There are two equations with two unknowns (k, theta), so solve:
#               x_bar = k * theta --> k = x_bar / theta
#       and substituting into the second equation:
#               s^2   = (x_bar / theta) * theta ^2 = x_bar * theta
#           --> theta = s^2 / x_bar
#       and again substituing back into the first equation:
#               k = x_bar / theta = x_bar / (s^2 / x_bar) = x_bar^2 / s^2
#       Hence, our two estimates for k and theta will be:
#               k_hat     = x_bar^2 / s^2 = mean(svc)^2 / var(svc)
#               theta_hat = s^2 / x_bar   = var(svc) / mean(svc)

k_hat = mean(svc)^2 / var(svc)
theta_hat = var(svc) / mean(svc)
print(paste("MOM parameter estimates when fitting gamma (k,theta):", 
            k_hat, theta_hat))

#       
#   (b) now plot an empirical cumulative distribution function (ecf)
#       for the service times, and superimpose the gamma cdf
#       using the parameter estimates for k and theta

plot.stepfun(ecdf(svc), pch = "", main = "gamma CDF fit to service ECDF")
curve(pgamma(x, shape = k_hat, scale = theta_hat), col = "red", 
       lwd = 2, add = TRUE)

#   (c) and now print the fit, as determined by the Kolmogorov-Smirnov
#       goodness-of-fit test, noting the produced D value (corresponding
#       to the largest vertical line between pgamma and the ecdf):

ks_fit_gamma <- ks.test(svc, "pgamma", shape = k_hat, scale = theta_hat)
print(paste("K-S measure for gamma goodness of fit:", ks_fit_gamma$statistic))
# add the fit statistic to the graphic
text(150, 0.3, paste("ks.test D statistic:", 
                    format(ks_fit_gamma$statistic, digits = 4)))

#   (d) Again, the K-S test should not be used when there are
#       ties in the data, so we can remedy this by adding a small amount of
#       noise to each service time, and noting that the produced D value is
#       essentially the same as before:

k_hat_noise = mean(svc_with_noise)^2 / var(svc_with_noise)
theta_hat_noise = var(svc_with_noise) / mean(svc_with_noise)
print(paste("MOM parameter estimates when fitting gamma (k,theta), with noise:", 
            k_hat_noise, theta_hat_noise))
ks_fit_gamma_check <- ks.test(svc_with_noise, 
                        "pgamma", shape = k_hat_noise, scale = theta_hat_noise)
print(paste("K-S measure for gamma goodness of fit (with noise):", 
        ks_fit_gamma_check$statistic))
