import streamlit as st
import uuid
from src.ai_engine import get_fabric_recommendation
from src.pdf_generator import export_to_pdf

from streamlit_echarts import st_echarts

def parse_metrics(text):
    if "METRIC_DATA:" in text:
        try:
            p = text.split("METRIC_DATA:")[1].split("|")
            return {
                "GSM": p[0].split(":")[1],
                "DUR": int(p[1].split(":")[1]),
                "BRE": int(p[2].split(":")[1]),
                "SUS": int(p[3].split(":")[1]),
                "Price": p[4].split(":")[1],
                "COST": int(p[5].split(":")[1])
            }
        except: return None
    return None

def render_performance_radar(m):
    options = {
        "radar": {"indicator": [
            {"name": "Durability", "max": 100}, {"name": "Breathability", "max": 100},
            {"name": "Sustainability", "max": 100}, {"name": "Cost Efficiency", "max": 100}
        ]},
        "series": [{"type": "radar", "data": [{"value": [m["DUR"], m["BRE"], m["SUS"], m["COST"]], 
                    "areaStyle": {"color": "#2E4053", "opacity": 0.4}}]}]
    }
    st_echarts(options, height="300px")

def render_ui_components(content):
    metrics = parse_metrics(content)
    if metrics:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.metric("Target Weight", metrics["GSM"])
            st.metric("Market Tier", metrics["Price"])
            st.metric("Eco-Score", f"{metrics['SUS']}/100")
        with col2:
            render_performance_radar(metrics)
        
        # Styled Care Label
        st.markdown(f"""
        <div style="border: 2px dashed #2E4053; padding: 15px; border-radius: 10px; background-color: #F4F6F7; margin: 10px 0;">
            <p style="margin:0; font-weight:bold; color:#2E4053;">🧵 PRODUCTION CARE SPEC:</p>
            <p style="margin:5px 0; font-size: 0.9em;">Standard Industrial Grade | Heat Resistance: { "High" if "Denim" in content or "Cotton" in content else "Low" } | Bio-degradable: Yes</p>
        </div>
        """, unsafe_allow_html=True)

        # Buyer Insights Section
        render_buyer_insights(content)

def render_buyer_insights(content):
    with st.expander("🇮🇳 Indian Market & Buyer Match", expanded=True):
        col1, col2 = st.columns(2)
        
        # Simple extraction logic for UI highlighting
        hub = "Not Specified"
        if "Hub:" in content: hub = content.split("Hub:")[1].split("\n")[0]
        elif "HUB:" in content: hub = content.split("HUB:")[1].split("\n")[0]
        
        with col1:
            st.markdown("#### 🏢 Targeted Buyer Segments")
            if "Export" in content: st.info("🎯 **Primary:** International Export Houses")
            if "Retail" in content or "Domestic" in content: st.info("🛍️ **Primary:** Domestic Retail Chains (Westside/Reliance)")
            if "Boutique" in content: st.info("👗 **Primary:** Premium Designer Boutiques")
            
        with col2:
            st.markdown("#### 📍 Sourcing/Production Hub")
            st.success(f"**Recommended Location:** {hub}")
            st.caption("Strategic hub based on material availability and labor expertise.")

st.set_page_config(page_title="Fabric Intel AI", page_icon="🧵", layout="wide")

# Session State
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = str(uuid.uuid4())
    st.session_state.conversations[st.session_state.current_chat_id] = []

# Sidebar
with st.sidebar:
    st.title("🧵 Fabric Intel")
    if st.button("➕ New Analysis", use_container_width=True):
        st.session_state.current_chat_id = str(uuid.uuid4())
        st.session_state.conversations[st.session_state.current_chat_id] = []
        st.rerun()
    
    st.divider()
    st.subheader("History")
    for cid in reversed(list(st.session_state.conversations.keys())):
        history = st.session_state.conversations[cid]
        label = history[0]["content"][:20] + "..." if history else "Empty Chat"
        if st.button(label, key=cid, use_container_width=True):
            st.session_state.current_chat_id = cid
            st.rerun()

# Main Chat Interface
st.title("Fabric-to-Garment Advisor")
st.caption("Detailed Technical Recommendations | Powered by Llama 3.3 & Groq")

current_history = st.session_state.conversations[st.session_state.current_chat_id]

# Starter Prompts
if not current_history:
    st.write("### Choose a starting point:")
    cols = st.columns(2)
    starters = [
        "Premium Linen set for South Asian Summer",
        "High-performance Winter Sportswear",
        "Sustainable Silk Blouse for Luxury Market",
        "Durable Denim Workwear Jacket"
    ]
    for i, s in enumerate(starters):
        if cols[i%2].button(s, use_container_width=True):
            prompt = s
            current_history.append({"role": "user", "content": prompt})
            with st.spinner("Analyzing..."):
                res = get_fabric_recommendation(current_history)
                current_history.append({"role": "assistant", "content": res})
            st.rerun()

for i, msg in enumerate(current_history):
    with st.chat_message(msg["role"]):
        # Clean text for display (remove the raw metric tag)
        display_text = msg["content"].split("METRIC_DATA:")[0]
        st.markdown(display_text)
        
        if msg["role"] == "assistant":
            render_ui_components(msg["content"]) # Added Dashboard/Label
            # Parse metrics again for the PDF generator
            m_obj = parse_metrics(msg["content"])
            pdf_data = export_to_pdf(display_text, metrics=m_obj)
            st.download_button(
                "📥 Download Tech-Spec PDF", 
                data=pdf_data, 
                file_name=f"TechSpec_{i}.pdf", 
                mime="application/pdf",
                key=f"btn_{st.session_state.current_chat_id}_{i}"
            )

# Chat Input
if user_input := st.chat_input("Describe the garment, market, and season..."):
    current_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Consulting Textile Intelligence Stack..."):
            response = get_fabric_recommendation(current_history)
            clean_display = response.split("METRIC_DATA:")[0]
            st.markdown(clean_display)
            render_ui_components(response) # Added Dashboard/Label
            m_obj = parse_metrics(response)
            pdf_data = export_to_pdf(clean_display, metrics=m_obj)
            st.download_button("📥 Download Tech-Spec PDF", data=pdf_data, file_name="Report.pdf", mime="application/pdf")
    
    current_history.append({"role": "assistant", "content": response})
    st.session_state.conversations[st.session_state.current_chat_id] = current_history