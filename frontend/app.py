import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Knowledge Repository", layout="wide")
st.title("📚 Knowledge Repository")

menu = ["Search Documents", "Upload Document", "Manage Tags"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Search Documents":
    st.header("Search Documents")
    search_query = st.text_input("Search by title or description")
    
    if st.button("Search"):
        params = {"search": search_query} if search_query else {}
        response = requests.get(f"{API_URL}/documents/", params=params)
        
        if response.status_code == 200:
            docs = response.json()
            if not docs:
                st.info("No documents found.")
            for doc in docs:
                with st.expander(f"{doc['title']} (ID: {doc['id']})"):
                    st.write(f"**Description:** {doc['description']}")
                    tags = ", ".join([t['name'] for t in doc['tags']])
                    st.write(f"**Tags:** {tags if tags else 'None'}")
                    st.write(f"**Versions:** {len(doc['versions'])}")
                    for v in doc['versions']:
                        st.write(f"- Version {v['version_number']}: {v['filename']}")
        else:
            st.error("Failed to fetch documents")

elif choice == "Upload Document":
    st.header("Upload a New Document or Version")
    
    upload_type = st.radio("What would you like to do?", ("Create New Document", "Add Version to Existing Document"))
    
    if upload_type == "Create New Document":
        title = st.text_input("Document Title")
        desc = st.text_area("Description")
        uploaded_file = st.file_uploader("Choose a file")
        
        if st.button("Create & Upload"):
            if title and uploaded_file:
                # 1. Create Document
                doc_data = {"title": title, "description": desc}
                doc_res = requests.post(f"{API_URL}/documents/", json=doc_data)
                
                if doc_res.status_code == 200:
                    doc_id = doc_res.json()['id']
                    
                    # 2. Upload File
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    upload_res = requests.post(f"{API_URL}/documents/{doc_id}/upload/", files=files)
                    
                    if upload_res.status_code == 200:
                        st.success("Document created and file uploaded successfully!")
                    else:
                        st.error("Document created, but file upload failed.")
                else:
                    st.error("Failed to create document.")
            else:
                st.warning("Please provide a title and select a file.")

    else:
        doc_id = st.number_input("Document ID", min_value=1, step=1)
        uploaded_file = st.file_uploader("Choose a file for the new version")
        
        if st.button("Upload New Version"):
            if uploaded_file:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                upload_res = requests.post(f"{API_URL}/documents/{doc_id}/upload/", files=files)
                if upload_res.status_code == 200:
                    st.success(f"New version uploaded successfully! Version: {upload_res.json().get('version')}")
                else:
                    st.error("Failed to upload version. Please check the Document ID.")
            else:
                st.warning("Please select a file.")

elif choice == "Manage Tags":
    st.header("Manage Document Tags")
    
    doc_id = st.number_input("Document ID to Tag", min_value=1, step=1)
    tag_name = st.text_input("Tag Name")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Tag"):
            if tag_name:
                res = requests.post(f"{API_URL}/documents/{doc_id}/tags/", params={"tag_name": tag_name})
                if res.status_code == 200:
                    st.success(f"Tag '{tag_name}' added to Document {doc_id}")
                else:
                    st.error("Failed to add tag.")
            else:
                st.warning("Please enter a tag name.")
                
    with col2:
        if st.button("Remove Tag"):
            if tag_name:
                res = requests.delete(f"{API_URL}/documents/{doc_id}/tags/{tag_name}")
                if res.status_code == 200:
                    st.success(f"Tag '{tag_name}' removed from Document {doc_id}")
                else:
                    st.error("Failed to remove tag.")
            else:
                st.warning("Please enter a tag name.")
