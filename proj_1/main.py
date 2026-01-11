import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ssl
import certifi
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

from linear_regression_scratch import LinearRegressionScratch
from linear_regression_sklearn import LinearRegressionSklearn, evaluate_model

# Fix SSL certificate verification issue on macOS
# Configure SSL to use certifi's certificate bundle for HTTPS connections
def create_ssl_context():
    return ssl.create_default_context(cafile=certifi.where())

#ssl._create_default_https_context is a python internal variable
# called whenever python executes an attept to make an https connection
# this line means that whenever an SSL context is used for https, use the one I created manually
# "Every time Python tries to connect to an HTTPS website, use the certificates from the certifi package to verify it."
ssl._create_default_https_context = create_ssl_context


def load_and_explore_data():
    print("=" * 60)
    print("LOADING CALIFORNIA HOUSING DATASET")
    print("=" * 60)
    
    housing = fetch_california_housing()
    X = housing.data
    y = housing.target
    feature_names = housing.feature_names
    
    df = pd.DataFrame(X, columns=feature_names)
    df['Target'] = y
    
    print("\nDataset Shape:")
    print(f"  Samples: {X.shape[0]}")
    print(f"  Features: {X.shape[1]}")
    
    print("\nFeature Names:")
    for i, name in enumerate(feature_names):
        print(f"  {i + 1}. {name}")
    
    print("\nDataset Statistics:")
    print(df.describe().round(2))
    
    print("\nTarget Variable (Median House Value in $100,000s):")
    print(f"  Min: ${y.min() * 100000:,.0f}")
    print(f"  Max: ${y.max() * 100000:,.0f}")
    print(f"  Mean: ${y.mean() * 100000:,.0f}")
    
    return X, y, feature_names, df


def visualize_data(df, feature_names):
    print("\n" + "=" * 60)
    print("CREATING DATA VISUALIZATIONS")
    print("=" * 60)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    ax1 = axes[0, 0]
    ax1.hist(df['Target'], bins=50, edgecolor='black', alpha=0.7, color='steelblue')
    ax1.set_xlabel('Median House Value ($100,000s)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Distribution of House Prices')
    ax1.axvline(df['Target'].mean(), color='red', linestyle='--', label=f"Mean: {df['Target'].mean():.2f}")
    ax1.legend()
    
    ax2 = axes[0, 1]
    correlations = df.corr()['Target'].drop('Target').sort_values()
    colors = ['green' if c > 0 else 'red' for c in correlations]
    correlations.plot(kind='barh', ax=ax2, color=colors)
    ax2.set_xlabel('Correlation with House Price')
    ax2.set_title('Feature Correlations with Target')
    ax2.axvline(0, color='black', linestyle='-', linewidth=0.5)
    
    ax3 = axes[1, 0]
    sample_idx = np.random.choice(len(df), size=min(2000, len(df)), replace=False)
    ax3.scatter(df['MedInc'].iloc[sample_idx], df['Target'].iloc[sample_idx], 
                alpha=0.3, s=10, color='steelblue')
    ax3.set_xlabel('Median Income')
    ax3.set_ylabel('Median House Value ($100,000s)')
    ax3.set_title('Income vs House Price')
    
    ax4 = axes[1, 1]
    scatter = ax4.scatter(df['Longitude'].iloc[sample_idx], 
                          df['Latitude'].iloc[sample_idx],
                          c=df['Target'].iloc[sample_idx], 
                          cmap='viridis', alpha=0.5, s=10)
    ax4.set_xlabel('Longitude')
    ax4.set_ylabel('Latitude')
    ax4.set_title('Geographic Distribution of House Prices')
    plt.colorbar(scatter, ax=ax4, label='Price ($100,000s)')
    
    plt.tight_layout()
    plt.savefig('data_exploration.png', dpi=150, bbox_inches='tight')
    print("  Saved: data_exploration.png")
    plt.close()


def visualize_training(scratch_model, sklearn_results, scratch_results):
    print("\n" + "=" * 60)
    print("CREATING TRAINING VISUALIZATIONS")
    print("=" * 60)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1 = axes[0]
    ax1.plot(scratch_model.cost_history, color='steelblue', linewidth=1.5)
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Cost (MSE)')
    ax1.set_title('Gradient Descent Convergence')
    ax1.set_yscale('log')
    ax1.grid(True, alpha=0.3)
    
    ax1.scatter([0], [scratch_model.cost_history[0]], color='red', s=100, 
                zorder=5, label=f'Initial: {scratch_model.cost_history[0]:.4f}')
    ax1.scatter([len(scratch_model.cost_history)-1], [scratch_model.cost_history[-1]], 
                color='green', s=100, zorder=5, 
                label=f'Final: {scratch_model.cost_history[-1]:.4f}')
    ax1.legend()
    
    ax2 = axes[1]
    models = ['From Scratch', 'Scikit-learn']
    train_r2 = [scratch_results['train_r2'], sklearn_results['train_r2']]
    test_r2 = [scratch_results['test_r2'], sklearn_results['test_r2']]
    
    x = np.arange(len(models))
    width = 0.35
    
    bars1 = ax2.bar(x - width/2, train_r2, width, label='Train R²', color='steelblue')
    bars2 = ax2.bar(x + width/2, test_r2, width, label='Test R²', color='coral')
    
    ax2.set_ylabel('R² Score')
    ax2.set_title('Model Performance Comparison')
    ax2.set_xticks(x)
    ax2.set_xticklabels(models)
    ax2.legend()
    ax2.set_ylim(0, 1)
    
    for bar in bars1 + bars2:
        height = bar.get_height()
        ax2.annotate(f'{height:.3f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('training_visualization.png', dpi=150, bbox_inches='tight')
    print("  Saved: training_visualization.png")
    plt.close()


def visualize_predictions(y_test, scratch_pred, sklearn_pred):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    sample_size = min(500, len(y_test))
    idx = np.random.choice(len(y_test), sample_size, replace=False)
    
    for ax, pred, title in [(axes[0], scratch_pred, 'From Scratch'),
                            (axes[1], sklearn_pred, 'Scikit-learn')]:
        ax.scatter(y_test[idx], pred[idx], alpha=0.5, s=20, color='steelblue')
        
        min_val = min(y_test.min(), pred.min())
        max_val = max(y_test.max(), pred.max())
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, 
                label='Perfect Prediction')
        
        ax.set_xlabel('Actual Price ($100,000s)')
        ax.set_ylabel('Predicted Price ($100,000s)')
        ax.set_title(f'{title}: Actual vs Predicted')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('predictions_comparison.png', dpi=150, bbox_inches='tight')
    print("  Saved: predictions_comparison.png")
    plt.close()


def main():
    print("\n" + "=" * 60)
    print("HOUSE PRICE PREDICTOR")
    print("Linear Regression: From Scratch vs Scikit-learn")
    print("=" * 60)
    
    X, y, feature_names, df = load_and_explore_data()
    
    visualize_data(df, feature_names)
    
    print("\n" + "=" * 60)
    print("SPLITTING DATA")
    print("=" * 60)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"  Training samples: {len(X_train)}")
    print(f"  Testing samples: {len(X_test)}")
    
    print("\n" + "=" * 60)
    print("TRAINING: LINEAR REGRESSION FROM SCRATCH")
    print("=" * 60)
    scratch_model = LinearRegressionScratch(learning_rate=0.1, n_iterations=1000)
    scratch_model.fit(X_train, y_train)
    
    print("\n" + "=" * 60)
    print("TRAINING: SCIKIT-LEARN LINEAR REGRESSION")
    print("=" * 60)
    sklearn_model = LinearRegressionSklearn()
    sklearn_model.fit(X_train, y_train)
    print("  Training complete (uses closed-form solution)")
    
    print("\n" + "=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)
    
    scratch_results = evaluate_model(
        scratch_model, X_train, X_test, y_train, y_test, 
        "Linear Regression (From Scratch)"
    )
    
    sklearn_results = evaluate_model(
        sklearn_model, X_train, X_test, y_train, y_test,
        "Linear Regression (Scikit-learn)"
    )
    
    scratch_pred = scratch_model.predict(X_test)
    sklearn_pred = sklearn_model.predict(X_test)
    
    visualize_training(scratch_model, sklearn_results, scratch_results)
    visualize_predictions(y_test, scratch_pred, sklearn_pred)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("  1. Both implementations achieve similar R² scores")
    print("  2. From-scratch uses gradient descent (iterative)")
    print("  3. Sklearn uses normal equation (closed-form)")
    print("  4. Feature normalization is crucial for gradient descent")
    print("\nOutput Files Generated:")
    print("  - data_exploration.png: Dataset visualizations")
    print("  - training_visualization.png: Training process and comparison")
    print("  - predictions_comparison.png: Actual vs predicted values")
    
    print("\n" + "=" * 60)
    print("EXPERIMENT COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
