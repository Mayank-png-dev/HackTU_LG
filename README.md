# 🚀🔥 **LiverGuard** – AI + IoT Powered Non-Invasive Liver Health Screening 🧠📡

> ### 🩺⚡ *Real-time. Non-invasive. AI-driven.*  
> **LiverGuard** is an end-to-end **AI + IoT system** for **real-time liver health risk screening** using multi-sensor signals and **ensemble machine learning**.  
> Built for **hackathons, demos, and rapid deployment**.

---

## 🌟✨ **Why LiverGuard?**

- 🧪 **Non-Invasive Screening** – No blood tests, no pain  
- 🤖 **Ensemble AI Models** – XGBoost, Random Forest, SVMs + Stacking/Voting  
- 📡 **IoT-Enabled** – Real-time data via ESP32  
- 🌐 **Live Web Dashboard** – Streamlit UI  
- ⚡ **Production-Ready Backend** – FastAPI + `.pkl` model artifacts  
- 🔁 **Train → Serialize → Deploy** – Clean ML ops pipeline

---

## 🧩🏗️ **System Architecture**

**➡️ Data Flow:**  
**Sensors 🧠 → ESP32 📡 → FastAPI (ML Inference) ⚙️ → Streamlit Web App 🌐**

**🧱 Layers:**
- 🧪 **Sensing Layer:** Generic physiological + imaging signals  
- 📡 **Edge Layer:** ESP32 streams readings over Wi-Fi  
- 🧠 **ML Inference Layer:** Python backend loads `.pkl` models  
- 🌐 **Application Layer:** Streamlit dashboard for real-time results

---

## 🛠️💻 **Tech Stack**

**Backend ⚙️**  
- 🐍 Python, ⚡ FastAPI  
- 📦 scikit-learn, XGBoost, CatBoost  
- 💾 Joblib (model serialization)

**ML 🧠**  
- 🎨 Feature Engineering (Yellowness Index)  
- 📏 Robust Scaling  
- 🧩 Ensemble Learning (Voting + Stacking)  
- 📈 ROC–AUC Optimization

**Frontend 🌐**  
- 🖥️ Streamlit

**IoT 📡**  
- 🔌 ESP32 (Wi-Fi streaming)

---

## 🧪🧠 **Machine Learning Pipeline**

### ✨ Feature Engineering
- 🎨 RGB → XYZ color space  
- ⚖️ Gray-world white balance  
- 🔆 Gamma correction  
- 🟡 **Yellowness Index** (proxy biomarker)  
- 📊 Physiological + demographic features

### 🤖 Models Used
- 🌳 Random Forest  
- 🚀 XGBoost  
- 🐱 CatBoost  
- 🧲 SVM (RBF + Polynomial)  
- 📐 Logistic Regression (meta-learner)

### 🧩 Ensembles
- 🗳️ **Soft Voting (Production Model)**  
- 🧠 **Stacked Ensemble (Best Offline ROC–AUC)**

### 📊 Evaluation
- 📈 ROC–AUC (primary metric)  
- 🎯 Precision, Recall, F1  
- 🧪 ROC Curves

---

## 📦💾 **Serialized Artifacts**

```txt
models/
 ├── scaler.pkl          # 🔁 Preprocessing scaler
 ├── voting_model.pkl   # ⚡ Production inference model
 └── stacked_model.pkl  # 🏆 Best offline accuracy model
