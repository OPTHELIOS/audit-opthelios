import streamlit as st
import os

# --- 1. CONFIGURATION & STATE ---
st.set_page_config(page_title="Opthelios Expert v4", layout="wide", page_icon="☀️")

if 'extra_counters' not in st.session_state:
    st.session_state.extra_counters = []

# --- 2. STYLE CSS AVANCÉ (Interface Claire & Professionnelle) ---
st.markdown("""
    <style>
    /* Fond et polices */
    .stApp { background-color: #FDFDFD; color: #1E1E1E; }
    
    /* Cartes blanches avec ombre légère */
    div[data-testid="stExpander"], .custom-card {
        background-color: white !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
        padding: 15px;
        margin-bottom: 15px;
    }

    /* Titres et Accents */
    h1, h2, h3 { color: #2C3E50 !important; font-family: 'Helvetica Neue', sans-serif; }
    .section-header { 
        color: #FF7F00; 
        font-size: 1.1em; 
        font-weight: 700; 
        text-transform: uppercase; 
        border-bottom: 2px solid #FF7F00; 
        margin: 20px 0 15px 0;
        padding-bottom: 5px;
    }

    /* Boutons Orange Opthelios */
    .stButton>button {
        background-color: #FF7F00 !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        font-weight: 600 !important;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(255,127,0,0.3); }

    /* Score de santé (Couleurs) */
    .health-bar { height: 20px; border-radius: 10px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. EN-TÊTE ---
st.title("☀️ Diagnostic Expert Opthelios")
c_top1, c_top2 = st.columns([2, 1])
with c_top1:
    nom_site = st.text_input("📍 Opération", placeholder="Ex: Résidence Helios")
    adr_site = st.text_input("🏠 Adresse / GPS")
with c_top2:
    photo_main = st.camera_input("📸 Photo de garde")

# --- 4. FICHE D'IDENTITÉ ---
st.header("📋 Fiche d'Identité de l'Installation")

with st.expander("🛠️ Configuration Technique détaillée", expanded=True):
    
    # --- CAPTEURS SOLAIRES ---
    st.markdown('<p class="section-header">☀️ Capteurs Solaires</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 2, 1.5])
    with c1:
        st.text_input("Marque", key="m_cap")
        st.text_input("Référence", key="r_cap")
        st.selectbox("Type de capteurs", ["Capteurs plans", "Capteurs tubulaires", "Moquette solaire"], key="t_cap")
    with c2:
        st.number_input("Nombre total de capteurs", min_value=1, value=1)
        st.number_input("Nombre de rangées (champs)", min_value=1, value=1)
        st.number_input("Inclinaison (°)", value=45)
    with c3:
        st.markdown("**Orientation & Azimut**")
        azimut = st.number_input("Azimut (°)", value=0, help="0=Sud, -90=Est, 90=Ouest")
        # Boussole visuelle simple
        direction = "S"
        if -22.5 < azimut <= 22.5: direction = "S"
        elif 22.5 < azimut <= 67.5: direction = "SO"
        elif 67.5 < azimut <= 112.5: direction = "O"
        elif -67.5 < azimut <= -22.5: direction = "SE"
        elif -112.5 < azimut <= -67.5: direction = "E"
        
        st.info(f"🧭 Orientation : **{direction}**")
        st.caption("0°: Sud | -90°: Est | +90°: Ouest")

    # --- STATION SOLAIRE ---
    st.markdown('<p class="section-header">🔌 Station Solaire</p>', unsafe_allow_html=True)
    cs1, cs2 = st.columns(2)
    with cs1:
        st.markdown("**Circulateur Solaire**")
        st.text_input("Marque", key="m_circ", placeholder="ex: Grundfos")
        st.text_input("Référence", key="r_circ", placeholder="ex: Solar 25-120")
    with cs2:
        st.markdown("**Régulateur Solaire**")
        st.text_input("Marque", key="m_reg")
        st.text_input("Référence", key="r_reg")

    # --- STOCKAGE ---
    st.markdown('<p class="section-header">📦 Stockage Solaire</p>', unsafe_allow_html=True)
    nb_ballons = st.number_input("Nombre de ballons", min_value=1, value=1)
    if nb_ballons >= 2:
        st.selectbox("Raccordement", ["En série", "En parallèle"], key="r_hydra")
    
    for i in range(int(nb_ballons)):
        st.markdown(f"**Ballon n°{i+1}**")
        cb1, cb2, cb3 = st.columns(3)
        cb1.text_input("Marque/Réf", key=f"mb_{i}")
        cb2.text_input("Volume (L)", key=f"vb_{i}")
        cb3.selectbox("Typologie", ["Sanitaire", "Eau technique"], key=f"tb_{i}")

    # --- DISTRIBUTION ---
    st.markdown('<p class="section-header">🚿 Distribution Sanitaire</p>', unsafe_allow_html=True)
    cd1, cd2 = st.columns(2)
    with cd1:
        st.selectbox("Type", ["Bouclage sanitaire", "Traceur électrique", "Non présent"], key="dist")
        st.radio("Conformité", ["Conforme", "Non conforme"], horizontal=True, key="dist_c")
    with cd2:
        st.text_area("Commentaires distribution")

    # --- ÉTAT VISUEL GLOBAL (Graduation Professionnelle) ---
    st.markdown('<p class="section-header">🌟 État Général du Matériel</p>', unsafe_allow_html=True)
    score = st.select_slider(
        "Note de l'état visuel (0=HS, 10=Neuf)",
        options=list(range(11)),
        value=5
    )
    
    # Indicateur visuel de couleur
    colors = ["#FF0000", "#FF4500", "#FF8C00", "#FFD700", "#ADFF2F", "#32CD32"]
    idx = min(score // 2, 5)
    st.markdown(f"""
        <div style="background-color:{colors[idx]}; height:10px; width:100%; border-radius:5px;"></div>
        <p style="text-align:center; font-weight:bold;">Indice de santé : {score}/10</p>
    """, unsafe_allow_html=True)

# --- 5. AUDIT TECHNIQUE ---
st.divider()
st.header("🔍 Audit Technique")

# ... (Le reste de la logique d'audit reste identique à la v3, mais profite du nouveau design clair)
# J'inclus ici la logique dynamique pour l'équilibrage vue précédemment

pts_capteurs = ["Vitrages", "Absorbeur", "Fixation", "Étanchéité", "Sondes"]
if 'nb_rangees' in st.session_state and st.session_state.nb_rangees > 1:
    pts_capteurs.append("Équilibrage des champs")

with st.expander("📁 Audit des Capteurs"):
    for p in pts_capteurs:
        st.markdown(f"**{p}**")
        c1, c2, c3 = st.columns([1, 2, 1])
        c1.selectbox("Statut", ["Conforme", "Défaut", "N/C"], key=f"s_{p}", label_visibility="collapsed")
        c2.text_input("Note", key=f"o_{p}", label_visibility="collapsed")
        c3.camera_input("📷", key=f"c_{p}", label_visibility="collapsed")

# --- BOUTON FINAL ---
if st.button("🚀 CLÔTURER L'EXPERTISE"):
    st.balloons()
    st.success("Rapport en cours de génération...")