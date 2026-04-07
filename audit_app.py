import streamlit as st
import os
import base64

# --- CONFIGURATION ---
st.set_page_config(page_title="Opthelios Expertise Solaire", layout="wide", page_icon="☀️")

# --- CSS CORRECTIF (BANDEAU, TITRES, CONTRASTE) ---
with st.sidebar:
    st.header("🎨 Options d'affichage")
    theme_choice = st.radio("Mode de l'interface", ["Clair ☀️", "Sombre 🌙"])

# Variables de couleurs pour éviter l'illisibilité
if theme_choice == "Clair ☀️":
    bg, card, txt, border, hover_txt = "#F8F9FA", "#FFFFFF", "#000000", "#DDDDDD", "#FF7F00"
else:
    bg, card, txt, border, hover_txt = "#0E1117", "#161B22", "#FFFFFF", "#30363D", "#FF7F00"

st.markdown(f"""
    <style>
    /* Fixer la couleur du texte dans la barre latérale */
    [data-testid="stSidebar"] {{ background-color: {bg} !important; }}
    [data-testid="stSidebar"] * {{ color: {txt} !important; }}
    
    /* Fond de l'app et textes généraux */
    .stApp {{ background-color: {bg}; color: {txt}; }}
    h1, h2, h3, label, p, span, b, .stWidgetLabel {{ color: {txt} !important; }}
    
    /* Correction des titres de sections (Expanders) pour éviter le noir au survol */
    .streamlit-expanderHeader {{ background-color: {card} !important; color: {txt} !important; border: 1px solid {border} !important; }}
    .streamlit-expanderHeader:hover {{ color: {hover_txt} !important; }}
    
    /* Conteneurs */
    .info-card, .ballon-card, .counter-block {{ background-color: {card} !important; border: 1px solid {border} !important; padding: 20px; border-radius: 10px; margin-bottom: 15px; }}
    
    .section-header {{ color: #FF7F00 !important; font-size: 1.2em; font-weight: bold; border-bottom: 2px solid #FF7F00; margin-bottom: 15px; padding-bottom: 5px; }}
    </style>
    """, unsafe_allow_html=True)

# --- EN-TÊTE ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    if os.path.exists("logo.png"): st.image("logo.png", width=120)
with col_title:
    st.title("Opthelios, expertise solaire")

# --- 1. IDENTIFICATION ---
st.markdown('<p class="section-header">📂 Identification du Projet</p>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("📍 Opération", placeholder="ex: Résidence Helios")
        st.text_input("👤 Maîtrise d'Ouvrage (MOA)")
        st.text_input("🏠 Adresse complète")
    with c2:
        st.date_input("📅 Date du diagnostic")
        st.camera_input("📸 Photo de garde")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 2. FICHE D'IDENTITÉ & BOUSSOLE ---
st.header("📋 Fiche d'Identité de l'Installation")
with st.expander("🛠️ Détails du Matériel", expanded=True):
    st.markdown('<p class="section-header">☀️ Capteurs Solaires</p>', unsafe_allow_html=True)
    cp1, cp2, cp3 = st.columns([2, 1, 1])
    with cp1:
        st.text_input("Marque / Référence Capteurs")
        st.number_input("Nombre de capteurs", min_value=1, value=1)
    with cp2:
        azimut = st.number_input("Azimut (°)", value=163, help="0°=Nord, 90°=Est, 180°=Sud, 270°=Ouest")
        st.number_input("Inclinaison (°)", value=45)
    with cp3:
        # BOUSSOLE DYNAMIQUE
        st.write("**Boussole Orientation**")
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; background: white; border-radius: 50%; width: 100px; height: 100px; margin: auto; border: 2px solid #FF7F00; position: relative;">
                <div style="position: absolute; width: 2px; height: 80px; background: red; transform: rotate({azimut}deg); transition: transform 0.5s;"></div>
                <b style="color: black; z-index: 2;">S</b>
            </div>
            <p style="text-align: center; font-size: 0.8em; margin-top: 5px;">Axe : {azimut}°</p>
        """, unsafe_allow_html=True)

    st.markdown('<p class="section-header">⚙️ Station & Stockage</p>', unsafe_allow_html=True)
    cs1, cs2 = st.columns(2)
    cs1.text_input("Circulateur (Modèle/Réf)")
    cs2.text_input("Régulateur (Modèle/Réf)")
    
    nb_b = st.number_input("Nombre de ballons", 1, 5, 1)
    for i in range(int(nb_b)):
        st.markdown(f'<div class="ballon-card"><b>Ballon n°{i+1}</b>', unsafe_allow_html=True)
        cb1, cb2 = st.columns(2)
        cb1.text_input("Marque", key=f"m{i}")
        cb2.text_input("Volume (L)", key=f"v{i}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 3. AUDIT TECHNIQUE COMPLET (POINTS WORD) ---
st.header("🔍 Audit Technique")
sections = {
    "📄 Documentation & Élec": ["présence et conformité du schéma d'éxécution", "présence et conformité du schéma Electrique", "présence et conformité de l'Analyse Fonctionnelle", "Contrôle des raccordements électriques", "Conformités de l'installation générale", "Mise à la terre de l'installation"],
    "☀️ Capteurs": ["absence de vannes d'isolement sur tuyauterie capteurs", "Dispositif de traversé de toiture ou de parois adapté", "Supports capteurs conformes", "Raccordement correct des capteurs", "Accès capteurs sécurisé", "Absence de masque proche"],
    "⚖️ Équilibrage": ["Dispositif d'équilibrage sur chaque champ capteurs", "Dispositifs d'équilibrages sécurisés et exploitables (lisible)", "Matériaux (tuyauteries) conformes à l'usage"],
    "💧 Hydraulique": ["Circulation capteurs et échangeur dans le bon sens", "Présence de vannes pour raccordement pompe de remplissage", "Dégazeur sur ALLER chaud", "Soupape de sécurité conforme", "Bidon de récupération", "Circulateur sur RETOUR froid", "Clapet anti-retour", "Vannes 3 voies"],
    "🎈 Expansion": ["Vase d'expansion adapté", "Volume suffisant", "Dispositif d'isolement/mise à l'air", "Raccordement sur RETOUR froid", "Pression conforme"],
    "📦 Échangeur & Stockage": ["Echangeur en contre-courant", "Vannes d'isolement échangeur", "Puissance échangeur", "Local hors gel", "Ouverture de porte", "Accès piquages/brides", "Vidange et chasse", "Protection cathodique", "Calorifuge", "Lyres anti-thermosiphon"],
    "🚿 Distribution ECS": ["Mitigeur présent", "T° max respectée", "Bouclage conforme", "Clapets anti-retour", "Bouclage calorifugé"],
    "📊 Métrologie & Tests": ["Manomètre", "Débitmètre", "Sonde ensoleillement", "Sonde T° capteur", "Sonde Bas de ballon", "Prélèvement fluide", "Compteur Eau froide", "Tests étanchéité", "Réseau rincé", "Télécontrôleur conforme", "Connexion à distance"]
}

for sec, pts in sections.items():
    with st.expander(f"📁 {sec}"):
        for p in pts:
            st.markdown(f"**{p}**")
            col_st, col_obs, col_cam, col_file = st.columns([1, 1.5, 1, 1])
            col_st.selectbox("Verdict", ["Conforme", "Défaut", "N/C", "S/O"], key=f"s_{p}", label_visibility="collapsed")
            col_obs.text_input("Note", key=f"o_{p}", label_visibility="collapsed", placeholder="Observations...")
            col_cam.camera_input("Photo", key=f"ph_{p}", label_visibility="collapsed")
            col_file.file_uploader("Joint (PDF/JPG)", key=f"f_{p}", label_visibility="collapsed")

# --- 4. SYNTHÈSE ---
st.divider()
st.header("🏁 Synthèse")
st.markdown('<div class="info-card">', unsafe_allow_html=True)
col_s1, col_s2 = st.columns([2, 1])
with col_s1:
    st.subheader("Plan d'Actions")
    st.table([{"Prio": "🔴 P1", "Action": "Sécurité (Vase, Soupape, Mitigeur)"}, {"Prio": "🟠 P2", "Action": "Maintenance (Fluide, Rinçage)"}, {"Prio": "🔵 P3", "Action": "Suivi (Métrologie, Télégestion)"}])
with col_s2:
    st.slider("Note globale / 10", 0, 10, 5)
    st.text_area("Conclusion technique")
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚀 VALIDER L'EXPERTISE"):
    st.balloons()
    st.success("Audit validé avec l'ensemble des pièces jointes.")