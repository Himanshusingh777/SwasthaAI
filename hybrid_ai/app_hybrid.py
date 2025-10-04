import os
from flask import Flask, render_template, request
from model_trainer import load_model
from medicine_lookup import fetch_medicine
from utils import translate_to_hindi, safe_text

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

clf = load_model()

@app.route('/hybrid', methods=['GET', 'POST'])
def hybrid_route():
    result = None
    query = ""
    mode = ""
    if request.method == 'POST':
        query = safe_text(request.form.get('query',''))
        search_type = request.form.get('type', 'auto')
        if search_type == 'medicine' or (search_type == 'auto' and query.lower().startswith('medicine:')):
            mode = 'medicine'
            medicine_name = query.split(':',1)[1].strip() if query.lower().startswith('medicine:') else query
            med = fetch_medicine(medicine_name)
            if med:
                desc_hi = med.get('description_hi') or (translate_to_hindi(med.get('description_en')) if med.get('description_en') else None)
                result = {
                    "mode": "medicine",
                    "query": medicine_name,
                    "name": med.get('name'),
                    "description_en": med.get('description_en'),
                    "description_hi": desc_hi,
                    "price_hint": med.get('price_hint'),
                    "similar": med.get('similar') or med.get('similarMedicines') or []
                }
            else:
                result = {"mode":"medicine", "error":"No information found."}
        else:
            mode = 'symptom'
            try:
                preds = clf.predict_proba([query])
                labels = clf.classes_
                probs = preds[0]
                pairs = sorted(zip(labels, probs), key=lambda x: x[1], reverse=True)[:3]
                suggestions = [{"disease": l, "confidence": round(float(p)*100,1)} for l,p in pairs]
                top_label = pairs[0][0]
                advice_en = f"Possible condition: {top_label}. Please consult a doctor."
                advice_hi = translate_to_hindi(advice_en) or ""
                result = {
                    "mode": "symptom",
                    "query": query,
                    "predictions": suggestions,
                    "advice_en": advice_en,
                    "advice_hi": advice_hi
                }
            except Exception as e:
                result = {"mode":"symptom","error":str(e)}
    return render_template('hybrid.html', result=result, query=query, mode=mode)

if __name__ == "__main__":
    app.run(debug=True)
