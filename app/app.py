
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import lime.lime_tabular
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(__file__)

model         = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
feature_names = joblib.load(os.path.join(BASE_DIR, "feature_names.pkl"))
X_train       = joblib.load(os.path.join(BASE_DIR, "X_train.pkl"))

# Build LIME explainer on the fly
explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X_train,
    feature_names=feature_names,
    class_names=["Fail", "Pass"],
    mode="classification"
)

st.set_page_config(page_title="Student Performance Predictor", layout="wide")
st.title("🎓 Student Performance Prediction & Early Intervention")
st.markdown("Adjust the student details in the sidebar to predict **Pass / Fail**.")

st.sidebar.header("📋 Student Details")
G1        = st.sidebar.slider("Grade Period 1 (G1)", 0, 20, 10)
G2        = st.sidebar.slider("Grade Period 2 (G2)", 0, 20, 10)
studytime = st.sidebar.selectbox("Study Time (1=<2h  2=2-5h  3=5-10h  4=>10h)", [1,2,3,4])
failures  = st.sidebar.selectbox("Past Class Failures", [0,1,2,3])
absences  = st.sidebar.slider("Number of Absences", 0, 75, 5)
age       = st.sidebar.slider("Age", 15, 22, 17)
Medu      = st.sidebar.selectbox("Mother Education (0=none to 4=higher)", [0,1,2,3,4])
Fedu      = st.sidebar.selectbox("Father Education (0=none to 4=higher)", [0,1,2,3,4])
famrel    = st.sidebar.slider("Family Relationship Quality (1-5)", 1, 5, 3)
freetime  = st.sidebar.slider("Free Time After School (1-5)", 1, 5, 3)
goout     = st.sidebar.slider("Going Out with Friends (1-5)", 1, 5, 3)
Dalc      = st.sidebar.slider("Workday Alcohol (1-5)", 1, 5, 1)
Walc      = st.sidebar.slider("Weekend Alcohol (1-5)", 1, 5, 1)
health    = st.sidebar.slider("Health Status (1-5)", 1, 5, 3)

input_data = {f: 0 for f in feature_names}
input_data.update({
    "age": age, "Medu": Medu, "Fedu": Fedu,
    "studytime": studytime, "failures": failures,
    "famrel": famrel, "freetime": freetime,
    "goout": goout, "Dalc": Dalc, "Walc": Walc,
    "health": health, "absences": absences,
    "G1": G1, "G2": G2
})
input_df = pd.DataFrame([input_data])[feature_names]

pred       = model.predict(input_df)[0]
pred_proba = model.predict_proba(input_df)[0]

col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Prediction Result")
    label = "✅ PASS" if pred == 1 else "❌ FAIL — At Risk"
    color = "green" if pred == 1 else "red"
    st.markdown(f"<h2 style='color:{color}'>{label}</h2>", unsafe_allow_html=True)
    st.write(f"**Pass probability:** {pred_proba[1]*100:.1f}%")
    st.write(f"**Fail probability:** {pred_proba[0]*100:.1f}%")
    st.progress(float(pred_proba[1]))
with col2:
    st.subheader("📋 Input Summary")
    key_features = {"G1": G1, "G2": G2, "Study Time": studytime,
                    "Failures": failures, "Absences": absences, "Age": age}
    st.table(pd.DataFrame(key_features.items(), columns=["Feature", "Value"]))

st.subheader("🔍 LIME Explanation — Why this prediction?")
exp = explainer.explain_instance(
    input_df.values[0],
    model.predict_proba,
    num_features=10
)
fig = exp.as_pyplot_figure()
plt.tight_layout()
st.pyplot(fig)

st.markdown("**Key contributing factors:**")
for feat, weight in exp.as_list():
    arrow = "🟢" if weight > 0 else "🔴"
    st.write(f"{arrow} `{feat}` — impact: {weight:.4f}")

if pred == 0:
    st.subheader("🚨 Counselor Intervention Suggestions")
    st.error("This student is predicted to FAIL. Recommended actions:")
    suggestions = set()
    for feat, weight in exp.as_list():
        if weight < 0:
            if "G1" in feat or "G2" in feat:
                suggestions.add("📚 Low prior grades — arrange tutoring or academic support.")
            if "studytime" in feat:
                suggestions.add("⏰ Low study time — encourage a structured study plan.")
            if "failures" in feat:
                suggestions.add("⚠️ Prior failures detected — proactive counseling needed.")
            if "absences" in feat:
                suggestions.add("📅 High absences — investigate attendance issues.")
            if "Dalc" in feat or "Walc" in feat:
                suggestions.add("🍺 Alcohol consumption may be affecting performance.")
            if "goout" in feat:
                suggestions.add("🏠 Excessive socialising may be reducing study time.")
    for s in suggestions:
        st.write(s)
else:
    st.success("✅ Student is on track. Continue monitoring performance.")
