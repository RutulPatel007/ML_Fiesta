# 🌟 Vanni X: Kannada Audio to Intelligent Q&A System 🚀

### 🔍 Overview
**Vanni X** is an advanced AI system designed to transform Kannada audio into an intelligent Q&A experience. By leveraging state-of-the-art AI technologies, it bridges the gap between audio data and actionable insights, enabling seamless user interaction with audio-derived knowledge. 

This project is submitted for a hackathon, and we've fine-tuned it for both functionality and ease of deployment.

---

### 🛠️ Features
- 🎙️ **Audio-to-Text Conversion**: Powered by **Whisper AI**, enabling highly accurate transcription of Kannada audio into English text.
- 🤖 **Fine-Tuned LLaMA Model**: Enhanced with custom Q&A datasets using **LoRA** and **QLoRA** for precise, context-aware responses.
- 💻 **Interactive Streamlit App**: 
  - **Input**: Accepts queries in text or audio format.
  - **Output**: Delivers responses in both **text** and **audio** formats for a comprehensive user experience.

---

### 🔧 How to Run the Project
#### **Pre-requisites**
- Install Python (3.8+ recommended)

#### **Step-by-Step Guide**
1. **Clone the Repository and Install necessary dependencies**  
   ```bash
   git clone https://github.com/RutulPatel007/VANNI-X.git
   cd VANNI-X
   pip install -r requirements.txt
   ```

2. **Start the Express Server**  
   Navigate to the `server` folder and start the backend:  
   ```bash
   cd server
   npm install
   node index.js
   ```

3. **Run the Fine-Tuned Model**  
   Navigate to the `model` folder and execute the Jupyter notebook to load the fine-tuned LLaMA model:  
   ```bash
   cd model
   jupyter notebook
   ```  
   Open `lora_finetuned_model.ipynb` and run all cells to host the model. Update the **model's API URL** in the Express server (`server/index.js`).

4. **Launch the Streamlit Web App**  
   Navigate to the `web_app` folder and start the Streamlit app:  
   ```bash
   cd ../web_app
   streamlit run chat.py
   ```

#### **Commands Summary**
```bash
# Clone repository
git clone https://github.com/RutulPatel007/VANNI-X.git
cd VANNI-X
pip install -r requirements.txt

# Start Express server
cd server
npm install
node index.js

# Run the model
cd model
jupyter notebook

# Start Streamlit web app
cd ../web_app
streamlit run chat.py
```

---

### 📚 Technology Stack
- **Whisper AI**: For Kannada-to-English audio transcription.
- **LLaMA**: Fine-tuned with **LoRA** and **QLoRA** for domain-specific Q&A.
- **Express.js**: Backend server for routing and API integration.
- **Flask**: Hosting the fine-tuned LLaMA model.
- **Streamlit**: For building a dynamic, user-friendly web interface.
- **PyTorch**: Powering model training and inference.

---

### 🚀 Use Cases
- **Language Learning**: Enhance English comprehension for Kannada speakers.
- **Customer Support**: Automate queries for Kannada-speaking users.
- **Education**: Enable interactive study aids using Kannada audio content.

---

### 👥 Team
- Rutul Patel
- Aryaman Pathak
- Shreyas Biradar

---

### 🌟 Why Choose Vanni X?
- **Inclusive**: Empowers Kannada-speaking communities.
- **Interactive**: Provides real-time Q&A with multi-format outputs.
- **State-of-the-Art**: Combines advanced AI techniques for superior performance.

---


### 🙌 Acknowledgments
Special thanks to:
- **OpenAI** for Whisper AI.
- **Hugging Face** for model fine-tuning resources.
- The open-source community for datasets and inspiration.

