"""
⚡ Quick Start Script - Run Sentiment Analysis in One Command
This script sets up and runs the sentiment analysis with minimal configuration.
"""

import os
import sys

# Change to the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Import and run the main analyzer
from sentiment_analyzer import (
    install_missing_dependencies,
    analyze_patient_reviews,
    create_pie_chart,
    create_bar_chart
)

if __name__ == "__main__":
    try:
        # Step 1: Install dependencies
        install_missing_dependencies()
        
        # Step 2: Run sentiment analysis
        df_results, sentiment_counts, total_reviews = analyze_patient_reviews(
            input_csv=os.path.join('Inputs', 'patient_reviews.csv'),
            output_csv=os.path.join('Outputs', 'patient_reviews_with_sentiment.csv'),
            generate_if_missing=True
        )

        # Step 3: Create visualizations with total review count (saved to Outputs/)
        create_pie_chart(sentiment_counts, os.path.join('Outputs', 'sentiment_pie_chart.png'), total_reviews)
        create_bar_chart(sentiment_counts, os.path.join('Outputs', 'sentiment_bar_chart.png'), total_reviews)
        
        print("\n🎉 SUCCESS! All files have been generated!")
        print(f"\n📊 Analysis Summary:")
        print(f"   Total Reviews Analyzed: {total_reviews:,}")
        print(f"\n📂 Check the following files in your project folder:")
        print("   📊 Outputs/patient_reviews_with_sentiment.csv")
        print("   📈 Outputs/sentiment_pie_chart.png")
        print("   📊 Outputs/sentiment_bar_chart.png")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
