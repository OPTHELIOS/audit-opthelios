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

if 'extra_counters' not in st.session_state:
    st.session_state.extra_counters = []

# --- 2. GESTION DU THÈME & STYLE (Lisibilité Maximale) ---
with st.sidebar:
    st.header("🎨 Options d'affichage")
    theme_choice = st.radio("Mode de l'interface", ["Clair ☀️", "Sombre 🌙"])

if theme_choice == "Clair ☀️":
    bg_app, bg_card, txt_main, border_col = "#F8F9FA", "#FFFFFF", "#000000", "#DDDDDD"
else:
    bg_app, bg_card, txt_main, border_col = "#0E1117", "#161B22", "#FFFFFF", "#30363D"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_app}; color: {txt_main}; }}
    .section-header {{ color: #FF7F00 !important; font-size: 1.2em; font-weight: bold; border-bottom: 2px solid #FF7F00; margin-bottom: 15px; padding-bottom: 5px; }}
    .info-card, .counter-block {{ 
        background-color: {bg_card} !important; 
        border: 1px solid {border_col} !important; 
        padding: 20px; border-radius: 10px; margin-bottom: 15px; 
    }}
    /* Forçage de la visibilité des textes et étiquettes */
    label p, .stMarkdown p, b, p, span {{ color: {txt_main} !important; }}
    .stButton>button {{ background-color: #FF7F00 !important; color: white !important; font-weight: bold !important; border-radius: 10px !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. EN-TÊTE AVEC VOTRE LOGO ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    else:
        st.write("☀️")
with col_title:
    st.title("Opthelios, expertise solaire")

# --- 4. IDENTIFICATION DU PROJET & GÉOLOCALISATION ---
st.markdown('<p class="section-header">📂 Identification du Projet & Géolocalisation</p>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    col_id1, col_id2 = st.columns([1, 1])
    with col_id1:
        nom_site = st.text_input("📍 Désignation de l'opération", placeholder="ex: Résidence Helios")
        client_moa = st.text_input("👤 Maîtrise d'Ouvrage (MOA)")
        adr_site = st.text_input("🏠 Adresse complète")
        st.write("**Coordonnées GPS**")
        c_gps1, c_gps2 = st.columns(2)
        lat = c_gps1.number_input("Latitude", format="%.6f", value=48.8566)
        lon = c_gps2.number_input("Longitude", format="%.6f", value=2.3522)
    with col_id2:
        if MAP_AVAILABLE:
            m = folium.Map(location=[lat, lon], zoom_start=16)
            folium.Marker([lat, lon]).add_to(m)
            st_folium(m, width="100%", height=220)
        photo_main = st.camera_input("📸 Photo de garde")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. AUDIT TECHNIQUE (POINTS DE CONTRÔLE DOCX) ---
st.header("🔍 Audit Technique")

# Données extraites strictement de votre fichier Word
sections_data = {
    "📄 Documentation & Élec": ["présence et conformité du schéma d'éxécution", "présence et conformité du schéma Electrique", "présence et conformité de l'Analyse Fonctionnelle", "Contrôle des raccordements électriques", "Conformités de l'installation générale", "Mise à la terre de l'installation"],
    "☀️ Capteurs": ["absence de vannes d'isolement sur tuyauterie capteurs", "Dispositif de traversé de toiture ou de parois adapté", "Supports capteurs conformes", "Raccordement correct des capteurs", "Accès capteurs sécurisé", "Absence de masque proche"],
    "⚖️ Équilibrage & Réseau": ["Dispositif d'équilibrage sur chaque champ capteurs", "Dispositifs d'équilibrages sécurisés et exploitables (lisible)", "Matériaux (tuyauteries) conformes à l'usage"],
    "💧 Hydraulique Solaire": ["Circulation capteurs et échangeur dans le bon sens", "Présence de vannes pour raccordement pompe de remplissage", "Présence d'un dégazeur sur la conduite chaud (ALLER)", "Soupape de sécurité présente et conforme", "Bidon de récupération avec contrôle de niveau", "Circulateur/pompe solaire sur le froid (RETOUR)", "Présence Clapet anti-retour froid (RETOUR)", "Vannes 3 voies (V3V) fonctionnelles"],
    "🎈 Expansion": ["Présence d'un vase d'expansion adapté", "Volume du vase d'expansion suffisant", "Présence d'un dispositif d'isolement et de mise à l'air", "Raccordement du vase sur le froid (RETOUR)", "Pression du vase conforme"],
    "📦 Stockage & Échangeur": ["Raccordement de l'échangeur en contre-courant", "Vannes d'isolement échangeur", "Puissance de l'échangeur suffisante", "Ballons dans local fermé, hors gel", "accès complet aux piquages et bride(s)", "Absence Clapet anti-retour entre les ballons", "Vannes de vidange et de chasse", "protection cathodique ballon", "calorifuge du stockage", "Coudes vers le bas sur les piquages (Lyres)"],
    "🚿 Distribution ECS": ["Mitigeur présent", "Température maximale de l'ECS respectée", "Raccordement correct du bouclage", "Présence des clapets anti-retour", "Bouclage calorifugé"],
    "📊 Métrologie & Tests": ["Manomètre de contrôle", "Débitmètre(s) présent(s)", "Sonde d'ensoleillement bien placée", "Seuil d'éclairement conforme", "Sonde de température capteur", "Dispositif de prélèvement du liquide caloporteur", "Compteur volumétrique Eau froide", "Tests d'étanchéité conforme", "Réseau rincé", "Télécontrôleur conforme", "Connexion à distance fonctionnelle"]
}

for sec, pts in sections_data.items():
    with st.expander(f"📁 {sec}"):
        for p in pts:
            st.markdown(f"**{p}**")
            c1, c2, c3 = st.columns([1, 2, 1])
            c1.selectbox("Statut", ["Conforme", "Défaut", "N/C", "S/O"], key=f"s_{p}", label_visibility="collapsed")
            c2.text_input("Note", key=f"o_{p}", label_visibility="collapsed", placeholder="Observations...")
            c3.camera_input("Photo", key=f"ph_{p}", label_visibility="collapsed")

# --- 6. SYNTHÈSE FINALE ---
st.divider()
st.header("🏁 Synthèse & Plan d'Actions")
st.markdown('<div class="info-card">', unsafe_allow_html=True)
col_s1, col_s2 = st.columns([2, 1])
with col_s1:
    st.subheader("Plan d'Intervention")
    plan = [
        {"Priorité": "🔴 P1", "Action": "Organes de Sécurité (Vase, Soupape, Mitigeur)"},
        {"Priorité": "🟠 P2", "Action": "Maintenance (Fluide & Calorifuge)"},
        {"Priorité": "🔵 P3", "Action": "Métrologie & Télégestion"}
    ]
    st.table(plan)
with col_s2:
    score = st.slider("Santé de l'installation / 10", 0, 10, 5)
    st.text_area("Conclusion technique finale", height=150)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚀 VALIDER L'EXPERTISE"):
    st.balloons()
    st.success("Rapport d'expertise finalisé.")