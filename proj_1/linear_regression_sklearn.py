#this is the easy way to do linear regression
# imports prebuilt linear regression class to solve for weights
from sklearn.linear_model import LinearRegression

# import pre-built normalization function (z = (x-mu)/stddev)
from sklearn.preprocessing import StandardScaler

# import functions like sum of squared errors, r^2
from sklearn.metrics import mean_squared_error, r2_score

# numpy library for arrays and matrix multiplication
import numpy as np


class LinearRegressionSklearn:
    
    def __init__(self):
        # built in solver from sklearn
        self.model = LinearRegression()
        # sk learn version of normalization
        self.scaler = StandardScaler()
        

    def fit(self, X, y):
        X = np.array(X)
        y = np.array(y)
        
        # calculate and save the mean/std from this data
        # transform - apply the math to this data
        X_scaled = self.scaler.fit_transform(X)
        
        #
        self.model.fit(X_scaled, y)
        
        return self
    
    def predict(self, X):
        X = np.array(X)
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def score(self, X, y):
        X = np.array(X)
        X_scaled = self.scaler.transform(X)
        return self.model.score(X_scaled, y)
    
    def get_coefficients(self):
        return self.model.coef_, self.model.intercept_


def evaluate_model(model, X_train, X_test, y_train, y_test, model_name="Model"):
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    
    train_mse = mean_squared_error(y_train, train_pred)
    test_mse = mean_squared_error(y_test, test_pred)
    train_r2 = r2_score(y_train, train_pred)
    test_r2 = r2_score(y_test, test_pred)
    
    print(f"\n{model_name} Results:")
    print("-" * 40)
    print(f"Training MSE: {train_mse:.4f}")
    print(f"Testing MSE:  {test_mse:.4f}")
    print(f"Training R²:  {train_r2:.4f}")
    print(f"Testing R²:   {test_r2:.4f}")
    
    return {
        'train_mse': train_mse,
        'test_mse': test_mse,
        'train_r2': train_r2,
        'test_r2': test_r2
    }
