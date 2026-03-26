# 🩺 Patient Review Sentiment Analysis System
## 📑 Complete Project Index

Welcome to your sentiment analysis project! This file serves as your navigation guide.

---

## 🚀 **START HERE**

### 1️⃣ Run the Analyzer (30 seconds)
```bash
python sentiment_analyzer.py
```

### 2️⃣ View the Results
- `patient_reviews_preprocessed.csv` - Preprocessed reviews used for sentiment analysis
- `patient_reviews_removed.csv` - Reviews removed during preprocessing (with reason)
- `patient_reviews_with_sentiment.csv` - CSV with analysis
- `sentiment_pie_chart.png` - Pie chart
- `sentiment_bar_chart.png` - Bar chart

---

## 📁 **Project Files**

### 🔴 **MAIN SCRIPTS**

| File | Purpose | Run With |
|------|---------|----------|
| `sentiment_analyzer.py` | Main script with all features | `python sentiment_analyzer.py` |
| `quickstart.py` | Simplified entry point | `python quickstart.py` |

### 🟢 **DATA FILES**

| File | Description |
|------|---|
| `sample_patient_reviews.csv` | Example input format (10 reviews) |
| `patient_reviews.csv` | Generated sample data (1000 reviews) |
| `patient_reviews_preprocessed.csv` | Preprocessed reviews used for sentiment analysis |
| `patient_reviews_removed.csv` | Rows removed by preprocessing (includes `remove_reason`) |
| `patient_reviews_with_sentiment.csv` | Analysis results with sentiment labels |

### 🔵 **VISUALIZATION**

| File | Description |
|------|---|
| `sentiment_pie_chart.png` | Pie chart of sentiment distribution |
| `sentiment_bar_chart.png` | Bar chart of sentiment counts |

### 📚 **DOCUMENTATION**

| File | Read For |
|------|----------|
| **README.md** | Overview, features, installation, troubleshooting |
| **USER_GUIDE.md** | Code examples, advanced usage, tips |
| **CONFIGURATION.md** | Customization options, advanced features |
| **PROJECT_SUMMARY.md** | Complete project summary and next steps |
| **requirements.txt** | List of Python package dependencies |
| **INDEX.md** | This navigation file |

---

## 📖 **DOCUMENTATION GUIDE**

### 🎯 **If you want to...**

#### **Get Started Quickly**
→ Run: `python sentiment_analyzer.py`

#### **Understand Features**
→ Read: `README.md`

#### **See Code Examples**
→ Read: `USER_GUIDE.md`

#### **Customize Behavior**
→ Read: `CONFIGURATION.md`

#### **View Project Overview**
→ Read: `PROJECT_SUMMARY.md`

#### **Troubleshoot Issues**
→ Check `README.md` "Troubleshooting" section or `USER_GUIDE.md`

---

## 🎨 **QUICK REFERENCE**

### CSV Input Format
```csv
patient_id,review
PATIENT_001,Doctor was great!
PATIENT_002,Terrible experience.
```
**Required Column**: `review`

### CSV Output Format
```csv
patient_id,review,polarity_score,sentiment
PATIENT_001,Doctor was great!,0.65,Positive
PATIENT_002,Terrible experience.,-0.75,Negative
```

### Sentiment Categories
- **Positive** (✨): polarity > 0.1
- **Neutral** (😐): -0.1 ≤ polarity ≤ 0.1
- **Negative** (😔): polarity < -0.1

---

## 🛠️ **COMMON TASKS**

### Task 1: Run Analysis with Your Data
```bash
# Edit sentiment_analyzer.py:
# Change: input_csv='patient_reviews.csv'
# To: input_csv='your_file.csv'
python sentiment_analyzer.py
```

### Task 2: Change Sentiment Thresholds
See `CONFIGURATION.md` → Section 3: Sentiment Classification Thresholds

### Task 3: Change Chart Colors
See `CONFIGURATION.md` → Section 4: Visualization Customization

### Task 4: View Code Examples
See `USER_GUIDE.md` → Advanced Usage Examples (5 examples provided)

### Task 5: Add Sample Reviews
See `CONFIGURATION.md` → Section 2: Sample Data Generation

---

## 📊 **FEATURES CHECKLIST**

- ✅ Automatic dependency installation
- ✅ CSV file loading and validation
- ✅ Sentiment analysis (Positive/Negative/Neutral)
- ✅ Polarity scoring (-1.0 to 1.0)
- ✅ Results export to CSV
- ✅ Pie chart visualization
- ✅ Bar chart visualization
- ✅ Console statistics and reporting
- ✅ Error handling with try/except
- ✅ Sample data generation (1000 reviews)
- ✅ Well-commented code
- ✅ Progress indicators with emojis
- ✅ Comprehensive documentation

---

## 🚀 **GETTING STARTED**

### Step 1: Install Dependencies
The script auto-installs, or manually:
```bash
pip install -r requirements.txt
python -m textblob.download_corpora
# (Optional) Download NLTK corpora used by the preprocessing pipeline:
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

### Step 2: Run the Script
```bash
python sentiment_analyzer.py
```

### Step 3: Check Results
- `patient_reviews_with_sentiment.csv` - Open in Excel
- `sentiment_pie_chart.png` - View pie chart
- `sentiment_bar_chart.png` - View bar chart

### Step 4: Customize (Optional)
See `CONFIGURATION.md` for customization options

---

## 💡 **TIPS**

- 📁 Keep CSV in same folder as script
- 📋 Ensure CSV has 'review' column
- ⚙️ First run takes longer (installing packages)
- 📊 Charts are saved as PNG (open with image viewer)
- 💾 Results are appended to output CSV (backup original)
- 🔧 Edit thresholds to adjust sentiment sensitivity

---

## 🐛 **TROUBLESHOOTING**

### "ModuleNotFoundError: No module named 'textblob'"
→ Run script normally (auto-installs) or: `pip install textblob`

### "KeyError: 'review'"
→ Ensure CSV has column named exactly 'review'

### "File not found"
→ Place CSV in same folder or provide full path

### Charts don't display
→ Check project folder for PNG files, open with image viewer

### Script is slow
→ Normal for 1000+ reviews (30-60 seconds expected)

See `USER_GUIDE.md` for more troubleshooting.

---

## 📈 **EXAMPLE OUTPUTS**

### Console Output (Excerpt)
```
🩺 PATIENT REVIEW SENTIMENT ANALYSIS SYSTEM

📊 Sentiment Distribution:
   ✨ Positive: 474 reviews (47.4%)
   😔 Negative: 272 reviews (27.2%)
   😐 Neutral:  254 reviews (25.4%)

   Total Reviews: 1,000
   Average Polarity Score: 0.1073

📁 Output Files Generated:
   💾 CSV:  patient_reviews_with_sentiment.csv
   📊 Chart: sentiment_pie_chart.png
   📊 Chart: sentiment_bar_chart.png
```

### CSV Output (Sample Row)
```
PATIENT_0001, "Doctor was professional", 0.65, Positive
```

---

## 🔗 **QUICK LINKS**

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Main documentation & features |
| [USER_GUIDE.md](USER_GUIDE.md) | 20+ code examples & usage |
| [CONFIGURATION.md](CONFIGURATION.md) | Advanced customization |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Project overview |
| [requirements.txt](requirements.txt) | Python dependencies |

---

## 🎓 **LEARNING RESOURCES**

- **TextBlob**: https://textblob.readthedocs.io/
- **Pandas**: https://pandas.pydata.org/docs/
- **Matplotlib**: https://matplotlib.org/stable/contents.html
- **Sentiment Analysis Basics**: https://en.wikipedia.org/wiki/Sentiment_analysis

---

## 🎯 **PROJECT STATS**

- **Main Script**: ~600 lines of code
- **Documentation**: 5 comprehensive guides
- **Functions**: 6 main + helpers
- **Output Files**: CSV + 2 charts
- **Sample Data**: 1000 reviews
- **Python Version**: 3.7+
- **Dependencies**: 3 (pandas, textblob, matplotlib)

---

## 🎉 **YOU'RE ALL SET!**

Your sentiment analysis system is **ready to use**.

### Next Steps:
1. Run: `python sentiment_analyzer.py`
2. View results in CSV and PNG files
3. Customize using CONFIGURATION.md
4. Integrate into your projects

---

## 📞 **SUPPORT**

- 📖 Check relevant documentation file
- 🔍 Search CONFIGURATION.md for customization
- 💡 See USER_GUIDE.md for code examples
- ✅ Review README.md troubleshooting section

---

**Version**: 1.0  
**Status**: ✅ Ready to Use  
**Created**: November 2025

**Happy Analyzing! 📊✨**
