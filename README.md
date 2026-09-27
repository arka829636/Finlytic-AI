# Finlytic AI — Intelligent Personal Finance Assistant

Finlytic AI is a multi-user personal finance application built with **Python and Streamlit**. It combines financial analytics, machine learning, rule-based financial assistance, semantic search, and a local **Retrieval-Augmented Generation (RAG)** pipeline to help users understand and manage their financial data.

The application allows users to securely maintain their own financial data, analyze income and expenses, track budgets, identify unusual transactions, estimate future expenses, and ask finance-related questions through an intelligent Finance Chat interface.

---

## 🚀 Key Features

### 🔐 1. Authentication & Multi-User Support

Finlytic AI supports multiple users with isolated financial data.

Features include:

- User registration
- User login
- Password authentication
- Password reset using a temporary verification code
- Session-based authentication
- Separate database for each user
- User-specific transactions
- User-specific budgets
- User-specific analytics

Each user's financial information is stored separately to prevent data mixing between accounts.

---

### 📊 2. Financial Dashboard

The dashboard provides an overview of the user's financial condition.

It includes:

- Total income
- Total expenses
- Total savings
- Savings rate
- Expense breakdown
- Category-wise spending
- Financial summaries
- Visual analytics

The dashboard helps users understand their overall financial behavior from a single interface.

---

### 💳 3. Transaction Management

Users can manage their financial transactions.

Supported information includes:

- Transaction date
- Description
- Category
- Amount
- Transaction type
- Income
- Expense

The application stores transaction data in a user-specific SQLite database.

---

### 📈 4. Financial Analytics

Finlytic AI performs data analysis on financial transactions.

Analytics include:

- Income analysis
- Expense analysis
- Category-wise spending
- Savings analysis
- Spending patterns
- Monthly financial summaries
- Expense comparisons

The project uses Python data-processing libraries to transform raw transaction data into meaningful financial insights.

---

# 🤖 Machine Learning Features

### 🔮 5. Expense Prediction

Finlytic AI includes a machine-learning-based expense prediction module.

The system analyzes historical expense data and estimates future expenses.

The prediction pipeline includes:

1. Retrieve historical transaction data
2. Prepare expense data
3. Generate time-based features
4. Train the prediction model
5. Generate a future expense estimate
6. Compare the prediction with historical spending

Example output:

```text
Predicted next expense: ₹386.62
Historical average: ₹534.97
Expected change: -27.8%
```

The prediction module is intended as an experimental financial forecasting feature rather than a financial guarantee.

---

### 🚨 6. Anomaly Detection

Finlytic AI uses **Isolation Forest**, an unsupervised machine learning algorithm, to identify potentially unusual expense transactions.

The system analyzes transaction amounts and classifies transactions as:

- Normal
- Anomalous

Example result from the project dataset:

```text
Total expense transactions: 192
Normal transactions: 182
Anomalies detected: 10
Anomaly rate: 5.2%
```

This can help users identify transactions that deserve further review.

---

# 💬 Finance Chat

### 🧠 7. Intelligent Finance Chat

Finlytic AI includes a Finance Chat interface where users can ask questions about their financial data.

The system recognizes different types of financial questions.

Supported intents include:

- Income
- Expenses
- Savings
- Category spending
- Expense analysis
- Savings projection
- Expense prediction
- Anomaly detection
- Financial comparison
- Financial advice
- General financial questions

Example questions:

```text
Give me an overview of my finances.

How can I reduce my spending?

Am I saving enough?

Why are my expenses high?

How much can I save next month?

What is my highest spending category?
```

The system analyzes the user's financial data and provides a contextual response.

---

# 🧠 LLM Integration

Finlytic AI includes an LLM integration layer through a dedicated client module.

The architecture supports:

- LLM-based financial responses
- Financial-data context
- Mock LLM mode
- Real API integration

For the current project version, **Mock LLM mode is enabled** so the application can run without purchasing API credits.

Configuration:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5.6
MOCK_LLM=true
```

The real LLM integration can be enabled later by configuring the required API credentials.

---

# 📚 Retrieval-Augmented Generation (RAG)

Finlytic AI includes a local semantic RAG pipeline for retrieving relevant financial knowledge.

The RAG system is designed to provide finance-related information from a controlled local knowledge base rather than relying only on the language model.

## RAG Pipeline

```text
User Question
      ↓
Query Processing
      ↓
Semantic Embedding
      ↓
Knowledge Base Search
      ↓
Similarity Calculation
      ↓
Relevance Filtering
      ↓
Relevant Financial Context
      ↓
Finance Chat
```

---

## 🔎 Semantic Search

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

for generating semantic embeddings.

The embedding model produces vectors with:

```text
384 dimensions
```

The system compares the query embedding with stored document embeddings using similarity scoring.

This allows the system to retrieve content based on semantic meaning rather than only exact keyword matching.

---

## 📖 Knowledge Base

The current local knowledge base is:

```text
data/knowledge_base/finance_basics.md
```

It contains financial information organized into sections such as:

- Emergency Fund
- Budgeting
- Savings Rate
- Needs and Wants
- Debt Management
- Financial Safety

---

## 🧩 RAG Chunking

The knowledge base is processed using section-aware chunking.

The pipeline:

1. Reads the Markdown knowledge base
2. Detects section headings
3. Preserves section titles
4. Splits larger sections into smaller chunks
5. Generates embeddings
6. Stores the embeddings in memory
7. Retrieves the most relevant chunks

The current chunking configuration uses approximately:

```text
Maximum chunk size: 180 words
Overlap: 30 words
```

---

## 🎯 Relevance Filtering

Retrieved documents are filtered using a relevance threshold.

Current threshold:

```text
0.40
```

Only sufficiently relevant knowledge-base sections are shown to the user.

For example, a question about an emergency fund can retrieve:

```text
Emergency Fund
Relevance: 0.600
```

while lower-relevance results can be removed.

This reduces irrelevant knowledge-base content being displayed to the user.

---

# 🏗️ System Architecture

High-level architecture:

```text
                    ┌─────────────────────┐
                    │        User         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    │       app.py        │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
 ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
 │ Authentication │   │ Finance        │   │ RAG Engine     │
 │     System     │   │ Analytics      │   │                │
 └───────┬────────┘   └───────┬────────┘   └───────┬────────┘
         │                    │                    │
         ▼                    ▼                    ▼
 ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
 │ Auth Database  │   │ User Database  │   │ Knowledge Base │
 │    auth.db    │   │ SQLite DB      │   │ finance_basics │
 └────────────────┘   └───────┬────────┘   └────────────────┘
                              │
               ┌──────────────┼──────────────┐
               │              │              │
               ▼              ▼              ▼
        ┌────────────┐ ┌────────────┐ ┌───────────────┐
        │ Analytics  │ │ ML Modules │ │ Finance Chat  │
        └────────────┘ └─────┬──────┘ └───────┬───────┘
                             │                │
                             ▼                ▼
                    ┌────────────────┐ ┌───────────────┐
                    │ Prediction     │ │ LLM Client    │
                    │ + Anomaly      │ │ / Mock LLM    │
                    └────────────────┘ └───────────────┘
```

For a detailed architecture explanation, see `architecture.md`.

---

# 🛠️ Technology Stack

## Programming Language

- Python

## Frontend / UI

- Streamlit

## Data Processing

- Pandas
- NumPy

## Data Visualization

- Matplotlib
- Seaborn
- Streamlit visual components

## Database

- SQLite

## Authentication

- SQLite
- PBKDF2-HMAC-SHA256 password hashing
- Session-based authentication

## Machine Learning

- Scikit-learn
- Isolation Forest
- Expense prediction model

## NLP / RAG

- Sentence Transformers
- `all-MiniLM-L6-v2`
- Semantic embeddings
- Cosine similarity / vector similarity
- Local Markdown knowledge base

## LLM

- OpenAI-compatible LLM client architecture
- Mock LLM mode

## Configuration

- python-dotenv
- `.env`

## Development Tools

- VS Code
- Git
- GitHub

---

# 📁 Project Structure

```text
ai-personal-finance-assistant/
│
├── app.py
├── app_final_polished.py
├── README.md
├── architecture.md
├── config.toml
├── .gitignore
│
├── data/
│   └── knowledge_base/
│       └── finance_basics.md
│
├── src/
│   ├── analysis.py
│   ├── anomaly_detection.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── finance_chat.py
│   ├── llm_client.py
│   ├── ml_expense_prediction.py
│   └── rag_engine.py
│
└── .streamlit/
```

---

# 🔐 Data & Security

The project includes several security-oriented design choices.

### Password Security

Passwords are not stored as plain text.

The authentication system uses:

```text
PBKDF2-HMAC-SHA256
```

with:

- Random salt
- 100,000 iterations
- Secure password hashing

### Environment Variables

API credentials are stored using environment variables.

Example:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5.6
MOCK_LLM=true
```

The `.env` file is excluded from Git using `.gitignore`.

### Database Protection

Database files are also excluded from Git:

```gitignore
*.db
*.sqlite
*.sqlite3
```

This prevents local user financial data from being committed to the repository.

---

# 🗃️ Multi-User Database Architecture

The authentication database is separated from user financial databases.

```text
data/
│
├── auth.db
│
└── users/
    ├── user_1.db
    ├── user_2.db
    ├── user_3.db
    └── ...
```

The architecture provides logical data isolation between users.

Each user receives their own financial database containing their:

- Transactions
- Budgets
- Application metadata

---

# 📊 Example Financial Analysis

The application can generate summaries such as:

```text
Income:        ₹135,000
Expenses:      ₹102,714.10
Savings:       ₹32,285.90
Savings Rate:  23.9%
```

It can also identify major spending categories and provide category-level insights.

---

# 🔬 Machine Learning Results

The current experimental expense prediction model produced:

```text
Predicted expense: ₹386.62
Historical average: ₹534.97
Expected change: -27.8%

MAE:  ₹376.54
RMSE: ₹477.07
R²:   -0.0542
```

The relatively low/negative R² indicates that the current prediction model is experimental and should not be treated as a production-grade forecasting system.

The project intentionally presents these results transparently rather than claiming highly accurate financial prediction.

---

# 🎯 Project Objectives

The main objectives of Finlytic AI are:

1. Build a practical personal finance management application.
2. Implement secure multi-user authentication.
3. Separate financial data between users.
4. Analyze income and expenses.
5. Implement budget tracking.
6. Apply machine learning to financial transaction data.
7. Detect potentially unusual transactions.
8. Predict future expenses experimentally.
9. Build an intelligent finance-oriented chat interface.
10. Implement a local semantic RAG pipeline.
11. Combine structured financial data with unstructured financial knowledge.
12. Demonstrate an end-to-end Data Science + ML + AI application.

---

# 💡 Real-World Problem

Managing personal finances often involves scattered transaction records, manual expense analysis, and difficulty understanding spending patterns.

Finlytic AI attempts to combine these activities into one application.

Instead of only showing transaction records, the system provides:

```text
Financial Data
      ↓
Data Processing
      ↓
Analytics
      ↓
Machine Learning
      ↓
Anomaly Detection
      ↓
Finance Chat
      ↓
Financial Knowledge Retrieval
```

This creates a single environment for exploring personal financial information.

---

# 🧪 Current Project Status

## Implemented

- [x] User registration
- [x] User login
- [x] Password reset
- [x] Multi-user support
- [x] User-specific databases
- [x] Transaction management
- [x] Financial dashboard
- [x] Financial analytics
- [x] Budget management
- [x] Expense prediction
- [x] Anomaly detection
- [x] Finance Chat
- [x] Mock LLM integration
- [x] Local finance knowledge base
- [x] Section-aware RAG chunking
- [x] Semantic embeddings
- [x] Semantic retrieval
- [x] Relevance filtering
- [x] Git/GitHub project setup

---

# 🚧 Future Roadmap

The following features are planned improvements rather than currently completed features.

### RAG Improvements

- Grounded natural-language answer generation
- Hybrid keyword + semantic retrieval
- Reranking
- RAG evaluation
- Hallucination protection
- Personalized financial knowledge retrieval

### AI Improvements

- Better financial intent detection
- Personalized recommendations
- Conversation memory
- More advanced financial forecasting
- Improved anomaly detection features

### Application Improvements

- Improved UI/UX
- Mobile-friendly interface
- Production deployment
- Improved authentication architecture
- More scalable database architecture

---

# ▶️ How to Run the Project

## 1. Clone the repository

```bash
git clone https://github.com/arka829636/ai-personal-finance-assistant.git
```

```bash
cd ai-personal-finance-assistant
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5.6
MOCK_LLM=true
```

The application can run in Mock LLM mode without an API key.

## 5. Run the application

Use:

```bash
python -m streamlit run app.py --server.fileWatcherType none
```

The application will open in the browser.

---

# 🧑‍💻 Development Notes

The application is designed as a modular project.

Important modules include:

| Module | Responsibility |
|---|---|
| `app.py` | Main Streamlit application |
| `auth.py` | Authentication and password management |
| `database.py` | User-specific database management |
| `analysis.py` | Financial analysis |
| `finance_chat.py` | Finance Chat logic |
| `llm_client.py` | LLM integration |
| `ml_expense_prediction.py` | Expense prediction |
| `anomaly_detection.py` | ML anomaly detection |
| `rag_engine.py` | Semantic RAG pipeline |
| `config.py` | Environment/configuration management |

---

# 🎓 Skills Demonstrated

This project demonstrates practical experience in:

- Python
- Data Analysis
- Data Processing
- SQL / SQLite
- Streamlit
- Machine Learning
- Unsupervised Learning
- Anomaly Detection
- Natural Language Processing
- Semantic Search
- Embeddings
- Retrieval-Augmented Generation
- LLM Integration
- Authentication
- Multi-user Architecture
- Database Design
- Git & GitHub
- Modular Software Architecture

---

# 📌 Project Highlights

Finlytic AI combines multiple areas of modern software and AI development:

```text
Python
   │
   ├── Data Analysis
   │
   ├── Database
   │
   ├── Machine Learning
   │       ├── Expense Prediction
   │       └── Anomaly Detection
   │
   ├── Finance Chat
   │
   ├── LLM Integration
   │
   └── RAG
          ├── Knowledge Base
          ├── Chunking
          ├── Embeddings
          ├── Semantic Retrieval
          └── Relevance Filtering
```

---

# ⚠️ Disclaimer

Finlytic AI is an educational and portfolio project.

The financial insights, predictions, anomaly detection results, and recommendations generated by the application are intended for demonstration and informational purposes only. They should not be treated as professional financial advice or guaranteed financial forecasts.

---

# 👨‍💻 Author

**Arka Mondal**

MCA Student | Data Science | Machine Learning | AI | RAG

---

## ⭐ Project

**Finlytic AI — Intelligent Personal Finance Assistant**

A practical portfolio project combining:

**Data Analytics + Machine Learning + AI + LLM + RAG + Database + Streamlit**
