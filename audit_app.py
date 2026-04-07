import streamlit as st
import os

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Opthelios Expert v4.1", layout="wide", page_icon="☀️")

if 'extra_counters' not in st.session_state:
    st.session_state.extra_counters = []

# --- 2. GESTION DU THÈME ---
with st.sidebar:
    st.header("🎨 Affichage")
    theme_choice = st.radio("Mode de l'interface", ["Clair ☀️", "Sombre 🌙"])

bg_card = "#FFFFFF" if theme_choice == "Clair ☀️" else "#161B22"
border_col = "#DDDDDD" if theme_choice == "Clair ☀️" else "#30363D"

st.markdown(f"""
    <style>
    .section-header {{ color: #FF7F00 !important; font-size: 1.2em; font-weight: bold; border-bottom: 2px solid #FF7F00; margin-bottom: 15px; padding-bottom: 5px; }}
    .ballon-card, .counter-block, .info-card {{ background-color: {bg_card}; border: 1px solid {border_col}; padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
    .stButton>button {{ background-color: #FF7F00 !important; color: white !important; font-weight: bold !important; border-radius: 20px !important; width: 100%; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. IDENTIFICATION DU PROJET (VERSION PROFESSIONNELLE) ---
st.title("☀️ Diagnostic Expert Opthelios")
st.markdown('<p class="section-header">📂 Identification du Projet & Intervenants</p>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    c_p1, c_p2, c_p3 = st.columns([2, 2, 1.5])
    with c_p1:
        nom_site = st.text_input("📍 Désignation de l'opération", placeholder="ex: Résidence du Rail")
        client_moa = st.text_input("👤 Maîtrise d'Ouvrage (MOA)", placeholder="ex: ICF Habitat")
        exploit_site = st.text_input("⚙️ Exploitant / Mainteneur", placeholder="ex: Dalkia, Engie...")
    with c_p2:
        adr_site = st.text_input("🏠 Adresse complète")
        coordonnees_gps = st.text_input("🌐 Coordonnées GPS", placeholder="Latitude, Longitude")
        date_visite = st.date_input("📅 Date du diagnostic")
    with c_p3:
        photo_main = st.camera_input("📸 Cliché de garde")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. FICHE D'IDENTITÉ MATÉRIEL ---
st.header("📋 Fiche d'Identité Technique")
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
        azimut = st.number_input("Azimut (°)", value=0)
        st.info(f"🧭 Direction : {azimut}°")

    # STATION SOLAIRE
    st.markdown('<p class="section-header">🔌 Station Solaire & Régulation</p>', unsafe_allow_html=True)
    cs1, cs2 = st.columns(2)
    with cs1:
        st.text_input("Circulateur Solaire (Marque/Réf)", key="m_circ")
    with cs2:
        st.text_input("Régulateur Solaire (Marque/Réf)", key="m_reg")

    # STOCKAGE (Multi-ballons)
    st.markdown('<p class="section-header">📦 Ballons de Stockage</p>', unsafe_allow_html=True)
    nb_ballons = st.number_input("Nombre de ballons solaires", min_value=1, value=1)
    if nb_ballons >= 2: st.selectbox("Raccordement", ["En série", "En parallèle"], key="r_hydra")
    
    for i in range(int(nb_ballons)):
        st.markdown(f'<div class="ballon-card"><b>Ballon n°{i+1}</b>', unsafe_allow_html=True)
        cb1, cb2, cb3 = st.columns(3)
        cb1.text_input("Marque/Réf", key=f"mb_{i}")
        cb2.text_input("Volume (L)", key=f"vb_{i}")
        cb3.selectbox("Typologie", ["Sanitaire", "Eau technique"], key=f"tb_{i}")
        cb1.number_input("Nb échangeur(s)", 0, 3, 1, key=f"eb_{i}")
        cb2.selectbox("État visuel", ["Correct", "Défaut", "HS"], key=f"etb_{i}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ÉTAT GLOBAL
    st.markdown('<p class="section-header">🌟 Indice de Santé Matériel</p>', unsafe_allow_html=True)
    score = st.select_slider("Note de 0 à 10", options=list(range(11)), value=5)
    colors = ["#FF0000", "#FF4500", "#FF8C00", "#FFD700", "#ADFF2F", "#32CD32"]
    st.markdown(f'<div style="background-color:{colors[min(score//2, 5)]}; height:10px; border-radius:5px;"></div>', unsafe_allow_html=True)

# --- 5. AUDIT TECHNIQUE (FUSION WORD + SCRIPT) ---
st.divider()
st.header("🔍 Audit Technique Complet")

# Fusion des points du document Word 
sections_data = {
    "📄 Documentation & Élec": [
        "Schéma d'éxécution (présence et conformité)", "Schéma Electrique (présence et conformité)", 
        "Analyse Fonctionnelle (présence et conformité)", "Contrôle des raccordements électriques",
        "Conformités de l'installation générale", "Mise à la terre de l'installation"
    ],
    "☀️ Capteurs & Toiture": [
        "Absence de vannes d'isolement sur tuyauterie capteurs", "Dispositif de traversé de toiture adapté",
        "Supports capteurs conformes", "Raccordement correct des capteurs", "Accès capteurs sécurisé",
        "Absence de masque proche", "Matériaux (tuyauteries) conformes à l'usage", "Isolants UV"
    ],
    "💧 Hydraulique & Circuit Primaire": [
        "Circulation capteurs et échangeur dans le bon sens", "Vannes pour raccordement pompe de remplissage",
        "Dégazeur sur la conduite ALLER capteur", "Soupape de sécurité présente et conforme",
        "Bidon de récupération avec contrôle de niveau", "Circulateur sur le RETOUR capteurs",
        "Clapet anti-retour RETOUR capteurs", "Vannes 3 voies (V3V) fonctionnelles"
    ],
    "🎈 Système d'Expansion": [
        "Présence d'un vase d'expansion adapté", "Volume du vase d'expansion suffisant",
        "Dispositif d'isolement et mise à l'air pour vase", "Raccordement du vase sur le RETOUR",
        "Pression du vase conforme"
    ],
    "🔄 Échangeur Solaire Externe": [
        "Raccordement de l'échangeur en contre-courant", "Vannes d'isolement en entrée/sortie échangeur",
        "Puissance de l'échangeur suffisante"
    ],
    "📦 Ballons de Stockage": [
        "Ballons dans local fermé, hors gel", "Ouverture de porte permettant passage ballon",
        "Accès complet aux piquages et brides", "Raccordement ballon(s) conforme",
        "Absence Clapet anti-retour entre les ballons", "Vannes de vidange et chasse en partie basse",
        "Prise de température en partie haute", "Protection cathodique ballon",
        "Calorifuge du stockage", "Coudes vers le bas sur les piquages (lyres)"
    ],
    "🚿 Distribution ECS": [
        "Mitigeur présent", "Température max ECS respectée aux puisages",
        "Raccordement correct du bouclage", "Présence des clapets anti-retour", "Bouclage calorifugé"
    ],
    "🧪 Fluide & Tests": [
        "pH du fluide", "Protection Antigel (°C)", "Analyse visuelle",
        "Tests d'étanchéité conforme", "Pression d'épreuve recommandée/réglée", "Réseau rincé"
    ],
    "📊 Métrologie & Télécontrôle": [
        "Manomètre de contrôle circuit solaire", "Débitmètre(s) présent(s)",
        "Sonde d'ensoleillement bien placée", "Sonde de température capteur bien placée",
        "Sonde de température Bas de ballon bien placée", "Prélèvement du liquide caloporteur",
        "Thermomètre en entrée/sortie échangeur", "Compteur volumétrique Eau froide",
        "Télécontrôleur conforme", "Connexion à distance fonctionnelle", "COMPTEURS"
    ]
}

# Ajout dynamique équilibrage
if nb_rangees > 1:
    sections_data["☀️ Capteurs & Toiture"].insert(6, "Dispositif d'équilibrage sur chaque champ")
    sections_data["☀️ Capteurs & Toiture"].insert(7, "Dispositifs d'équilibrages sécurisés et exploitables")

def display_c(label, type_c, key_id):
    st.markdown(f'<div class="counter-block"><b>📊 {label}</b>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c1:
        st.radio("Présent ?", ["Oui", "Non"], key=f"p_{key_id}", horizontal=True)
        st.radio("Conforme ?", ["Oui", "Non"], key=f"c_{key_id}", horizontal=True)
    with c2:
        if type_c in ["ESU", "Calorimètre", "Électrique"]: st.text_input("Index (kWh/MWh)", key=f"i_{key_id}")
        if type_c in ["ESU", "Calorimètre", "Volumétrique", "Vecs"]: st.text_input("Volume (m3)", key=f"v_{key_id}")
        st.checkbox("Sondes en doigts de gant ?", key=f"d_{key_id}")
    with c3: st.camera_input("Photo", key=f"cam_{key_id}")
    st.markdown('</div>', unsafe_allow_html=True)

for sec, pts in sections_data.items():
    with st.expander(f"📁 {sec}"):
        for p in pts:
            if p == "COMPTEURS":
                display_c("Compteur ESU", "ESU", "f_esu")
                display_c("Compteur ECS (Vecs)", "Vecs", "f_vecs")
                # Gestion extras
                ca1, ca2 = st.columns(2)
                n_n = ca1.text_input("Nom nouveau compteur", key="n_n")
                n_t = ca2.selectbox("Type", ["Calorimètre", "Volumétrique", "Électrique"], key="n_t")
                if st.button("Ajouter"):
                    if n_n: st.session_state.extra_counters.append({"name": n_n, "type": n_t}); st.rerun()
                for i, c in enumerate(st.session_state.extra_counters):
                    display_c(c['name'], c['type'], f"extra_{i}")
            else:
                st.markdown(f"**{p}**")
                c1, c2, c3 = st.columns([1.5, 3, 1])
                with c1: st.selectbox(f"Statut {p}", ["Conforme", "Défaut", "N/C", "S/O"], key=f"s_{p}", label_visibility="collapsed")
                with c2: st.text_input(f"Note {p}", key=f"o_{p}", label_visibility="collapsed", placeholder="Observations...")
                with c3: st.camera_input(f"Photo {p}", key=f"ph_{p}", label_visibility="collapsed")

if st.button("🚀 CLÔTURER L'EXPERTISE"):
    st.balloons()
    st.success("Rapport validé.")