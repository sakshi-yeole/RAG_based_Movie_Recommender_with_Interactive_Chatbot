import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

from utils import get_movie_poster_by_title
from llm_integration import CineFusionLLM

CHROMA_PATH = "./artifacts/chroma_movies"
DATA_PATH = "./data/RAG_cleaned_data.csv"

st.set_page_config(page_title="CineFusion AI", layout="wide")

if "recommended_movies" not in st.session_state:
    st.session_state.recommended_movies = []

if "chat" not in st.session_state:
    st.session_state.chat = []

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

api_key = st.sidebar.text_input("Gemini API Key", type="password")
if not api_key:
    st.sidebar.warning("Please add your Gemini API key")
    st.stop()

@st.cache_resource
def load_all():
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection("movies_rag")
    df = pd.read_csv(DATA_PATH)
    return embed_model, collection, df

embed_model, collection, df = load_all()
llm = CineFusionLLM(model_name="gemini-2.5-flash", temperature=0.7, api_key=api_key)

def search_movies(query, k=15):
    emb = embed_model.encode([query]).tolist()
    return collection.query(query_embeddings=emb, n_results=k)


st.title("🎬 movie recommendation system")
left, right = st.columns(2)


with left:
    st.subheader("🔍 Find Movies")
    query = st.text_input("What do you want to watch?")
    search_btn = st.button("Recommend")


    if search_btn and query:
        st.session_state.recommended_movies = []
        st.session_state.chat = []
        st.session_state.last_query = query

        results = search_movies(query, k=10)
        metas = results["metadatas"][0]
        docs = results["documents"][0]

        movie_map = {}
        for meta, doc in zip(metas, docs):
            idx = meta["movie_index"]
            if idx not in movie_map:
                movie_map[idx] = doc

        movie_text = "\n\n".join(movie_map.values())

        selected_titles_str = llm.select_best_movies(query, movie_text)
        selected_titles = [t.strip().lower() for t in selected_titles_str.split(',') if t.strip()]

        for idx in movie_map:
            row = df.iloc[idx]
            title = row["title"].lower()

        
            if any(candidate in title or title in candidate for candidate in selected_titles):
                st.session_state.recommended_movies.append({
                    "title": row["title"],
                    "year": str(row["release_date"])[:4],
                    "description": row["description"]
                })

            if len(st.session_state.recommended_movies) == 6:
                break

    if st.session_state.recommended_movies:
        st.write("### 🎯 Recommended Movies")

        cols = st.columns(3)

        for i, movie in enumerate(st.session_state.recommended_movies):
            with cols[i % 3]:
                with st.container():
                    poster = get_movie_poster_by_title(movie["title"])
                    if poster:
                        st.image(poster, use_container_width=True)

                    st.markdown(
                        f"""
                        <div style="text-align:center">
                            <strong>{movie['title']}</strong><br/>
                            <span style="color:gray">({movie['year']})</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

with right:
    st.subheader("🧠 Why these movies?")

    if st.session_state.recommended_movies:
        movies_text = "\n".join(
            [m["title"] + ": " + m["description"]
             for m in st.session_state.recommended_movies]
        )

        explanation = llm.explain_recommendations(
            st.session_state.last_query,
            movies_text
        )
        st.write(explanation)

    st.subheader("💬 QnA Chatbot")

    for msg in st.session_state.chat:
        st.write(f"**{msg['role']}:** {msg['text']}")

    user_msg = st.text_input("Ask about the recommended movies")
    send = st.button("Send")

    if send and user_msg and st.session_state.recommended_movies:
        st.session_state.chat.append({"role": "You", "text": user_msg})

        context = "\n\n".join(
            [m["description"] for m in st.session_state.recommended_movies]
        )

        reply = llm.generate(user_msg, [context])
        st.session_state.chat.append({"role": "Bot", "text": reply})

        st.rerun()
