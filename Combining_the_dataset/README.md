# Combining the Dataset – Multi-Sensor Data Fusion

This folder contains the notebooks and scripts used to combine and align data coming from multiple sensing modalities in the LiverGuard project.

The goal of this step is to construct a single, ML-ready dataset by fusing:
- Camera-based features (RGB, color composites)
- Thermal sensor readings (Temp9061, Temp9064)
- Bio-signal features (GSR)
- Physiological attributes (Age, Gender, BMI)

This data fusion step enables true multi-modal learning, where the machine learning model can learn correlations across visual, thermal, and bio-impedance signals together.

---

## 📁 Contents

- `combining_the_dataset_.ipynb`  
  Notebook that:
  - Loads raw datasets from different sensor pipelines  
  - Aligns samples using a common subject/sample ID (`S. No.`)  
  - Merges features into a unified table  
  - Exports the final fused dataset for ML training  

---

## 🔧 What This Step Does

1. **Load Raw Data**  
   Reads Excel/CSV files containing camera features and bio-signal data.

2. **Align Samples**  
   Matches rows from different datasets using a common identifier (`S. No.`) so that features from different sensors correspond to the same subject.

3. **Merge Features**  
   Combines RGB, thermal, GSR, and physiological features into a single DataFrame.

4. **Export Final Dataset**  
   Saves the fused dataset for downstream ML preprocessing and training.

---

## 🧠 Why Data Fusion?

In a real-world deployment, the LiverGuard device collects multiple complementary signals from different sensors.  
Combining these modalities at the data level allows the ML model to:
- Capture cross-sensor correlations  
- Improve robustness compared to single-sensor approaches  
- Better reflect the real multi-sensor hardware setup

---

## ⚠️ Notes

- This step focuses only on **data engineering and fusion**.  
- Label normalization and ML-specific preprocessing are handled in the ML pipeline notebooks.  
- The fused dataset produced here is the input to the machine learning training and inference stages.

---

## 🚀 Next Steps

- Feature normalization and encoding  
- Label fusion and class balancing  
- Model training and evaluation  
- Integration with backend API for real-time inference
