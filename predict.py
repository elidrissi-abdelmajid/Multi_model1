from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
# from sentiment_predict import predict_sentiment
# Initialize FastAPI app
app = FastAPI()
from langdetect import detect

try:
    with open('train_model/tfidf_vectorizer.pkl', 'rb') as f:
        loaded_vectorizer = pickle.load(f)
    print("TF-IDF vectorizer loaded successfully!")
except FileNotFoundError:
    print("TF-IDF vectorizer file not found!")
except Exception as e:
    print(f"Error loading TF-IDF vectorizer: {e}")

with open('train_model/svm_famille_model.pkl', 'rb') as f:
     svm_famille = pickle.load(f)
with open('train_model/svm_produit_model.pkl', 'rb') as f:
     svm_produit = pickle.load(f)
with open('train_model/svm_objet_model.pkl', 'rb') as f:
     svm_objet = pickle.load(f)
with open('train_model/svm_cat_model.pkl', 'rb') as f:
     svm_first_cat = pickle.load(f)


# Function to detect language
def detect_language(text):
    try:
        detected_lang = detect(text)  # Detects the language
        if detected_lang == 'fr':
            return 'francais'  # French
        elif detected_lang == 'en': 
            return 'english'  # English
        elif detected_lang == 'ar':  
            return 'arabic' 
        else :
            return "Darija"
    except Exception as e:
        return "Error"  # If language detection fails
# Define a Pydantic model for input validation
class MessageInput(BaseModel):
    message: str

@app.post("/predict/")
async def predict(input_data: MessageInput):
    try:
        # Get the message from the request
        message = input_data.message
        
        # Transform the message using the TF-IDF vectorizer
        message_tfidf = loaded_vectorizer.transform([message])
        
        # Make predictions using the loaded models
        first_cat_prediction = svm_first_cat.predict(message_tfidf)[0]
        famille_prediction = svm_famille.predict(message_tfidf)[0]
        produit_prediction = svm_produit.predict(message_tfidf)[0]
        objet_prediction = svm_objet.predict(message_tfidf)[0]

        # Return predictions as JSON
        if first_cat_prediction =="CLAIM" : 
            return {
                        "langue" : detect_language(message),     
                        "first categorie" :first_cat_prediction,
                        "famille":  famille_prediction,
                        "produit":  produit_prediction,
                        "objet":    objet_prediction,
                        # "sentiment" : predict_sentiment(message)                                             
            }
        else :
            return {
                "langue" : detect_language(message),
                "first categorie" :first_cat_prediction,
                # "sentiment" : predict_sentiment(message)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
input="bonjour je suis la pour toi"
print(svm_first_cat.predict(loaded_vectorizer.transform([input]))[0])