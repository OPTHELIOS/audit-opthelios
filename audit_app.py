import streamlit as st
import os

# --- TENTATIVE D'IMPORTATION DES MODULES DE CARTE ---
try:
    from streamlit_folium import st_folium
    import folium
    MAP_AVAILABLE = True
except ImportError:
    MAP_AVAILABLE = False

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Opthelios Expertise Solaire", layout="wide", page_icon="☀️")

# --- 2. STYLE CSS DÉFINITIF ---
with st.sidebar:
    st.header("🎨 Options d'affichage")
    theme_choice = st.radio("Mode de l'interface", ["Clair ☀️", "Sombre 🌙"])

if theme_choice == "Clair ☀️":
    bg, card, txt, border = "#F8F9FA", "#FFFFFF", "#000000", "#DDDDDD"
else:
    bg, card, txt, border = "#0E1117", "#161B22", "#FFFFFF", "#30363D"

st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{ background-color: {bg} !important; border-right: 1px solid {border}; }}
    [data-testid="stSidebar"] * {{ color: {txt} !important; }}
    .stApp {{ background-color: {bg}; color: {txt}; }}
    .streamlit-expanderHeader {{ background-color: {card} !important; color: {txt} !important; border: 1px solid {border} !important; }}
    .streamlit-expanderHeader:hover {{ color: #FF7F00 !important; }}
    .info-card, .ballon-card {{ background-color: {card} !important; border: 1px solid {border} !important; padding: 20px; border-radius: 10px; margin-bottom: 15px; }}
    .section-header {{ color: #FF7F00 !important; font-size: 1.2em; font-weight: bold; border-bottom: 2px solid #FF7F00; margin-bottom: 15px; padding-bottom: 5px; }}
    label p, .stMarkdown p, b, p, span, .stWidgetLabel {{ color: {txt} !important; }}
    .stButton>button {{ background-color: #FF7F00 !important; color: white !important; font-weight: bold; border-radius: 8px; width: 100%; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. EN-TÊTE ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    if os.path.exists("logo.png"): 
        st.image("logo.png", width=120)
with col_title:
    st.title("Opthelios, expertise solaire")

# --- 4. IDENTIFICATION & GPS ---
st.markdown('<p class="section-header">📂 Identification du Projet & Géolocalisation</p>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1:
        st.text_input("📍 Opération", placeholder="ex: Résidence Helios")
        st.text_input("👤 Maîtrise d'Ouvrage (MOA)")
        st.text_input("🏠 Adresse complète")
        st.write("**Coordonnées GPS**")
        cg1, cg2 = st.columns(2)
        lat = cg1.number_input("Latitude", format="%.6f", value=48.8566)
        lon = cg2.number_input("Longitude", format="%.6f", value=2.3522)
    with c2:
        if MAP_AVAILABLE:
            m = folium.Map(location=[lat, lon], zoom_start=17)
            folium.Marker([lat, lon]).add_to(m)
            st_folium(m, width="100%", height=250)
        st.camera_input("📸 Photo de garde")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. FICHE D'IDENTITÉ & BOUSSOLE ---
st.header("📋 Fiche d'Identité")
with st.expander("🛠️ Détails du Matériel", expanded=True):
    cp1, cp2, cp3 = st.columns([2, 1, 1])
    with cp1:
        st.text_input("Marque / Référence Capteurs")
        st.number_input("Nombre de capteurs", min_value=1, value=1)
    with cp2:
        azimut = st.number_input("Azimut (°)", value=163)
        st.number_input("Inclinaison (°)", value=45)
    with cp3:
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; background: white; border-radius: 50%; width: 100px; height: 100px; margin: auto; border: 2px solid #FF7F00; position: relative;">
                <div style="position: absolute; width: 2px; height: 80px; background: red; transform: rotate({azimut}deg);"></div>
                <b style="color: black; z-index: 2;">S</b>
            </div>
        """, unsafe_allow_html=True)

# --- 6. AUDIT TECHNIQUE ---
st.header("🔍 Audit Technique")
sections = {
    "📄 Documentation & Élec": ["Schéma d'éxécution", "Schéma Electrique", "Analyse Fonctionnelle", "Mise à la terre"],
    "☀️ Capteurs": ["Vannes d'isolement", "Supports capteurs", "Accès sécurisé", "Absence de masque"],
    "💧 Hydraulique": ["Sens de circulation", "Soupape de sécurité", "Circulateur sur RETOUR", "Clapet anti-retour"],
    "🎈 Expansion": ["Vase d'expansion adapté", "Volume suffisant", "Pression conforme"],
    "📦 Stockage": ["Echangeur contre-courant", "Local hors gel", "Protection cathodique", "Calorifuge"],
    "📊 Métrologie": ["Manomètre", "Débitmètre", "Sonde ensoleillement", "Connexion à distance"]
}

for sec, pts in sections.items():
    with st.expander(f"📁 {sec}"):
        for p in pts:
            st.markdown(f"**{p}**")
            col1, col2, col3, col4 = st.columns([1, 1.5, 1, 1])
            col1.selectbox("Verdict", ["Conforme", "Défaut", "N/C", "S/O"], key=f"s_{p}", label_visibility="collapsed")
            col2.text_input("Observations", key=f"o_{p}", label_visibility="collapsed")
            col3.camera_input("Photo", key=f"cam_{p}", label_visibility="collapsed")
            col4.file_uploader("Fichier", key=f"f_{p}", label_visibility="collapsed")

# --- 7. NOUVEAU : ANNEXES TECHNIQUES ---
st.header("📁 Annexes Techniques Globales")
st.markdown('<div class="info-card">', unsafe_allow_html=True)
st.info("Utilisez cette section pour téléverser les documents globaux (Schémas PDF, Rapports d'essais fluides, Fiches techniques constructeurs).")
annexes = st.file_uploader("Ajouter des documents d'expertise (PDF, JPG, PNG)", accept_multiple_files=True, key="global_annexes")
if annexes:
    st.write(f"✅ {len(annexes)} fichier(s) prêt(s) pour l'archivage.")
st.markdown('</div>', unsafe_allow_html=True)

# --- 8. SYNTHÈSE ---
st.divider()
st.header("🏁 Synthèse")
st.markdown('<div class="info-card">', unsafe_allow_html=True)
col_s1, col_s2 = st.columns([2, 1])
with col_s1:
    st.subheader("Plan d'Actions")
    st.table([{"Prio": "🔴 P1", "Action": "Sécurité"}, {"Prio": "🟠 P2", "Action": "Maintenance"}, {"Prio": "🔵 P3", "Action": "Suivi"}])
with col_s2:
    st.slider("Note / 10", 0, 10, 5)
    st.text_area("Conclusion technique")
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚀 VALIDER L'EXPERTISE"):
    st.balloons()
    st.success("Rapport et annexes enregistrés.")