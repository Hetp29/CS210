import re 
import math 
from collections import Counter, defaultdict 

def load_stopwords(filename):
    with open(filename, 'r') as file:
        stopwords = [line.strip() for line in file]
    return set(stopwords)

def clean_text(text):
    text = re.sub(r'https?://\S+', '', text)
    words_with_spaces = re.findall(r'[\w]+|\s+', text)
    text = ''.join(words_with_spaces)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text 

def remove_stopwords(text, stopwords):
    words = text.split()
    filtered_words = [word for word in words if word not in stopwords]
    return ' '.join(filtered_words)

def apply_stemming(text):
    words = text.split()
    stemmed_words = []
    
    for word in words:
        if word.endswith('ing'):
            stemmed = word[:-3]
            if stemmed:
                stemmed_words.append(stemmed)
            else:
                stemmed_words.append(word)
        elif word.endswith('ly'):
            stemmed = word[:-2]
            if stemmed:
                stemmed_words.append(stemmed)
            else:
                stemmed_words.append(word)
        elif word.endswith('ment'):
            stemmed = word[:-4]
            if stemmed:
                stemmed_words.append(stemmed)
            else:
                stemmed_words.append(word)
        else:
            stemmed_words.append(word)
    
    return ' '.join(stemmed_words)

def preprocess_document(doc_path, stopwords):
    with open(doc_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    cleaned_text = clean_text(content)
    text_without_stopwords = remove_stopwords(cleaned_text, stopwords)
    stemmed_text = apply_stemming(text_without_stopwords)
    
    return stemmed_text

def compute_tf(document_text):
    words = document_text.split()
    word_count = Counter(words)
    total_words = len(words)
    
    tf = {}
    for word, count in word_count.items():
        tf[word] = count / total_words
        
    return tf

def compute_idf(documents):
    word_doc_count = defaultdict(int)
    total_docs = len(documents)
    
    for doc in documents:
        unique_words = set(doc.split())
        for word in unique_words:
            word_doc_count[word] += 1
    
    idf = {}
    for word, doc_count in word_doc_count.items():
        idf[word] = math.log(total_docs / doc_count) + 1
        
    return idf

def compute_tfidf(tf, idf):
    tfidf = {}
    for word, tf_value in tf.items():
        tfidf[word] = round(tf_value * idf.get(word, 0), 2)
    
    return tfidf


def get_top_n_words(tfidf_scores, n=5):
    sorted_words = sorted(tfidf_scores.items(), key=lambda x: (-x[1], x[0]))
    return sorted_words[:n]

def main():
    with open('tfidf_docs.txt', 'r') as file:
        doc_paths = [line.strip() for line in file]
    
    stopwords = load_stopwords('stopwords.txt')
    preprocessed_docs = []
    
    for doc_path in doc_paths:
        preprocessed_content = preprocess_document(doc_path, stopwords)
        preproc_path = f"preproc_{doc_path}"
        with open(preproc_path, 'w', encoding='utf-8') as file:
            file.write(preprocessed_content)
        
        preprocessed_docs.append(preprocessed_content)
        
    idf = compute_idf(preprocessed_docs)
    for i, (doc_path, preprocessed_content) in enumerate(zip(doc_paths, preprocessed_docs)):
        tf = compute_tf(preprocessed_content)
        tfidf_scores = compute_tfidf(tf, idf)
        top_words = get_top_n_words(tfidf_scores, 5)
        tfidf_path = f"tfidf_{doc_path}"
        with open(tfidf_path, 'w', encoding='utf-8') as file:
            formatted_list = "[" + ", ".join([f"('{word}', {score})" for word, score in top_words]) + "]"
            file.write(formatted_list)

if __name__ == "__main__":
    main()