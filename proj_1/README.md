# Project 1: House Price Predictor

## Overview
This project implements **Linear Regression from scratch** using NumPy and compares it with scikit-learn's implementation. It's designed to teach the fundamental concepts of machine learning optimization.

## Concepts Learned
- **Gradient Descent**: Iterative optimization algorithm
- **Cost Functions**: Mean Squared Error (MSE)
- **Feature Normalization**: Z-score standardization
- **Train/Test Split**: Evaluating model generalization
- **R² Score**: Coefficient of determination

## Project Structure
```
proj_1/
├── main.py                      # Main script - run this
├── linear_regression_scratch.py # From-scratch implementation
├── linear_regression_sklearn.py # Sklearn wrapper for comparison
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## Installation
```bash
cd proj_1
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```

## Dataset
Uses the **California Housing** dataset (built into sklearn):
- 20,640 samples
- 8 features (income, house age, rooms, etc.)
- Target: Median house value ($100,000s)

## Key Implementation Details

### Gradient Descent Algorithm
```
For each iteration:
    1. predictions = X · weights + bias
    2. error = predictions - y
    3. gradient_w = (1/m) · X^T · error
    4. gradient_b = (1/m) · sum(error)
    5. weights = weights - learning_rate · gradient_w
    6. bias = bias - learning_rate · gradient_b
```

### Why Feature Normalization?
Without normalization, features with larger scales dominate gradient updates, causing slow or failed convergence.

## Output
The script generates three visualization files:
1. `data_exploration.png` - Dataset analysis
2. `training_visualization.png` - Gradient descent convergence
3. `predictions_comparison.png` - Model predictions vs actual

## Expected Results
Both implementations should achieve R² ≈ 0.60 on this dataset, demonstrating that our from-scratch version works correctly.
