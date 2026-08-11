import streamlit as st
import recommender
from omdb import get_movie_data

st.set_page_config(
    page_title=" AI Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)
@st.cache_data(ttl=86400)
def get_cached_movie_data(title):
    return get_movie_data(title)
# ---------- Watchlist ----------
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

st.title("🎬 Movie Maxx ")
st.write("Discover Your Next Favorite Movie.")
st.markdown(
    """
    <style>
    .title {
        font-size: 2.5rem;
        color: #FF4B4B;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #FAFAFA;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    </style>
    <div class="title">🎬 AI Movie Recommendation System</div>
    <div class="subtitle">Find movies similar to your favorite ones!</div>
    """,
    unsafe_allow_html=True,
)


# ---------- Sidebar ----------
st.sidebar.title("🎬 About")

st.sidebar.info("""
### AI Movie Recommendation System

**🤖 Machine Learning**
- Sentence Transformer
- Cosine Similarity

**📂 Dataset**
IMDb Movie Dataset

**👨‍💻 Developed By**
Anurag Singh
""")
st.sidebar.header("❤️ My Watchlist")

if st.session_state.watchlist:
    for movie in st.session_state.watchlist:
        st.sidebar.write(f"🎬 {movie}")

    if st.sidebar.button("🗑 Clear Watchlist"):
        st.session_state.watchlist = []
        st.rerun()
else:
    st.sidebar.write("No movies added yet.")

movie_list = sorted(recommender.df["Title"].tolist())

movie = st.selectbox(
    "🎥 Choose a Movie",
    movie_list,
    index=None,
    placeholder="Select a movie..."
)

if movie:

    with st.spinner("🍿 Finding similar movies..."):
        recommendations = recommender.recommend(movie)

    st.subheader("Recommended Movies")

    cols = st.columns(5)

    for i, (_, row) in enumerate(recommendations.iterrows()):

        movie_data = get_cached_movie_data(row["Title"])

        with cols[i]:

            if movie_data:

                if movie_data["Poster"] != "N/A":
                    st.image(movie_data["Poster"])

                st.markdown(f"### {movie_data['Title']}")
                st.write(f"⭐ IMDb: {movie_data['imdbRating']}")
                st.write(f"📅 {movie_data['Year']}")
                st.write(f"🎭 {movie_data['Genre']}")
                st.write(f"⏱ {movie_data['Runtime']}")
                st.write(f"🎬 {movie_data['Director']}")
                st.write(movie_data["Plot"])
                if st.button(f"❤️ Add to Watchlist", key=f"watch_{row['Title']}"):
                    if row["Title"] not in st.session_state.watchlist:
                      st.session_state.watchlist.append(row["Title"])
                      st.success(f"{row['Title']} added to your watchlist!")
                    else:
                     st.info("Movie is already in your watchlist.")