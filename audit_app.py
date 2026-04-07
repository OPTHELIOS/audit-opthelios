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
st.set_page_config(page_title="Opthelios Expert v4.7", layout="wide", page_icon="☀️")

if 'extra_counters' not in st.session_state:
    st.session_state.extra_counters = []

# --- 2. GESTION DU THÈME & STYLE (CORRECTIF FINAL CONTRASTE) ---
with st.sidebar:
    st.header("🎨 Options d'affichage")
    theme_choice = st.radio("Mode de l'interface", ["Clair ☀️", "Sombre 🌙"])

# Définition des variables de couleurs pour le CSS
if theme_choice == "Clair ☀️":
    bg_app = "#F8F9FA"
    bg_card = "#FFFFFF"
    txt_main = "#1A1C1E"  # Noir/Gris foncé pour le texte
    txt_label = "#1A1C1E"
    border_col = "#DDDDDD"
    table_text = "#1A1C1E"
else:
    bg_app = "#0E1117"
    bg_card = "#161B22"
    txt_main = "#FFFFFF"
    txt_label = "#E0E0E0"
    border_col = "#30363D"
    table_text = "#FFFFFF"

st.markdown(f"""
    <style>
    /* Fond de l'application */
    .stApp {{ background-color: {bg_app}; color: {txt_main}; }}
    
    /* En-têtes de section */
    .section-header {{ color: #FF7F00 !important; font-size: 1.2em; font-weight: bold; border-bottom: 2px solid #FF7F00; margin-bottom: 15px; padding-bottom: 5px; }}
    
    /* Conteneurs (Cards) */
    .info-card, .ballon-card, .counter-block {{ 
        background-color: {bg_card} !important; 
        border: 1px solid {border_col} !important; 
        padding: 20px; border-radius: 10px; margin-bottom: 15px; 
    }}
    
    /* Forçage de la couleur de TOUS les textes (Labels, Markdowns, Textes simples) */
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, label p, span, b, p {{
        color: {txt_main} !important;
    }}
    
    /* Correction spécifique pour les tableaux (Synthèse) */
    .stTable td, .stTable th {{
        color: {table_text} !important;
    }}
    
    /* Correction pour les labels de formulaires (étiquettes au-dessus des champs) */
    label, .stWidgetLabel p {{
        color: {txt_label} !important;
        font-weight: 500 !important;
    }}

    /* Bouton principal */
    .stButton>button {{ background-color: #FF7F00 !important; color: white !important; font-weight: bold !important; border-radius: 20px !important; width: 100%; border: none; }}
    
    /* Style des expandeurs */
    .streamlit-expanderHeader {{
        color: {txt_main} !important;
        background-color: {bg_card} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. IDENTIFICATION DU PROJET & GÉOLOCALISATION ---
st.title("☀️ Diagnostic Expert Opthelios")
st.markdown('<p class="section-header">📂 Identification du Projet & Géolocalisation</p>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1:
        nom_site = st.text_input("📍 Désignation de l'opération", placeholder="ex: Résidence Helios")
        moa = st.text_input("👤 Maîtrise d'Ouvrage (MOA)")
        exploit = st.text_input("⚙️ Exploitant / Mainteneur")
        adr = st.text_input("🏠 Adresse complète")
        st.write("**Coordonnées GPS**")
        cg1, cg2 = st.columns(2)
        lat = cg1.number_input("Latitude", format="%.6f", value=48.8566)
        lon = cg2.number_input("Longitude", format="%.6f", value=2.3522)
        date_visite = st.date_input("📅 Date du diagnostic")
    with c2:
        if MAP_AVAILABLE:
            st.write("🗺️ **Localisation interactive**")
            m = folium.Map(location=[lat, lon], zoom_start=16)
            folium.Marker([lat, lon], tooltip="Installation").add_to(m)
            st_folium(m, width="100%", height=250)
        else:
            st.info("💡 Ajoutez 'folium' et 'streamlit-folium' au fichier requirements.txt pour activer la carte.")
        photo_garde = st.camera_input("📸 Photo de garde")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. FICHE D'IDENTITÉ ---
st.header("📋 Fiche d'Identité")
with st.expander("🛠️ Détails de l'Installation", expanded=True):
    st.markdown('<p class="section-header">☀️ Capteurs Solaires</p>', unsafe_allow_html=True)
    cp1, cp2, cp3 = st.columns([2, 2, 1.5])
    with cp1:
        st.text_input("Marque capteurs", key="mc")
        st.text_input("Référence capteurs", key="rc")
    with cp2:
        nb_c = st.number_input("Nombre de capteurs", min_value=1, value=1)
        nb_r = st.number_input("Nombre de rangées", min_value=1, value=1)
    with cp3:
        azi = st.number_input("Azimut (°)", value=0)
        st.markdown(f"**Orientation :** {azi}°")

    st.markdown('<p class="section-header">📦 Stockage</p>', unsafe_allow_html=True)
    nb_b = st.number_input("Nombre de ballons", 1, 10, 1)
    for i in range(int(nb_b)):
        st.markdown(f'<div class="ballon-card"><b>Ballon n°{i+1}</b>', unsafe_allow_html=True)
        cb1, cb2 = st.columns(2)
        cb1.text_input("Marque/Modèle", key=f"m{i}")
        cb2.text_input("Volume (L)", key=f"v{i}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. AUDIT TECHNIQUE (Points du document Word) ---
st.divider()
st.header("🔍 Audit Technique")

# On intègre tous les points de contrôle du document Word [cite: 1]
audit_points = {
    "📄 Documentation & Élec": ["Schéma d'éxécution", "Schéma Electrique", "Analyse Fonctionnelle", "Raccordements électriques", "Mise à la terre"],
    "☀️ Capteurs & Toiture": ["Absence de vannes d'isolement", "Traversée de toiture", "Supports capteurs", "Raccordement correct", "Accès sécurisé", "Absence de masque"],
    "💧 Hydraulique": ["Sens de circulation", "Vannes remplissage", "Dégazeur ALLER", "Soupape sécurité", "Bidon récupération", "Circulateur RETOUR", "Clapet anti-retour"],
    "🎈 Expansion": ["Vase adapté", "Volume suffisant", "Isolement/Mise à l'air", "Pression conforme"],
    "📦 Stockage": ["Local hors gel", "Passage de porte", "Accès piquages/bride", "Protection cathodique", "Calorifuge", "Lyres anti-thermosiphon"],
    "🚿 Distribution ECS": ["Mitigeur présent", "T° max respectée", "Bouclage conforme", "Clapets AR", "Bouclage calorifugé"],
    "🧪 Fluide & Tests": ["pH fluide", "Protection Antigel (°C)", "Étanchéité conforme", "Réseau rincé"],
    "📊 Métrologie & Télégestion": ["Manomètre", "Débitmètre", "Sonde ensoleillement", "Sonde T° capteur", "Télécontrôleur conforme", "Connexion à distance", "COMPTEURS"]
}

def display_counter(label, kid):
    st.markdown(f'<div class="counter-block"><b>📊 {label}</b>', unsafe_allow_html=True)
    ca, cb, cc = st.columns([1, 1.5, 1])
    with ca:
        st.radio("Présent ?", ["Oui", "Non"], key=f"p{kid}", horizontal=True)
    with cb:
        st.text_input("Index relevé", key=f"i{kid}")
        st.checkbox("Sondes en doigts de gant ?", key=f"d{kid}")
    with cc:
        st.camera_input("Photo index", key=f"ph{kid}")
    st.markdown('</div>', unsafe_allow_html=True)

for sec, pts in audit_points.items():
    with st.expander(f"📁 {sec}"):
        for p in pts:
            if p == "COMPTEURS":
                display_counter("Compteur ESU", "esu")
                display_counter("Compteur ECS", "ecs")
            else:
                st.markdown(f"**{p}**")
                col1, col2, col3 = st.columns([1, 2, 1])
                col1.selectbox("Statut", ["Conforme", "Défaut", "N/C", "S/O"], key=f"s{p}", label_visibility="collapsed")
                col2.text_input("Observations", key=f"o{p}", label_visibility="collapsed", placeholder="Notes...")
                col3.camera_input("Photo", key=f"c{p}", label_visibility="collapsed")

# --- 6. SYNTHÈSE DÉCISIONNELLE (Correction de l'affichage) ---
st.divider()
st.header("🏁 Synthèse Décisionnelle")
st.markdown('<div class="info-card">', unsafe_allow_html=True)
col_s1, col_s2 = st.columns([2, 1])

with col_s1:
    st.markdown("### 📋 Plan d'Intervention Priorisé")
    # Utilisation d'un dictionnaire pour s'assurer que le tableau s'affiche correctement
    plan_data = [
        {"Priorité": "🔴 P1 (Urgent)", "Domaine": "Sécurité / Sanitaire", "Action": "Vase d'expansion, Soupape ou Mitigeur"},
        {"Priorité": "🟠 P2 (Important)", "Domaine": "Maintenance", "Action": "Fluide caloporteur, Calorifuge"},
        {"Priorité": "🔵 P3 (Amélioration)", "Domaine": "Suivi", "Action": "Métrologie, Télégestion"}
    ]
    st.table(plan_data)

with col_s2:
    st.markdown("### 🌟 Score Global")
    score_final = st.slider("Note de l'installation / 10", 0, 10, 5)
    st.metric("Indice de Santé", f"{score_final}/10")
    st.text_area("Conclusion & Recommandations", height=150, placeholder="Rédigez votre avis d'expert ici...")

st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚀 VALIDER L'EXPERTISE ET GÉNÉRER LE RAPPORT"):
    st.balloons()
    st.success("Expertise enregistrée avec succès.")