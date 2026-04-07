import streamlit as st
from streamlit_folium import st_folium
import folium

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Opthelios Expert v4.5", layout="wide", page_icon="☀️")

if 'extra_counters' not in st.session_state:
    st.session_state.extra_counters = []

# --- 2. GESTION DU THÈME & STYLE (Correctif Contraste) ---
with st.sidebar:
    st.header("🎨 Options d'affichage")
    theme_choice = st.radio("Mode de l'interface", ["Clair ☀️", "Sombre 🌙"])

# Variables de couleurs dynamiques pour éviter l'illisibilité
if theme_choice == "Clair ☀️":
    bg_app, bg_card, txt_main, border_col = "#F8F9FA", "#FFFFFF", "#1A1C1E", "#DDDDDD"
else:
    bg_app, bg_card, txt_main, border_col = "#0E1117", "#161B22", "#FFFFFF", "#30363D"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_app}; color: {txt_main}; }}
    .section-header {{ color: #FF7F00 !important; font-size: 1.2em; font-weight: bold; border-bottom: 2px solid #FF7F00; margin-bottom: 15px; padding-bottom: 5px; }}
    .info-card, .ballon-card, .counter-block {{ 
        background-color: {bg_card} !important; 
        border: 1px solid {border_col} !important; 
        padding: 20px; border-radius: 10px; margin-bottom: 15px; color: {txt_main} !important;
    }}
    /* Forcer la visibilité des textes et labels */
    label p, .stMarkdown p, b {{ color: {txt_main} !important; }}
    .stButton>button {{ background-color: #FF7F00 !important; color: white !important; font-weight: bold !important; border-radius: 20px !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. IDENTIFICATION DU PROJET & GÉOLOCALISATION ---
st.title("☀️ Diagnostic Expert Opthelios")
st.markdown('<p class="section-header">📂 Identification du Projet & Géolocalisation</p>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    col_id1, col_id2 = st.columns([1, 1])
    
    with col_id1:
        nom_site = st.text_input("📍 Désignation de l'opération", placeholder="ex: Résidence Helios")
        client_moa = st.text_input("👤 Maîtrise d'Ouvrage (MOA)")
        exploit_site = st.text_input("⚙️ Exploitant / Mainteneur")
        adr_site = st.text_input("🏠 Adresse complète")
        st.write("**Coordonnées GPS**")
        c_gps1, c_gps2 = st.columns(2)
        lat = c_gps1.number_input("Latitude", format="%.6f", value=48.8566)
        lon = c_gps2.number_input("Longitude", format="%.6f", value=2.3522)
        date_visite = st.date_input("📅 Date du diagnostic")

    with col_id2:
        st.write("🗺️ **Localisation interactive**")
        m = folium.Map(location=[lat, lon], zoom_start=16)
        folium.Marker([lat, lon], tooltip="Installation").add_to(m)
        st_folium(m, width="100%", height=250)
        photo_main = st.camera_input("📸 Photo de garde")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. FICHE D'IDENTITÉ TECHNIQUE ---
st.header("📋 Fiche d'Identité")
with st.expander("🛠️ Configuration Matérielle", expanded=True):
    # Capteurs
    st.markdown('<p class="section-header">☀️ Capteurs Solaires</p>', unsafe_allow_html=True)
    cp1, cp2, cp3 = st.columns([2, 2, 1.5])
    with cp1:
        st.text_input("Marque", key="m_cap")
        st.text_input("Référence", key="r_cap")
        st.selectbox("Type", ["Capteurs plans", "Capteurs tubulaires", "Moquette solaire"], key="t_cap")
    with cp2:
        nb_capteurs = st.number_input("Nombre total de capteurs", min_value=1, value=1)
        nb_rangees = st.number_input("Nombre de rangées (champs)", min_value=1, value=1)
        st.number_input("Inclinaison (°)", value=45)
    with cp3:
        azimut = st.number_input("Azimut (°)", value=0)
        st.info(f"🧭 Azimut : {azimut}°")

    # Station Solaire
    st.markdown('<p class="section-header">🔌 Station Solaire & Régulation</p>', unsafe_allow_html=True)
    cs1, cs2 = st.columns(2)
    with cs1:
        st.text_input("Circulateur : Marque", key="mcir")
        st.text_input("Circulateur : Référence", key="rcir")
    with cs2:
        st.text_input("Régulateur : Marque", key="mreg")
        st.text_input("Régulateur : Référence", key="rreg")

    # Stockage
    st.markdown('<p class="section-header">📦 Stockage Solaire</p>', unsafe_allow_html=True)
    nb_ballons = st.number_input("Nombre de ballons", min_value=1, value=1)
    for i in range(int(nb_ballons)):
        st.markdown(f'<div class="ballon-card"><b>Ballon n°{i+1}</b>', unsafe_allow_html=True)
        cb1, cb2, cb3 = st.columns(3)
        cb1.text_input(f"Marque/Réf {i}", key=f"mb_{i}")
        cb2.text_input(f"Volume (L) {i}", key=f"vb_{i}")
        cb3.selectbox(f"Typologie {i}", ["Sanitaire", "Eau technique"], key=f"tb_{i}")
        st.markdown('</div>', unsafe_allow_html=True)

    # État visuel
    st.markdown('<p class="section-header">🌟 État Général du Matériel</p>', unsafe_allow_html=True)
    score = st.select_slider("Note de 0 à 10", options=list(range(11)), value=5)
    colors = ["#FF0000", "#FF4500", "#FF8C00", "#FFD700", "#ADFF2F", "#32CD32"]
    st.markdown(f'<div style="background-color:{colors[min(score//2, 5)]}; height:12px; border-radius:6px;"></div>', unsafe_allow_html=True)

# --- 5. AUDIT TECHNIQUE COMPLET (Intégration Document Word) ---
st.divider()
st.header("🔍 Audit Technique")

sections_data = {
    "📄 Documentation & Élec": ["Schéma d'éxécution", "Schéma Electrique", "Analyse Fonctionnelle", "Raccordements électriques", "Installation générale", "Mise à la terre"],
    "☀️ Capteurs & Toiture": ["Absence vannes isolement", "Traversée de toiture", "Supports capteurs", "Raccordement capteurs", "Accès sécurisé", "Absence de masque", "Tuyauteries conformes", "Isolants UV"],
    "💧 Hydraulique": ["Sens de circulation", "Vannes remplissage", "Dégazeur ALLER", "Soupape sécurité", "Bidon récupération", "Circulateur RETOUR", "Clapet anti-retour", "V3V fonctionnelles"],
    "🎈 Expansion": ["Vase adapté", "Volume suffisant", "Isolement/Mise à l'air", "Raccordement RETOUR", "Pression conforme"],
    "🔄 Échangeur": ["Raccordement contre-courant", "Vannes isolement", "Puissance suffisante"],
    "📦 Stockage": ["Local hors gel", "Passage porte", "Accès piquages/brides", "Raccordement conforme", "Absence Clapet AR entre ballons", "Vidange/Chasse bas", "Prise T° haut", "Protection cathodique", "Calorifuge", "Lyres anti-thermosiphon"],
    "🚿 Distribution": ["Mitigeur présent", "T° max respectée", "Bouclage conforme", "Clapets AR", "Bouclage calorifugé"],
    "🧪 Fluide & Tests": ["pH fluide", "Antigel (°C)", "Analyse visuelle", "Étanchéité conforme", "Pression d'épreuve", "Réseau rincé"],
    "📊 Métrologie & Télégestion": ["Manomètre", "Débitmètre", "Sonde ensoleillement", "Seuil éclairement", "Sonde T° capteur", "Sonde T° bas ballon", "Prélèvement fluide", "Thermomètre échangeur", "Compteur Eau froide", "Télécontrôleur conforme", "Connexion à distance", "COMPTEURS"]
}

if nb_rangees > 1:
    sections_data["☀️ Capteurs & Toiture"].extend(["Équilibrage par champ", "Équilibrages exploitables"])

def display_c(label, key_id):
    st.markdown(f'<div class="counter-block"><b>📊 {label}</b>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c1: 
        st.radio("Présent ?", ["Oui", "Non"], key=f"p_{key_id}", horizontal=True)
        st.radio("Conforme ?", ["Oui", "Non"], key=f"c_{key_id}", horizontal=True)
    with c2:
        st.text_input("Index (kWh/m3)", key=f"i_{key_id}")
        st.checkbox("Sondes en doigts de gant ?", key=f"d_{key_id}")
    with c3: st.camera_input("Photo", key=f"cam_{key_id}")
    st.markdown('</div>', unsafe_allow_html=True)

for sec, pts in sections_data.items():
    with st.expander(f"📁 {sec}"):
        for p in pts:
            if p == "COMPTEURS":
                display_c("Compteur ESU", "esu")
                display_c("Compteur ECS (Vecs)", "vecs")
            else:
                st.markdown(f"**{p}**")
                c1, c2, c3 = st.columns([1, 2, 1])
                c1.selectbox("Statut", ["Conforme", "Défaut", "N/C", "S/O"], key=f"s_{p}", label_visibility="collapsed")
                c2.text_input("Note", key=f"o_{p}", label_visibility="collapsed", placeholder="Observations...")
                c3.camera_input("Photo", key=f"ph_{p}", label_visibility="collapsed")

# --- 6. SYNTHÈSE & PLAN D'ACTIONS ---
st.divider()
st.header("🏁 Synthèse Décisionnelle")
st.markdown('<div class="info-card">', unsafe_allow_html=True)
col_s1, col_s2 = st.columns([2, 1])
with col_s1:
    st.subheader("Plan d'Intervention Priorisé")
    plan = [
        {"Priorité": "🔴 P1 (Immédiat)", "Action": "Sécurité (Vase, Soupape, Mitigeur)", "Impact": "Risque majeur"},
        {"Priorité": "🟠 P2 (Maintenance)", "Action": "Fluide Caloporteur & Calorifuge", "Impact": "Performance"},
        {"Priorité": "🔵 P3 (Amélioration)", "Action": "Métrologie & Télégestion", "Impact": "Suivi expert"}
    ]
    st.table(plan)
with col_s2:
    st.metric("Indice de Santé Global", f"{score}/10")
    st.text_area("Conclusion & Recommandations", height=150)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚀 VALIDER L'EXPERTISE"):
    st.balloons()
    st.success("Rapport finalisé et prêt pour exportation.")