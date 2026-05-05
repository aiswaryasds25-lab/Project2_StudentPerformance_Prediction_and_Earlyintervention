# Student Performance Prediction and Early Intervention

## Team Members
- Aiswarya S
- Arun P.S
- Sanika J.R

## Problem Statement
Predict whether students will pass or fail using academic and demographic data, and identify at-risk students early.

## Dataset
UCI Student Performance Dataset

##  Motivation

Student performance prediction is important for:
- Identifying weak students early
- Supporting academic planning
- Improving overall success rates

##  Dataset Description

- Source: UCI Student Performance Dataset
- Records: ~395 students
- Features include:
  - G1, G2 (previous grades)
  - Study time
  - Failures
  - Absences
  - Family and social attributes

###  Target Variable
- **Pass (1)** → Final grade ≥ 10  
- **Fail (0)** → Final grade < 10  

---

##  Methodology

### 1. Data Preprocessing
- Handled missing values
- Converted categorical variables using encoding
- Created target variable (Pass/Fail)

### 2. Exploratory Data Analysis (EDA)
- Distribution of grades
- Relationship between study time and performance
- Failure patterns

### 3. Feature Engineering
- Removed irrelevant features
- Encoded categorical variables

### 4. Model Building
Models used:
- Logistic Regression
- Decision Tree
- Gradient Boosting

### 5. Model Evaluation

| Model | Accuracy |
|------|--------|
| Logistic Regression | 92.4% |
| Decision Tree | 88.6% |
| Gradient Boosting | 86.0% |

 Logistic Regression performed best and was selected as final model.

---

##  Model Explainability

We used LIME to interpret individual predictions.

Example insight:
- Low G1 and G2 strongly indicate failure risk
- Low study time contributes to poor performance


---

##  Deployment

The model is deployed using Streamlit.

🔗 Live App: 

