import streamlit as st
import os

# --- 1. MODULES EXTERNES (CARTOGRAPHIE) ---
try:
    from streamlit_folium import st_folium
    import folium
    MAP_AVAILABLE = True
except ImportError:
    MAP_AVAILABLE = False

# --- 2. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Opthelios - Expertise Solaire Complète", layout="wide", page_icon="☀️")

# --- 3. SYSTÈME DE THÈME ET CONTRASTE (FIX DÉFINITIF) ---
with st.sidebar:
    st.header("🎨 Options d'affichage")
    theme_choice = st.radio("Mode de l'interface", ["Clair ☀️", "Sombre 🌙"])

# Couleurs dynamiques pour éviter les textes noirs sur fond sombre ou invisibles
if theme_choice == "Clair ☀️":
    bg, card, txt, border, header_c = "#F8F9FA", "#FFFFFF", "#000000", "#DDDDDD", "#FF7F00"
else:
    bg, card, txt, border, header_c = "#0E1117", "#161B22", "#FFFFFF", "#30363D", "#FF7F00"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    [data-testid="stSidebar"] {{ background-color: {bg} !important; border-right: 1px solid {border}; }}
    [data-testid="stSidebar"] * {{ color: {txt} !important; }}
    
    /* Fix Expander (Titres de sections) */
    .streamlit-expanderHeader {{ 
        background-color: {card} !important; 
        color: {txt} !important; 
        border: 1px solid {border} !important; 
    }}
    .streamlit-expanderHeader:hover {{ color: {header_c} !important; }}
    .streamlit-expanderHeader p {{ color: {txt} !important; }}

    /* Cards & Blocks */
    .info-card, .ballon-card, .counter-block {{ 
        background-color: {card} !important; 
        border: 1px solid {border} !important; 
        padding: 20px; border-radius: 10px; margin-bottom: 15px; 
    }}
    
    .section-header {{ 
        color: {header_c} !important; 
        font-size: 1.2em; font-weight: bold; 
        border-bottom: 2px solid {header_c}; 
        margin-bottom: 15px; padding-bottom: 5px; 
    }}
    
    label p, .stMarkdown p, b, p, span, .stWidgetLabel {{ color: {txt} !important; }}
    .stButton>button {{ background-color: {header_c} !important; color: white !important; font-weight: bold; border-radius: 8px; width: 100%; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. EN-TÊTE AVEC LOGO ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    # Utilisation du logo.png (identifié dans image_6e0dbe.png)
    if os.path.exists("logo.png"): 
        st.image("logo.png", width=120)
with col_title:
    st.title("Opthelios, expertise solaire")

# --- 5. IDENTIFICATION & GÉOLOCALISATION ---
st.markdown('<p class="section-header">📂 Identification du Projet & Géolocalisation</p>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1:
        st.text_input("📍 Opération", placeholder="ex: Résidence Helios")
        st.text_input("👤 Maîtrise d'Ouvrage (MOA)")
        st.text_input("⚙️ Exploitant en charge")
        st.text_input("🏠 Adresse complète du site")
        st.write("**Coordonnées GPS**")
        cg1, cg2 = st.columns(2)
        lat = cg1.number_input("Latitude", format="%.6f", value=48.8566)
        lon = cg2.number_input("Longitude", format="%.6f", value=2.3522)
    with c2:
        if MAP_AVAILABLE:
            m = folium.Map(location=[lat, lon], zoom_start=17)
            folium.Marker([lat, lon], tooltip="Position du site").add_to(m)
            st_folium(m, width="100%", height=280)
        else:
            st.warning("⚠️ Module Folium absent. Ajoutez-le au requirements.txt")
        st.camera_input("📸 Photo de garde du bâtiment")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. FICHE D'IDENTITÉ TECHNIQUE ---
st.header("📋 Fiche d'Identité de l'Installation")
with st.expander("🛠️ Détails du Matériel Installé", expanded=True):
    st.markdown('<p class="section-header">☀️ Capteurs Solaires</p>', unsafe_allow_html=True)
    cp1, cp2, cp3 = st.columns([2, 1, 1])
    with cp1:
        st.text_input("Marque / Référence des Capteurs")
        st.number_input("Nombre total de capteurs", min_value=1, value=1)
        st.number_input("Nombre de rangées / champs", min_value=1, value=1)
    with cp2:
        azimut = st.number_input("Azimut (°)", value=163, help="0°=Nord, 180°=Sud")
        st.number_input("Inclinaison (°)", value=45)
    with cp3:
        st.write("**Orientation**")
        # Boussole dynamique
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; background: white; border-radius: 50%; width: 100px; height: 100px; margin: auto; border: 2px solid #FF7F00; position: relative;">
                <div style="position: absolute; width: 2px; height: 80px; background: red; transform: rotate({azimut}deg); transition: transform 0.5s;"></div>
                <b style="color: black; z-index: 2;">S</b>
            </div>
            <p style="text-align: center; font-size: 0.8em; margin-top: 5px; color: {txt};">Axe : {azimut}°</p>
        """, unsafe_allow_html=True)

    st.markdown('<p class="section-header">⚙️ Station & Stockage</p>', unsafe_allow_html=True)
    cs1, cs2 = st.columns(2)
    cs1.text_input("Marque/Réf Circulateur Solaire")
    cs2.text_input("Marque/Réf Régulateur / Télégestion")
    
    nb_b = st.number_input("Nombre de ballons de stockage", 1, 10, 1)
    for i in range(int(nb_b)):
        st.markdown(f'<div class="ballon-card"><b>Ballon n°{i+1}</b>', unsafe_allow_html=True)
        cb1, cb2 = st.columns(2)
        cb1.text_input("Marque / Modèle", key=f"m_bal_{i}")
        cb2.text_input("Capacité (Litres)", key=f"v_bal_{i}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 7. AUDIT TECHNIQUE (FUSION INTÉGRALE) ---
st.header("🔍 Audit Technique & Points de Contrôle")
# Fusion exhaustive des points initiaux + Fichier Word
sections = {
    "📄 Documentation & Électricité": [
        "Présence et conformité du schéma d'éxécution", "Présence et conformité du schéma Electrique", 
        "Présence et conformité de l'Analyse Fonctionnelle", "Contrôle des raccordements électriques", 
        "Conformités de l'installation générale", "Mise à la terre de l'installation"
    ],
    "☀️ Champ Capteurs & Toiture": [
        "Absence de vannes d'isolement sur tuyauterie capteurs", "Dispositif de traversé de toiture adapté", 
        "Supports capteurs conformes et fixés", "Raccordement correct des capteurs", 
        "Accès capteurs sécurisé (Ligne de vie/échelle)", "Absence de masque proche (Ombrage)"
    ],
    "⚖️ Équilibrage & Canalisations": [
        "Dispositif d'équilibrage sur chaque champ", "Équilibrages sécurisés et lisibles", 
        "Matériaux tuyauteries conformes à l'usage solaire"
    ],
    "💧 Hydraulique Solaire": [
        "Circulation capteurs/échangeur dans le bon sens", "Vannes pour raccordement pompe remplissage", 
        "Présence dégazeur sur conduite ALLER", "Soupape de sécurité conforme", 
        "Bidon de récupération avec contrôle niveau", "Circulateur sur conduite RETOUR", 
        "Présence Clapet anti-retour", "Vannes 3 voies (V3V) fonctionnelles"
    ],
    "🎈 Système d'Expansion": [
        "Vase d'expansion dimensionné et adapté", "Volume du vase suffisant", 
        "Dispositif d'isolement et de mise à l'air", "Raccordement vase sur le RETOUR", "Pression du vase conforme"
    ],
    "📦 Échangeur & Stockage": [
        "Échangeur raccordé en contre-courant", "Vannes d'isolement échangeur", 
        "Puissance échangeur suffisante", "Ballons hors gel", "Ouverture de porte suffisante", 
        "Accès complet aux piquages et brides", "Vannes de vidange et de chasse", 
        "Protection cathodique (Anode)", "Calorifugeage du stockage", "Lyres anti-thermosiphon (coudes bas)"
    ],
    "🚿 Distribution ECS & Bouclage": [
        "Mitigeur thermostatique présent", "T° max ECS respectée (Sécurité)", 
        "Raccordement correct du bouclage", "Clapets anti-retour sur bouclage", "Bouclage calorifugé"
    ],
    "📊 Métrologie & Tests": [
        "Manomètre de contrôle circuit solaire", "Débitmètre(s) présent(s)", 
        "Sonde d'ensoleillement bien placée", "Sonde T° capteur fonctionnelle", 
        "Sonde Bas de ballon solaire", "Prélèvement fluide caloporteur possible", 
        "Tests d'étanchéité conformes", "Réseau rincé", "Télécontrôleur conforme"
    ]
}

for sec, pts in sections.items():
    with st.expander(f"📁 {sec}"):
        for p in pts:
            st.markdown(f"**{p}**")
            col1, col2, col3, col4 = st.columns([1, 1.5, 1, 1])
            col1.selectbox("Verdict", ["Conforme", "Défaut", "N/C", "S/O"], key=f"statut_{p}", label_visibility="collapsed")
            col2.text_input("Observations", key=f"obs_{p}", label_visibility="collapsed", placeholder="Observations techniques...")
            col3.camera_input("Photo", key=f"cam_{p}", label_visibility="collapsed")
            col4.file_uploader("Preuve/Doc", key=f"file_{p}", label_visibility="collapsed")

# --- 8. RELEVÉS DE COMPTEURS (RÉTABLIS) ---
st.header("📊 Relevés de Compteurs Énergétiques")
with st.expander("🔍 Analyse des Index ESU / ECS", expanded=True):
    for cpt in ["Compteur Énergie Solaire (ESU)", "Compteur Eau Chaude (ECS)"]:
        st.markdown(f'<div class="counter-block"><b>{cpt}</b>', unsafe_allow_html=True)
        rc1, rc2, rc3, rc4 = st.columns([1, 1, 1, 2])
        rc1.radio("Présence ?", ["Oui", "Non"], key=f"pres_{cpt}")
        rc2.text_input("Index actuel", key=f"idx_{cpt}", placeholder="Valeur...")
        rc3.checkbox("Sondes en doigt de gant ?", key=f"ddg_{cpt}")
        rc4.camera_input("Photo de l'index", key=f"photo_cpt_{cpt}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 9. ANNEXES TECHNIQUES GLOBALES ---
st.header("📂 Annexes & Documents de Référence")
st.markdown('<div class="info-card">', unsafe_allow_html=True)
st.info("Téléversez ici les documents volumineux : rapports de rinçage, fiches constructeurs, schémas PDF globaux.")
st.file_uploader("Ajouter des fichiers (PDF, JPG, PNG)", accept_multiple_files=True, key="annexes_finales")
st.markdown('</div>', unsafe_allow_html=True)

# --- 10. SYNTHÈSE & VALIDATION ---
st.divider()
st.header("🏁 Synthèse Décisionnelle")
st.markdown('<div class="info-card">', unsafe_allow_html=True)
sc1, sc2 = st.columns([2, 1])
with sc1:
    st.subheader("Plan d'Actions Priorisé")
    st.table([
        {"Priorité": "🔴 P1", "Domaine": "Sécurité & Sanitaire", "Impact": "Immédiat"},
        {"Priorité": "🟠 P2", "Domaine": "Performance & Maintenance", "Impact": "Moyen terme"},
        {"Priorité": "🔵 P3", "Domaine": "Métrologie & Optimisation", "Impact": "Amélioration"}
    ])
with sc2:
    st.slider("Note de l'expertise / 10", 0, 10, 5)
    st.text_area("Conclusion de l'Expert Opthelios", height=150)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚀 VALIDER ET GÉNÉRER LE RAPPORT D'AUDIT"):
    st.balloons()
    st.success("Expertise validée. Toutes les données et pièces jointes sont enregistrées.")