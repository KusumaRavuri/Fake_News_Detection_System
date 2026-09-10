# 📰 TruthLens — Fake News Detection System

An NLP and machine learning-based web application that classifies news text as **Fake** or **Real**.

## 🚀 Live Demo

👉 **[Open TruthLens](https://truthlens-fake-news.streamlit.app/)**

## 📌 Overview

**TruthLens** uses Natural Language Processing (NLP) and machine learning to analyze the text of a news article and predict whether it is likely to be **Fake** or **Real**.

The project provides a simple Streamlit interface where users can enter news text and receive an instant prediction.

> **Note:** The prediction is based on patterns learned from the training dataset and should not be treated as a definitive fact-checking or source-verification system.

## ✨ Features

- 📰 Classifies news as **Fake** or **Real**
- 🔤 Uses **TF-IDF** for text feature extraction
- 🤖 Uses **Logistic Regression** for classification
- 📊 Achieved **99.37% accuracy** on the evaluated dataset
- 🌐 Interactive Streamlit web interface
- ⚡ Fast text-based prediction
- 💾 Saved model and vectorizer for inference

## 🛠️ Tech Stack

- **Python**
- **Pandas** — Data preprocessing and handling
- **NumPy** — Numerical operations
- **Scikit-learn** — Machine learning and evaluation
- **TF-IDF** — Text feature extraction
- **Logistic Regression** — Classification model
- **Streamlit** — Web interface
- **Pickle** — Model and vectorizer serialization

## 🔄 How It Works

```text
News Text
   ↓
Text Preprocessing
   ↓
TF-IDF Vectorization
   ↓
Logistic Regression Model
   ↓
Fake / Real Prediction
```

## 📊 Model Performance

| Metric | Score |
|---|---:|
| Accuracy | **99.37%** |

The reported accuracy is based on the project's evaluated dataset and may not represent performance on new or real-world news sources.

## 📂 Project Structure

```text
Fake_News_Detection_System/
│
├── app.py
├── model.pkl
├── vectorizer.pkl
├── requirements.txt
└── README.md
```

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/KusumaRavuri/Fake_News_Detection_System.git
cd Fake_News_Detection_System
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🖥️ Usage

1. Open the application.
2. Enter or paste a news article/text.
3. Click the prediction button.
4. View the **Fake** or **Real** result.

## 📦 Saved Model Files

The trained components are stored for reuse during prediction:

- `model.pkl` — trained Logistic Regression model
- `vectorizer.pkl` — fitted TF-IDF vectorizer

## ⚠️ Limitations

- Predictions depend on the quality and coverage of the training dataset.
- The model may misclassify unfamiliar writing styles or topics.
- It analyzes the provided text rather than independently verifying claims.
- It does not perform live source or URL verification.

## 🔮 Future Improvements

- Add transformer-based models such as BERT
- Support multiple languages
- Add source and URL verification
- Improve robustness using larger and more diverse datasets
- Provide confidence scores and explainable predictions

## 👩‍💻 Author

**Kusuma Ravuri**

B.Tech — Computer Science and Engineering, GITAM

**GitHub:** https://github.com/KusumaRavuri
