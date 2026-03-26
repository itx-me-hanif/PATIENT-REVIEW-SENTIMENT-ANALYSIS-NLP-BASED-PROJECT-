# 🩺 Patient Review Sentiment Analysis System

A comprehensive Python project for performing sentiment analysis on patient reviews in healthcare centers. The system reads reviews from a CSV file, classifies them as Positive/Negative/Neutral, and generates insightful visualizations.

## 📋 Features

✅ **Automated Dependency Installation**: Automatically installs missing required packages  
✅ **Sentiment Analysis**: Uses TextBlob for polarity-based sentiment classification  
✅ **Data Generation**: Generates 1000 random sample reviews if no input file exists  
✅ **CSV Output**: Saves results with polarity scores and sentiment labels  
✅ **Visualizations**: Creates both pie and bar charts of sentiment distribution  
✅ **Error Handling**: Comprehensive try/except blocks for robust file handling  
✅ **Progress Tracking**: Friendly console messages with progress indicators (✅, 💾, 📊)  
✅ **Well-Commented**: Detailed comments throughout the code  
✅ **NLP Preprocessing Pipeline**: HTML stripping, contraction expansion, emoji handling, tokenization, stopword removal, lemmatization, simple spell-check heuristics; rows that become empty or invalid are removed and recorded

## 📦 Requirements

- Python 3.7+
- **pandas**: Data manipulation and CSV handling
- **textblob**: Sentiment analysis
- **matplotlib**: Data visualization
- **random**: Random data generation (built-in)
- **nltk**: Tokenization, stopwords, lemmatization, POS tagging (used by preprocessing)
- **beautifulsoup4**: HTML stripping during preprocessing
- **contractions**: Expand common contractions in text
- **emoji**: Convert emojis to text (demojize)
- **pyspellchecker**: Best-effort misspelling detection (heuristic)

The script will automatically install missing dependencies on first run.

## 🚀 Quick Start

### 1. **Run the Script**

```bash
python sentiment_analyzer.py
```

### 2. **What Happens**

1. ✅ Checks and installs missing dependencies
2. 📂 Loads `Inputs/patient_reviews.csv` (or generates 1000 sample reviews if not found)
3. 📊 Performs sentiment analysis on all reviews
3a. 🧹 Preprocesses reviews and writes `patient_reviews_preprocessed.csv` (kept) and `patient_reviews_removed.csv` (dropped rows with `remove_reason`)
4. 💾 Saves results to `patient_reviews_with_sentiment.csv`
5. 📈 Generates pie and bar charts
6. 🎯 Displays summary statistics in console

## 📁 Input File Format

Expected CSV structure with a `review` column:

```csv
patient_id,review
PATIENT_0001,"Doctor was very professional and caring."
PATIENT_0002,"Terrible experience. Long wait times."
PATIENT_0003,"Average service, nothing special."
```

**Required Column**: `review` (text content of patient review)  
**Optional Columns**: Any additional columns (patient_id, date, etc.) are preserved

## 📊 Output Files

### 1. **patient_reviews_with_sentiment.csv**
Enhanced CSV with sentiment analysis results:

```csv
patient_id,review,polarity_score,sentiment
PATIENT_0001,"Doctor was caring...",0.65,Positive
PATIENT_0002,"Terrible experience...",-0.75,Negative
PATIENT_0003,"Average service...",0.05,Neutral
```

**Columns**:
- `polarity_score`: Float between -1.0 (very negative) to 1.0 (very positive)
- `sentiment`: Classification as "Positive", "Negative", or "Neutral"

### 2. **sentiment_pie_chart.png**
Pie chart showing percentage distribution of sentiments with:
- Color coding (Green=Positive, Red=Negative, Gray=Neutral)
- Percentage labels
- Professional styling at 300 DPI

### 3. **sentiment_bar_chart.png**
Bar chart displaying count of each sentiment with:
- Value labels on top of bars
- Thousands separator for readability
- Formatted axes
- Professional styling at 300 DPI

## 📈 Console Output Example

```
======================================================================
🩺 PATIENT REVIEW SENTIMENT ANALYSIS SYSTEM
======================================================================

🔍 Checking for required dependencies...
   ✅ pandas is already installed
   ✅ textblob is already installed
   ✅ matplotlib is already installed

📂 STEP 1: Loading Data...
----------------------------------------------------------------------
✅ Successfully loaded 'patient_reviews.csv'
   📊 Total reviews: 1000

📊 STEP 2: Analyzing Sentiment...
----------------------------------------------------------------------
Processing 1000 reviews...
   ✅ Processed 100/1000 reviews
   ✅ Processed 200/1000 reviews
   ...
   ✅ Sentiment analysis completed for all reviews

💾 STEP 3: Saving Results...
----------------------------------------------------------------------
✅ Results saved to `Outputs/patient_reviews_with_sentiment.csv` (and other artifacts in `Outputs/`)

📈 STEP 4: Summary Statistics
----------------------------------------------------------------------

📊 Sentiment Distribution:
   ✨ Positive: 350 reviews (35.0%)
   😔 Negative: 320 reviews (32.0%)
   😐 Neutral:  330 reviews (33.0%)

   Total Reviews: 1,000
   Average Polarity Score: 0.0234

🎨 STEP 5: Creating Visualizations...
----------------------------------------------------------------------
✅ Pie chart saved to 'sentiment_pie_chart.png'
✅ Bar chart saved to 'sentiment_bar_chart.png'

======================================================================
✅ ANALYSIS COMPLETE!
======================================================================

📁 Output Files Generated:
    💾 CSV:  `Outputs/patient_reviews_with_sentiment.csv`
     💾 CSV:  `Outputs/patient_reviews_preprocessed.csv`
     💾 CSV:  `Outputs/patient_reviews_removed.csv`
    📊 Chart: `Outputs/sentiment_pie_chart.png`
    📊 Chart: `Outputs/sentiment_bar_chart.png`

✨ Thank you for using the Sentiment Analysis System!
```

## 🔧 Customization

### Modify Sentiment Thresholds

Edit the `analyze_sentiment()` function to adjust polarity thresholds:

```python
def analyze_sentiment(review_text):
    blob = TextBlob(str(review_text))
    polarity = blob.sentiment.polarity
    
    if polarity > 0.2:      # Increased threshold
        sentiment = 'Positive'
    elif polarity < -0.2:   # Increased threshold
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    return polarity, sentiment
```

### Generate Custom Sample Data

Edit the sample reviews in `generate_sample_reviews()` function:

```python
positive_reviews = [
    "Your custom positive review...",
    # Add more reviews
]
```

### Change Output File Names

Modify the parameters when calling `analyze_patient_reviews()`:

```python
df_results, sentiment_counts = analyze_patient_reviews(
    input_csv='your_file.csv',
    output_csv='your_output.csv',
    generate_if_missing=True
)
```

## 🛠️ Sentiment Analysis Method

The script uses **TextBlob's sentiment polarity** scoring:

- **Polarity**: Ranges from -1.0 (completely negative) to 1.0 (completely positive)
  - Polarity > 0.1 → **Positive** ✨
  - Polarity < -0.1 → **Negative** 😔
  - -0.1 ≤ Polarity ≤ 0.1 → **Neutral** 😐

## ❓ Troubleshooting

### Issue: Module not found error
**Solution**: The script automatically installs dependencies. If issues persist, manually run:
```bash
pip install pandas textblob matplotlib
python -m textblob.download_corpora
# For preprocessing you may also need to download NLTK corpora:
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

### Issue: 'review' column not found
**Solution**: Ensure your CSV has a column named exactly `review`. Rename if necessary.

### Issue: No input file
**Solution**: The script automatically generates 1000 sample reviews. Or provide `patient_reviews.csv` in the same directory.

### Issue: Charts not displaying
**Solution**: Charts are saved as PNG files. Open them with an image viewer. File paths are shown in console output.

## 📚 Code Structure

```
sentiment_analyzer.py
├── install_missing_dependencies()    # Auto-install packages
├── generate_sample_reviews()         # Generate random data
├── analyze_sentiment()               # Single review analysis
├── analyze_patient_reviews()         # Main analysis pipeline
├── create_pie_chart()                # Pie visualization
├── create_bar_chart()                # Bar visualization
└── if __name__ == "__main__":       # Entry point
```

## 📝 License

Open source - Free to use and modify

## 👨‍💻 Author

Healthcare Analytics Team  
November 2025

---

**Happy Analyzing! 🎉**
