#this is the hard way to solve linear regression
#implemented gradient descent
#calculates the error
#finds the slope of the error (which is the gradient)
#taking steps DOWNHILL to calibrate the best weights

# basic concepts
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
        
    def _compute_cost(self, X, y, weights, bias):
        m = len(y)
        predictions = np.dot(X, weights) + bias
        cost = (1 / (2 * m)) * np.sum((predictions - y) ** 2)
        return cost
    
    def _compute_gradients(self, X, y, weights, bias):
        m = len(y)
        predictions = np.dot(X, weights) + bias
        errors = predictions - y
        
        dw = (1 / m) * np.dot(X.T, errors)
        
        db = (1 / m) * np.sum(errors)
        
        return dw, db
    
    def fit(self, X, y):
        #store the x and y data
        #X are the input features
        X = np.array(X)
        #y are the target values
        y = np.array(y)
        
        # create the normalized features by running the previous normalize function
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
            # dw = gradient(slope) for weights
            # db = gradient (slope) for bias

            #if dw is positive = then increasing the weight increases error, so the weight should be decreased
            # example of tuple unpacking
                # first return of function goes to dw, second return goes to db
            dw, db = self._compute_gradients(X_normalized, y, self.weights, self.bias)
            
            # updating step
            # subtracting the gradient means going down hill which is minimizing error
            # self.weights is a vector ex: [0, 0, 0]
            # dw is a vector ex: [5, -2, 1]
            # learning rate is a scalar ex: [0.01]
            # operates on all features simulatenously

            self.weights = self.weights - self.learning_rate * dw
            self.bias = self.bias - self.learning_rate * db
            
            cost = self._compute_cost(X_normalized, y, self.weights, self.bias)
            self.cost_history.append(cost)
            
            if (i + 1) % 100 == 0:
                print(f"Iteration {i + 1}/{self.n_iterations}, Cost: {cost:.6f}")
        
        return self
    
    def predict(self, X):
        X = np.array(X)
        X_normalized = self._normalize_features(X, fit=False)
        return np.dot(X_normalized, self.weights) + self.bias
    
    def score(self, X, y):
        y = np.array(y)
        predictions = self.predict(X)
        
        ss_res = np.sum((y - predictions) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        
        return 1 - (ss_res / ss_tot)


def demonstrate_gradient_descent():
    print("\n=== Gradient Descent Demonstration ===")
    print("Finding minimum of f(x) = x² using gradient descent")
    print("Derivative: f'(x) = 2x")
    
    x = 10.0
    learning_rate = 0.1
    
    print(f"\nStarting at x = {x}")
    
    for i in range(10):
        gradient = 2 * x
        x = x - learning_rate * gradient
        print(f"Step {i + 1}: x = {x:.6f}, f(x) = {x**2:.6f}")
    
    print(f"\nConverged to x ≈ {x:.6f} (true minimum is x = 0)")


if __name__ == "__main__":
    demonstrate_gradient_descent()
