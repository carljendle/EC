source("circle.r")


params <- list(x_min = - 3, x_max = 3, y_min = -3, y_max = 3, n_vals = 10000, tol = 0.3, r_min = 1.5, r_max = 2.8)
sc <- data_generator(params)

print(sc)
