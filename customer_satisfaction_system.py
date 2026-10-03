"""
Customer Satisfaction Classification System
Classifies customer feedback using NLP and machine learning
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, roc_curve
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

def generate_feedback_dataset(n_samples=1000, random_state=42):
    """Generate synthetic customer feedback dataset"""
    np.random.seed(random_state)
    
    positive_keywords = ['excellent', 'great', 'amazing', 'wonderful', 'fantastic', 'love', 'perfect', 'outstanding', 'superb', 'brilliant']
    neutral_keywords = ['okay', 'average', 'decent', 'acceptable', 'moderate', 'fair', 'standard', 'normal', 'regular']
    negative_keywords = ['terrible', 'awful', 'horrible', 'bad', 'poor', 'hate', 'disappointed', 'waste', 'useless', 'worst']
    
    feedback_texts = []
    labels = []
    
    for i in range(n_samples):
        sentiment = np.random.choice([0, 1, 2], p=[0.3, 0.35, 0.35])  # 0=negative, 1=neutral, 2=positive
        
        if sentiment == 2:  # Positive
            keywords = np.random.choice(positive_keywords, size=np.random.randint(2, 4))
            text = f"This product is {keywords[0]}. I really {keywords[1] if len(keywords) > 1 else 'love'} it. Highly recommend!"
        elif sentiment == 1:  # Neutral
            keywords = np.random.choice(neutral_keywords, size=np.random.randint(1, 3))
            text = f"The product is {keywords[0]}. It's {keywords[1] if len(keywords) > 1 else 'okay'}. Nothing special but works."
        else:  # Negative
            keywords = np.random.choice(negative_keywords, size=np.random.randint(2, 4))
            text = f"This is {keywords[0]}. I'm very {keywords[1] if len(keywords) > 1 else 'disappointed'}. Would not recommend."
        
        feedback_texts.append(text)
        labels.append(sentiment)
    
    df = pd.DataFrame({
        'Feedback_ID': [f'FB{i:04d}' for i in range(n_samples)],
        'Customer_Feedback': feedback_texts,
        'Satisfaction_Level': labels
    })
    
    return df

def extract_text_features(texts):
    """Extract TF-IDF features from text"""
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english', ngram_range=(1, 2))
    features = vectorizer.fit_transform(texts)
    return features, vectorizer

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple satisfaction classification models"""
    models = {}
    results = []
    
    # Logistic Regression
    print("Training Logistic Regression...")
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    y_proba_lr = lr.predict_proba(X_test)[:, 1] if lr.predict_proba(X_test).shape[1] > 1 else lr.predict_proba(X_test)[:, 0]
    
    models['Logistic Regression'] = lr
    results.append({
        'Model': 'Logistic Regression',
        'Accuracy': accuracy_score(y_test, y_pred_lr),
        'Precision': precision_score(y_test, y_pred_lr, average='weighted', zero_division=0),
        'Recall': recall_score(y_test, y_pred_lr, average='weighted', zero_division=0),
        'F1-Score': f1_score(y_test, y_pred_lr, average='weighted', zero_division=0)
    })
    
    # Random Forest
    print("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    
    models['Random Forest'] = rf
    results.append({
        'Model': 'Random Forest',
        'Accuracy': accuracy_score(y_test, y_pred_rf),
        'Precision': precision_score(y_test, y_pred_rf, average='weighted', zero_division=0),
        'Recall': recall_score(y_test, y_pred_rf, average='weighted', zero_division=0),
        'F1-Score': f1_score(y_test, y_pred_rf, average='weighted', zero_division=0)
    })
    
    # Gradient Boosting
    print("Training Gradient Boosting...")
    gb = GradientBoostingClassifier(n_estimators=100, random_state=42)
    gb.fit(X_train, y_train)
    y_pred_gb = gb.predict(X_test)
    
    models['Gradient Boosting'] = gb
    results.append({
        'Model': 'Gradient Boosting',
        'Accuracy': accuracy_score(y_test, y_pred_gb),
        'Precision': precision_score(y_test, y_pred_gb, average='weighted', zero_division=0),
        'Recall': recall_score(y_test, y_pred_gb, average='weighted', zero_division=0),
        'F1-Score': f1_score(y_test, y_pred_gb, average='weighted', zero_division=0)
    })
    
    return models, pd.DataFrame(results), y_pred_rf

def plot_satisfaction_distribution(df):
    """Plot satisfaction level distribution"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    satisfaction_counts = df['Satisfaction_Level'].value_counts().sort_index()
    labels_map = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
    colors = ['#e74c3c', '#f39c12', '#2ecc71']
    
    axes[0].bar([labels_map[i] for i in satisfaction_counts.index], satisfaction_counts.values, 
               color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0].set_ylabel('Count', fontsize=11, fontweight='bold')
    axes[0].set_title('Customer Satisfaction Distribution', fontsize=12, fontweight='bold')
    axes[0].grid(axis='y', alpha=0.3)
    
    for i, v in enumerate(satisfaction_counts.values):
        axes[0].text(i, v + 10, str(v), ha='center', fontweight='bold')
    
    # Satisfaction percentages
    satisfaction_pct = (satisfaction_counts / len(df) * 100).round(2)
    axes[1].pie(satisfaction_pct.values, labels=[labels_map[i] for i in satisfaction_pct.index],
               colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
    axes[1].set_title('Satisfaction Level Distribution (%)', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/satisfaction_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved: satisfaction_distribution.png")
    plt.close()

def plot_model_comparison(results_df):
    """Plot model performance comparison"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    x = np.arange(len(results_df))
    width = 0.2
    
    for idx, metric in enumerate(metrics):
        axes[0].bar(x + idx * width, results_df[metric], width, label=metric, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    axes[0].set_xlabel('Model', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Score', fontsize=11, fontweight='bold')
    axes[0].set_title('Model Performance Comparison', fontsize=12, fontweight='bold')
    axes[0].set_xticks(x + width * 1.5)
    axes[0].set_xticklabels(results_df['Model'], fontsize=10)
    axes[0].legend(fontsize=9, loc='lower right')
    axes[0].grid(axis='y', alpha=0.3)
    axes[0].set_ylim([0, 1.1])
    
    # Accuracy comparison
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    axes[1].bar(results_df['Model'], results_df['Accuracy'], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1].set_ylabel('Accuracy', fontsize=11, fontweight='bold')
    axes[1].set_title('Model Accuracy Comparison', fontsize=12, fontweight='bold')
    axes[1].grid(axis='y', alpha=0.3)
    axes[1].set_ylim([0, 1.1])
    
    for i, v in enumerate(results_df['Accuracy']):
        axes[1].text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/satisfaction_model_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: satisfaction_model_comparison.png")
    plt.close()

def plot_confusion_matrices(models, X_test, y_test):
    """Plot confusion matrices"""
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    
    labels_map = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
    
    for idx, (model_name, model) in enumerate(models.items()):
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                   xticklabels=[labels_map[i] for i in range(3)],
                   yticklabels=[labels_map[i] for i in range(3)],
                   cbar=False, annot_kws={'fontsize': 10, 'fontweight': 'bold'})
        axes[idx].set_title(f'{model_name}', fontsize=12, fontweight='bold')
        axes[idx].set_ylabel('True Label', fontsize=10, fontweight='bold')
        axes[idx].set_xlabel('Predicted Label', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/satisfaction_confusion_matrices.png', dpi=300, bbox_inches='tight')
    print("Saved: satisfaction_confusion_matrices.png")
    plt.close()

def plot_feature_importance(models):
    """Plot feature importance"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Random Forest
    rf = models['Random Forest']
    feature_importance_rf = pd.DataFrame({
        'Feature': range(len(rf.feature_importances_)),
        'Importance': rf.feature_importances_
    }).sort_values('Importance', ascending=False).head(10)
    
    axes[0].barh(feature_importance_rf['Feature'].astype(str), feature_importance_rf['Importance'],
                color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0].set_xlabel('Importance', fontsize=11, fontweight='bold')
    axes[0].set_title('Random Forest - Top 10 Features', fontsize=12, fontweight='bold')
    axes[0].invert_yaxis()
    axes[0].grid(axis='x', alpha=0.3)
    
    # Gradient Boosting
    gb = models['Gradient Boosting']
    feature_importance_gb = pd.DataFrame({
        'Feature': range(len(gb.feature_importances_)),
        'Importance': gb.feature_importances_
    }).sort_values('Importance', ascending=False).head(10)
    
    axes[1].barh(feature_importance_gb['Feature'].astype(str), feature_importance_gb['Importance'],
                color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1].set_xlabel('Importance', fontsize=11, fontweight='bold')
    axes[1].set_title('Gradient Boosting - Top 10 Features', fontsize=12, fontweight='bold')
    axes[1].invert_yaxis()
    axes[1].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/satisfaction_feature_importance.png', dpi=300, bbox_inches='tight')
    print("Saved: satisfaction_feature_importance.png")
    plt.close()

def plot_sentiment_trends(df):
    """Plot sentiment analysis trends"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    labels_map = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
    colors = ['#e74c3c', '#f39c12', '#2ecc71']
    
    # Sentiment distribution by category
    satisfaction_counts = df['Satisfaction_Level'].value_counts().sort_index()
    axes[0, 0].bar([labels_map[i] for i in satisfaction_counts.index], satisfaction_counts.values,
                  color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0, 0].set_ylabel('Count', fontsize=10, fontweight='bold')
    axes[0, 0].set_title('Sentiment Distribution', fontsize=11, fontweight='bold')
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # Feedback length by sentiment
    df['Feedback_Length'] = df['Customer_Feedback'].str.len()
    feedback_by_sentiment = df.groupby('Satisfaction_Level')['Feedback_Length'].mean()
    axes[0, 1].bar([labels_map[i] for i in feedback_by_sentiment.index], feedback_by_sentiment.values,
                  color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0, 1].set_ylabel('Average Length', fontsize=10, fontweight='bold')
    axes[0, 1].set_title('Average Feedback Length by Sentiment', fontsize=11, fontweight='bold')
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # Word count by sentiment
    df['Word_Count'] = df['Customer_Feedback'].str.split().str.len()
    word_by_sentiment = df.groupby('Satisfaction_Level')['Word_Count'].mean()
    axes[1, 0].bar([labels_map[i] for i in word_by_sentiment.index], word_by_sentiment.values,
                  color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1, 0].set_ylabel('Average Word Count', fontsize=10, fontweight='bold')
    axes[1, 0].set_title('Average Word Count by Sentiment', fontsize=11, fontweight='bold')
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Sentiment percentage
    sentiment_pct = (satisfaction_counts / len(df) * 100).round(2)
    axes[1, 1].pie(sentiment_pct.values, labels=[labels_map[i] for i in sentiment_pct.index],
                  colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
    axes[1, 1].set_title('Sentiment Distribution (%)', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/satisfaction_sentiment_trends.png', dpi=300, bbox_inches='tight')
    print("Saved: satisfaction_sentiment_trends.png")
    plt.close()

def main():
    print("="*80)
    print("CUSTOMER SATISFACTION CLASSIFICATION SYSTEM")
    print("="*80)
    
    # Generate dataset
    print("\n[1] Generating synthetic customer feedback dataset...")
    df = generate_feedback_dataset(n_samples=1000)
    df.to_csv('/home/ubuntu/satisfaction_data.csv', index=False)
    print(f"Dataset generated: {len(df)} customer reviews")
    satisfaction_counts = df['Satisfaction_Level'].value_counts().sort_index()
    print(f"Negative: {satisfaction_counts.get(0, 0)}, Neutral: {satisfaction_counts.get(1, 0)}, Positive: {satisfaction_counts.get(2, 0)}")
    
    # Extract features
    print("\n[2] Extracting TF-IDF features from feedback...")
    X, vectorizer = extract_text_features(df['Customer_Feedback'].values)
    y = df['Satisfaction_Level'].values
    print(f"Feature matrix shape: {X.shape}")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training set: {X_train.shape[0]}, Test set: {X_test.shape[0]}")
    
    # Train models
    print("\n[3] Training satisfaction classification models...")
    models, results_df, y_pred_rf = train_models(X_train, X_test, y_train, y_test)
    results_df.to_csv('/home/ubuntu/satisfaction_model_results.csv', index=False)
    print("\nModel Results:")
    print(results_df.to_string(index=False))
    
    # Generate visualizations
    print("\n[4] Generating visualizations...")
    plot_satisfaction_distribution(df)
    plot_model_comparison(results_df)
    plot_confusion_matrices(models, X_test, y_test)
    plot_feature_importance(models)
    plot_sentiment_trends(df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - All visualizations saved")
    print("="*80)

if __name__ == "__main__":
    main()
