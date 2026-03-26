import os
import shutil

base = r"D:/Professional/Projects/Review_Sentiment_Analysis_Project/Review_Analyzer_Main_Project/.venv/nltk_data/tokenizers"
src = os.path.join(base, 'punkt')
dst = os.path.join(base, 'punkt_tab')
if not os.path.exists(dst):
    os.makedirs(dst, exist_ok=True)
# copy english.pickle
shutil.copy(os.path.join(src, 'english.pickle'), os.path.join(dst, 'english.pickle'))
# copy PY3 dir if exists
src_py3 = os.path.join(src, 'PY3')
dst_py3 = os.path.join(dst, 'PY3')
if os.path.exists(src_py3) and not os.path.exists(dst_py3):
    shutil.copytree(src_py3, dst_py3)

print('Copied punkt resources into punkt_tab folder')
