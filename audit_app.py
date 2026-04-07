import streamlit as st
import base64
import os

# --- TENTATIVE D'IMPORTATION DES MODULES DE LOCALISATION ---
try:
    from streamlit_folium import st_folium
    import folium
    MAP_AVAILABLE = True
except ImportError:
    MAP_AVAILABLE = False

# --- 1. CONFIGURATION DU DIAGNOSTIC ---
st.set_page_config(page_title="Opthelios Expertise Pro v5.2", layout="wide", page_icon="☀️")

# Fonction pour encoder l'image du filigrane
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Chargement du filigrane "Soleil Logo.png"
watermark_html = ""
if os.path.exists("Soleil Logo.png"):
    bin_str = get_base64_image("Soleil Logo.png")
    watermark_html = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        background-size: 60%; /* Taille du filigrane */
        opacity: 0.07; /* Transparence très légère pour le filigrane */
        z-index: -1;
    }}
    /* On s'assure que le contenu reste au-dessus et lisible */
    .main .block-container {{
        z-index: 1;
    }}
    </style>
    """
    st.markdown(watermark_html, unsafe_allow_html=True)

# --- 2. GESTION DU THÈME & STYLE CSS ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png")
    st.header("🎨 Interface")
    theme_choice = st.radio("Thème d'affichage", ["Clair ☀️", "Sombre 🌙"], horizontal=True)

# Définition de couleurs adaptatives
if theme_choice == "Sombre 🌙":
    bg_color, card_bg, text_color, border_color = "#0E1117", "#161B22", "#FFFFFF", "#30363D"
else:
    bg_color, card_bg, text_color, border_color = "#F8F9FA", "#FFFFFF", "#1A1C1E", "#DEE2E6"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    h1, h2, h3, label, p, span, b {{ color: {text_color} !important; }}
    .info-card, .counter-block {{ 
        background-color: {card_bg} !important; 
        border: 1px solid {border_color} !important; 
        padding: 20px; border-radius: 10px; margin-bottom: 15px;
    }}
    .stButton>button {{ background-color: #ff7f00 !important; color: white !important; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. EN-TÊTE ---
col_logo, col_text = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
with col_text:
    st.title("☀️ Opthelios, Expertise Solaire")

# --- 4. IDENTIFICATION & CARTE ---
st.markdown('<div class="info-card">', unsafe_allow_html=True)
c1, c2 = st.columns([2, 1])
with c1:
    nom_site = st.text_input("📍 Désignation de l'opération")
    moa = st.text_input("👤 Maîtrise d'Ouvrage (MOA)")
    adr = st.text_input("🏠 Adresse")
    cg1, cg2 = st.columns(2)
    lat = cg1.number_input("Lat", format="%.6f", value=48.8566)
    lon = cg2.number_input("Lon", format="%.6f", value=2.3522)
with c2:
    if MAP_AVAILABLE:
        m = folium.Map(location=[lat, lon], zoom_start=17)
        folium.Marker([lat, lon]).add_to(m)
        st_folium(m, width="100%", height=220)
    st.camera_input("📸 Photo de garde")
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. POINTS DE CONTRÔLE (Source : point de contrôle.docx) ---
# Intégration simplifiée pour l'exemple
st.header("🔍 Audit Technique")
with st.expander("📁 Contrôles Hydrauliques & Expansion"):
    pts = ["Soupape de sécurité présente", "Vase d'expansion adapté", "Pression du vase conforme"]
    for p in pts:
        col1, col2, col3 = st.columns([2, 2, 1])
        col1.markdown(f"**{p}**")
        col2.selectbox("Verdict", ["Conforme", "Défaut", "N/C"], key=f"v_{p}", label_visibility="collapsed")
        col3.camera_input("📷", key=f"c_{p}", label_visibility="collapsed")

# --- 6. SYNTHÈSE ---
st.divider()
st.header("🏁 Synthèse")
col_s1, col_s2 = st.columns([2, 1])
with col_s1:
    st.table([
        {"Priorité": "🔴 P1", "Action": "Sécurité (Vase, Soupape)"},
        {"Priorité": "🟠 P2", "Action": "Maintenance (Fluide)"}
    ])
with col_s2:
    st.metric("Santé Globale", "7/10")
    st.text_area("Conclusion de l'expert")

if st.button("🚀 GÉNÉRER LE RAPPORT FINAL"):
    st.balloons()
    st.success("Rapport en cours de génération avec le filigrane Opthelios.")