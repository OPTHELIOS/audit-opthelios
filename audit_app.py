import streamlit as st
import os

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Opthelios Expert v4", layout="wide", page_icon="☀️")

if 'extra_counters' not in st.session_state:
    st.session_state.extra_counters = []

# --- 2. GESTION DU THÈME (SIDEBAR) ---
with st.sidebar:
    st.header("🎨 Affichage")
    # Cette option permet de basculer proprement sans casser le CSS
    theme_choice = st.radio("Mode de l'interface", ["Clair ☀️", "Sombre 🌙"])

# --- 3. CSS ADAPTATIF (ZÉRO CONFLIT) ---
# On définit des variables qui s'adaptent au choix de l'utilisateur
if theme_choice == "Clair ☀️":
    bg_card = "#FFFFFF"
    txt_col = "#1A1C1E"
    border_col = "#DDDDDD"
else:
    bg_card = "#161B22"
    txt_col = "#FFFFFF"
    border_col = "#30363D"

st.markdown(f"""
    <style>
    .section-header {{ 
        color: #FF7F00 !important; 
        font-size: 1.2em; 
        font-weight: bold; 
        text-transform: uppercase; 
        border-bottom: 2px solid #FF7F00; 
        margin: 25px 0 15px 0;
        padding-bottom: 5px;
    }}
    .ballon-card, .counter-block {{
        background-color: {bg_card};
        border: 1px solid {border_col};
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }}
    .stButton>button {{
        background-color: #FF7F00 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 20px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. EN-TÊTE ---
st.title("☀️ Diagnostic Expert Opthelios")
c1, c2 = st.columns([2, 1])
with c1:
    nom_site = st.text_input("📍 Opération", placeholder="Nom du projet...")
    adr_site = st.text_input("🏠 Adresse / GPS")
with c2:
    photo_main = st.camera_input("📸 Photo de garde")

# --- 5. FICHE D'IDENTITÉ (RESTAURÉE ET COMPLÉTÉE) ---
st.header("📋 Fiche d'Identité")

with st.expander("🛠️ Configuration de l'installation", expanded=True):
    
    # CAPTEURS
    st.markdown('<p class="section-header">☀️ Capteurs Solaires</p>', unsafe_allow_html=True)
    cp1, cp2, cp3 = st.columns([2, 2, 1.5])
    with cp1:
        st.text_input("Marque", key="m_cap")
        st.text_input("Référence", key="r_cap")
        st.selectbox("Type", ["Capteurs plans", "Capteurs tubulaires", "Moquette solaire"], key="t_cap")
    with cp2:
        nb_capteurs = st.number_input("Nombre de capteurs", min_value=1, value=1)
        nb_rangees = st.number_input("Nombre de rangées (champs)", min_value=1, value=1)
        st.number_input("Inclinaison (°)", value=45)
    with cp3:
        azimut = st.number_input("Azimut (°)", value=0, help="0=Sud, -90=Est, 90=Ouest")
        st.info(f"🧭 Azimut : {azimut}°")

    # STATION SOLAIRE
    st.markdown('<p class="section-header">🔌 Station Solaire</p>', unsafe_allow_html=True)
    cs1, cs2 = st.columns(2)
    with cs1:
        st.markdown("**Circulateur Solaire**")
        st.text_input("Marque", key="m_circ")
        st.text_input("Référence", key="r_circ")
    with cs2:
        st.markdown("**Régulateur Solaire**")
        st.text_input("Marque", key="m_reg")
        st.text_input("Référence", key="r_reg")

    # STOCKAGE
    st.markdown('<p class="section-header">📦 Stockage Solaire</p>', unsafe_allow_html=True)
    nb_ballons = st.number_input("Nombre de ballons", min_value=1, value=1)
    if nb_ballons >= 2:
        st.selectbox("Raccordement hydraulique", ["En série", "En parallèle"], key="r_hydra")
    
    for i in range(int(nb_ballons)):
        st.markdown(f'<div class="ballon-card"><b>Ballon n°{i+1}</b>', unsafe_allow_html=True)
        cb1, cb2, cb3 = st.columns(3)
        cb1.text_input("Marque/Réf", key=f"mb_{i}")
        cb2.text_input("Volume (L)", key=f"vb_{i}")
        cb3.selectbox("Typologie", ["Sanitaire", "Eau technique"], key=f"tb_{i}")
        cb1.number_input("Nb échangeurs", 0, 3, 1, key=f"eb_{i}")
        cb2.selectbox("État visuel", ["Correct", "Non conforme", "HS"], key=f"etb_{i}")
        st.markdown('</div>', unsafe_allow_html=True)

    # DISTRIBUTION
    st.markdown('<p class="section-header">🚿 Distribution Sanitaire</p>', unsafe_allow_html=True)
    cd1, cd2 = st.columns(2)
    with cd1:
        st.selectbox("Type", ["Bouclage sanitaire", "Traceur électrique", "Non présent"], key="dist")
        st.radio("Conformité distribution", ["Conforme", "Non conforme"], horizontal=True, key="dist_c")
    with cd2:
        st.text_area("Observations distribution")

    # ÉTAT VISUEL GLOBAL
    st.markdown('<p class="section-header">🌟 État Général du Matériel</p>', unsafe_allow_html=True)
    score = st.select_slider("Note (0=Mauvais, 10=Excellent)", options=list(range(11)), value=5)
    colors = ["#FF0000", "#FF4500", "#FF8C00", "#FFD700", "#ADFF2F", "#32CD32"]
    st.markdown(f'<div style="background-color:{colors[min(score//2, 5)]}; height:15px; width:100%; border-radius:10px;"></div>', unsafe_allow_html=True)

# --- 6. AUDIT TECHNIQUE (TOUTES LES SECTIONS RESTAURÉES) ---
st.divider()
st.header("🔍 Audit Technique")

# On définit les points pour chaque section
sections_data = {
    "📄 Documentation & Élec": ["Schéma d'exécution", "Schéma Electrique", "Mise à la terre", "Signalétique"],
    "☀️ Capteurs & Toiture": [
        "Intégrité des vitrages", "État de l'absorbeur", "Fixation châssis", "Étanchéité toiture", 
        "Sondes capteurs : Position & Fixation", "Traversée de toiture", "Isolants UV"
    ],
    "🧪 Fluide Caloporteur": ["pH du fluide", "Protection Antigel (°C)", "Analyse visuelle"],
    "💧 Circuit primaire": [
        "Sens de circulation", "Vannes remplissage", "Dégazeur Aller", "Soupape conforme", 
        "Vase : Pression gonflage", "Vase : Pression statique", "Vase : État membrane", "Disconnecteur"
    ],
    "📦 Stockage & Echangeur": ["Echangeur (Entartrage)", "Protection cathodique", "Calorifugeage", "Lyres anti-thermosiphon", "Soupape sécurité"],
    "📊 Régulation & Métrologie": [
        "Manomètre", "Débitmètre", "Sonde T1 (Cohérence)", "Sonde T2 (Cohérence)", 
        "Consigne Max (°C)", "Décharge thermique", "COMPTEURS"
    ]
}

# Ajout dynamique de l'équilibrage si > 1 rangée
if nb_rangees > 1:
    sections_data["☀️ Capteurs & Toiture"].insert(4, "Équilibrage hydraulique des champs")
    sections_data["☀️ Capteurs & Toiture"].insert(5, "Uniformité des retours par rangée")

def display_counter(label, type_c, key_id):
    st.markdown(f'<div class="counter-block"><b>📊 {label}</b>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c1:
        st.radio("Présent ?", ["Oui", "Non"], key=f"p_{key_id}", horizontal=True)
        st.radio("Conforme ?", ["Oui", "Non"], key=f"c_{key_id}", horizontal=True)
    with c2:
        if type_c in ["ESU", "Calorimètre", "Électrique"]:
            st.text_input("Index (kWh/MWh)", key=f"i_{key_id}")
        if type_c in ["ESU", "Calorimètre", "Volumétrique", "Vecs"]:
            st.text_input("Volume (m3)", key=f"v_{key_id}")
        st.checkbox("Sondes en doigts de gant ?", key=f"d_{key_id}")
    with c3: st.camera_input("Photo", key=f"cam_{key_id}")
    st.markdown('</div>', unsafe_allow_html=True)

# Boucle d'affichage des sections
for sec, pts in sections_data.items():
    with st.expander(f"📁 {sec}"):
        for p in pts:
            if p == "COMPTEURS":
                display_counter("Compteur ESU", "ESU", "esu_f")
                display_counter("Compteur ECS (Vecs)", "Vecs", "vecs_f")
                # Gestion dynamique
                ca1, ca2 = st.columns(2)
                n_n = ca1.text_input("Nom nouveau compteur", key="n_n")
                n_t = ca2.selectbox("Type", ["Calorimètre", "Volumétrique", "Électrique"], key="n_t")
                if st.button("Ajouter ce compteur"):
                    if n_n: st.session_state.extra_counters.append({"name": n_n, "type": n_t}); st.rerun()
                for i, c in enumerate(st.session_state.extra_counters):
                    display_counter(c['name'], c['type'], f"extra_{i}")
            else:
                st.markdown(f"**{p}**")
                c1, c2, c3 = st.columns([1.5, 3, 1])
                with c1:
                    opts = ["Conforme", "Non Conforme", "N/C", "S/O"]
                    if "Sonde" in p or "Cohérence" in p: opts = ["Oui", "Non", "N/C"]
                    st.selectbox(f"Statut {p}", opts, key=f"s_{p}", label_visibility="collapsed")
                with c2:
                    st.text_input(f"Note {p}", key=f"o_{p}", label_visibility="collapsed", placeholder="Note / Mesure...")
                with c3:
                    st.camera_input(f"Photo {p}", key=f"ph_{p}", label_visibility="collapsed")

# --- 7. FIN ---
if st.button("🚀 CLÔTURER L'EXPERTISE"):
    st.balloons()
    st.success("Expertise terminée.")