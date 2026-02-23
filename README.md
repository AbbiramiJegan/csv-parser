# 🪵 Edge AI Wood Quality Control Center

An end-to-end, fully local Edge AI application designed for industrial quality control. This project leverages an **NVIDIA Jetson Orin Nano**, **Ollama**, **Langflow**, and **Streamlit** to analyze live wood defect scanner data and provide a conversational AI assistant—all without sending a single byte of data to the cloud.

## ✨ Features
* **100% Local Processing:** Zero cloud costs and complete data privacy.
* **Live Data Monitoring:** A responsive Streamlit dashboard highlighting high-severity defects in real-time.
* **Conversational AI Agent:** Ask complex questions about the production line (e.g., *"What defect was detected on item ID 102?"*) and get context-aware answers.
* **Visual AI Pipeline:** Easy-to-edit backend logic powered by Langflow.

## 🛠️ Architecture & Tech Stack
* **Hardware:** NVIDIA Jetson Orin Nano (8GB) configured with a static IP.
* **Local LLM:** [Ollama](https://ollama.ai/) running the lightweight `granite3.1-moe:1b-instruct-q8_0` model.
* **Backend logic:** [Langflow](https://langflow.org/) (REST API).
* **Frontend:** [Streamlit](https://streamlit.io/) (Python).

## 📂 Repository Structure
```text
wood-quality-control/
├── .streamlit/
│   └── secrets.toml        # Excluded from git; should contain IPs and API keys
├── data/
│   └── temp_file.csv       # Sample factory scanner data
├── langflow/
│   └── CSV_Parser.json     # Exported Langflow pipeline
├── app.py                  # Streamlit frontend application
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

## 🚀 Step-by-Step Setup Guide

### 1. Prerequisites

You will need an NVIDIA Jetson (or any machine capable of running local LLMs) and a machine to run the Streamlit frontend (this can be the same Jetson device or a separate laptop on the same local network).

### 2. Backend Setup (on the Jetson Orin Nano)

SSH into your edge device:

```bash
ssh user@<YOUR_JETSON_IP>

```

**Install and Run Ollama:**
Follow the instructions on the [Ollama website](https://ollama.ai/) to install it. Once installed, pull the required model:

```bash
ollama run granite3.1-moe:1b-instruct-q8_0

```

**Install and Run Langflow:**
Install Langflow via pip and start the server:

```bash
pip install langflow
langflow run --host 0.0.0.0

```

### 3. Configure the AI Pipeline

1. Open your browser and navigate to the Langflow UI at `http://<YOUR_JETSON_IP>:7860`.
2. Click **Import** and upload the `langflow/CSV_Parser.json` file from this repository.
3. In the Langflow canvas, locate the **Read File** node and update the file path to point to your local `data/temp_file.csv`.
4. Click **Build API** (or API endpoints) in Langflow to generate your `FLOW_ID` and an `API_KEY`.

### 4. Frontend Setup (on your Laptop or Jetson)

Clone this repository to the machine where you want to run the dashboard.

Install the required Python libraries:

```bash
pip install -r requirements.txt

```

Create a Streamlit secrets file to securely store your configuration:

```bash
mkdir .streamlit
touch .streamlit/secrets.toml

```

Add your specific configuration to `.streamlit/secrets.toml`:

```toml
# .streamlit/secrets.toml
JETSON_IP = "192.168.6.21" # Replace with your Jetson's IP
FLOW_ID = "YOUR_LANGFLOW_ID"
API_KEY = "YOUR_LANGFLOW_API_KEY"

```

*(Note: Ensure `.streamlit/secrets.toml` is listed in your `.gitignore` file so you do not accidentally publish your keys!)*

### 5. Run the Application

Start the Streamlit dashboard:

```bash
streamlit run app.py

```

Open the local URL provided by Streamlit in your browser. You should now see the live scanner data table and the conversational defect analyst ready to take your questions!

## 📝 Usage Example

Once the dashboard is running, try asking the AI:

* *"How many items have a 'High' severity defect?"*
* *"What is the confidence score for item ID 106?"*
* *"Are there any Split defects reported today?"*

## 🤝 Contributing

Contributions are welcome! If you find a way to optimize the Langflow pipeline, improve the UI, or want to add support for different scanner data formats, please open an issue or submit a pull request.