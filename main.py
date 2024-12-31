# This is a sample Python script.
#import pickle
import joblib as jl
import pandas as pd
import streamlit as st

st.header("Predicting Chronic Critical Illness in Bone Trauma Patients: An AI-Based Approach for ICU Healthcare Providers")
st.sidebar.title("Selection of Parameters")
st.sidebar.markdown("Picking up parameters")

Pelvic_fractrue = st.sidebar.selectbox("Pelvic fractrue", ("No", "Closed", "Open"))
Ventilation = st.sidebar.selectbox("Mechanical ventilation", ("No", "Yes"))
Respiratory_failure = st.sidebar.selectbox("Respiratory failure", ("No", "Yes"))
Pneumonia = st.sidebar.selectbox("Pneumonia", ("No", "Yes"))
Sepsis = st.sidebar.selectbox("Sepsis", ("No", "Yes"))
Heart_rate = st.sidebar.slider("Heart rate (Beats per minute)", 60, 120)
Respiratory_rate = st.sidebar.slider("Respiratory rate (Beats per minute)", 12, 30)
Albumin = st.sidebar.slider("Albumin (g/dL)", 2.00, 5.00)
Glucose = st.sidebar.slider("Glucose (mg/dL)", 90.0, 190.0)
Calcium = st.sidebar.slider("Total serum calcium (mg/dL)", 6.00, 10.00)
Hematocrit = st.sidebar.slider("Hematocrit (%)", 25.00, 45.00)
OASIS = st.sidebar.slider("OASIS",  20, 45)
SAPSII = st.sidebar.slider("SAPSII", 20, 50)
SOFA = st.sidebar.slider("SOFA", 0, 12)

if st.button("Submit"):
    Xgbc_clf = jl.load("Xgbc_clf_final_round2.pkl")
    x = pd.DataFrame([[Pelvic_fractrue, Ventilation, Respiratory_failure, Pneumonia, Sepsis, Heart_rate, Respiratory_rate, Albumin, Glucose, Calcium, Hematocrit, OASIS,
                              SAPSII, SOFA]],
                     columns=["Pelvic_fractrue", "Ventilation", "Respiratory_failure", "Pneumonia", "Sepsis", "Heart_rate", "Respiratory_rate", "Albumin", "Glucose", "Calcium", "Hematocrit", "OASIS",
                              "SAPSII", "SOFA"])

    x = x.replace(["No", "Yes"], [0, 1])
    x = x.replace(["No", "Closed", "Open"], [0, 1, 2])

    # Get prediction
    prediction = Xgbc_clf.predict_proba(x)[0, 1]
        # Output prediction
    st.text(f"Probability of developing PerCI: {'{:.2%}'.format(round(prediction, 5))}")
    if prediction < 0.586:
        st.success(f"Risk group: low-risk group")
    else:
        st.error(f"Risk group: High-risk group")

st.subheader('Model information')
st.markdown('The eXGBM model demonstrated excellent prediction performance, with the highest value of AUC (0.979, 95%CI: 0.970-0.991) among all the models evaluated. It outperformed the RF model (AUC: 0.957, 95%CI: 0.941-0.967) and the SVM model (AUC: 0.911, 95%CI: 0.878-0.928). The LR model had a relatively lower AUC of 0.753 (95%CI: 0.714-0.793).In terms of accuracy, precision, recall, specificity, F1 score, Brier score, and Log loss, the eXGBM model performed the best among all the models evaluated. External validation of the eXGBM model demonstrated a high AUC of 0.887 (95%CI: 0.863-0.917), indicating good generalizability.')
