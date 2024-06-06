from flask import Flask, render_template, request
app = Flask(__name__)

#--------------
import re
import zeyrek
import nltk
import joblib
import tensorflow as tf

nltk.download('punkt')
analyzer = zeyrek.MorphAnalyzer()

import logging
zeyrek_rulebasedanalyzer_logger = logging.getLogger('zeyrek.rulebasedanalyzer')
zeyrek_rulebasedanalyzer_logger.setLevel(logging.CRITICAL)

model = tf.keras.models.load_model('model4.h5')
with open('tokenizer4.pkl', 'rb') as f:
    token_dict = joblib.load(f)

emotions = ["neşeli", "kızgın", "mutlu", "kıskanç", "sürpriz", "üzgün", "heyecanlı", "inatçı", "şaşkın", "korku"]
emotion_dict = {idx: emotion for idx, emotion in enumerate(emotions)}

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip()
    return text

def split_sentence(sentence):
    sentence = preprocess_text(sentence)
    tokens = []
    words = sentence.split()
    for word in words:
        analyses = analyzer.analyze(word)
        for analysis in analyses:
            for parse in analysis:
                try:
                    data = parse.formatted
                    data = data.split(" ")[1]
                    datas = data.split("|")
                    for d in datas:
                        for i in d.split("+"):
                            if ":" in i:
                                tokens.append(i.split(":")[0])
                except:
                    tokens.append(parse.word)
                break  # Taking the first parse for simplicity
            break  # Taking the first analysis for simplicity
    return tokens

def text_to_token_indices(tokens):
    return [token_dict[token] for token in tokens if token in token_dict]

def texts_to_sequences(text):
    tokens = split_sentence(text)
    print(tokens)
    token_indices = [text_to_token_indices(tokens)]
    padded_sequence = tf.keras.preprocessing.sequence.pad_sequences(token_indices, maxlen=model.input_shape[1])
    return padded_sequence

# Duygu tahmini fonksiyonu
def predict_emotion(sentence):
    scaled_padded_sequence = texts_to_sequences(sentence)
    prediction = model.predict(scaled_padded_sequence)[0]
    # En yüksek olasılığa sahip üç duygu
    top_3_indices = prediction.argsort()[::-1]
    top_3_emotions = [(emotion_dict[idx].capitalize(), prediction[idx]) for idx in top_3_indices]
    return top_3_emotions


#--------------

@app.route('/') 
def index(): 
    return render_template('index.html')

# Duygu tahmini yapma route'u 
@app.route('/predict', methods=['POST'])  
def predict():  
    if request.method == 'POST':  
        print(request.form) 
        if 'text' in request.form:  
            text = request.form['text'] 
            # Metni vektöre dönüştür  
            prediction = predict_emotion(text) 
            # Tahmini yap  
            text = request.form['text'] 
            # Tahmini sonucu döndür  
            return render_template('result.html', prediction=prediction, text=text)  
        else:  
            return "Form verisinde 'text' alanı bulunamadı." 

if __name__ == '__main__': 
    app.run(debug=True)