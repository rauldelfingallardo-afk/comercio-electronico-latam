#linea 28 segundo commit

PROMPT_TRIAJE_ECOMMERCE = """
	Eres un especialista en triaje automatizado para el Service Desk de un E-commerce.
	Dado el mensaje del cliente, devuelve SÓLO un JSON con la siguiente estructura:\n
	{\n
	 "decision": "AUTO_RESOLVER" | "PEDIR_INFO" | "ABRIR_TICKET_LOGISTICA" | "ESCALAR_URGENTE",\n
	 "urgencia": "BAJA" | "MEDIANA" | "ALTA" | "CRITICA",\n
	 "categoria": "DEVOLUCIONES" | "ENVIOS" | "PAGOS_Y_FACTURACION" | "PRODUCTO_Y_STOCK" | "SOPORTE_TECNICO",\n
	 "campos_faltantes": ["numero_pedido", "correo_registro", "motivo_especifico"]
	}\n

	Reglas para 'decision' y 'urgencia':

	- **AUTO_RESOLVER** (Urgencia: BAJA o MEDIANA):\n
	  * Consultas generales sobre políticas de envío, tablas de talles, horarios o métodos de pago.\n
	  * Ejemplos: "¿Cuánto tarda el envío a mi zona?", "¿Tienen cuotas sin interés?", "¿Cuál es su política de cambios?".\n

	- **PEDIR_INFO** (Urgencia: BAJA):\n
	  * El mensaje del cliente es impreciso, no especifica el problema o le faltan datos críticos para poder revisar el sistema (como el número de orden).\n
	  * Ejemplos: "Mi pedido no llegó", "Quiero hacer un cambio", "Tuve un problema con el pago".\n
	  * Nota: Rellenar la lista 'campos_faltantes' con los datos que se necesitan para procesar la ayuda.\n

	- **ABRIR_TICKET_LOGISTICA** (Urgencia: MEDIANA o ALTA):\n
	  * Solicitudes explícitas de cancelación de órdenes que aún no se han despachado, cambios de dirección de entrega urgentes o reclamos de productos faltantes en el paquete.\n
	  * Ejemplos: "Me equivoqué de dirección y compré hace una hora, cambien la dirección a Calle Falsa 123, a dos casas del kiosko chiringuito", "Me llegó el paquete, pero falta el pantalón".\n

	- **ESCALAR_URGENTE** (Urgencia: ALTA o CRITICA):\n
	  * Casos de sospecha de fraude, pasarelas de pago caídas que cobran doble, productos que llegaron rotos/dañados, o retrasos logísticos graves con más de 5 días de demora prometida.\n
	  * Ejemplos: "Me cobraron dos veces la misma compra", "El perfume llegó roto y derramado", "Mi pedido tenía fecha para el lunes pasado y sigue en viaje".\n

	Analiza el mensaje del cliente, define la 'categoria' correspondiente y decide la acción más adecuada.
"""

from typing import Literal, List, Dict
from pydantic import BaseModel, Field

class TriajeOut(BaseModel):
  decision: Literal["AUTO_RESOLVER", "PEDIR_INFO", "ABRIR_TICKET_LOGISTICA", "ESCALAR_URGENTE"]
  urgencia: Literal["BAJA", "MEDIANA", "ALTA", "CRITICA"]
  categoria: Literal["DEVOLUCIONES", "ENVIOS", "PAGOS_Y_FACTURACION", "PRODUCTO_Y_STOCK", "SOPORTE_TECNICO"]
  campos_faltantes: List[str] = Field(default_factory=list)
  #campos_faltantes: ["numero_pedido", "correo_registro", "motivo_especifico"]

from langchain_core.messages import SystemMessage, HumanMessage

chain_de_triaje = llm.with_structured_output(TriajeOut)

def triaje(mensaje: str) -> Dict:
  salida: TriajeOut = chain_de_triaje.invoke(
      [
          SystemMessage(content=PROMPT_TRIAJE_ECOMMERCE),
          HumanMessage(content=mensaje)
      ]
  )
  return salida.model_dump()

mensajes_de_prueba = [
	"Hice una compra hace una semana para una dirección en zona urbana y el paquete todavía no me llegó, ¿dónde está?",
	"Me equivoqué al escribir la dirección de mi pedido, puse Calle Mexico 123 y era 1234, ¡ayuda antes de que lo envíen!",
	"Acabo de recibir mi paquete hace dos horas, viene todo aplastado por el correo y el producto adentro está roto.",
	"El teléfono se me cayó al suelo por accidente, se rompió la pantalla y no prende. ¿Me lo cubre la garantía?",
	"Hola, mi producto de BimBam Buy dejó de funcionar de la nada y quiero usar la garantía de fábrica.",
	"Compré una campera hace 5 días, pero me arrepentí, está sin usar y quiero que me devuelvan el dinero.",
	"Me acaba de llegar el paquete, pero me mandaron unas zapatillas negras en vez de las rojas que compré.",
	"El banco me cobró la compra en la tarjeta, pero no me llegó ningún correo de confirmación ni número de orden.",
	"Intenté comprar, pero el sistema me rechaza la tarjeta todo el tiempo, ¿qué puedo hacer?",
	"Revisé mi cuenta del banco y me aparece que me cobraron dos veces exactamente el mismo monto por mi pedido.",
	"Ya me aprobaron la devolución del dinero, ¿cuánto tiempo tarda en verse reflejado el reembolso?",
	"Hola, envié mi postulación para el programa de afiliados hace unos días y quería saber si ya me aprobaron la cuenta.",
	"¿Qué pasa con mi comisión si un usuario compró con mi enlace de afiliado, pero luego devolvió el producto?",
	"Me llegó una alerta diciendo que mi cuenta de afiliado está suspendida por publicar precios incorrectos, exijo una revisión.",
	"¿Quién es Zinedine Zidane?"
]

for pregunta in mensajes_de_prueba:
  r = triaje(pregunta)
  print(f"{pregunta} -> {r}")

"""# RAG"""

!pip install -q langchain_community faiss-cpu langchain-text-splitters pymupdf

from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader

docs = []

for documento in Path("/content/BimBam Buy").glob("*.pdf"):
    try:
        loader = PyMuPDFLoader(str(documento))
        docs.extend(loader.load())
        print(f"Archivo cargado: {documento.name}")
    except Exception as e:
        print(f"Error cargando archivo: {documento.name}: {e}")

print(f"Total de documentos cargados: {len(docs)}")

from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
chunks = splitter.split_documents(docs)

for chunk in chunks:
  print(chunk)
  print("------------------")

len(chunks)

from langchain_google_genai import GoogleGenerativeAIEmbeddings

modelo_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GEMINI_API_KEY
)