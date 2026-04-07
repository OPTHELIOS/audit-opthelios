import streamlit as st
import os

# --- TENTATIVE D'IMPORTATION DES MODULES DE CARTE ---
try:
    from streamlit_folium import st_folium
    import folium
    MAP_AVAILABLE = True
except ImportError:
    MAP_AVAILABLE = False

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Opthelios Expertise Solaire", layout="wide", page_icon="☀️")

# --- 2. STYLE CSS (Contraste forcé pour lisibilité) ---
with st.sidebar:
    st.header("🎨 Options d'affichage")
    theme_choice = st.radio("Mode de l'interface", ["Clair ☀️", "Sombre 🌙"])

bg, card, txt, border = ("#F8F9FA", "#FFFFFF", "#000000", "#DDDDDD") if theme_choice == "Clair ☀️" else ("#0E1117", "#161B22", "#FFFFFF", "#30363D")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    .section-header {{ color: #FF7F00 !important; font-size: 1.2em; font-weight: bold; border-bottom: 2px solid #FF7F00; margin-bottom: 15px; padding-bottom: 5px; }}
    .info-card, .ballon-card, .counter-block {{ background-color: {card} !important; border: 1px solid {border} !important; padding: 20px; border-radius: 10px; margin-bottom: 15px; }}
    label p, .stMarkdown p, b, p, span {{ color: {txt} !important; }}
    .stButton>button {{ background-color: #FF7F00 !important; color: white !important; font-weight: bold !important; border-radius: 10px !important; width: 100%; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. EN-TÊTE AVEC VOTRE LOGO ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
with col_title:
    st.title("Opthelios, expertise solaire")

# --- 4. IDENTIFICATION & GÉOLOCALISATION ---
st.markdown('<p class="section-header">📂 Identification du Projet</p>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1:
        st.text_input("📍 Opération", placeholder="ex: Résidence Helios")
        st.text_input("👤 Maîtrise d'Ouvrage (MOA)")
        st.text_input("🏠 Adresse complète")
        st.write("**Coordonnées GPS**")
        cg1, cg2 = st.columns(2)
        lat = cg1.number_input("Lat", format="%.6f", value=48.8566)
        lon = cg2.number_input("Lon", format="%.6f", value=2.3522)
    with c2:
        if MAP_AVAILABLE:
            m = folium.Map(location=[lat, lon], zoom_start=16)
            folium.Marker([lat, lon]).add_to(m)
            st_folium(m, width="100%", height=220)
        st.camera_input("📸 Photo de garde")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. FICHE D'IDENTITÉ DE L'INSTALLATION ---
st.header("📋 Fiche d'Identité de l'Installation")
with st.expander("🛠️ Détails du Matériel", expanded=True):
    # Capteurs
    st.markdown('<p class="section-header">☀️ Capteurs Solaires</p>', unsafe_allow_html=True)
    cp1, cp2, cp3 = st.columns([2, 1, 1])
    with cp1:
        st.text_input("Marque / Référence")
        st.selectbox("Type", ["Capteurs plans", "Tubulaires", "Moquette"])
    with cp2:
        st.number_input("Nombre de capteurs", min_value=1, value=1)
        st.number_input("Nombre de rangées", min_value=1, value=1)
    with cp3:
        st.number_input("Azimut (°)", value=163)
        st.number_input("Inclinaison (°)", value=45)

    # Station & Stockage
    st.markdown('<p class="section-header">⚙️ Station Solaire & Stockage</p>', unsafe_allow_html=True)
    cs1, cs2 = st.columns(2)
    cs1.text_input("Marque/Réf Circulateur")
    cs2.text_input("Marque/Réf Régulateur")
    
    nb_b = st.number_input("Nombre de ballons", 1, 10, 1)
    for i in range(int(nb_b)):
        st.markdown(f'<div class="ballon-card"><b>Ballon n°{i+1}</b>', unsafe_allow_html=True)
        cb1, cb2 = st.columns(2)
        cb1.text_input("Marque/Modèle", key=f"m{i}")
        cb2.text_input("Volume (L)", key=f"v{i}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. AUDIT TECHNIQUE (Points de contrôle docx) ---
st.header("🔍 Audit Technique")
sections = {
    "📄 Documentation & Élec": ["présence et conformité du schéma d'éxécution", "présence et conformité du schéma Electrique", "présence et conformité de l'Analyse Fonctionnelle", "Contrôle des raccordements électriques", "Conformités de l'installation générale", "Mise à la terre de l'installation"],
    "☀️ Capteurs": ["absence de vannes d'isolement sur tuyauterie capteurs", "Dispositif de traversé de toiture ou de parois adapté", "Supports capteurs conformes", "Raccordement correct des capteurs", "Accès capteurs sécurisé", "Absence de masque proche"],
    "⚖️ Équilibrage & Canalisations": ["Dispositif d'équilibrage sur chaque champ capteurs", "Dispositifs d'équilibrages sécurisés et exploitables (lisible)", "Matériaux (tuyauteries) conformes à l'usage"],
    "💧 Hydraulique Solaire": ["Circulation capteurs et échangeur dans le bon sens", "Présence de vannes pour raccordement pompe de remplissage", "Présence d'un dégazeur sur la conduite chaud (ALLER)", "Soupape de sécurité présente et conforme", "Bidon de récupération avec contrôle de niveau", "Circulateur/pompe solaire sur le froid (RETOUR)", "Présence Clapet anti-retour froid (RETOUR)", "Vannes 3 voies (V3V) fonctionnelles"],
    "🎈 Expansion": ["Présence d'un vase d'expansion adapté", "Volume du vase d'expansion suffisant", "Présence d'un dispositif d'isolement et de mise à l'air", "Raccordement du vase sur le froid (RETOUR)", "Pression du vase conforme"],
    "📦 Échangeur & Stockage": ["Raccordement de l'échangeur en contre-courant", "Vannes d'isolement échangeur", "Puissance de l'échangeur suffisante", "Ballons dans local fermé, hors gel", "ouverture de porte permettant le passage", "accès complet aux piquages et bride(s)", "Vannes de vidange et de chasse", "protection cathodique ballon", "calorifuge du stockage", "Lyres anti-thermosiphon"],
    "🚿 Distribution ECS": ["Mitigeur présent", "Température maximale de l'ECS respectée", "Raccordement correct du bouclage", "Présence des clapets anti-retour", "Bouclage calorifugé"],
    "📊 Métrologie & Tests": ["Manomètre de contrôle", "Débitmètre(s) présent(s)", "Sonde d'ensoleillement bien placée", "Seuil d'éclairement conforme", "Sonde de température capteur", "Dispositif de prélèvement du liquide caloporteur", "Compteur volumétrique Eau froide", "Tests d'étanchéité conforme", "Réseau rincé", "Télécontrôleur conforme", "Connexion à distance fonctionnelle"]
}

for sec, pts in sections.items():
    with st.expander(f"📁 {sec}"):
        for p in pts:
            st.markdown(f"**{p}**")
            col1, col2, col3 = st.columns([1, 2, 1])
            col1.selectbox("Statut", ["Conforme", "Défaut", "N/C", "S/O"], key=f"s_{p}", label_visibility="collapsed")
            col2.text_input("Note", key=f"o_{p}", label_visibility="collapsed", placeholder="Observations...")
            col3.camera_input("Photo", key=f"ph_{p}", label_visibility="collapsed")

# --- 7. SYNTHÈSE ---
st.divider()
st.header("🏁 Synthèse")
st.markdown('<div class="info-card">', unsafe_allow_html=True)
col_s1, col_s2 = st.columns([2, 1])
with col_s1:
    st.subheader("Plan d'Actions Priorisé")
    st.table([{"Priorité": "🔴 P1", "Action": "Sécurité & Sanitaire"}, {"Priorité": "🟠 P2", "Action": "Maintenance & Fluide"}, {"Priorité": "🔵 P3", "Action": "Suivi & Métrologie"}])
with col_s2:
    st.slider("Note de l'installation / 10", 0, 10, 5)
    st.text_area("Conclusion de l'expert")
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚀 VALIDER L'EXPERTISE"):
    st.balloons()