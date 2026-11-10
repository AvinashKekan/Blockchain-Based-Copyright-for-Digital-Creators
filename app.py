import streamlit as st
import pandas as pd
from datetime import datetime
from blockchain import Blockchain

# --- PAGE CONFIG ---
st.set_page_config(page_title="IP-Guard | Nayan Kshirsagar", layout="wide")

# --- UI STYLING (THEME AWARE) ---
st.markdown("""
    <style>
    /* 1. Remove Top White Space from Inputs */
    div[data-testid="stWidgetLabel"] { display: none; }
    
    /* 2. Theme-Aware Footer (Natural Flow) */
    .footer {
        width: 100%;
        text-align: center;
        padding: 20px;
        margin-top: 50px;
        border-top: 1px solid var(--secondary-background-color);
        color: var(--text-color);
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    /* 3. Button Styling (Burgundy - High Contrast) */
    div.stButton > button {
        background-color: #880e4f !important;
        color: white !important;
        border-radius: 8px;
        font-weight: 600;
        height: 3em;
        width: 100%;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* 4. Navigation Pills Styling */
    div[role="radiogroup"] {
        background-color: var(--secondary-background-color);
        padding: 8px;
        border-radius: 10px;
        border: 1px solid var(--background-color);
    }
    
    /* 5. Typography Polish */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE STATE ---
if 'ip_ledger' not in st.session_state:
    st.session_state.ip_ledger = Blockchain()

# --- HEADER ---
st.title("⚖️ Blockchain-Based Copyright for Digital Creators")
st.write("Secure Proof of Existence for Intellectual Property.")

# Spacer
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# --- NAVIGATION ---
view = st.pills("Menu", ["Register Asset", "Public Gallery", "Security Audit"], selection_mode="single", default="Register Asset", label_visibility="collapsed")

st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# --- VIEW 1: REGISTER ASSET ---
if view == "Register Asset":
    st.subheader("Timestamp Your Work")
    
    with st.container(border=True):
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Asset Title**")
            title = st.text_input("Title", placeholder="e.g. Research Paper V1", label_visibility="collapsed")
            
            st.markdown("**Creator Name**")
            creator = st.text_input("Creator", value="Nayan Kshirsagar", label_visibility="collapsed") 
        
        with c2:
            st.markdown("**Category**")
            # UPDATED: Added more options here
            category_options = [
                "UI/UX Design", 
                "Research Paper", 
                "Source Code", 
                "Digital Art / Illustration",
                "Photography",
                "Music / Audio Track",
                "Video Production",
                "3D Model / Asset",
                "Brand Identity / Logo",
                "E-Book / Article"
            ]
            category = st.selectbox("Type", category_options, label_visibility="collapsed")
            
            st.markdown("**Timestamp**")
            st.info(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        st.markdown("**Description**")
        desc = st.text_area("Description", placeholder="Brief description of the unique aspects of this work...", label_visibility="collapsed")

        st.write("") # Spacer
        
        if st.button("Generate Proof of Existence"):
            if title and desc:
                data = {
                    "Title": title,
                    "Creator": creator,
                    "Type": category,
                    "Desc": desc
                }
                st.session_state.ip_ledger.add_new_block(data)
                st.success(f"✅ Success! Blockchain Certificate generated for '{title}'")
            else:
                st.warning("⚠️ Title and Description are required.")

# --- VIEW 2: PUBLIC GALLERY ---
elif view == "Public Gallery":
    st.subheader("Verified Asset Repository")
    
    if len(st.session_state.ip_ledger.chain) < 2:
        st.info("No assets registered yet.")
    else:
        cols = st.columns(3)
        for idx, block in enumerate(st.session_state.ip_ledger.chain[1:]):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"<h4 style='color:#e91e63; margin:0;'>{block.data['Title']}</h4>", unsafe_allow_html=True)
                    st.caption(f"{block.data['Type']}")
                    st.markdown(f"**Owner:** {block.data['Creator']}")
                    st.divider()
                    st.code(f"Hash: {block.hash[:15]}...", language="text")

# --- VIEW 3: SECURITY AUDIT ---
elif view == "Security Audit":
    st.subheader("System Integrity & Data")
    
    with st.container(border=True):
        st.write("### 🔍 Blockchain Integrity Check")
        if st.button("Run Integrity Audit"):
            if st.session_state.ip_ledger.verify_chain():
                st.success("✅ System Verified: Secure")
            else:
                st.error("🚨 SECURITY ALERT: Tampering Detected")

    st.subheader("📜 Raw Ledger Data")
    chain_data = []
    for block in st.session_state.ip_ledger.chain:
        chain_data.append({
            "Index": block.index,
            "Timestamp": block.timestamp,
            "Title": block.data if isinstance(block.data, str) else block.data.get("Title", "Genesis"),
            "Current Hash": block.hash
        })
    st.dataframe(pd.DataFrame(chain_data), use_container_width=True, hide_index=True)

# --- FOOTER ---
st.markdown("""
    <div class="footer">
        Developed by <strong>Nayan Kshirsagar</strong> | MSc IT Project | 2025-2026
    </div>
""", unsafe_allow_html=True)