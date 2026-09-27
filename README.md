# FinanceAI --- AI Personal Finance Assistant

FinanceAI is a multi-user personal finance application built with Python
and Streamlit. It combines financial analytics, machine-learning
components, rule-based finance assistance, and a local semantic RAG
pipeline to help users understand their spending and financial data.

## Current Project Status

**Portfolio-ready student project --- v1.0**

Implemented: - User registration, login, logout and password reset -
Multi-user data isolation with per-user SQLite databases - Financial
dashboard and KPI analysis - Transaction management - Budget tracking
and analysis - Expense analytics - Expense prediction experiment -
Isolation Forest anomaly detection - Finance Chat with intent
detection - Mock LLM mode without paid API credits - Local finance
knowledge base - Section-aware RAG chunking - Sentence Transformer
semantic embeddings - 384-dimensional embeddings using
`all-MiniLM-L6-v2` - Cosine-similarity retrieval - Relevance filtering -
Finance Chat integration with semantic RAG - Streamlit UI/UX

## Architecture

``` mermaid
flowchart TD
    U[User] --> UI[Streamlit UI]
    UI --> AUTH[Authentication]
    AUTH --> ADB[(Auth SQLite DB)]

    UI --> APP[FinanceAI Application Layer]
    APP --> UDB[(Per-user SQLite DB)]

    APP --> ANA[Analytics & Dashboard]
    APP --> BUD[Budget Module]
    APP --> ML1[Expense Prediction]
    APP --> ML2[Isolation Forest Anomaly Detection]
    APP --> CHAT[Finance Chat]

    CHAT --> INTENT[Intent Detection]
    CHAT --> RAG[Semantic RAG]
    RAG --> KB[finance_basics.md]
    RAG --> EMB[all-MiniLM-L6-v2]
    EMB --> SIM[Cosine Similarity]
    SIM --> FILTER[Relevance Filter >= 0.40]

    CHAT --> MOCK[Mock LLM]
```

## Technology Stack

  Technology              Purpose
  ----------------------- -----------------------------------------
  Python                  Core application and data/ML logic
  Streamlit               Web application and UI
  SQLite                  Authentication and user financial data
  Pandas                  Data processing and analytics
  NumPy                   Numerical operations
  Plotly                  Interactive visualization
  Scikit-learn            ML prediction/anomaly components
  Isolation Forest        Unsupervised anomaly detection
  Sentence Transformers   Semantic embeddings
  all-MiniLM-L6-v2        Local embedding model
  Git/GitHub              Version control and portfolio
  `.env`                  Local configuration
  Mock LLM                AI demonstration without paid API usage

## RAG Pipeline

``` text
User question
    ↓
Finance Chat
    ↓
Semantic embedding
    ↓
Cosine similarity search
    ↓
Relevant knowledge chunks
    ↓
Relevance filter (>= 0.40)
    ↓
FinanceAI Knowledge Base response
```

Current knowledge-base sections: - Emergency Fund - Budgeting - Savings
Rate - Needs and Wants - Debt Management - Financial Safety

## Machine Learning

### Expense Prediction

The project contains an experimental expense prediction component with
evaluation metrics including: - MAE - RMSE - R²

The current model is presented honestly as an experimental forecasting
component; prediction accuracy is not claimed to be production-grade.

### Anomaly Detection

Isolation Forest is used for unsupervised expense anomaly detection.

Example evaluation run: - Expense transactions: 192 - Detected
anomalies: 10 - Normal transactions: 182 - Anomaly rate: 5.2%

## Security / Data Design

-   Passwords are hashed using PBKDF2-HMAC-SHA256 with random salts.
-   Authentication data is stored separately from user financial
    databases.
-   Each user receives a separate SQLite database.
-   `.env` is excluded from Git.
-   Database files are excluded from Git.
-   API credentials are not required for the current Mock LLM
    configuration.

## Run Locally

From the project root:

``` powershell
python -m streamlit run app.py --server.fileWatcherType none
```

The `fileWatcherType none` option avoids the optional-module
file-watcher issue encountered with the Transformers dependency.

## Current Limitations

The project is portfolio-ready but not a production fintech system.

Current limitations: - Mock LLM is enabled because no paid API credits
are being used. - RAG currently retrieves and displays grounded
knowledge rather than generating a fully synthesized LLM answer from
retrieved context. - Expense prediction is experimental and has limited
predictive strength. - Authentication/database state is designed for the
student portfolio application, not a production multi-instance
deployment. - Financial information is educational/general and should
not be treated as individualized financial advice.

## Future Roadmap

1.  RAG grounded answer generation
2.  Personalized RAG using user financial data
3.  RAG evaluation dataset and retrieval metrics
4.  Hybrid keyword + semantic retrieval
5.  Reranking
6.  Conversation memory
7.  Production database/authentication architecture
8.  Deployment and monitoring

## Resume Description

**FinanceAI --- AI Personal Finance Assistant**

Built a multi-user personal finance application using Python and
Streamlit with transaction analytics, budgeting, machine-learning
expense analysis, Isolation Forest anomaly detection, Finance Chat, and
a local semantic RAG pipeline using Sentence Transformers and a finance
knowledge base.

## Interview Summary

The strongest way to explain the project is:

> "FinanceAI is a multi-user personal finance assistant that combines
> traditional financial analytics with machine learning and semantic
> RAG. Users can manage transactions and budgets, analyze spending,
> detect anomalous expenses, experiment with expense prediction, and ask
> finance questions. The RAG layer uses a local finance knowledge base,
> Sentence Transformer embeddings, cosine similarity retrieval, and
> relevance filtering, so the current version does not require paid LLM
> API credits."
