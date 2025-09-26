import streamlit as st
from openai import OpenAI

# Configuración de la API desde secrets
api_key = st.secrets["openai"]["api_key"]
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Chatbot Delivery Orders", page_icon="📦")
st.title("Chatbot Delivery Orders 📦")

# Descripción
st.markdown("Haz preguntas sobre tus documentos de delivery orders (ej: cliente, contenedor, peso).")

# Guardar historial en session_state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "Eres un asistente que responde preguntas sobre delivery orders, limitate a responder por la info que te preguntan y en lo posible hazlo de forma listada, si una info no esta, comentalo, sy te preguntan algo aparte del doc, responde pero menciona que no esta en el doc o que no lo ves."}
    ]

# Mostrar historial en pantalla
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

# Entrada de usuario (chat estilo moderno de Streamlit)
if prompt := st.chat_input("Escribe tu pregunta..."):
    # Agregar mensaje del usuario
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Llamar a OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state["messages"]
    )

    # Obtener respuesta del asistente
    answer = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": answer})

    # Mostrar respuesta
    st.chat_message("assistant").write(answer)