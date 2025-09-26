from openai import OpenAI
import streamlit as st
import PyPDF2

# Configuración de la API
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.set_page_config(page_title="Chatbot de Documentos", page_icon="📄", layout="wide")

st.title("📄 Chatbot de Delivery Orders")
st.write("Sube un documento (PDF) y haz preguntas sobre su contenido.")

# --- Subir documento ---
uploaded_file = st.file_uploader("📤 Sube tu Delivery Order (PDF)", type=["pdf"])

document_text = ""

if uploaded_file is not None:
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        document_text += page.extract_text()

    st.success("✅ Documento cargado correctamente.")
    st.text_area("Texto extraído del documento:", document_text[:1000] + "..." if len(document_text) > 1000 else document_text, height=200)

# --- Chat ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "Eres un asistente que responde preguntas sobre el documento cargado."}
    ]

# Mostrar historial de chat
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# Entrada del usuario
if prompt := st.chat_input("Haz una pregunta sobre el documento..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Crear contexto
    context_prompt = f"""
    Aquí está el contenido del documento:

    {document_text}

    Ahora responde la siguiente pregunta del usuario de forma concisa y clara:
    {prompt}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un experto en logística y análisis de delivery orders."},
            {"role": "user", "content": context_prompt}
        ],
        max_tokens=500,
        temperature=0.3,
    )

    reply = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)





