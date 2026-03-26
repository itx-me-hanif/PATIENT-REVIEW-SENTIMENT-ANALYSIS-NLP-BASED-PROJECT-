# 📖 User Guide & Code Examples

## 🚀 Running the Project

### Option 1: Quick Start (Recommended)
```bash
python sentiment_analyzer.py
```
This will automatically:
- Install missing dependencies
- Load or generate sample data
- Perform sentiment analysis
- Generate visualizations

### Option 2: Using the Quickstart Script
```bash
python quickstart.py
```
Simplified version with essential functionality.

### Option 3: Run from Python Code
```python
from sentiment_analyzer import (
    analyze_patient_reviews,
    create_pie_chart,
    create_bar_chart
)

# Run analysis
df, sentiment_counts = analyze_patient_reviews(
    input_csv='Inputs/patient_reviews.csv',
    output_csv='Outputs/patient_reviews_with_sentiment.csv',
    generate_if_missing=True
)

# Create charts
create_pie_chart(sentiment_counts)
create_bar_chart(sentiment_counts)
```

---

## 💾 Working with Your Own Data

### Step 1: Prepare Your CSV File
Your file must have a `review` column with patient review text:

```csv
patient_id,date,review
P001,2025-11-01,"Great service and caring doctors"
P002,2025-11-02,"Worst experience ever. Very rude staff"
P003,2025-11-03,"Average. Nothing special"
```

### Step 2: Update the Script
Modify the input filename in `sentiment_analyzer.py`:

```python
df_results, sentiment_counts = analyze_patient_reviews(
    input_csv='your_file.csv',  # Change this
    output_csv='results.csv',
    generate_if_missing=False   # Don't generate if you have data
)

Note: `analyze_patient_reviews()` now includes a preprocessing pipeline. After running, you will find two additional files in the `Outputs/` folder:
- `Outputs/patient_reviews_preprocessed.csv` — cleaned reviews used for sentiment analysis (column `preprocessed_text`)
- `Outputs/patient_reviews_removed.csv` — reviews removed during preprocessing with a `remove_reason` column for auditing

If this is your first time using the preprocessing features, download required NLTK corpora:

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```
```

### Step 3: Run
```bash
python sentiment_analyzer.py
```

---

## 📊 Advanced Usage Examples

### Example 1: Custom Sentiment Thresholds
```python
def analyze_sentiment_custom(review_text):
    """Custom sentiment thresholds"""
    from textblob import TextBlob
    
    blob = TextBlob(str(review_text))
    polarity = blob.sentiment.polarity
    
    # More strict thresholds
    if polarity > 0.3:
        return polarity, 'Very Positive'
    elif polarity > 0.1:
        return polarity, 'Positive'
    elif polarity < -0.3:
        return polarity, 'Very Negative'
    elif polarity < -0.1:
        return polarity, 'Negative'
    else:
        return polarity, 'Neutral'

# Use in your analysis
polarity, sentiment = analyze_sentiment_custom(
    "This was an amazing experience!"
)
print(f"Sentiment: {sentiment} (Score: {polarity})")
```

### Example 2: Filter Reviews by Sentiment
```python
import pandas as pd

# Load the results
df = pd.read_csv('patient_reviews_with_sentiment.csv')

# Get positive reviews
positive_reviews = df[df['sentiment'] == 'Positive']
print(f"Positive reviews: {len(positive_reviews)}")

# Get negative reviews
negative_reviews = df[df['sentiment'] == 'Negative']
print(f"Negative reviews: {len(negative_reviews)}")

# Export only negative reviews
negative_reviews.to_csv('negative_reviews_only.csv', index=False)
```

### Example 3: Generate Statistics Report
```python
import pandas as pd

df = pd.read_csv('patient_reviews_with_sentiment.csv')

# Calculate statistics
stats = {
    'Total Reviews': len(df),
    'Positive Count': len(df[df['sentiment'] == 'Positive']),
    'Negative Count': len(df[df['sentiment'] == 'Negative']),
    'Neutral Count': len(df[df['sentiment'] == 'Neutral']),
    'Average Polarity': df['polarity_score'].mean(),
    'Min Polarity': df['polarity_score'].min(),
    'Max Polarity': df['polarity_score'].max(),
    'Std Deviation': df['polarity_score'].std(),
}

# Print report
print("\n📊 SENTIMENT ANALYSIS REPORT")
print("=" * 40)
for key, value in stats.items():
    if isinstance(value, float):
        print(f"{key}: {value:.4f}")
    else:
        print(f"{key}: {value}")

# Calculate percentages
total = stats['Total Reviews']
print("\n📈 SENTIMENT BREAKDOWN")
print(f"Positive: {(stats['Positive Count']/total*100):.1f}%")
print(f"Negative: {(stats['Negative Count']/total*100):.1f}%")
print(f"Neutral:  {(stats['Neutral Count']/total*100):.1f}%")
```

### Example 4: Analyze by Date Range (if date column exists)
```python
import pandas as pd

df = pd.read_csv('patient_reviews_with_sentiment.csv')
df['date'] = pd.to_datetime(df['date'])

# Filter by date range
oct_reviews = df[(df['date'] >= '2025-10-01') & 
                 (df['date'] < '2025-11-01')]

print(f"October reviews: {len(oct_reviews)}")
print(f"Positive: {len(oct_reviews[oct_reviews['sentiment'] == 'Positive'])}")
print(f"Negative: {len(oct_reviews[oct_reviews['sentiment'] == 'Negative'])}")
```

### Example 5: Process Multiple CSV Files
```python
from sentiment_analyzer import analyze_patient_reviews
import os

# Process all CSV files in a folder
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

for csv_file in csv_files:
    print(f"\nProcessing {csv_file}...")
    df, sentiment_counts = analyze_patient_reviews(
        input_csv=csv_file,
        output_csv=f"analyzed_{csv_file}",
        generate_if_missing=False
    )
    print(f"Done! Results saved to analyzed_{csv_file}")
```

---

## 🎯 Sentiment Score Interpretation

### Understanding Polarity Scores

| Score Range | Sentiment | Meaning |
|---|---|---|
| 1.0 | Very Positive | Extremely positive, strong praise |
| 0.3 to 1.0 | Positive | Favorable review with praise |
| 0.1 to 0.3 | Slightly Positive | Mostly positive |
| -0.1 to 0.1 | Neutral | Balanced or unbiased review |
| -0.3 to -0.1 | Slightly Negative | Mostly negative |
| -1.0 to -0.3 | Negative | Unfavorable review with criticism |
| -1.0 | Very Negative | Extremely negative, strong complaint |

### Classification Rules (Default)
- **Positive**: polarity > 0.1 ✨
- **Neutral**: -0.1 ≤ polarity ≤ 0.1 😐
- **Negative**: polarity < -0.1 😔

---

## 🔧 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'textblob'"

**Solution 1**: Let the script install it automatically (run normally)

**Solution 2**: Manual installation
```bash
pip install textblob
python -m textblob.download_corpora
```
```bash
# If you use preprocessing features, also ensure NLTK corpora are available:
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

### Problem: "KeyError: 'review' - column not found"

**Solution**: Your CSV file doesn't have a 'review' column.
- Rename your column to 'review'
- Or modify the script to use your column name:

```python
# In analyze_patient_reviews(), change:
for idx, review in enumerate(df['your_column_name']):  # Your column here
```

### Problem: Script is very slow

**Possible causes**:
- Large number of reviews (1000+ is normal and expected)
- Slow computer or disk
- TextBlob corpora not properly loaded

**Solution**: Be patient! 1000 reviews take 30-60 seconds typically.

### Problem: Charts not showing

**Solution**: Charts are saved as PNG files in the project folder
- Check folder: `c:\Users\MUHAMMAD HANIF\OneDrive\Desktop\NLP & AI\sentiment_analysis_project`
- Files: `sentiment_pie_chart.png` and `sentiment_bar_chart.png`
- Open with any image viewer

---

## 📈 Visualization Customization

### Change Chart Colors
Edit the `create_pie_chart()` and `create_bar_chart()` functions:

```python
colors = {
    'Positive': '#FF6B6B',  # Red instead of green
    'Negative': '#4ECDC4',  # Teal instead of red
    'Neutral': '#FFE66D'    # Yellow instead of gray
}
```

### Change Chart Size
```python
# In create_pie_chart():
fig, ax = plt.subplots(figsize=(12, 10))  # Larger chart

# In create_bar_chart():
fig, ax = plt.subplots(figsize=(14, 8))   # Wider chart
```

### Save in Different Format
```python
# Change PNG to JPG, PDF, SVG, etc.
plt.savefig(output_path.replace('.png', '.jpg'), dpi=300)
# or
plt.savefig(output_path.replace('.png', '.pdf'), dpi=300)
```

---

## 💡 Tips & Best Practices

1. **Always backup original CSV**: Before running, keep a copy of your original data
2. **Use meaningful column names**: Include 'review' column for best results
3. **Clean data**: Remove special characters if possible before analysis
4. **Check sample**: Review first few rows of output to verify accuracy
5. **Adjust thresholds**: If results seem off, fine-tune sentiment thresholds
6. **Large datasets**: For 10,000+ reviews, consider processing in batches
7. **Version control**: Keep track of analysis results with timestamps

---

## 🚀 Performance Tips

For large datasets (10,000+ reviews):

```python
# Process in batches
import pandas as pd

csv_file = 'patient_reviews.csv'
chunksize = 1000
chunks = pd.read_csv(csv_file, chunksize=chunksize)

for i, chunk in enumerate(chunks):
    print(f"Processing chunk {i+1}...")
    # Analyze each chunk
    # Save results
```

---

## 📞 Support

If you encounter issues:
1. Check this guide first
2. Review console error messages carefully
3. Verify CSV format matches expected structure
4. Try with sample data first
5. Check Python version: `python --version` (need 3.7+)

---

## 🎓 Learning Resources

- **TextBlob Sentiment**: https://textblob.readthedocs.io/
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Matplotlib Guide**: https://matplotlib.org/stable/contents.html
- **Sentiment Analysis Basics**: https://en.wikipedia.org/wiki/Sentiment_analysis

---

**Happy analyzing! 📊✨**
