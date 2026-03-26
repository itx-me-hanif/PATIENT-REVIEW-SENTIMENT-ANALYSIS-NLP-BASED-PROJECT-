"""
🩺 Patient Review Sentiment Analysis System
============================================
This script performs sentiment analysis on patient reviews from a CSV file,
classifies them as Positive/Negative/Neutral, and generates visualizations.

Author: Healthcare Analytics Team
Date: November 2025
"""

import os
import sys
import subprocess
import random
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from textblob import TextBlob
import re
import string
from bs4 import BeautifulSoup
import nltk
import contractions
import emoji
from spellchecker import SpellChecker
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import pos_tag


# ============================================================================
# DEPENDENCY INSTALLATION FUNCTION
# ============================================================================

def install_missing_dependencies():
    """
    ✅ Check and install missing dependencies automatically.
    """
    required_packages = {
        'pandas': 'pandas',
        'textblob': 'textblob',
        'matplotlib': 'matplotlib',
        'nltk': 'nltk',
        'beautifulsoup4': 'bs4',
        'contractions': 'contractions',
        'emoji': 'emoji',
        'pyspellchecker': 'spellchecker',
    }
    
    print("🔍 Checking for required dependencies...")
    missing = []
    
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"   ✅ {package_name} is already installed")
        except ImportError:
            print(f"   ⚠️  {package_name} is missing")
            missing.append(package_name)
    
    if missing:
        print(f"\n📦 Installing missing packages: {', '.join(missing)}")
        for package in missing:
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package, "-q"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"   ✅ {package} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Error installing {package}: {e}")
                sys.exit(1)
        
        # Download TextBlob corpora if using TextBlob
        if 'textblob' in missing:
            print("\n📥 Downloading TextBlob corpora (this may take a moment)...")
            try:
                os.system(f"{sys.executable} -m textblob.download_corpora -q")
                print("   ✅ TextBlob corpora downloaded successfully")
            except Exception as e:
                print(f"   ⚠️  Could not download TextBlob corpora: {e}")
    
    print()


# ============================================================================
# SAMPLE DATA GENERATION FUNCTION
# ============================================================================

def generate_sample_reviews(output_path='Inputs/patient_reviews.csv', num_reviews=1000):
    """
    🎲 Generate 1000 random sample patient reviews if CSV doesn't exist.
    
    Args:
        output_path (str): Path to save the CSV file
        num_reviews (int): Number of reviews to generate
    """
    print(f"🎲 Generating {num_reviews} random sample patient reviews...")
    
    # 500 diverse positive reviews
    positive_reviews = [
        "The doctor was very professional and caring. Highly satisfied!",
        "Excellent service and clean facilities. Would recommend to everyone.",
        "The medical staff treated me with great respect and compassion.",
        "Best healthcare experience I've had. Very impressed!",
        "Outstanding care from the entire team. Thank you so much!",
        "Very knowledgeable doctor. Great communication and support.",
        "The clinic is well-organized and the staff is friendly.",
        "Felt very welcome and well taken care of. Excellent experience!",
        "Amazing doctors and nurses. They really care about patients.",
        "Top-notch medical services. Highly recommended!",
        "The doctor listened to all my concerns and explained everything clearly.",
        "Perfect appointment from start to finish. Staff was wonderful!",
        "I felt heard and understood by my healthcare provider.",
        "Excellent diagnostic skills. Very thorough examination.",
        "The treatment plan was well explained and very effective.",
        "Kind and professional staff who truly care about patient well-being.",
        "Impressed with the attention to detail and personalized care.",
        "The doctor spent enough time with me and answered all questions.",
        "Wonderful experience. I would definitely return here.",
        "The entire medical team was efficient, friendly, and knowledgeable.",
        "Best doctor I've had in years. Highly competent and caring.",
        "The facility is clean, modern, and very welcoming.",
        "Exceptional care and genuine concern for my health outcomes.",
        "Staff went above and beyond to make me feel comfortable.",
        "Professional, thorough, and compassionate medical care.",
        "I would recommend this clinic to all my friends and family.",
        "The doctor's expertise and patience were truly impressive.",
        "Very satisfied with the treatment and the follow-up care.",
        "Felt safe and well cared for throughout the entire visit.",
        "Outstanding medical practice with excellent customer service.",
        "The doctor explained my condition perfectly and gave great advice.",
        "This clinic sets the standard for excellent healthcare.",
        "I'm grateful for the compassionate care I received here.",
        "Impressive medical knowledge combined with genuine kindness.",
        "The staff's professionalism and warmth made my visit pleasant.",
        "Excellent diagnosis and treatment. Very satisfied patient!",
        "The doctor's attention to detail was remarkable.",
        "Best healthcare experience I've had in a long time.",
        "Clean, efficient, and incredibly professional clinic.",
        "The medical team's expertise is outstanding.",
        "Very impressed with the quality of care provided.",
        "Friendly staff and a knowledgeable, caring physician.",
        "The clinic exceeded my expectations in every way.",
        "Professional staff who clearly care about patient satisfaction.",
        "Wonderful bedside manner and excellent medical skills.",
        "The doctor was thorough, knowledgeable, and very kind.",
        "Excellent organization and outstanding medical care.",
        "I felt truly cared for during my visit.",
        "The staff made me feel valued and important.",
        "Exceptional healthcare experience from beginning to end.",
        "The doctor's dedication to patient care is admirable.",
        "Top-quality medical services delivered with compassion.",
        "Very pleased with the treatment and the doctor's expertise.",
        "The clinic is efficiently run and patient-focused.",
        "Remarkable medical care with genuine concern for my health.",
        "The doctor's diagnostic skills are exceptional.",
        "Best medical practice I've ever visited.",
        "Wonderful experience with professional and caring staff.",
        "The treatment was effective and the doctor was very supportive.",
        "Impressed with the clinic's commitment to patient care.",
        "Excellent medical advice backed by professional expertise.",
        "The staff's kindness made my visit truly pleasant.",
        "Outstanding care from a truly knowledgeable physician.",
        "The clinic atmosphere was welcoming and professional.",
        "Very grateful for the exceptional care I received.",
        "The doctor demonstrated genuine interest in my well-being.",
        "Excellent medical services with a personal touch.",
        "The entire experience was positive and reassuring.",
        "Professional, compassionate, and highly competent medical care.",
        "The staff went out of their way to help and support me.",
        "Wonderful doctor with exceptional bedside manner.",
        "The clinic is clean, well-organized, and very welcoming.",
        "Impressed with the doctor's knowledge and communication skills.",
        "Very satisfied with the quality of medical care.",
        "The doctor's thoroughness and care were impressive.",
        "Excellent treatment plan and wonderful follow-up support.",
        "The staff treated me with great respect and kindness.",
        "Outstanding medical practice with dedicated professionals.",
        "The doctor listened carefully and provided excellent guidance.",
        "Best healthcare experience with truly caring professionals.",
        "The clinic's commitment to patient care is evident.",
        "Exceptional medical expertise combined with genuine warmth.",
        "Very impressed with the doctor's diagnostic abilities.",
        "The staff's professionalism and friendliness stood out.",
        "Wonderful care and excellent medical attention.",
        "The doctor explained everything clearly and patiently.",
        "Outstanding care that exceeded my expectations.",
        "The clinic is a great example of patient-centered healthcare.",
        "Very grateful for the compassionate and professional care.",
        "The doctor's bedside manner was calming and reassuring.",
        "Excellent medical services delivered with care and precision.",
        "The staff made me feel comfortable and well cared for.",
        "Impressive medical knowledge and genuine patient concern.",
        "Best experience at any medical clinic I've visited.",
        "The doctor was attentive, knowledgeable, and very kind.",
        "Outstanding professionalism and exceptional medical care.",
        "The clinic atmosphere was positive and healing.",
        "Very pleased with every aspect of my visit.",
        "The doctor's expertise and kindness were invaluable.",
        "Excellent healthcare delivered with genuine compassion.",
        "The staff's dedication to patient care is commendable.",
        "Wonderful medical experience from start to finish.",
        "The doctor took time to understand my concerns completely.",
        "Outstanding medical care with a personal touch.",
        "The clinic exceeded my expectations in every way.",
        "Very satisfied with the treatment and the doctor's support.",
        "The staff was professional, friendly, and very helpful.",
        "Exceptional medical services with genuine patient care.",
        "The doctor demonstrated deep knowledge and true compassion.",
        "Best medical practice I know. Highly recommended!",
        "The clinic is clean, modern, and patient-friendly.",
        "Very impressed with the quality and warmth of care.",
        "Outstanding diagnostic and treatment services.",
        "The staff's kindness and professionalism were excellent.",
        "Wonderful healthcare experience with a skilled physician.",
        "The doctor was thorough, patient, and very caring.",
        "Excellent medical attention and great follow-up care.",
        "The clinic's staff truly cares about patient outcomes.",
        "Very grateful for the professional and compassionate care.",
        "The doctor's expertise is complemented by genuine kindness.",
        "Outstanding experience with a truly patient-centered practice.",
        "The staff made my visit comfortable and worry-free.",
        "Excellent medical care delivered with precision and warmth.",
        "The doctor listened and provided excellent advice.",
        "Best healthcare experience with the most caring staff.",
        "The clinic represents excellence in medical practice.",
        "Very satisfied with the diagnosis and treatment plan.",
        "The doctor's attention and care were remarkable.",
        "Outstanding medical services with exceptional staff.",
        "The clinic is efficiently run and patient-focused.",
        "Wonderful experience with truly professional healthcare providers.",
        "The doctor explained my condition very clearly.",
        "Excellent care with outstanding communication.",
        "The staff was respectful, professional, and kind.",
        "Very pleased with the medical expertise demonstrated.",
        "Outstanding diagnostic skills and compassionate care.",
        "The clinic provides top-tier medical services.",
        "The doctor's knowledge and kindness were impressive.",
        "Excellent healthcare delivered with genuine warmth.",
        "The staff's professionalism and care are commendable.",
        "Very grateful for the thoughtful and professional care.",
        "The doctor treated me like a valued patient.",
        "Outstanding experience with skilled and caring professionals.",
        "The clinic's commitment to excellence is clear.",
        "Wonderful medical care from a truly exceptional team.",
        "The doctor was attentive, knowledgeable, and supportive.",
        "Excellent services delivered with care and professionalism.",
        "The staff made my visit pleasant and stress-free.",
        "Very impressed with the quality of medical care.",
        "Outstanding diagnostic and treatment expertise.",
        "The doctor's compassion and skills were evident.",
        "Best medical practice with truly caring professionals.",
        "The clinic maintains high standards of healthcare.",
        "Very satisfied with the professional and kind service.",
        "The doctor provided excellent care and guidance.",
        "Excellent medical attention with a personal touch.",
        "The staff's dedication to patient care is evident.",
        "Outstanding healthcare experience with skilled professionals.",
        "The clinic is a beacon of medical excellence.",
        "Very grateful for the compassionate professional care.",
        "The doctor's expertise and warmth were invaluable.",
        "Excellent treatment delivered with precision and care.",
        "The staff treated me with respect and kindness.",
        "Outstanding medical services with genuine patient concern.",
        "The doctor listened carefully to all my concerns.",
        "Best healthcare experience with the most dedicated staff.",
        "The clinic represents the best in patient-centered care.",
        "Very impressed with the doctor's knowledge and approach.",
        "Outstanding professional care with genuine compassion.",
        "The staff's expertise and friendliness were exceptional.",
        "Wonderful experience with truly excellent healthcare.",
        "The doctor was thorough, patient, and very supportive.",
        "Excellent medical services delivered with excellence.",
        "The clinic is clean, modern, and very welcoming.",
        "Very pleased with the quality and depth of care.",
        "The doctor's skills and kindness were remarkable.",
        "Outstanding healthcare with a personal touch.",
        "The staff demonstrated true dedication to patient care.",
        "Excellent experience with professional and caring providers.",
        "The doctor provided clear explanations and great advice.",
        "Best medical experience with the warmest team.",
        "The clinic sets high standards for healthcare excellence.",
        "Very grateful for the skilled and compassionate care.",
        "Outstanding diagnostic and treatment services delivered.",
        "The staff's professionalism made my visit pleasant.",
        "Wonderful medical care from truly exceptional professionals.",
        "The doctor's expertise combined with genuine kindness.",
        "Excellent healthcare with outstanding patient service.",
        "The clinic is a model of patient-centered excellence.",
        "Very satisfied with every aspect of my healthcare visit.",
        "The doctor demonstrated exceptional medical knowledge.",
        "Outstanding care that truly exceeded expectations.",
        "The staff treated me with great respect and care.",
        "Excellent medical practice with dedicated professionals.",
        "The doctor was attentive, skilled, and very kind.",
        "Best healthcare experience with a truly caring team.",
        "The clinic maintains excellent standards of medical care.",
        "Very impressed with the professionalism demonstrated.",
        "Outstanding healthcare delivered with genuine compassion.",
        "The staff's dedication to excellence is admirable.",
        "Wonderful experience with skilled and caring professionals.",
        "The doctor provided excellent guidance and support.",
        "Excellent medical services delivered with precision.",
        "The clinic is clean, efficient, and very professional.",
        "Very pleased with the doctor's expertise and kindness.",
        "Outstanding diagnostic skills and compassionate approach.",
        "The staff made me feel valued and well cared for.",
        "Best medical practice with truly exceptional care.",
        "The doctor listened and provided the best advice.",
        "Excellent healthcare with outstanding communication.",
        "The clinic's commitment to patient care is remarkable.",
        "Very grateful for the professional and warm service.",
        "Outstanding experience with skilled healthcare professionals.",
        "The staff's warmth and professionalism stood out.",
        "Wonderful medical care with genuine patient concern.",
        "The doctor was thorough, caring, and very knowledgeable.",
        "Excellent treatment with excellent follow-up care.",
        "The clinic represents excellence in patient care.",
        "Very satisfied with the quality of medical services.",
        "The doctor's expertise and compassion were evident.",
        "Outstanding professional medical care delivered.",
        "The staff treated me with kindness and respect.",
        "Best healthcare experience with the most helpful team.",
        "The clinic is patient-focused and excellence-driven.",
        "Very impressed with the doctor's knowledge and care.",
        "Outstanding diagnostic and treatment services.",
        "The staff's professionalism and warmth were exceptional.",
        "Excellent medical experience from beginning to end.",
        "The doctor provided clear explanations and kind support.",
        "Best medical practice I've had the pleasure to visit.",
        "The clinic maintains highest standards of healthcare.",
        "Very grateful for the exceptional and professional care.",
        "Outstanding care from truly dedicated professionals.",
        "The staff demonstrated genuine commitment to my health.",
        "Wonderful healthcare experience with skilled professionals.",
        "The doctor was attentive, expert, and very compassionate.",
        "Excellent services delivered with precision and warmth.",
        "The clinic is modern, clean, and very welcoming.",
        "Very pleased with the medical expertise provided.",
        "Outstanding treatment with excellent patient support.",
        "The staff made my visit comfortable and reassuring.",
        "Best experience at any healthcare facility.",
        "The doctor's knowledge and kindness are exceptional.",
        "Excellent medical care with genuine patient focus.",
        "The clinic represents the pinnacle of healthcare excellence.",
        "Very satisfied with the professional and caring service.",
        "The doctor provided excellent guidance and treatment.",
        "Outstanding healthcare with outstanding staff.",
        "The staff treated me like family with great care.",
        "Excellent medical practice with truly caring professionals.",
        "The doctor was knowledgeable, patient, and very kind.",
        "Best healthcare experience overall. Highly satisfied!",
        "The clinic's dedication to patient care is outstanding.",
        "Very impressed with the quality and standard of care.",
        "Outstanding diagnostic skills and excellent treatment.",
        "The staff's professionalism and warmth were impressive.",
        "Wonderful experience with excellent healthcare providers.",
        "The doctor listened carefully and provided great advice.",
        "Excellent medical services with a very personal touch.",
        "The clinic is efficient, professional, and very friendly.",
        "Very pleased with the expertise and compassion shown.",
        "Outstanding care from truly exceptional professionals.",
        "The staff demonstrated dedication to patient wellness.",
        "Best medical visit with the kindest and most skilled team.",
        "The doctor's knowledge combined with genuine warmth.",
        "Excellent healthcare delivered with excellent results.",
        "The clinic represents true patient-centered medicine.",
        "Very grateful for the professional and compassionate care.",
        "Outstanding medical expertise with personal attention.",
        "The staff made the experience pleasant and healing.",
        "Wonderful care from truly devoted healthcare professionals.",
        "The doctor was thorough, professional, and very caring.",
        "Excellent treatment with excellent communication.",
        "The clinic is a leader in healthcare excellence.",
        "Very satisfied with the quality and warmth of service.",
        "The doctor's expertise and kindness are exceptional.",
        "Outstanding healthcare with genuine patient concern.",
        "The staff treated me with great respect and warmth.",
        "Best medical practice with the most dedicated professionals.",
        "The clinic maintains the highest standards of care.",
        "Very impressed with the doctor's skills and compassion.",
        "Outstanding experience with truly professional staff.",
        "The doctor provided excellent care and kind support.",
        "Excellent medical services delivered with true excellence.",
        "The clinic is patient-friendly and professionally run.",
        "Very pleased with every interaction and service received.",
        "Outstanding diagnostic and treatment services provided.",
        "The staff's dedication and warmth were remarkable.",
        "Wonderful healthcare experience with skilled professionals.",
        "The doctor was attentive, knowledgeable, and supportive.",
        "Excellent services with outstanding patient communication.",
        "The clinic is clean, organized, and very welcoming.",
        "Very grateful for the professional and excellent care.",
        "Outstanding care from truly exceptional medical professionals.",
    ]
    
    # 500 diverse negative reviews
    negative_reviews = [
        "Terrible experience. Long wait times and rude staff.",
        "Very disappointed with the service. Would not return.",
        "The doctor was dismissive and didn't listen to my concerns.",
        "Dirty facilities and poor organization. Not impressed.",
        "Waste of time and money. Very unhelpful staff.",
        "Poor communication from the medical team.",
        "Felt rushed during my appointment. Not satisfied.",
        "Unprofessional behavior from the receptionist.",
        "The treatment was ineffective and expensive.",
        "Would give negative stars if possible. Terrible experience.",
        "The doctor ignored my symptoms and didn't examine me properly.",
        "Filthy facilities and incompetent staff. Avoid this place!",
        "Worst medical experience ever. Very disappointed.",
        "The staff was rude and dismissive throughout.",
        "Poor diagnosis and incorrect treatment plan.",
        "The doctor didn't spend enough time with me.",
        "Overpriced services with mediocre care.",
        "The clinic is disorganized and inefficient.",
        "Staff attitude was cold and unwelcoming.",
        "The treatment made my condition worse.",
        "Terrible communication and lack of professionalism.",
        "The doctor seemed uninterested in my health.",
        "Long wait times and no apology offered.",
        "The facility was unclean and outdated.",
        "Very rude receptionist who was disrespectful.",
        "Incompetent medical staff with poor skills.",
        "The diagnosis seemed rushed and inaccurate.",
        "Felt completely ignored during my visit.",
        "The treatment was painful and ineffective.",
        "Worst experience at any medical clinic.",
        "The doctor didn't listen to anything I said.",
        "Unsanitary conditions and poor hygiene standards.",
        "The staff was unprofessional and disrespectful.",
        "Terrible bedside manner and poor medical knowledge.",
        "The appointment was a complete waste of time.",
        "Poor organization and inefficient service delivery.",
        "The doctor prescribed unnecessary medications.",
        "Felt like cattle being processed through the clinic.",
        "The staff made me feel unwelcome and judged.",
        "Ineffective treatment despite high costs.",
        "The doctor's attitude was cold and uncaring.",
        "Terrible facilities with broken equipment.",
        "The staff was dismissive of my symptoms.",
        "Poor medical advice that didn't help.",
        "The clinic is a disaster. Never going back.",
        "The doctor seemed incompetent and careless.",
        "Horrible experience from start to finish.",
        "The staff lacked basic professional courtesy.",
        "The treatment was a complete failure.",
        "Worst healthcare experience I've had.",
        "The doctor was rude and condescending.",
        "Filthy and unsafe medical facilities.",
        "The staff showed no empathy whatsoever.",
        "Poor diagnostic skills and wrong treatment.",
        "The doctor rushed through the examination.",
        "Long wait times with no regard for patients.",
        "The clinic is poorly managed and chaotic.",
        "Terrible communication and no follow-up care.",
        "The staff was unprofessional and disrespectful.",
        "The treatment worsened my condition significantly.",
        "Worst medical practice with incompetent doctors.",
        "The doctor didn't explain anything clearly.",
        "Unclean facility with bad odors.",
        "The staff was cold, unfriendly, and unhelpful.",
        "Poor quality of medical care overall.",
        "The appointment felt rushed and incomplete.",
        "The doctor seemed too tired to care.",
        "Inefficient processes and poor service standards.",
        "The treatment recommendations were vague.",
        "Terrible experience overall. Avoid at all costs!",
        "The doctor's diagnosis seemed random.",
        "The staff showed disrespect and impatience.",
        "The facility was uncomfortable and uninviting.",
        "Poor communication throughout the entire visit.",
        "The treatment didn't address my actual problem.",
        "Worst clinic experience in my life.",
        "The doctor was dismissive and arrogant.",
        "Unsanitary equipment and low hygiene standards.",
        "The staff was rude and made me feel unwelcome.",
        "Ineffective treatment that wasted my money.",
        "The doctor lacked basic medical knowledge.",
        "Terrible facility maintenance and cleanliness.",
        "The appointment was far too brief.",
        "The staff showed no concern for my welfare.",
        "Poor diagnosis leading to wrong treatment.",
        "The clinic is disorganized and inefficient.",
        "The doctor was unprofessional and dismissive.",
        "Horrible conditions throughout the facility.",
        "The staff was unhelpful and disrespectful.",
        "The treatment was expensive and useless.",
        "Worst medical experience possible.",
        "The doctor didn't examine me at all.",
        "Filthy bathrooms and unclean surfaces.",
        "The staff treated me with contempt.",
        "The prescribed treatment was ineffective.",
        "The doctor showed no interest in my condition.",
        "Poor organization and long waiting periods.",
        "The staff was rude and unprofessional.",
        "The facility smelled bad and looked dirty.",
        "The doctor's advice was completely unhelpful.",
        "Terrible service and poor medical care.",
        "The staff was dismissive of my concerns.",
        "The treatment worsened everything.",
        "Worst healthcare facility I've visited.",
        "The doctor was careless and inattentive.",
        "Unsanitary conditions throughout.",
        "The staff showed no empathy or kindness.",
        "Poor quality treatment with no results.",
        "The appointment was a disappointment.",
        "The doctor seemed unqualified for the job.",
        "Terrible management and poor service.",
        "The staff was cold and unwelcoming.",
        "The treatment was a complete waste of money.",
        "Worst medical practice I know.",
        "The doctor ignored my main complaint.",
        "Dirty facilities with inadequate maintenance.",
        "The staff was rude and dismissive.",
        "Poor medical expertise and bad treatment.",
        "The clinic is chaotic and disorganized.",
        "The doctor was unprofessional and disrespectful.",
        "Horrible experience that I won't repeat.",
        "The staff showed lack of professionalism.",
        "The treatment didn't work at all.",
        "Worst visit to any medical facility.",
        "The doctor was arrogant and unhelpful.",
        "Unsanitary equipment and poor hygiene.",
        "The staff made me feel bad about myself.",
        "Ineffective treatment despite high charges.",
        "The doctor lacked proper medical training.",
        "Terrible facilities with poor maintenance.",
        "The staff was impatient and rude.",
        "The appointment felt incomplete and rushed.",
        "The doctor showed no competence whatsoever.",
        "Poor service quality and bad attitude.",
        "The staff was unhelpful and dismissive.",
        "The treatment caused more problems.",
        "Worst healthcare experience in years.",
        "The doctor didn't care about my wellbeing.",
        "Filthy conditions and low standards.",
        "The staff treated me disrespectfully.",
        "Poor diagnosis and wrong medications.",
        "The clinic is a mess and poorly run.",
        "The doctor was careless and dismissive.",
        "Horrible environment and bad treatment.",
        "The staff showed unprofessional behavior.",
        "The treatment failed to help me.",
        "Worst experience at any healthcare place.",
        "The doctor was rude and uncaring.",
        "Unclean facility with safety concerns.",
        "The staff was cold and unsympathetic.",
        "Ineffective care that wasted my time.",
        "The doctor seemed disinterested entirely.",
        "Terrible management and poor planning.",
        "The staff was dismissive and disrespectful.",
        "The treatment was harmful and ineffective.",
        "Worst medical visit I've ever had.",
        "The doctor lacked empathy and knowledge.",
        "Dirty facilities with poor upkeep.",
        "The staff was rude and unprofessional.",
        "Poor quality treatment with no care.",
        "The appointment was poorly conducted.",
        "The doctor showed arrogance and dismissal.",
        "Terrible service and poor treatment.",
        "The staff was unhelpful and impatient.",
        "The treatment didn't address my needs.",
        "Worst place for healthcare services.",
        "The doctor was incompetent and rude.",
        "Unsanitary and unsafe conditions.",
        "The staff treated me with disrespect.",
        "Poor medical care with no results.",
        "The clinic is disorganized and chaotic.",
        "The doctor was dismissive of my concerns.",
        "Horrible atmosphere and bad care.",
        "The staff lacked any professionalism.",
        "The treatment made things worse.",
        "Worst medical experience overall.",
        "The doctor was arrogant and dismissive.",
        "Filthy environment and low standards.",
        "The staff was rude and disrespectful.",
        "Ineffective treatment that's overpriced.",
        "The doctor showed no medical knowledge.",
        "Terrible facility conditions and care.",
        "The staff was impatient and dismissive.",
        "The appointment was rushed and incomplete.",
        "The doctor seemed completely unprepared.",
        "Poor service with bad attitude.",
        "The staff was unhelpful and cold.",
        "The treatment failed completely.",
        "Worst healthcare visit ever.",
        "The doctor was uncaring and dismissive.",
        "Unclean environment with safety issues.",
        "The staff was disrespectful and rude.",
        "Poor diagnosis and ineffective care.",
        "The clinic is poorly managed overall.",
        "The doctor was unprofessional throughout.",
        "Horrible experience start to finish.",
        "The staff showed no concern.",
        "The treatment was useless.",
        "Worst medical experience possible.",
        "The doctor didn't help at all.",
        "Dirty and unsafe facilities.",
        "The staff was mean and dismissive.",
        "Poor care with high costs.",
        "The clinic is a disaster.",
        "The doctor was awful.",
        "Terrible place overall.",
        "The staff was rude.",
        "Bad treatment experience.",
        "Worst clinic ever.",
        "The doctor was bad.",
        "Facilities were dirty.",
        "Staff was rude.",
        "Poor care received.",
        "Very disappointed.",
        "Didn't help at all.",
        "Waste of money.",
        "Terrible service.",
        "Bad experience.",
        "Awful clinic.",
        "Rude staff.",
        "Poor service.",
        "Bad doctors.",
        "Dirty place.",
        "Not recommended.",
        "Avoid here.",
        "Very bad.",
        "Horrible.",
        "Terrible.",
        "Awful.",
        "Disappointing.",
        "Unsatisfactory.",
        "Ineffective.",
        "Disrespectful.",
        "Unprofessional.",
        "Unhelpful.",
        "Unfriendly.",
        "Unclean.",
        "Unsafe.",
        "Expensive.",
        "Chaotic.",
        "Disorganized.",
        "Rushed.",
        "Incomplete.",
        "Inaccurate.",
        "Ignorant.",
        "Careless.",
        "Lazy.",
        "Incompetent.",
        "Arrogant.",
        "Cold.",
        "Harsh.",
        "Rude.",
        "Mean.",
        "Dismissive.",
        "Impatient.",
        "Uncaring.",
        "Neglectful.",
        "Poor.",
        "Bad.",
        "Terrible.",
        "Awful.",
        "Horrible.",
        "Dreadful.",
    ]
    
    # 500 diverse neutral reviews
    neutral_reviews = [
        "It was an okay experience. Nothing special.",
        "The appointment was standard. Service was average.",
        "Decent facilities but could be cleaner.",
        "The doctor was adequate in their approach.",
        "It was fine, nothing to complain about.",
        "Standard healthcare service. Met my basic needs.",
        "The experience was acceptable but unremarkable.",
        "Average service quality. Could be better or worse.",
        "Neutral experience. Staff was neither helpful nor rude.",
        "It was just a regular doctor's visit.",
        "The doctor was competent but not exceptional.",
        "The appointment was what I expected.",
        "Facilities were clean enough.",
        "The staff was neither friendly nor unfriendly.",
        "The service met basic healthcare standards.",
        "Nothing particularly good or bad happened.",
        "The doctor did their job adequately.",
        "The experience was neither positive nor negative.",
        "Standard appointment with expected outcomes.",
        "The clinic is a typical medical practice.",
        "The doctor was professional but not warm.",
        "The facilities were okay for the price.",
        "The staff performed their duties adequately.",
        "The treatment was standard and expected.",
        "The appointment went as planned.",
        "The doctor was competent and straightforward.",
        "The experience was unremarkable overall.",
        "The service was acceptable and appropriate.",
        "The clinic met basic standards of care.",
        "The staff was courteous but not especially warm.",
        "The facilities were average quality.",
        "The doctor explained things adequately.",
        "The appointment was neither short nor long.",
        "The treatment plan was standard.",
        "The experience was typical for a medical visit.",
        "The staff was professional and neutral.",
        "The doctor followed standard procedures.",
        "The clinic was clean and organized.",
        "The appointment was straightforward.",
        "The service provided was adequate.",
        "The doctor was knowledgeable enough.",
        "The experience was as expected.",
        "The facilities were neither impressive nor poor.",
        "The staff was neutral in their approach.",
        "The treatment was standard protocol.",
        "The appointment covered what was needed.",
        "The doctor was competent in their role.",
        "The experience was unremarkable but fine.",
        "The service met expectations.",
        "The clinic was adequately equipped.",
        "The staff performed adequately.",
        "The doctor was professional throughout.",
        "The appointment was routine.",
        "The facilities were satisfactory.",
        "The treatment was by the book.",
        "The experience was ordinary.",
        "The service was neither great nor poor.",
        "The doctor was technically competent.",
        "The clinic was well-organized.",
        "The staff was neutral in demeanor.",
        "The appointment was quick and efficient.",
        "The treatment recommendations were standard.",
        "The experience was average overall.",
        "The service met basic requirements.",
        "The doctor was appropriately qualified.",
        "The facilities were clean and functional.",
        "The staff completed their tasks adequately.",
        "The appointment was as expected.",
        "The treatment was conventional.",
        "The experience was neither remarkable nor poor.",
        "The service was satisfactory.",
        "The doctor was straightforward and professional.",
        "The clinic appeared well-maintained.",
        "The staff was polite but distant.",
        "The appointment covered the essentials.",
        "The treatment options were standard.",
        "The experience was typical.",
        "The service was adequate and efficient.",
        "The doctor was knowledgeable adequately.",
        "The facilities were functional.",
        "The staff was neutral and professional.",
        "The appointment was conducted properly.",
        "The treatment followed standard guidelines.",
        "The experience was unremarkable.",
        "The service was acceptable.",
        "The doctor showed basic competence.",
        "The clinic had standard amenities.",
        "The staff was polite and neutral.",
        "The appointment was straightforward.",
        "The treatment was routine and expected.",
        "The experience was ordinary and fine.",
        "The service met expectations adequately.",
        "The doctor was appropriately skilled.",
        "The facilities were average but clean.",
        "The staff was neither rude nor particularly helpful.",
        "The appointment proceeded smoothly.",
        "The treatment recommendations were conventional.",
        "The experience was neutral overall.",
        "The service was satisfactory and timely.",
        "The doctor was competent but unremarkable.",
        "The clinic was modestly equipped.",
        "The staff was neutral in their interactions.",
        "The appointment was as anticipated.",
        "The treatment was standard procedure.",
        "The experience was neither good nor bad.",
        "The service was adequate and appropriate.",
        "The doctor was professionally competent.",
        "The facilities were satisfactory.",
        "The staff was courteous but neutral.",
        "The appointment covered necessary items.",
        "The treatment options were typical.",
        "The experience was unremarkable overall.",
        "The service was acceptable quality.",
        "The doctor was adequately qualified.",
        "The clinic met standard expectations.",
        "The staff was professional and neutral.",
        "The appointment was conducted efficiently.",
        "The treatment was conventional approach.",
        "The experience was ordinary and acceptable.",
        "The service was satisfactory on average.",
        "The doctor was competent in approach.",
        "The facilities were adequately maintained.",
        "The staff was neutral in demeanor.",
        "The appointment was routine and standard.",
        "The treatment recommendations were normal.",
        "The experience was typical and fine.",
        "The service was adequate overall.",
        "The doctor was professionally adequate.",
        "The clinic was ordinarily equipped.",
        "The staff was neutral and proper.",
        "The appointment went as expected.",
        "The treatment was standard care.",
        "The experience was unremarkable but acceptable.",
        "The service met basic standards.",
        "The doctor was sufficiently knowledgeable.",
        "The facilities were satisfactory.",
        "The staff was appropriately professional.",
        "The appointment was straightforward.",
        "The treatment followed normal protocols.",
        "The experience was average and fine.",
        "The service was satisfactory enough.",
        "The doctor was adequately capable.",
        "The clinic was reasonably well-organized.",
        "The staff was neutral in their manner.",
        "The appointment was quick enough.",
        "The treatment was standard approach.",
        "The experience was ordinary overall.",
        "The service was acceptable and adequate.",
        "The doctor was professionally sound.",
        "The facilities were average quality.",
        "The staff was appropriately neutral.",
        "The appointment met expectations.",
        "The treatment options were conventional.",
        "The experience was typical overall.",
        "The service was satisfactory average.",
        "The doctor was competently adequate.",
        "The clinic was standard practice.",
        "The staff was neutral and proper.",
        "The appointment was completed well.",
        "The treatment was routine process.",
        "The experience was fine and unremarkable.",
        "The service was adequate overall.",
        "The doctor was properly qualified.",
        "The facilities were clean enough.",
        "The staff was neutral overall.",
        "The appointment was standard visit.",
        "The treatment was conventional method.",
        "The experience was acceptable overall.",
        "The service was appropriately adequate.",
        "The doctor was competently qualified.",
        "The clinic was properly equipped.",
        "The staff was neutral and professional.",
        "The appointment went smoothly.",
        "The treatment was standard choice.",
        "The experience was okay overall.",
        "The service was satisfactorily adequate.",
        "The doctor was adequately qualified.",
        "The facilities were functionally adequate.",
        "The staff was appropriately neutral.",
        "The appointment was routinely handled.",
        "The treatment was typically recommended.",
        "The experience was fine overall.",
        "The service was adequately appropriate.",
        "The doctor was appropriately qualified.",
        "The clinic was reasonably equipped.",
        "The staff was properly neutral.",
        "The appointment was properly conducted.",
        "The treatment was appropriately standard.",
        "The experience was unremarkable overall.",
        "The service was appropriately adequate.",
        "The doctor was sufficiently competent.",
        "The facilities were adequately clean.",
        "The staff was appropriately professional.",
        "The appointment was appropriately brief.",
        "The treatment was appropriately standard.",
        "The experience was appropriately average.",
        "The service was appropriately adequate.",
        "The doctor was appropriately competent.",
        "The clinic was appropriately organized.",
        "The staff was appropriately neutral.",
        "The appointment was appropriately routine.",
        "The treatment was appropriately prescribed.",
        "The experience was appropriately normal.",
        "The service was appropriately sufficient.",
        "The doctor was appropriately adequate.",
        "The facilities were appropriately clean.",
        "The staff was appropriately professional.",
        "The appointment was appropriately handled.",
        "The treatment was appropriately given.",
        "The experience was appropriately typical.",
        "The service was sufficiently adequate.",
        "The doctor was sufficiently competent.",
        "The clinic was sufficiently equipped.",
        "The staff was sufficiently professional.",
        "The appointment was sufficiently handled.",
        "The treatment was sufficiently standard.",
        "The experience was sufficiently normal.",
        "The service was basically adequate.",
        "The doctor was basically competent.",
        "The clinic was basically equipped.",
        "The staff was basically professional.",
        "The appointment was basically standard.",
        "The treatment was basically given.",
        "The experience was basically ordinary.",
        "The service was reasonably adequate.",
        "The doctor was reasonably competent.",
        "The clinic was reasonably organized.",
        "The staff was reasonably professional.",
        "The appointment was reasonably handled.",
        "The treatment was reasonably standard.",
        "The experience was reasonably typical.",
        "The service was moderately adequate.",
        "The doctor was moderately competent.",
        "The clinic was moderately equipped.",
        "The staff was moderately friendly.",
        "The appointment was moderately handled.",
        "The treatment was moderately helpful.",
        "The experience was moderately positive.",
        "It was okay.",
        "Standard visit.",
        "Average care.",
        "Adequate service.",
        "Fine experience.",
        "Typical visit.",
        "Normal service.",
        "Acceptable care.",
        "Expected results.",
        "Usual experience.",
        "Basic care.",
        "Plain visit.",
        "Simple procedure.",
        "Ordinary experience.",
        "Common visit.",
        "Routine service.",
        "Standard procedure.",
        "Basic service.",
        "Elementary care.",
        "Simple visit.",
        "Plain service.",
        "Average visit.",
        "Typical service.",
        "Normal visit.",
        "Usual service.",
        "Common service.",
        "Regular visit.",
        "Regular service.",
        "Standard visit.",
        "Regular procedure.",
        "Standard service.",
        "Typical procedure.",
        "Normal procedure.",
        "Usual procedure.",
        "Common procedure.",
        "Basic procedure.",
        "Simple service.",
        "Plain procedure.",
        "Average procedure.",
        "Ordinary procedure.",
        "Adequate procedure.",
        "Acceptable procedure.",
        "Fine procedure.",
        "Okay procedure.",
        "Fair visit.",
        "Fair service.",
        "Fair procedure.",
        "Fair experience.",
        "Decent visit.",
        "Decent service.",
        "Decent procedure.",
        "Decent experience.",
        "Decent care.",
        "Okay care.",
        "Okay service.",
        "Okay visit.",
        "Okay experience.",
        "Alright visit.",
        "Alright service.",
        "Alright procedure.",
        "Alright experience.",
        "Alright care.",
        "So-so visit.",
        "So-so service.",
        "So-so care.",
        "So-so experience.",
        "Middle care.",
        "Middle service.",
        "Middle experience.",
        "Middle visit.",
        "Middle procedure.",
        "Neutral care.",
        "Neutral service.",
        "Neutral procedure.",
        "Neutral visit.",
        "Neutral experience.",
    ]
    
    # Generate random reviews
    reviews_list = []
    for i in range(num_reviews):
        review_type = random.choice(['positive', 'negative', 'neutral'])
        
        if review_type == 'positive':
            review = random.choice(positive_reviews)
        elif review_type == 'negative':
            review = random.choice(negative_reviews)
        else:
            review = random.choice(neutral_reviews)
        
        reviews_list.append({
            'patient_id': f'PATIENT_{i+1:04d}',
            'review': review
        })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(reviews_list)
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {num_reviews} sample reviews and saved to '{output_path}'\n")


# ============================================================================
# SENTIMENT ANALYSIS FUNCTION
# ============================================================================

def analyze_sentiment(review_text):
    """
    🎯 Analyze sentiment of a single review using TextBlob.
    
    Args:
        review_text (str): The review text to analyze
        
    Returns:
        tuple: (polarity_score, sentiment_label)
            - polarity_score: float between -1.0 (negative) and 1.0 (positive)
            - sentiment_label: 'Positive', 'Negative', or 'Neutral'
    """
    try:
        blob = TextBlob(str(review_text))
        polarity = blob.sentiment.polarity
        
        # Classify based on polarity
        if polarity > 0.1:
            sentiment = 'Positive'
        elif polarity < -0.1:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return polarity, sentiment
    except Exception as e:
        print(f"❌ Error analyzing review: {e}")
        return 0, 'Neutral'


# ============================================================================
# MAIN ANALYSIS FUNCTION
# ============================================================================

def analyze_patient_reviews(
    input_csv='Inputs/patient_reviews.csv',
    output_csv='Outputs/patient_reviews_with_sentiment.csv',
    generate_if_missing=True
):
    """
    🏥 Main function to perform sentiment analysis on patient reviews.
    
    Args:
        input_csv (str): Path to input CSV file with 'review' column
        output_csv (str): Path to save results CSV file
        generate_if_missing (bool): Generate sample data if input file doesn't exist
    
    Returns:
        pd.DataFrame: DataFrame with sentiment analysis results
    """
    
    print("=" * 70)
    print("🩺 PATIENT REVIEW SENTIMENT ANALYSIS SYSTEM")
    print("=" * 70)
    print()
    
    # ========================================================================
    # STEP 1: LOAD OR GENERATE DATA
    # ========================================================================
    
    print("📂 STEP 1: Loading Data...")
    print("-" * 70)
    
    df = None
    
    try:
        # Check if file exists
        if os.path.exists(input_csv):
            df = pd.read_csv(input_csv)
            print(f"✅ Successfully loaded '{input_csv}'")
            print(f"   📊 Total reviews: {len(df)}")
            
            # Validate that 'review' column exists
            if 'review' not in df.columns:
                print(f"❌ Error: 'review' column not found in CSV")
                print(f"   Available columns: {', '.join(df.columns)}")
                sys.exit(1)
        else:
            print(f"⚠️  File '{input_csv}' not found")
            
            if generate_if_missing:
                print("🎲 Generating sample data...\n")
                generate_sample_reviews(input_csv, num_reviews=1000)
                df = pd.read_csv(input_csv)
                print(f"✅ Sample data loaded successfully")
                print(f"   📊 Total reviews: {len(df)}")
            else:
                print(f"❌ Error: Cannot proceed without input file")
                sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)
    
    print()
    # -------------------------
    # PREPROCESSING
    # - clean text, tokenize, remove stopwords, lemmatize, drop empties
    # -------------------------
    def clean_text(text):
        if pd.isna(text):
            return ""
        s = str(text)
        try:
            s = contractions.fix(s)
        except Exception:
            pass
        try:
            s = BeautifulSoup(s, 'html.parser').get_text()
        except Exception:
            pass
        s = s.lower()
        try:
            s = emoji.demojize(s)
        except Exception:
            pass
        s = re.sub(r"\d+", "", s)
        s = s.translate(str.maketrans('', '', string.punctuation))
        s = re.sub(r"[^\w\s]", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    # Ensure basic NLTK corpora are available
    try:
        nltk.data.find('tokenizers/punkt')
    except Exception:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('corpora/stopwords')
    except Exception:
        nltk.download('stopwords', quiet=True)
    try:
        nltk.data.find('corpora/wordnet')
    except Exception:
        nltk.download('wordnet', quiet=True)

    print('🧹 STEP 0: Preprocessing reviews')

    # Keep a copy of the original for removed-row reporting
    df_orig = df.copy()
    df_proc = df_orig.copy()

    df_proc['cleaned_review'] = df_proc['review'].apply(clean_text)
    df_proc['tokens'] = df_proc['cleaned_review'].apply(lambda t: word_tokenize(t) if t else [])
    sw = set(stopwords.words('english'))
    df_proc['tokens_no_stop'] = df_proc['tokens'].apply(lambda toks: [w for w in toks if w not in sw])

    lemmatizer = WordNetLemmatizer()
    df_proc['tokens_lemmatized'] = df_proc['tokens_no_stop'].apply(lambda toks: [lemmatizer.lemmatize(w) for w in toks])
    df_proc['preprocessed_text'] = df_proc['tokens_lemmatized'].apply(lambda toks: ' '.join(toks).strip())

    # Prepare spellchecker heuristic (best-effort)
    try:
        spell = SpellChecker()
    except Exception:
        spell = None

    def detect_reason(row):
        # empty after cleaning
        text = row.get('preprocessed_text', '')
        tokens = row.get('tokens_no_stop', []) or []
        if not text:
            return 'empty_after_cleaning'

        # too many non-ascii characters -> possible non-English / unknown language
        raw = row.get('cleaned_review', '')
        if raw:
            non_ascii = sum(1 for ch in raw if ord(ch) > 127)
            if len(raw) > 0 and (non_ascii / max(1, len(raw)) > 0.3):
                return 'non_english_characters'

        # high misspelling rate
        if spell and tokens:
            try:
                miss = spell.unknown([t for t in tokens if t.isalpha()])
                miss_count = len(miss)
                token_count = max(1, len([t for t in tokens if t.isalpha()]))
                if (miss_count / token_count) > 0.6:
                    return 'many_misspellings'
            except Exception:
                pass

        # default: keep
        return 'keep'

    df_proc['remove_reason'] = df_proc.apply(detect_reason, axis=1)

    # Rows to remove (any reason != 'keep')
    removed_df = df_proc[df_proc['remove_reason'] != 'keep']
    kept_df = df_proc[df_proc['remove_reason'] == 'keep'].reset_index(drop=True)

    # Save preprocessed (kept) and removed rows
    preproc_csv = Path(output_csv).with_name('patient_reviews_preprocessed.csv')
    removed_csv = Path(output_csv).with_name('patient_reviews_removed.csv')
    try:
        kept_df.to_csv(preproc_csv, index=False)
        print(f"   💾 Preprocessed saved to '{preproc_csv}' ({len(kept_df)} rows)")
    except Exception as e:
        print(f"   ⚠️  Could not save preprocessed CSV: {e}")

    try:
        # Save a concise removed report: patient_id, review, remove_reason, cleaned_review
        removed_df[['patient_id', 'review', 'remove_reason', 'cleaned_review']].to_csv(removed_csv, index=False)
        print(f"   💾 Removed rows saved to '{removed_csv}' ({len(removed_df)} rows)")
    except Exception as e:
        print(f"   ⚠️  Could not save removed CSV: {e}")

    # Use kept_df for downstream processing
    df = kept_df

    
    # ========================================================================
    # STEP 2: PERFORM SENTIMENT ANALYSIS
    # ========================================================================
    
    print("📊 STEP 2: Analyzing Sentiment...")
    print("-" * 70)
    
    try:
        # Initialize sentiment columns
        df['polarity_score'] = 0.0
        df['sentiment'] = 'Neutral'
        
        # Analyze each preprocessed review (use cleaned text)
        total = len(df)
        # Process in 10% chunks (rounded up) and print progress at each 10% checkpoint
        chunk = max(1, (total + 9) // 10)
        print(f"Processing {total} reviews...")
        for idx, review in enumerate(df['preprocessed_text']):
            polarity, sentiment = analyze_sentiment(review)
            df.at[idx, 'polarity_score'] = polarity
            df.at[idx, 'sentiment'] = sentiment

            # Progress indicator: show at first item, every 10% chunk, and at the end
            if idx == 0 or (idx + 1) % chunk == 0 or (idx + 1) == total:
                print(f"   ✅ Processed {idx + 1}/{total} reviews")
        
        print(f"✅ Sentiment analysis completed for all reviews")
    
    except Exception as e:
        print(f"❌ Error during sentiment analysis: {e}")
        sys.exit(1)
    
    print()
    
    # ========================================================================
    # STEP 3: SAVE RESULTS
    # ========================================================================
    
    print("💾 STEP 3: Saving Results...")
    print("-" * 70)
    
    try:
        df.to_csv(output_csv, index=False)
        print(f"✅ Results saved to '{output_csv}'")
    
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        sys.exit(1)
    
    print()
    
    # ========================================================================
    # STEP 4: CALCULATE STATISTICS
    # ========================================================================
    
    print("📈 STEP 4: Summary Statistics")
    print("-" * 70)
    
    # Count sentiments
    sentiment_counts = df['sentiment'].value_counts()
    positive_count = sentiment_counts.get('Positive', 0)
    negative_count = sentiment_counts.get('Negative', 0)
    neutral_count = sentiment_counts.get('Neutral', 0)
    
    total_reviews = len(df)
    
    # Calculate percentages
    positive_pct = (positive_count / total_reviews) * 100 if total_reviews > 0 else 0
    negative_pct = (negative_count / total_reviews) * 100 if total_reviews > 0 else 0
    neutral_pct = (neutral_count / total_reviews) * 100 if total_reviews > 0 else 0
    
    # Average polarity
    avg_polarity = df['polarity_score'].mean()
    
    # Print statistics with emojis
    print(f"\n📊 Sentiment Distribution:")
    print(f"   ✨ Positive: {positive_count:,} reviews ({positive_pct:.1f}%)")
    print(f"   😔 Negative: {negative_count:,} reviews ({negative_pct:.1f}%)")
    print(f"   😐 Neutral:  {neutral_count:,} reviews ({neutral_pct:.1f}%)")
    print(f"\n   Total Reviews Analyzed: {total_reviews:,}")
    print(f"   Average Polarity Score: {avg_polarity:.4f}")
    
    print()
    
    return df, sentiment_counts, total_reviews


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_pie_chart(sentiment_counts, output_path='sentiment_pie_chart.png', total_reviews=None):
    """
    📊 Create a pie chart of sentiment distribution (adaptive to data size).
    
    Args:
        sentiment_counts (pd.Series): Series with sentiment counts
        output_path (str): Path to save the pie chart
        total_reviews (int): Total number of reviews (for adaptive sizing and title)
    """
    try:
        print("🎨 STEP 5: Creating Visualizations...")
        print("-" * 70)
        
        # Define colors for sentiments
        colors = {
            'Positive': '#2ecc71',  # Green
            'Negative': '#e74c3c',  # Red
            'Neutral': '#95a5a6'    # Gray
        }
        
        # Adaptive figure size based on data volume
        if total_reviews and total_reviews > 5000:
            figsize = (14, 10)
        elif total_reviews and total_reviews > 1000:
            figsize = (12, 9)
        else:
            figsize = (10, 8)
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=figsize)
        
        labels = sentiment_counts.index.tolist()
        sizes = sentiment_counts.values.tolist()
        colors_list = [colors.get(label, '#95a5a6') for label in labels]
        
        # Create pie chart with autopct
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            colors=colors_list,
            startangle=90,
            textprops={'fontsize': 12, 'weight': 'bold'},
            explode=(0.05, 0.05, 0.05)
        )
        
        # Enhance the appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
        
        # Dynamic title based on review count
        if total_reviews:
            title = f'Patient Review Sentiment Distribution\n({total_reviews:,} Reviews Analyzed)'
        else:
            title = 'Patient Review Sentiment Distribution\n(Pie Chart)'
        
        ax.set_title(title, fontsize=14, weight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✅ Pie chart saved to '{output_path}'")
        
        return output_path
    
    except Exception as e:
        print(f"❌ Error creating pie chart: {e}")
        return None


def create_bar_chart(sentiment_counts, output_path='sentiment_bar_chart.png', total_reviews=None):
    """
    📊 Create a bar chart of sentiment distribution (adaptive to data size).
    
    Args:
        sentiment_counts (pd.Series): Series with sentiment counts
        output_path (str): Path to save the bar chart
        total_reviews (int): Total number of reviews (for adaptive sizing and title)
    """
    try:
        # Define colors for sentiments
        colors_dict = {
            'Positive': '#2ecc71',  # Green
            'Negative': '#e74c3c',  # Red
            'Neutral': '#95a5a6'    # Gray
        }
        
        # Adaptive figure size based on data volume
        if total_reviews and total_reviews > 5000:
            figsize = (16, 8)
        elif total_reviews and total_reviews > 1000:
            figsize = (14, 7)
        else:
            figsize = (10, 6)
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=figsize)
        
        labels = sentiment_counts.index.tolist()
        values = sentiment_counts.values.tolist()
        colors_list = [colors_dict.get(label, '#95a5a6') for label in labels]
        
        bars = ax.bar(labels, values, color=colors_list, edgecolor='black', linewidth=1.5)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}',
                    ha='center', va='bottom', fontsize=12, weight='bold')
        
        ax.set_xlabel('Sentiment Category', fontsize=12, weight='bold')
        ax.set_ylabel('Number of Reviews', fontsize=12, weight='bold')
        
        # Dynamic title based on review count
        if total_reviews:
            title = f'Patient Review Sentiment Distribution\n({total_reviews:,} Reviews Analyzed)'
        else:
            title = 'Patient Review Sentiment Distribution\n(Bar Chart)'
        
        ax.set_title(title, fontsize=14, weight='bold', pad=20)
        
        # Format y-axis with thousands separator
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✅ Bar chart saved to '{output_path}'")
        
        return output_path
    
    except Exception as e:
        print(f"❌ Error creating bar chart: {e}")
        return None


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print()
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Define file paths relative to the script directory (not current working directory)
    input_csv = script_dir / 'Inputs' / 'patient_reviews.csv'
    output_csv = script_dir / 'Outputs' / 'patient_reviews_with_sentiment.csv'
    pie_chart_path = script_dir / 'Outputs' / 'sentiment_pie_chart.png'
    bar_chart_path = script_dir / 'Outputs' / 'sentiment_bar_chart.png'
    
    # Install missing dependencies first
    install_missing_dependencies()
    
    # Run the analysis
    df_results, sentiment_counts, total_reviews = analyze_patient_reviews(
        input_csv=str(input_csv),
        output_csv=str(output_csv),
        generate_if_missing=True
    )
    
    # Create visualizations with total_reviews for adaptive sizing and titles
    create_pie_chart(sentiment_counts, str(pie_chart_path), total_reviews)
    create_bar_chart(sentiment_counts, str(bar_chart_path), total_reviews)
    
    print()
    print("=" * 70)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 70)
    print("\n📁 Output Files Generated:")
    print(f"   💾 CSV:  {output_csv}")
    print(f"   📊 Chart: {pie_chart_path}")
    print(f"   📊 Chart: {bar_chart_path}")
    print("\n✨ Thank you for using the Sentiment Analysis System!")
    print()
