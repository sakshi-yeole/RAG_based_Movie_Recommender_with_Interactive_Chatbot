#  RAG-Based Movie Recommendation System with Intractive Chatbot

CineFusion is an explainable movie recommendation system built using a Retrieval-Augmented Generation (RAG) architecture. It integrates semantic retrieval, vector databases, and large language models** to provide relevant, transparent, and interactive movie recommendations.

---

##  Features

-  Semantic search using SBERT embeddings  
-  RAG-based recommendation with LLM re-ranking  
-  Context-aware chatbot grounded in retrieved documents  
-  Automatic explanation for each recommendation  
-  Movie poster integration using TMDB API  
-  Interactive UI built with Streamlit  

---

##  System Architecture

![Architecture Diagram](assets/images/archietecture.png)

---


##  Technology Stack

- **Language:** Python  
- **NLP Model:** Sentence-BERT (all-MiniLM-L6-v2)  
- **Vector Database:** ChromaDB  
- **LLM:** gemini-2.5-flash
- **Framework:** LangChain (LCEL)  
- **UI:** Streamlit  
- **API:** TMDB API  

---

##  Project Structure
```
Movie-recommender/
│
├── app.py
├── llm_integration.py
├── utils.py
├── data/
│ └── cleaned_data.csv
├── artifacts/
│ └── chroma_movies/
├── notebooks/
│ └──eda_cleaning.ipynb
| ├── multiple_base_models.ipynb
│ └── recommender_nlp.ipynb
├── assets/
│ └── images/
├── requirements.txt
└── README.md
```
---
## Learning & Experimentation
```
Baseline models such as TF-IDF and Word2Vec were explored for understanding traditional retrieval methods before finalizing the RAG-based architecture.
```
---

##  Application Screenshots

![Search UI](assets/images/image3.png)

### 
![Recommendation Grid](assets/images/image1.png)
