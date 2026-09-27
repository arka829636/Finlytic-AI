# FinanceAI Architecture

## High-Level Architecture

``` text
                         ┌─────────────────────┐
                         │       User          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Streamlit UI      │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       Authentication          Finance Data          Finance Chat
              │                     │                     │
              ▼                     ▼                     ▼
        auth.db             User SQLite DB        Intent Detection
                                                        │
                              ┌─────────────────────────┼──────────────┐
                              │                         │              │
                              ▼                         ▼              ▼
                         Analytics                  ML/Rules        Semantic RAG
                              │                         │              │
                              │                 ┌───────┴───────┐      │
                              │                 │               │      │
                              │                 ▼               ▼      ▼
                              │          Expense Prediction  Anomaly  Knowledge Base
                              │                                  │      │
                              │                                  │      ▼
                              │                                  │ Embedding Model
                              │                                  │      │
                              │                                  │      ▼
                              │                                  │ Similarity Search
                              │                                  │      │
                              │                                  └──► Relevance Filter
                              │                                         │
                              └─────────────────────────────────────────┘
```

## Data Isolation

``` text
Authentication DB
     │
     ├── User 1
     │     └── data/users/user_1.db
     │
     ├── User 2
     │     └── data/users/user_2.db
     │
     └── User N
           └── data/users/user_N.db
```

This keeps each user's transaction and budget data separated at the
application/database layer.

## RAG Details

### Ingestion

`finance_basics.md` is parsed into section-aware document chunks.

### Embedding

`sentence-transformers/all-MiniLM-L6-v2` creates 384-dimensional vectors
locally.

### Retrieval

The user query is embedded and compared with document embeddings using
cosine similarity.

### Filtering

Retrieved chunks below the current relevance threshold of `0.40` are
removed from the displayed result.

### Current behavior

The system returns the relevant grounded knowledge section and its
source metadata. Full LLM-based answer synthesis is a planned next
stage.

## ML Components

### Expense Prediction

Historical expense data → feature/model processing → prediction →
MAE/RMSE/R² evaluation.

### Anomaly Detection

Expense amount data → Isolation Forest → anomaly/normal classification →
anomaly summary.
