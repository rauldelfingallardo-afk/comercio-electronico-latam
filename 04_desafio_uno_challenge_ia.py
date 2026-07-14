from langgraph.graph import START, END, StateGraph

workflow = StateGraph(AgentState)

workflow.add_node("triaje", nodo_triaje)
workflow.add_node("auto_resolver", nodo_auto_resolver)
workflow.add_node("pedir_info", nodo_pedir_info)
workflow.add_node("abrir_ticket", nodo_abrir_ticket)

workflow.add_edge(START, "triaje")
workflow.add_conditional_edges("triaje", arista_decision_triaje, {
    "rag": "auto_resolver",
    "info": "pedir_info",
    "ticket": "abrir_ticket"
})

workflow.add_conditional_edges("auto_resolver", arista_decision_rag, {
    "info": "pedir_info",
    "ticket": "abrir_ticket",
    "ok": END
})

workflow.add_edge("pedir_info", END)
workflow.add_edge("abrir_ticket", END)

grafo = workflow.compile()

from IPython.display import display, Image

graph_bytes = grafo.get_graph().draw_mermaid_png()
display(Image(graph_bytes))

PREGUNTA = "Puedo reembolsar mi internet?"

respuesta = grafo.invoke({"pregunta": PREGUNTA})
print("")
print(f"PREGUNTA: {PREGUNTA}")
print(f"DECISIÓN DE TRIAJE: {respuesta['triaje']['decision']} | URGENCIA: {respuesta['triaje']['urgencia']} | ACCIÓN FINAL: {respuesta['accion_final']}")
print(f"RESPUESTA: {respuesta['respuesta']}")
if respuesta['citaciones']:
  for i, citacion in enumerate(respuesta['citaciones']):
    print(f"    - CITACIÓN {i + 1}:")
    print(f"      Camino del documento: {citacion.metadata['file_path']}")
    print(f"      Contenido: {citacion.page_content.replace('\n', '')}")

mensajes_de_prueba = [
	"El banco me cobró la compra en la tarjeta, pero no me llegó ningún correo de confirmación ni número de orden. Preciso respuest",
	"Intenté comprar, pero el sistema me rechaza la tarjeta todo el tiempo, ¿qué puedo hacer?",
	"Ya me aprobaron la devolución del dinero, ¿cuánto tiempo tarda en verse reflejado el reembolso?",
	"Acabo de recibir mi paquete hace dos horas, viene todo aplastado por el correo y el producto adentro está roto. necesito devolverlo",
	"Hola, envié mi postulación para el programa de afiliados hace unos días y quería saber si ya me aprobaron la cuenta.",
	"¿Qué pasa con mi comisión si un usuario compró con mi enlace de afiliado, pero luego devolvió el producto?",
	"¿Quién fue Ronaldinho Gaucho?"
]

for prueba in mensajes_de_prueba:
  respuesta = grafo.invoke({"pregunta": prueba})
  print("")
  print(f"PREGUNTA: {prueba}")
  print(f"DECISIÓN DE TRIAJE: {respuesta['triaje']['decision']} | URGENCIA: {respuesta['triaje']['urgencia']} | ACCIÓN FINAL: {respuesta['accion_final']}")
  print(f"RESPUESTA: {respuesta['respuesta']}")
  if respuesta['citaciones']:
    for i, citacion in enumerate(respuesta['citaciones']):
      print(f"    - CITACIÓN {i + 1}:")
      print(f"      Camino del documento: {citacion.metadata['file_path']}")
      print(f"      Contenido: {citacion.page_content.replace('\n', '')}")
  print("-----------------------------------------------")