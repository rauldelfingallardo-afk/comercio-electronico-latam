# modelo_embeddings = GoogleGenerativeAIEmbeddings(
    #model="models/gemini-embedding-001",
    #google_api_key=GEMINI_API_KEY
# )
# NO ESTÁ ACTIVA // CAMBIANDO A LA API_KEY DE GROQ

from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(chunks, modelo_embeddings)

retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.3, "k": 4}
)

!pip install -q langchain langchain-core

!pip install -q langchain-classic

from langchain_classic.chains.combine_documents import create_stuff_documents_chain
prompt_rag = ChatPromptTemplate(
    [
        ("system",
         """
         Eres el especialista principal de Soporte Técnico y Experiencia del Cliente para nuestro E-commerce.
         Tu objetivo es brindar respuestas claras, amables, empáticas y altamente resolutivas, priorizando siempre la satisfacción del cliente.

         REGLAS DE OPERACIÓN SEVERAS:
         1. Confía ÚNICAMENTE en la información proporcionada en el 'Contexto' para responder la pregunta.
         2. Si el 'Contexto' no contiene la información necesaria para responder de forma precisa, di exactamente: "Lo siento, en este momento no tengo esa información disponible. Por favor, aguarda un momento y te comunicaré con un agente humano para ayudarte."
         3. No inventes políticas, precios, plazos de envío ni condiciones que no estén explícitamente escritos en el contexto.
         4. Mantén un tono profesional pero cercano (trata al cliente de "tú" o "usted" según la identidad de tu marca, idealmente "tú" de forma respetuosa).
         """),
        ("human", "Contexto de soporte de la empresa:\n{context}\n\nConsulta o reclamo del cliente:\n{input}")
    ]
)

document_chain = create_stuff_documents_chain(llm, prompt_rag)

def busqueda_de_respuestas_RAG(pregunta) -> Dict:
  documentos_relacionados = retriever.invoke(pregunta)

  if not documentos_relacionados:
    return {
        "respuesta": "No lo sé.",
        "citaciones": [],
        "documentos_encontrados": False
        }

  answer = document_chain.invoke({
      "input": pregunta,
      "context": documentos_relacionados
  })

  if answer.rstrip(".!?") == 'No lo sé':
    return {
        "respuesta": "No lo sé.",
        "citaciones": [],
        "documentos_encontrados": False
        }

  return {
        "respuesta": answer,
        "citaciones": documentos_relacionados,
        "documentos_encontrados": True
        }

r = busqueda_de_respuestas_RAG("Hola, mi producto de BimBam Buy dejó de funcionar de la nada y quiero usar la garantía de fábrica ¿Que debo hacer?")
print(r)

len(r["citaciones"])

mensajes_de_prueba = [
	"Acabo de recibir mi paquete hace dos horas, viene todo aplastado por el correo y el producto adentro está roto. ¿que hago?",
	"El teléfono se me cayó al suelo por accidente, se rompió la pantalla y no prende. ¿Me lo cubre la garantía?",
	"Hice una compra hace una semana para una dirección en zona urbana y el paquete todavía no me llegó, ¿dónde está?",
	"Me equivoqué al escribir la dirección de mi pedido, puse Calle México 123 y era 1234, ¡ayuda antes de que lo envíen!",
	"Hola, mi producto de BimBam Buy dejó de funcionar de la nada y quiero usar la garantía de fábrica.",
	"Compré una campera hace 5 días, pero me arrepentí, está sin usar y quiero que me devuelvan el dinero.",
	"me llego el paquete, pero me mandaron unas zapatillas negras en vez de las rojas que compré.",
	"El banco me cobró la compra en la tarjeta, pero no me llegó ningún correo de confirmación ni número de orden.",
	"Ya me aprobaron la devolución del dinero, ¿cuánto tiempo tarda en verse reflejado el reembolso?",
	"Hola, envié mi postulación para el programa de afiliados hace unos días y quería saber si ya me aprobaron la cuenta.",
	"¿Qué pasa con mi comisión si un usuario compró con mi enlace de afiliado, pero luego devolvió el producto?",
	"¿Quién es Zinedin Zidane?"
]

for pregunta in mensajes_de_prueba:
  respuesta_RAG = busqueda_de_respuestas_RAG(pregunta)
  print(f"PREGUNTA: {pregunta}")
  print(f"RESPUESTA: {respuesta_RAG['respuesta']}")
  if respuesta_RAG['documentos_encontrados']:
    for i, citacion in enumerate(respuesta_RAG['citaciones']):
      print(f"    - CITACIÓN {i + 1}:")
      print(f"      Camino del documento: {citacion.metadata['file_path']}")
      print(f"      Contenido: {citacion.page_content.replace('\n', '')}")
  print("----------------------------------------------------------------")

"""# Agente con LangGraph"""

!pip install -q langgraph

from typing import TypedDict, Optional

class AgentState(TypedDict, total = False):
  pregunta: str
  triaje: dict
  respuesta: Optional[str]
  citaciones: Optional[list]
  rag_exito: bool
  accion_final: str

def nodo_triaje(state: AgentState) -> AgentState:
  print("Ejecutando nodo 'triaje'...")
  return {"triaje": triaje(state["pregunta"])}

def nodo_auto_resolver(state: AgentState) -> AgentState:
  print("Ejecutando nodo 'auto_resolver'...")
  respuesta_RAG = busqueda_de_respuestas_RAG(state["pregunta"])

  update: AgentState = {
      "respuesta": respuesta_RAG["respuesta"],
      "citaciones": respuesta_RAG["citaciones"],
      "rag_exito": respuesta_RAG["documentos_encontrados"]
  }

  if respuesta_RAG["documentos_encontrados"]:
    update["accion_final"] = "AUTO_RESOLVER"

  return update

def nodo_pedir_info(state: AgentState) -> AgentState:
  print("Ejecutando nodo 'pedir_info'...")
  return {
      "respuesta": "Necesito más informaciones sobre tu pedido.",
      "citaciones": [],
      "accion_final": "PEDIR_INFO"
  }

def nodo_abrir_ticket(state: AgentState) -> AgentState:
  print("Ejecutando nodo 'abrir_ticket'...")

  tri = state["triaje"]

  return {
      "respuesta": f"Abrir ticket con urgencia {tri['urgencia']}. Pedido: {state['pregunta']}.",
      "citaciones": [],
      "accion_final": "ABRIR_TICKET"
  }

def arista_decision_triaje(state: AgentState) -> str:
  print("Decidiendo el flujo después del nodo 'triaje'...")
  tri = state["triaje"]

  if tri["decision"] == "AUTO_RESOLVER":
    return "rag"
  elif tri["decision"] == "PEDIR_INFO":
    return "info"
  else:
    return "ticket"

def arista_decision_rag(state: AgentState) -> str:
  print("Decidiendo el flujo después del nodo 'auto_resolver'...")

  if state["rag_exito"]:
    print("RAG con éxito, finalizando el flujo.")
    return "ok"

  KEYWORDS_ABRIR_TICKET = ["aprobación", "aprobar", "excepción", "liberación", "autorización",
                         "autorizar", "abrir ticket", "acceso especial"]

  if any(keyword in state["pregunta"].lower() for keyword in KEYWORDS_ABRIR_TICKET):
    print("RAG ha fallado, pero hay palabras relacionadas con abrir ticket.")
    return "ticket"

  print("RAG ha fallado, pediré más informaciones al usuario.")
  return "info"
