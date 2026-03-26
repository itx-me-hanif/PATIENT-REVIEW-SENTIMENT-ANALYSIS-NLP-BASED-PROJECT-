# ⚙️ Configuration & Customization Guide

## 📋 Project Configuration

This guide shows how to customize the sentiment analyzer to fit your needs.

---

## 1. Input/Output File Names

### Default Configuration (project layout uses Inputs/ and Outputs/)
```python
analyze_patient_reviews(
    input_csv='Inputs/patient_reviews.csv',
    output_csv='Outputs/patient_reviews_with_sentiment.csv',
    generate_if_missing=True
)
```

### Custom File Names
```python
analyze_patient_reviews(
    input_csv='healthcare_feedback.csv',
    output_csv='analysis_results.csv',
    generate_if_missing=False
)

create_pie_chart(sentiment_counts, 'my_pie_chart.png')
create_bar_chart(sentiment_counts, 'my_bar_chart.png')
```

---

## 2. Sample Data Generation

### Generate Different Number of Reviews
```python
# Generate 500 reviews instead of 1000
generate_sample_reviews('patient_reviews.csv', num_reviews=500)

# Generate 5000 reviews
generate_sample_reviews('patient_reviews.csv', num_reviews=5000)
```

### Add Custom Sample Reviews
Edit `generate_sample_reviews()` in `sentiment_analyzer.py`:

```python
positive_reviews = [
    "Outstanding service, highly satisfied!",
    "Excellent care and attention to detail",
    "Amazing experience, would return",
    "Your custom reviews here...",
]

negative_reviews = [
    "Poor service and rude staff",
    "Disappointed with the care received",
    "Waste of time and money",
    "Your custom reviews here...",
]

neutral_reviews = [
    "It was okay, average experience",
    "Nothing special, standard service",
    "Adequate but unremarkable",
    "Your custom reviews here...",
]
```

---

## 3. Sentiment Classification Thresholds

### Default Thresholds
```python
if polarity > 0.1:
    sentiment = 'Positive'
elif polarity < -0.1:
    sentiment = 'Negative'
else:
    sentiment = 'Neutral'
```

### Stricter Classification
```python
if polarity > 0.3:
    sentiment = 'Positive'
elif polarity < -0.3:
    sentiment = 'Negative'
else:
    sentiment = 'Neutral'
```

### More Granular Classification (Multi-level)
```python
def analyze_sentiment(review_text):
    """Enhanced sentiment analysis with 5 levels"""
    from textblob import TextBlob
    
    blob = TextBlob(str(review_text))
    polarity = blob.sentiment.polarity
    
    if polarity >= 0.5:
        sentiment = 'Very Positive'
    elif polarity > 0.1:
        sentiment = 'Positive'
    elif polarity > -0.1:
        sentiment = 'Neutral'
    elif polarity > -0.5:
        sentiment = 'Negative'
    else:
        sentiment = 'Very Negative'
    
    return polarity, sentiment
```

### Custom Threshold Configuration
```python
# Make thresholds configurable
SENTIMENT_THRESHOLDS = {
    'positive_threshold': 0.15,
    'negative_threshold': -0.15,
}

def analyze_sentiment(review_text):
    from textblob import TextBlob
    
    blob = TextBlob(str(review_text))
    polarity = blob.sentiment.polarity
    
    if polarity > SENTIMENT_THRESHOLDS['positive_threshold']:
        sentiment = 'Positive'
    elif polarity < SENTIMENT_THRESHOLDS['negative_threshold']:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    return polarity, sentiment
```

---

## 4. Visualization Customization

### Change Chart Colors
```python
def create_pie_chart(sentiment_counts, output_path='sentiment_pie_chart.png'):
    colors = {
        'Positive': '#1abc9c',  # Turquoise
        'Negative': '#e74c3c',  # Red
        'Neutral': '#95a5a6'    # Gray
    }
    # ... rest of code
```

### Color Palette Options
```python
# Professional palette
colors = {
    'Positive': '#27AE60',  # Green
    'Negative': '#C0392B',  # Dark Red
    'Neutral': '#34495E'    # Dark Blue Gray
}

# Vibrant palette
colors = {
    'Positive': '#00D2FC',  # Cyan
    'Negative': '#FF6B6B',  # Red
    'Neutral': '#FFE66D'    # Yellow
}

# Pastel palette
colors = {
    'Positive': '#A8E6CF',  # Mint
    'Negative': '#FFB3BA',  # Light Pink
    'Neutral': '#FFFFBA'    # Light Yellow
}
```

### Change Chart Size
```python
# Larger charts
fig, ax = plt.subplots(figsize=(14, 10))  # Wider and taller

# Wider bar chart
fig, ax = plt.subplots(figsize=(16, 6))

# Compact chart
fig, ax = plt.subplots(figsize=(8, 6))
```

### Save Charts in Different Formats
```python
# Save as multiple formats
formats = ['png', 'jpg', 'pdf', 'svg']

for fmt in formats:
    plt.savefig(f'sentiment_pie_chart.{fmt}', dpi=300, bbox_inches='tight')
    print(f"✅ Saved as {fmt}")
```

### Add Chart Annotations
```python
def create_bar_chart_with_annotations(sentiment_counts):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    labels = sentiment_counts.index.tolist()
    values = sentiment_counts.values.tolist()
    
    bars = ax.bar(labels, values, color=['#2ecc71', '#e74c3c', '#95a5a6'])
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}\n({height/sum(values)*100:.1f}%)',
                ha='center', va='bottom', fontsize=11, weight='bold')
    
    ax.set_title('Patient Review Sentiment Distribution', fontsize=14, weight='bold')
    plt.tight_layout()
    plt.savefig('sentiment_bar_chart_annotated.png', dpi=300)
```

---

## 5. Console Output Customization

### Reduce Verbosity
```python
# Skip progress updates
print(f"Processing {len(df)} reviews...")
for idx, review in enumerate(df['review']):
    polarity, sentiment = analyze_sentiment(review)
    df.at[idx, 'polarity_score'] = polarity
    df.at[idx, 'sentiment'] = sentiment
    # Only print every 500 reviews instead of every 100
    if (idx + 1) % 500 == 0:
        print(f"   ✅ Processed {idx + 1}/{len(df)} reviews")
```

### Add More Detailed Logging
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sentiment_analysis.log'),
        logging.StreamHandler()
    ]
)

# Use in code
logging.info(f"Processing file: {input_csv}")
logging.debug(f"Polarity score: {polarity}")
```

---

## 6. Error Handling Customization

### Custom Error Messages
```python
def analyze_sentiment(review_text):
    """Enhanced error handling"""
    try:
        if not review_text or str(review_text).strip() == '':
            return 0, 'Neutral'  # Empty review = Neutral
        
        blob = TextBlob(str(review_text))
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            sentiment = 'Positive'
        elif polarity < -0.1:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return polarity, sentiment
    
    except Exception as e:
        logging.error(f"Error analyzing review: {e}")
        return 0, 'Neutral'
```

### Validation Before Processing
```python
def validate_csv(input_csv):
    """Validate CSV before processing"""
    try:
        df = pd.read_csv(input_csv)
        
        # Check for required column
        if 'review' not in df.columns:
            raise ValueError("Missing 'review' column")
        
        # Check for empty dataframe
        if len(df) == 0:
            raise ValueError("CSV file is empty")
        
        # Check for null reviews
        null_count = df['review'].isnull().sum()
        if null_count > 0:
            logging.warning(f"Found {null_count} null reviews, will be treated as Neutral")
        
        return True
    
    except Exception as e:
        logging.error(f"CSV validation failed: {e}")
        return False
```

---

## 7. Performance Optimization

### Process Large Files in Batches
```python
def analyze_patient_reviews_batched(input_csv, batch_size=100):
    """Process large files in batches"""
    df = pd.read_csv(input_csv)
    results = []
    
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}...")
        
        for idx, review in enumerate(batch['review']):
            polarity, sentiment = analyze_sentiment(review)
            results.append({
                'patient_id': batch.iloc[idx].get('patient_id', ''),
                'review': review,
                'polarity_score': polarity,
                'sentiment': sentiment
            })
    
    return pd.DataFrame(results)
```

### Parallel Processing (Advanced)
```python
from multiprocessing import Pool

def analyze_sentiment_wrapper(review):
    """Wrapper for multiprocessing"""
    return analyze_sentiment(review)

def analyze_patient_reviews_parallel(df, num_processes=4):
    """Use multiple processes for faster analysis"""
    with Pool(num_processes) as pool:
        sentiments = pool.map(analyze_sentiment_wrapper, df['review'])
    
    df[['polarity_score', 'sentiment']] = pd.DataFrame(sentiments)
    return df
```

---

## 8. Environment Configuration

### Create Configuration File
`config.py`:
```python
# Configuration file for sentiment analyzer

# File paths
INPUT_CSV = 'Inputs/patient_reviews.csv'
OUTPUT_CSV = 'Outputs/patient_reviews_with_sentiment.csv'
PIE_CHART_PATH = 'Outputs/sentiment_pie_chart.png'
BAR_CHART_PATH = 'Outputs/sentiment_bar_chart.png'

# Sentiment thresholds
POSITIVE_THRESHOLD = 0.1
NEGATIVE_THRESHOLD = -0.1

# Sample data generation
GENERATE_SAMPLE_IF_MISSING = True
NUM_SAMPLE_REVIEWS = 1000

# Chart settings
CHART_DPI = 300
CHART_FIGSIZE_PIE = (10, 8)
CHART_FIGSIZE_BAR = (10, 6)

# Colors
SENTIMENT_COLORS = {
    'Positive': '#2ecc71',
    'Negative': '#e74c3c',
    'Neutral': '#95a5a6'
}

# Logging
LOG_FILE = 'sentiment_analysis.log'
LOG_LEVEL = 'INFO'
```

---

## 9. Preprocessing & Removed Rows

The analyzer now includes a preprocessing pipeline that runs before sentiment analysis. The pipeline performs steps such as:
- HTML stripping (`beautifulsoup4`)
- Contraction expansion (`contractions`)
- Emoji demojize (`emoji`)
- Lowercasing and punctuation/number removal
- Tokenization and stopword removal (`nltk`)
- Lemmatization (`nltk.wordnet`) and POS tagging
- Simple spell-check heuristics (`pyspellchecker`) to flag many misspellings

Outputs created by preprocessing:
- `patient_reviews_preprocessed.csv`: contains the cleaned/preprocessed text used for sentiment analysis (column `preprocessed_text`)
- `patient_reviews_removed.csv`: contains rows that were dropped during preprocessing. Each dropped row includes a `remove_reason` such as `empty_after_cleaning`, `non_english_characters`, or `many_misspellings` for auditing.

Configuration tips:
- If you want to skip heavy preprocessing (spell-check or POS tagging) for performance, add flags in `analyze_patient_reviews()` to toggle individual steps.
- Ensure NLTK corpora are available on the machine or download them on first run:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```


### Use Configuration in Main Script
```python
from config import *

# In analyze_patient_reviews():
df_results, sentiment_counts = analyze_patient_reviews(
    input_csv=INPUT_CSV,
    output_csv=OUTPUT_CSV,
    generate_if_missing=GENERATE_SAMPLE_IF_MISSING
)
```

---

## 9. Database Integration (Optional)

### Save Results to SQLite
```python
import sqlite3

def save_to_database(df, db_name='sentiment_analysis.db'):
    """Save results to SQLite database"""
    conn = sqlite3.connect(db_name)
    df.to_sql('reviews', conn, if_exists='replace', index=False)
    conn.close()
    print(f"✅ Results saved to {db_name}")

# Usage
save_to_database(df_results)
```

### Query Database
```python
import sqlite3
import pandas as pd

def query_database(db_name='sentiment_analysis.db', sentiment=None):
    """Query saved results"""
    conn = sqlite3.connect(db_name)
    
    if sentiment:
        query = f"SELECT * FROM reviews WHERE sentiment = '{sentiment}'"
    else:
        query = "SELECT * FROM reviews"
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df
```

---

## 🎯 Quick Customization Checklist

- [ ] Change input CSV filename
- [ ] Change output CSV filename
- [ ] Adjust sentiment thresholds
- [ ] Customize chart colors
- [ ] Change chart sizes
- [ ] Add sample reviews
- [ ] Modify console messages
- [ ] Enable logging
- [ ] Add error handling
- [ ] Configure batch processing

---

## 📝 Environment Variables (Optional)

```bash
# Set environment variables
$env:SENTIMENT_INPUT_CSV = "my_reviews.csv"
$env:SENTIMENT_OUTPUT_CSV = "my_results.csv"

# In Python
import os
input_csv = os.getenv('SENTIMENT_INPUT_CSV', 'patient_reviews.csv')
```

---

**Start customizing! 🚀**
