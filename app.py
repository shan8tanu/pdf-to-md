import streamlit as st
import os
import pandas as pd
from pathlib import Path
from core.processor import convert_pdf_to_md, inspect_tables
import fitz

# --- Page Config ---
st.set_page_config(layout="wide", page_title="PDF-to-Context Bridge")

# --- Header ---
st.title("📄 PDF-to-Context Bridge")
st.caption("Phase 4: Context Injection & Final Polish")

# --- Sidebar ---
# Defined at top, but will be updated on rerun
with st.sidebar:
    st.header("Control Panel")
    st.info(
        "1. Upload PDF.\n"
        "2. Click 'Convert'.\n"
        "3. Download Result."
    )
    
    # Download Button Logic
    # This checks session_state. If present, button renders.
    if 'markdown_result' in st.session_state:
        st.divider()
        st.success("Ready for Download")
        st.download_button(
            label="Download .md File",
            data=st.session_state['markdown_result'],
            file_name="converted_output.md",
            mime="text/markdown",
            type="primary"
        )
        if st.button("Reset / Clear"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# --- Helper: Render PDF Page ---
def render_pdf_page(pdf_path, page_num):
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        img_bytes = pix.tobytes("png")
        doc.close()
        return img_bytes
    except Exception as e:
        return None

# --- Main Interface ---
uploaded_file = st.file_uploader("Upload your PDF Document", type=['pdf'])

if uploaded_file:
    # Setup Temp Path
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    file_path = temp_dir / uploaded_file.name
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # --- Action Bar ---
    convert_btn = st.button("Convert to Markdown", type="primary")
    
    # --- Logic ---
    if convert_btn:
        with st.spinner("Processing Phases 1-4..."):
            try:
                # 1. Main Conversion (Phase 1, 2, 4)
                markdown_result = convert_pdf_to_md(str(file_path))
                st.session_state['markdown_result'] = markdown_result
                st.session_state['current_file_path'] = str(file_path)
                
                # 2. Table Inspection (Phase 3)
                detected_tables = inspect_tables(str(file_path))
                st.session_state['detected_tables'] = detected_tables
                
                st.toast("Processing Complete!", icon="✅")
                
                # FORCE RERUN to update Sidebar immediately
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {e}")

    # --- Results View ---
    if 'markdown_result' in st.session_state:
        st.divider()
        
        tab_main, tab_tables, tab_visual = st.tabs(["📝 Markdown Output", "📊 Phase 3: Table Debugger", "👁‍🗨 Split View"])
        
        # TAB 1: Main Output
        with tab_main:
            st.subheader("Final Context for LLM")
            st.text_area("Content", st.session_state['markdown_result'], height=600)

        # TAB 2: Table Debugger (Phase 3)
        with tab_tables:
            st.subheader("Detected Tables (Lattice Mode)")
            tables = st.session_state.get('detected_tables', [])
            
            if not tables:
                st.info("No explicit grid tables detected.")
            else:
                st.success(f"Detected {len(tables)} tables.")
                for t in tables:
                    with st.expander(f"Page {t['page']} - Table {t['index']}"):
                        try:
                            df = pd.DataFrame(t['content'])
                            st.dataframe(df, use_container_width=True)
                        except:
                            st.write(t['content'])

        # TAB 3: Visual Split (Phase 2)
        with tab_visual:
            try:
                doc_check = fitz.open(st.session_state['current_file_path'])
                total_pages = doc_check.page_count
                doc_check.close()
                
                c_left, c_right = st.columns([0.5, 0.5])
                
                with c_left:
                    st.info("PDF Source")
                    if "page_view_num" not in st.session_state: st.session_state.page_view_num = 0
                    
                    c1, c2, c3 = st.columns([1,2,1])
                    if c1.button("◀"): st.session_state.page_view_num = max(0, st.session_state.page_view_num - 1)
                    c2.write(f"Page {st.session_state.page_view_num + 1}")
                    if c3.button("▶"): st.session_state.page_view_num = min(total_pages - 1, st.session_state.page_view_num + 1)
                    
                    img = render_pdf_page(st.session_state['current_file_path'], st.session_state.page_view_num)
                    if img: st.image(img, use_container_width=True)

                with c_right:
                    st.info("Markdown Output")
                    st.markdown(st.session_state['markdown_result'])
            except Exception as e:
                st.warning(f"Could not render split view (File might be moved): {e}")
