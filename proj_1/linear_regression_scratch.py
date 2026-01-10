#this is the hard way to solve linear regression
#implemented gradient descent
#calculates the error
#finds the slope of the error (which is the gradient)
#taking steps DOWNHILL to calibrate the best weights

# basic concepts

    # Scalar - single number (no direction, just magnitude)
    # Vector - ordered list of scalars (think: row or column of numbers)
    # Matrix - grid of numbers w/ rows & columns (list of vectors stacked)

    # features (X); facts about the object
        # feature 1: mileage of a car (number)
        # feature 2: number of scratches on a car (number)
        # feature 3: age of a car (number)

    #weights(w); importance. how much does each feature impact the price
        # weight for feature 1: medium negative value (bc high mileage = lower price)
        # weight for feature 2: small negative value (bc scratches have negative impact, but not much)
        # weight for feature 3: potentially positive (?) older vintage = more valuable

    # when weights are [0, 0, 0] the model thinks nothing matters yet
    # bias (b) is the baseline. ex: when mileage is 0, age is 0, and scratches 0, the car still has a base value
    # ex price = (mileage * weight) + (age * weight) + base price(bias)

    # Gradient descent
        # self.weights is the position of your fingers on the sliders. 
        # dw (the gradient) is the instruction telling each finger which way to move.
        # the bowl idea
        # height on the bowl represents current weights
        # height represents error (cost)
            # high up = high error (model guessing poorly)
            # bottom of the bowl/valley = low error (model guessing well)

        # dw - the gradient for weights, the goal is to get to the bottom of the valley
       # calculate the gradient (dw) for each weight separately but simulatenously in each re-loop 
        # gradient = the slope of the ground under your current feet position
        # positive means bad logic
            # if the ground is sloping UP in front of your feet pos, if you move forward you are increasing weight, going up hill, and increasing error
                # go backward (decrease weight) to go down the slope which is weight = weight - (positive number)
            
            # if the ground is sloping down in front of feet post
                # go forward (increase weight) to go down the slope and reduce error
                # weight = weight - negative number
        # if a feature contributed a lot to the prediction, it gets more of the blame for the error
        # multiple weights adjusted per loop because a blame score (gradient) for every single feature FOUND BY: error * feature value then summing
        # error is tested by formula: prediction - actual. when the different is low, the gradient is low, and weights start to move less
        # each reloop should be getting closer to accurate weights

import numpy as np


class LinearRegressionScratch:

    #constructor for linearregressionscratch
    #learning_rate is the size of a step
    #y=mx+b
    #weights are 'm' the slope
    #bias is b 
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        #learning rate is step size. how big a step (correction) should be taken to correct a wrong output
        self.learning_rate = learning_rate
        #how many times to loop the updating process (for gradient descent)
        self.n_iterations = n_iterations
        #a weight for each feature

        self.weights = None
        #the intercept 
        self.bias = None
        # ? not sure 
        self.cost_history = []

        #saves the mean and standard deviation of training data
        self._mean = None
        self._std = None

    #normalization function (Z score normalization) 
    # transforms features so the mean is 0 and standard deviation is 1
    # z = X- mu / stddev, its the same function in stats class
    def _normalize_features(self, X, fit=False):
        #only fitting (calculating mean or standard deviation) for training data
        if fit:
            #calculate the average of columns (axis = 0), columns are the features
            self._mean = np.mean(X, axis=0)
            #calculate the standard deviation of columns
            self._std = np.std(X, axis=0)
            self._std[self._std == 0] = 1 #if the standard deviation is zero, hard code it to be 1 so there are no errors
            
        #returns the z score calculation
        return (X - self._mean) / self._std
        
    #calculates the (MSE) mean squared error
    # "how bad are the current weights?"
    def _compute_cost(self, X, y, weights, bias):
        # number of training examples (n) in data set
        m = len(y)
        # X (matrix of FEATURES) * weights (vector of knobs) + bias (base price)
        # predictions is an array of numbers representing a guess for every n
        predictions = np.dot(X, weights) + bias
        # cost formula
        # predictions - y: difference error for each n (every house in data set)
        # **2: squares each error
            # makes all errors positive, and punishes huge errors more
        # np.sum() adds up all squared errors into one final number
        # (1/(2*m)) : calculates the overall average
        cost = (1 / (2 * m)) * np.sum((predictions - y) ** 2)
        # the 'cost' is a single scalar number representing the RATING OF BADNESS for model
        # smaller cost = better model
        return cost
    
    # error calculation
    def _compute_gradients(self, X, y, weights, bias):
        m = len(y)
        # predictions : what the model thought the "price" was 
        predictions = np.dot(X, weights) + bias
        # predictions = guess, y = the actual, error = the difference
        errors = predictions - y
        
        # calculates the slope (gradient) for every single weight simultaneously
        # X.T transposes the feature matrix (flips X with features)
        # np.dot( ) performs the blame calculation by multiplying feature * error and then summing
        # (1/m) averages by dividing by m
        # dw = a list of slopes one for each feature
        dw = (1 / m) * np.dot(X.T, errors)
        

        #calculates the slope (gradient) for bias
        # bias is just a constant single number
        # sum all the errors to find out if on average we are guessing too high or low
        db = (1 / m) * np.sum(errors)
        
        #returns the list of weight slopes, and single bias slope 
        return dw, db

    #training loop - where learning takes place by implementing gradients, costs, and normalized data
    def fit(self, X, y):
        # convert the input data into arrays so that we can do matrix multiplication which deosnt work on normal python lists
        #store the x and y data
        #X are the input features
        X = np.array(X)
        #y are the target values
        y = np.array(y)
        
        # create the normalized features by running the previous normalize function
        # fit = True means its training data
        X_normalized = self._normalize_features(X, fit=True)
        
        #get the number of features (columns) by specifying [1]
        n_features = X_normalized.shape[1]
        #create an array for self.weights and fill it with 0's, the size is determined by the number of features
        self.weights = np.zeros(n_features)
        #set intercept to 0
        self.bias = 0
        #this is an empty list that will be used to store the error rate eventually
        self.cost_history = []
        
        #loop that runs an "iterations" number of times
        # each iteration is 1 step of learning
        for i in range(self.n_iterations):

            # inside the learning loop the direction to move has to be figured out
            # pass in current weights and bias to the _compute_gradients function
            # dw = a vector of gradients (slopes) for weights, calculated by multiplying features by errors
            # db = gradient (scalar slope) for bias

            #if dw is positive = then increasing the weight increases error, so the weight should be decreased
            # example of tuple unpacking
                # first return of function goes to dw, second return goes to db
            dw, db = self._compute_gradients(X_normalized, y, self.weights, self.bias)
            
            # updating step
            # subtracting the gradient means going down hill which is minimizing error
            # self.weights is a vector ex: [0, 0, 0]
            # dw is a vector ex: [5, -2, 1]
            # learning rate is a scalar ex: [0.01]
            # operates on all features simulatenously by multiplying the whole vectors

            self.weights = self.weights - self.learning_rate * dw
            self.bias = self.bias - self.learning_rate * db
            
            # calculate MSE (cost) and save it
            # MSE acts as a score for how well the model adjusted by the new weights
            cost = self._compute_cost(X_normalized, y, self.weights, self.bias)
            self.cost_history.append(cost)
            
            #every 100 loops/steps the model prints out its current cost to see if its getting smaller
            if (i + 1) % 100 == 0:
                print(f"Iteration {i + 1}/{self.n_iterations}, Cost: {cost:.6f}")
        
        #self is the trained object
        return self
    
    # this is using the model AFTER training is done
    # setting fit to false because now we are TESTING not training
    def predict(self, X):
        X = np.array(X)
        X_normalized = self._normalize_features(X, fit=False)
        # y = mx+b
        # np.dot(X_normalized, self.weights) = mx
        # self.bias = b
        return np.dot(X_normalized, self.weights) + self.bias
    

    # calculates R^2 the coefficient of determination
    # 
    def score(self, X, y):
        y = np.array(y)
        # make predictions on the X test data
        predictions = self.predict(X)
        
        # ss_res is residual sum of squares (sum of errors squared), how bad is the model
        ss_res = np.sum((y - predictions) ** 2)
        # ss_tot is total sum of squares 
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        
        # if the predictions are perfect, ss_res should be 0 and 1 -0 will be 1, which is a perfect score
        # 1.0 is a perfect score
        return 1 - (ss_res / ss_tot)


def demonstrate_gradient_descent():
    print("\n=== Gradient Descent Demonstration ===")
    print("Finding minimum of f(x) = x² using gradient descent")
    print("Derivative: f'(x) = 2x")
    # derivative : 
        # tells steepness of of slope
        # tells direction (positive = uphill to right, or negative = uphill to left)
    
    # random guess
    x = 10.0
    # step size
    learning_rate = 0.1
    
    print(f"\nStarting at x = {x}")
    
    for i in range(10):
        # gradient is 2 * x from previous loop
        gradient = 2 * x
        # update x, x = current x - (learning rate * gradient) 

        # loop 1 x = 8
        # loop 2 x = 6.4
        # loop 3 x = 5.12
        x = x - learning_rate * gradient
        print(f"Step {i + 1}: x = {x:.6f}, f(x) = {x**2:.6f}")
    
    print(f"\nConverged to x ≈ {x:.6f} (true minimum is x = 0)")


if __name__ == "__main__":
    demonstrate_gradient_descent()
