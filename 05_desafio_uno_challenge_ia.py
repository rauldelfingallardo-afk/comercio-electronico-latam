
## "Interfaz Gradio para el Agente"

import gradio as gr

def run_agent(pregunta: str) -> str:
  """Ejecuta el agente con la pregunta dada y formatea la salida."""
  respuesta = grafo.invoke({"pregunta": pregunta})

  output_str = []
  output_str.append(f"**PREGUNTA:** {pregunta}")
  output_str.append(f"**DECISIÓN DE TRIAJE:** {respuesta['triaje']['decision']} | **URGENCIA:** {respuesta['triaje']['urgencia']} | **ACCIÓN FINAL:** {respuesta['accion_final']}")
  output_str.append(f"**RESPUESTA:** {respuesta['respuesta']}")

  if respuesta.get('citaciones'):
    output_str.append("\n**CITACIONES:**")
    for i, citacion in enumerate(respuesta['citaciones']):
      output_str.append(f"    - CITACIÓN {i + 1}:")
      output_str.append(f"      **Camino del documento:** {citacion.metadata['file_path']}")
      output_str.append(f"      **Contenido:** {citacion.page_content.replace('\n', ' ')}")
  else:
      output_str.append("**CITACIONES:** No se encontraron citaciones relevantes.")

  return "\n".join(output_str)


# Crear la interfaz Gradio
interface = gr.Interface(
    fn=run_agent,
    inputs=gr.Textbox(lines=5, label="Ingresa tu pregunta al agente:", placeholder="Ej: ¿Cuál es su política de devoluciones?"),
    outputs=gr.Markdown(label="Respuesta del Agente"),
    title="Agente de Service Desk para E-commerce (BimBam Buy)",
    description="Este agente utiliza un sistema de triaje y RAG para responder a las consultas de los clientes."
)

# Lanzar la interfaz
interface.launch(debug=True, share=True)