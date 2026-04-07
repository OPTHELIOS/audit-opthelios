import streamlit as st
import os

# --- 1. CONFIGURATION & STATE ---
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
st.markdown("""
    <style>
    .counter-block { border-left: 4px solid #ff7f00; padding: 15px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
    .stButton>button { background-color: #ff7f00 !important; color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. EN-TÊTE ---
st.title("☀️ Diagnostic Expert Opthelios")
nom_site = st.text_input("📍 Nom de l'opération", placeholder="Ex: Résidence du Rail")

# --- 5. SECTIONS PRÉCÉDENTES (Résumé pour le code) ---
# [Ici se trouvent les sections Documentation, Capteurs, Fluide, Primaire, Stockage...]

# --- 6. RÉGULATION ET MÉTROLOGIE ---
st.divider()
st.header("📊 Régulation solaire et métrologie")

# Points standards
std_pts = ["Manomètre", "Débitmètre", "Sonde Capteur (T1)", "Sonde Ballon (T2)", "Consigne température max", "Décharge thermique"]
for p in std_pts:
    c1, c2, c3 = st.columns([1.5, 3, 1])
    with c1: st.selectbox(f"Verdict ({p})", ["OK", "Non Conforme", "N/C"], key=f"s_{p}")
    with c2: st.text_input(f"Note ({p})", key=f"o_{p}")
    with c3: st.camera_input("📷", key=f"c_{p}")

st.markdown("---")
st.subheader("🔢 Relevés de Compteurs")

# Fonction générique pour afficher un bloc compteur
def display_counter_block(label, type_c, key_id):
    st.markdown(f"**{label} ({type_c})**")
    with st.container():
        st.markdown('<div class="counter-block">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c1:
            st.radio("Présent ?", ["Oui", "Non"], key=f"pres_{key_id}", horizontal=True)
            st.radio("Conforme ?", ["Oui", "Non"], key=f"conf_{key_id}", horizontal=True)
        with c2:
            # Logique de questions selon le type
            if type_c in ["ESU", "Calorimètre", "Électrique"]:
                st.text_input("Index (kWh ou MWh)", key=f"idx_{key_id}")
            if type_c in ["ESU", "Calorimètre", "Volumétrique", "Vecs"]:
                st.text_input("Volume (m3)", key=f"vol_{key_id}")
            
            # Points complémentaires issus de la littérature (ADEME/SOCOL)
            st.checkbox("Sondes en doigts de gant ? (Précision)", key=f"dg_{key_id}")
            st.checkbox("Câblage blindé / Intégrité ?", key=f"cab_{key_id}")
        with c3:
            st.camera_input(f"Photo {label}", key=f"cam_{key_id}")
        st.markdown('</div>', unsafe_allow_html=True)

# 1. Affichage des compteurs fixes
display_counter_block("Compteur ESU", "ESU", "fixed_esu")
display_counter_block("Compteur ECS", "Vecs", "fixed_vecs")

# 2. Gestion des compteurs additionnels
st.markdown("#### ➕ Ajouter un compteur spécifique")
col_add1, col_add2 = st.columns([2, 1])
with col_add1:
    new_name = st.text_input("Nom du compteur", placeholder="Ex: Compteur Bouclage")
with col_add2:
    new_type = st.selectbox("Type", ["Calorimètre", "Volumétrique", "Électrique"])

if st.button("Ajouter le compteur à l'audit"):
    if new_name:
        st.session_state.extra_counters.append({"name": new_name, "type": new_type})
        st.rerun()

# 3. Affichage des compteurs ajoutés dynamiquement
for i, c in enumerate(st.session_state.extra_counters):
    st.divider()
    display_counter_block(c['name'], c['type'], f"extra_{i}")
    if st.button(f"🗑️ Supprimer {c['name']}", key=f"del_{i}"):
        st.session_state.extra_counters.pop(i)
        st.rerun()

# --- 7. FIN ---
st.divider()
if st.button("🚀 VALIDER L'AUDIT"):
    st.success("Données enregistrées.")