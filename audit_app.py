import streamlit as st
import os

# --- 1. CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="Opthelios Expert v3", layout="wide", page_icon="☀️")

# Initialisation pour les compteurs dynamiques
if 'extra_counters' not in st.session_state:
    st.session_state.extra_counters = []

# --- 2. GESTION DU THÈME & SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png")
    st.header("🎨 Interface")
    theme = st.radio("Mode", ["☀️ Clair", "🌙 Sombre"], horizontal=True)
    
    sidebar_bg = "#001f3f" if theme == "☀️ Clair" else "#000000"
    st.markdown(f"""
        <style>
        [data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; color: white !important; }}
        [data-testid="stSidebar"] * {{ color: white !important; }}
        </style>
    """, unsafe_allow_html=True)

# --- 3. CSS ADAPTATIF ET STYLES MÉTIER ---
if theme == "🌙 Sombre":
    bg, card, txt, brd = "#0E1117", "#161B22", "#FFFFFF", "#30363D"
else:
    bg, card, txt, brd = "#F8F9FA", "#FFFFFF", "#1A1C1E", "#D0D5DD"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    [data-testid="stExpander"] {{ background-color: {card} !important; border: 1px solid {brd} !important; border-radius: 8px !important; margin-bottom: 10px; }}
    h1, h2, h3, h4, label, p, span {{ color: {txt} !important; }}
    .stButton>button {{ background-color: #ff7f00 !important; color: white !important; font-weight: bold; border-radius: 8px; height: 3.5em; width: 100%; }}
    .counter-block {{ border-left: 5px solid #ff7f00; padding: 15px; margin: 15px 0; background-color: {bg}; border-radius: 8px; border: 1px solid {brd}; }}
    .lite-label {{ font-size: 0.9em; font-weight: bold; color: #ff7f00 !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. IDENTIFICATION DU SITE ---
st.title("☀️ Diagnostic Expert Opthelios")

col_top1, col_top2 = st.columns([2, 1])
with col_top1:
    nom_site = st.text_input("📍 Nom de l'opération", placeholder="Ex: Résidence du Rail")
    adr_site = st.text_input("🏠 Adresse & GPS", placeholder="Adresse / Coordonnées")
    client_site = st.text_input("👤 Client / MOA", placeholder="Ex: ICF Habitat")
with col_top2:
    photo_main = st.camera_input("📸 Photo de garde", key="main_pic")

# --- 5. FICHE D'IDENTITÉ ALLÉGÉE ---
st.divider()
st.header("📋 Fiche d'Identité Matériel")

def row_mat(label, key):
    c1, c2 = st.columns([3, 1])
    with c1: v = st.text_input(label, key=f"t_{key}")
    with c2: p = st.camera_input("📷", key=f"p_{key}")
    return v, p

with st.expander("🛠️ Caractéristiques Matérielles", expanded=False):
    col_mat1, col_mat2 = st.columns(2)
    with col_mat1:
        st.markdown("**☀️ Production Solaire**")
        row_mat("Marque/Réf Capteurs", "cap")
        st.selectbox("Orientation", ["Sud", "Sud-Est", "Sud-Ouest", "Est", "Ouest"])
        st.number_input("Inclinaison (°)", value=45)
        row_mat("Marque/Réf Circulateur", "circ")
    with col_mat2:
        st.markdown("**📦 Stockage & Appoint**")
        row_mat("Marque/Réf Ballons", "bal")
        st.number_input("Volume total (L)", value=1000, step=100)
        row_mat("Marque/Réf Régulateur", "reg")
        row_mat("Marque/Réf Appoint", "app")

# --- 6. FONCTION DE BLOC COMPTEUR (ESU, ECS, EXTRA) ---
def display_counter_block(label, type_c, key_id):
    st.markdown(f'<p class="lite-label">📊 {label}</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="counter-block">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c1:
            st.radio(f"Présent ?", ["Oui", "Non"], key=f"pres_{key_id}", horizontal=True)
            st.radio(f"Position conforme ?", ["Oui", "Non"], key=f"conf_{key_id}", horizontal=True)
        with c2:
            # Questions spécifiques selon le type
            if type_c in ["ESU", "Calorimètre", "Électrique"]:
                st.text_input("Index actuel (kWh ou MWh)", key=f"idx_{key_id}")
            
            if type_c in ["ESU", "Calorimètre", "Volumétrique", "Vecs"]:
                st.text_input("Valeur volume (m3)", key=f"vol_{key_id}")
            
            if type_c == "Électrique":
                st.text_input("Index Appoint (kWh/MWh)", key=f"idx_app_{key_id}")

            # Points complémentaires (Littérature Métrologie)
            st.checkbox("Sondes en doigts de gant ? (Précision)", key=f"dg_{key_id}")
            st.checkbox("Câblage blindé / Intégrité ?", key=f"cab_{key_id}")
        with c3:
            st.camera_input(f"Photo {label}", key=f"cam_{key_id}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 7. AUDIT TECHNIQUE ---
st.divider()
st.header("🔍 Audit Technique")

sections = {
    "📄 Documentation et conformité électrique": [
        "Schéma d'exécution", "Schéma Electrique", "Analyse Fonctionnelle", 
        "Raccordements", "Mise à la terre", "Signalétique de sécurité", "Livret d'entretien"
    ],
    
    "☀️ Capteurs & Toit": [
        "Intégrité des vitrages (OK / Fissuré / Condensation)",
        "Absorbeur (Normal / Décoloré / Traces de corrosion)",
        "Fixation châssis (Stable / Corrosion / Jeu mécanique)",
        "Étanchéité toiture (Conforme / Défaut / Non vérifiable)",
        "Inclinaison et Orientation (Valeurs numériques en degrés)",
        "Masques solaires (Présence d'ombrage)",
        "Absence de vannes d'isolement (Non conforme)", 
        "Dispositifs d'équilibrage sur chaque champ", 
        "État des systèmes d'équilibrages (Lisibles, manoeuvrables...)",
        "Purgeurs solaires avec vannes d'isolement", 
        "Sondes capteurs : position conforme", 
        "Sondes capteurs : fixation conforme", 
        "Sondes capteurs : jonction électrique conforme", 
        "Sondes capteurs : cable et boitier de jonction en bon état",
        "Traversée de toiture", "Accès sécurisé", "Isolants UV"
    ],
    
    "🧪 Fluide Caloporteur": ["Prélèvement fluide", "pH du fluide", "Protection Antigel (Réfractomètre)", "Analyse visuelle (Coloration)"],
    
    "💧 Circuit primaire solaire": [
        "Sens circulation", "Vannes remplissage", "Dégazeur Aller", "Soupape conforme", "Bidon récupération", 
        "Vase d'Expansion : Pression de gonflage (bar)",
        "Vase d'Expansion : Pression statique du circuit (bar)",
        "Vase d'Expansion : Vérification de la membrane (État : OK / HS)",
        "Disconnecteur"
    ],
    
    "📦 Stockage & Echangeur": ["Echangeur (Entartrage)", "Protection cathodique", "Calorifugeage", "Lyres anti-thermosiphon", "Soupape sécurité"],
    
    "📊 Régulation solaire et métrologie": [
        "Manomètre", "Débitmètre", 
        "Sonde Capteur (T1) : (Valeur cohérente : Oui/Non + Temp lue)", 
        "Sonde Ballon (T2) : (Valeur cohérente : Oui/Non + Temp lue)", 
        "Consigne de température max : (Valeur en °C)",
        "Paramètres de décharge thermique : (Activé / Désactivé)",
        "COMPTEURS" # Marqueur pour insérer les blocs compteurs
    ]
}

for sec, pts in sections.items():
    with st.expander(f"📁 {sec}", expanded=(sec == "📊 Régulation solaire et métrologie")):
        for p in pts:
            if p == "COMPTEURS":
                st.markdown("---")
                # Compteurs fixes
                display_counter_block("Compteur énergie solaire utile (ESU)", "ESU", "esu_fixed")
                display_counter_block("Compteur ECS (Vecs)", "Vecs", "vecs_fixed")
                
                # Gestion des compteurs dynamiques
                st.markdown("#### ➕ Ajouter un compteur spécifique")
                c_add1, c_add2 = st.columns([2, 1])
                with c_add1:
                    new_name = st.text_input("Nom du compteur", placeholder="Ex: Appoint Élec, Bouclage...", key="new_c_name")
                with c_add2:
                    new_type = st.selectbox("Type", ["Calorimètre", "Volumétrique", "Électrique"], key="new_c_type")
                
                if st.button("Ajouter à l'audit"):
                    if new_name:
                        st.session_state.extra_counters.append({"name": new_name, "type": new_type})
                        st.rerun()

                # Affichage des extras
                for i, c in enumerate(st.session_state.extra_counters):
                    st.divider()
                    display_counter_block(c['name'], c['type'], f"extra_{i}")
                    if st.button(f"🗑️ Supprimer {c['name']}", key=f"del_{i}"):
                        st.session_state.extra_counters.pop(i)
                        st.rerun()
            else:
                st.markdown(f"**{p}**")
                c_res, c_obs, c_cam = st.columns([1.5, 3, 1])
                
                # Logique de sélection adaptative
                v_label, options = "Verdict", ["Conforme", "Non Conforme", "N/C", "S/O"]
                if "Sonde" in p:
                    v_label, options = "Cohérent", ["Oui", "Non", "N/C"]
                elif "décharge thermique" in p:
                    v_label, options = "Statut", ["Activé", "Désactivé", "S/O"]
                elif "membrane" in p:
                    v_label, options = "État", ["OK", "HS", "N/C"]

                with c_res:
                    st.selectbox(v_label, options, key=f"s_{p}")
                with c_obs:
                    # Placeholders intelligents
                    ph = "Note / Mesure..."
                    if "gonflage" in p: ph = "Ex: 2.5 bar (mesuré isolé)"
                    if "Sonde" in p: ph = "Ex: 55°C lue"
                    st.text_input("Observation", key=f"o_{p}", placeholder=ph)
                with c_cam:
                    st.camera_input("📷", key=f"c_{p}")

# --- 8. GÉNÉRATION DU RAPPORT ---
st.divider()
col_gen, col_empty = st.columns([1, 2])
with col_gen:
    if st.button("🚀 GÉNÉRER LE RAPPORT FINAL"):
        if not nom_site:
            st.error("Veuillez saisir le nom de l'opération avant de valider.")
        else:
            st.balloons()
            st.success(f"Audit de '{nom_site}' terminé avec succès !")
            st.info("Le moteur PDF intégrera toutes les photos et relevés de compteurs.")