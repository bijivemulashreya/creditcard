# from flask import Flask, render_template, request
# import joblib
# import numpy as np

# app = Flask(__name__)
# model = joblib.load('data.pkl')
# scaler = joblib.load('scaler.pkl')  # If you scaled annual income, load the scaler

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     Car_Owner = 1 if request.form['Car_Owner'] == 'Yes' else 0
#     Propert_Owner = 1 if request.form['Propert_Owner'] == 'Yes' else 0
#     Annual_income = float(request.form['Annual_income'])

#     # Apply scaler if used during training
#     Annual_income_scaled = scaler.transform([[Annual_income]])[0][0]

#     education_map = {
#         "Secondary / secondary special": 0,
#         "Higher education": 1,
#         "Incomplete higher": 2,
#         "Lower secondary": 3,
#         "Academic degree": 4
#     }
#     EDUCATION = education_map[request.form['EDUCATION']]

#     features = np.array([[Car_Owner, Propert_Owner, Annual_income_scaled, EDUCATION]])
#     prediction = model.predict(features)[0]

#     result = "Approved" if prediction == 1 else "Not Approved"
#     return render_template('index.html', prediction=result)

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load('data.pkl')
scaler = joblib.load('scaler.pkl')  # If you scaled annual income, load the scaler

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    Car_Owner = 1 if request.form['Car_Owner'] == 'Yes' else 0
    Propert_Owner = 1 if request.form['Propert_Owner'] == 'Yes' else 0
    Annual_income = float(request.form['Annual_income'])

    education_map = {
        "Secondary / secondary special": 0,
        "Higher education": 1,
        "Incomplete higher": 2,
        "Lower secondary": 3,
        "Academic degree": 4
    }
    EDUCATION = education_map[request.form['EDUCATION']]

    # Rule-based approval system
    if Annual_income > 2000000:
        result = "Approved"
    elif 1000000 < Annual_income <= 2000000:
        if EDUCATION != 3 and Propert_Owner == 1:
            result = "Approved"
        else:
            result = "Not Approved"
    elif 300000 < Annual_income <= 1000000:
        if EDUCATION in [1, 4] and Car_Owner == 1 and Propert_Owner == 1:
            result = "Approved"
        else:
            result = "Not Approved"
    elif Annual_income <= 300000:
        result = "Not Approved"
    else:
        # If none of the conditions match (fallback to model)
        Annual_income_scaled = scaler.transform([[Annual_income]])[0][0]
        features = np.array([[Car_Owner, Propert_Owner, Annual_income_scaled, EDUCATION]])
        prediction = model.predict(features)[0]
        result = "Approved" if prediction == 1 else "Not Approved"

    return render_template('index.html', prediction=result)

if __name__ == '__main__':
    app.run(debug=True)
