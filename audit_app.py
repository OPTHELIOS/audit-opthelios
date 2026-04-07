import streamlit as st
import os

# --- 1. CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="Opthelios Expert v3", layout="wide", page_icon="☀️")

if 'extra_counters' not in st.session_state:
    st.session_state.extra_counters = []

# --- 2. GESTION DU THÈME ---
with st.sidebar:
    st.header("🎨 Interface")
    theme = st.radio("Mode", ["☀️ Clair", "🌙 Sombre"], horizontal=True)
    sidebar_bg = "#001f3f" if theme == "☀️ Clair" else "#000000"
    st.markdown(f"<style>[data-testid='stSidebar'] {{ background-color: {sidebar_bg} !important; }}</style>", unsafe_allow_html=True)

# --- 3. CSS & STYLES ---
st.markdown(f"""
    <style>
    .counter-block {{ border-left: 5px solid #ff7f00; padding: 15px; margin: 15px 0; border: 1px solid #ddd; border-radius: 8px; }}
    .stButton>button {{ background-color: #ff7f00 !important; color: white !important; font-weight: bold; border-radius: 8px; }}
    .ballon-card {{ background-color: rgba(255, 127, 0, 0.05); padding: 15px; border-radius: 10px; border: 1px dashed #ff7f00; margin-bottom: 10px; }}
    .section-header {{ color: #ff7f00; font-size: 1.2em; font-weight: bold; margin-top: 20px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. EN-TÊTE ---
st.title("☀️ Diagnostic Expert Opthelios")
col_info1, col_info2 = st.columns([2, 1])
with col_info1:
    nom_site = st.text_input("📍 Nom de l'opération", placeholder="Ex: Résidence du Rail")
    adr_site = st.text_input("🏠 Adresse & GPS")
    client_site = st.text_input("👤 Client / MOA")
with col_info2:
    photo_main = st.camera_input("📸 Photo de garde", key="main_pic")

# --- 5. FICHE D'IDENTITÉ MATÉRIEL ---
st.divider()
st.header("📋 Fiche d'Identité Matériel")

with st.expander("🛠️ Caractéristiques & Stockage", expanded=True):
    # --- PARTIE PRODUCTION ---
    st.markdown('<p class="section-header">☀️ Production Solaire</p>', unsafe_allow_html=True)
    c_p1, c_p2 = st.columns(2)
    with c_p1:
        st.text_input("Marque/Réf Capteurs", key="m_cap")
        st.selectbox("Orientation", ["Sud", "Sud-Est", "Sud-Ouest", "Est", "Ouest"])
    with c_p2:
        st.number_input("Inclinaison (°)", value=45)
        st.text_input("Marque/Réf Circulateur", key="m_circ")

    # --- PARTIE STOCKAGE DYNAMIQUE ---
    st.markdown('<p class="section-header">📦 Stockage Solaire</p>', unsafe_allow_html=True)
    nb_ballons = st.number_input("Nombre de ballons solaires", min_value=1, value=1, step=1)
    
    # Raccordement hydraulique (si plus de 1 ballon)
    if nb_ballons >= 2:
        st.info("Configuration multi-ballons détectée")
        st.selectbox("Raccordement hydraulique des ballons solaires", ["En série", "En parallèle"], key="raccord_hydra")

    # Boucle pour chaque ballon
    for i in range(int(nb_ballons)):
        st.markdown(f'<div class="ballon-card">', unsafe_allow_html=True)
        st.markdown(f"**Ballon n°{i+1}**")
        cb1, cb2, cb3 = st.columns([2, 1, 1])
        with cb1:
            st.text_input(f"Marque / Référence", key=f"m_bal_{i}")
        with cb2:
            st.text_input(f"Volume (L)", key=f"v_bal_{i}")
            st.selectbox(f"Typologie", ["Sanitaire (ECS)", "Eau technique (Tampon)"], key=f"t_bal_{i}")
        with cb3:
            st.number_input(f"Nombre d'échangeur(s)", min_value=0, max_value=3, value=1, key=f"e_bal_{i}")
            st.selectbox(f"État visuel", ["Correct", "Non conforme", "HS"], key=f"et_bal_{i}")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- PARTIE DISTRIBUTION ---
    st.markdown('<p class="section-header">🚿 Distribution Sanitaire</p>', unsafe_allow_html=True)
    cd1, cd2, cd3 = st.columns([1.5, 1, 1.5])
    with cd1:
        dist_type = st.selectbox("Type de distribution", ["Bouclage sanitaire", "Traceur électrique", "Non présent"], key="dist_type")
        dist_conf = st.radio("Conformité distribution", ["Conforme", "Non conforme"], horizontal=True, key="dist_conf")
    with cd2:
        dist_photo = st.camera_input("Photo Distribution", key="dist_photo")
    with cd3:
        dist_obs = st.text_area("Commentaires distribution", placeholder="Remarques sur le calorifuge, la pompe de bouclage...", key="dist_obs")

# --- 6. AUDIT TECHNIQUE ---
st.divider()
st.header("🔍 Audit Technique")

sections = {
    "📄 Documentation & Élec": ["Schéma d'exécution", "Schéma Electrique", "Mise à la terre", "Signalétique"],
    "☀️ Capteurs & Toit": ["Vitrages", "Absorbeur", "Fixation", "Étanchéité", "Inclinaison/Orient", "Masques", "Équilibrage", "Isolants UV"],
    "🧪 Fluide Caloporteur": ["pH", "Protection Antigel", "Analyse visuelle"],
    "💧 Circuit primaire": ["Sens circulation", "Dégazeur", "Vase : Pression gonflage", "Vase : Pression statique", "Vase : Membrane", "Soupape"],
    "📊 Régulation & Métrologie": ["Sonde T1", "Sonde T2", "Consigne Max", "Décharge thermique", "COMPTEURS"]
}

# Fonction pour les compteurs
def display_counter_block(label, type_c, key_id):
    st.markdown(f"**{label}**")
    with st.container():
        st.markdown('<div class="counter-block">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c1:
            st.radio("Présent ?", ["Oui", "Non"], key=f"pres_{key_id}", horizontal=True)
            st.radio("Conforme ?", ["Oui", "Non"], key=f"conf_{key_id}", horizontal=True)
        with c2:
            if type_c in ["ESU", "Calorimètre", "Électrique"]:
                st.text_input("Index (kWh ou MWh)", key=f"idx_{key_id}")
            if type_c in ["ESU", "Calorimètre", "Volumétrique", "Vecs"]:
                st.text_input("Volume (m3)", key=f"vol_{key_id}")
            st.checkbox("Sondes en doigts de gant ?", key=f"dg_{key_id}")
        with c3:
            st.camera_input("📷", key=f"cam_{key_id}")
        st.markdown('</div>', unsafe_allow_html=True)

for sec, pts in sections.items():
    with st.expander(f"📁 {sec}"):
        for p in pts:
            if p == "COMPTEURS":
                display_counter_block("Compteur ESU", "ESU", "fixed_esu")
                display_counter_block("Compteur ECS (Vecs)", "Vecs", "fixed_vecs")
                # Gestion dynamique des compteurs supplémentaires
                st.markdown("#### ➕ Ajouter un compteur")
                ca1, ca2 = st.columns(2)
                new_n = ca1.text_input("Nom", key="new_n")
                new_t = ca2.selectbox("Type", ["Calorimètre", "Volumétrique", "Électrique"], key="new_t")
                if st.button("Ajouter"):
                    if new_n:
                        st.session_state.extra_counters.append({"name": new_n, "type": new_t})
                        st.rerun()
                for i, c in enumerate(st.session_state.extra_counters):
                    display_counter_block(c['name'], c['type'], f"extra_{i}")
            else:
                c1, c2, c3 = st.columns([1.5, 3, 1])
                with c1: st.selectbox(f"Verdict ({p})", ["Conforme", "Non Conforme", "N/C", "S/O"], key=f"s_{p}")
                with c2: st.text_input(f"Note ({p})", key=f"o_{p}")
                with c3: st.camera_input("📷", key=f"c_{p}")

# --- 7. GÉNÉRATION ---
st.divider()
if st.button("🚀 GÉNÉRER LE RAPPORT FINAL"):
    if not nom_site:
        st.error("Nom de l'opération manquant.")
    else:
        st.balloons()
        st.success(f"Audit de {nom_site} validé avec succès.")