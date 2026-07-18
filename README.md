<div align="center">
  <img width="148" height="148" alt="E-commerce" src="https://github.com/user-attachments/assets/0f9f763a-0fbf-4911-b492-1370d8e05835" />
  <h1>Desafío Uno: Comercio Electrónico Latam (E-Commerce)</h1>
  <p>Análisis inteligente de documentos comerciales mediante Agentes de IA y Arquitectura RAG</p>
  
  [![Open In Colab](https://google.com)](https://google.com)
</div>

## 📌 Descripción del Proyecto

Este proyecto interactivo implementa un sistema avanzado de consulta y análisis para plataformas de e-commerce multiplataforma en Latinoamérica (compra, venta y afiliados). Está diseñado para dar devolución a nuestros afiliados y se ejecuta completamente en la nube a través de **Google Colab**.

El sistema procesa documentación comercial en formato PDF utilizando una arquitectura **RAG (Generación Aumentada por Recuperación)** y flujos de trabajo basados en grafos para responder preguntas complejas sobre el negocio.

---

## 🛠️ Stack Tecnológico

*   **Orquestación y Grafos:** `langchain` y `langgraph` para definir la lógica del agente.
*   **Modelo de Lenguaje (LLM):** `ChatGroq` con el modelo de última generación `llama-3.3-70b-versatile`.
*   **Procesamiento de Documentos:** `pymupdf` (fitz) para la extracción eficiente de texto desde archivos PDF.
*   **Base de Datos Vectorial:** `faiss-cpu` para el almacenamiento y búsqueda rápida de embeddings.
*   **Validación de Datos:** `pydantic` para garantizar estructuras de datos consistentes y seguras.
*   **Soporte de Desarrollo:** `pylance` (configuración recomendada para el entorno de desarrollo local opcional).
*   **Interfaz Gráfica:** gradio https://d9db23fcf608ebb3b2.gradio.live

---

## 🚀 Guía de Ejecución Paso a Paso en Google Colab

Sigue estas instrucciones para clonar y ejecutar el notebook del **desafío-uno** sin necesidad de configurar un entorno local:

### Paso 1: Abrir el Entorno
1. Copia la URL de este repositorio de GitHub.
2. Ve a [Google Colab](https://google.com).
3. En la ventana emergente, selecciona la pestaña **GitHub**.
4. Pega la URL del repositorio y presiona Enter.
5. Haz clic sobre el archivo 06_Desafio_uno_Challenge_COMPLETO.ipynb` de este proyecto completo para abrirlo.

### Paso 2: Configurar las Credenciales (API Keys)
El proyecto requiere conectarse a Groq. Sigue estos pasos dentro de Colab:
1. Haz clic en el icono de la **llave (Secrets / Secretos)** en la barra lateral izquierda de Colab.
2. Añade una nueva variable con el nombre: `GROQ_API_KEY`.
3. Pega tu clave de API de Groq en el campo de valor.
4. Asegúrate de activar el interruptor de **Acceso a Notebook (Notebook access)**.

### Paso 3: Carga de Archivos PDF
1. Haz clic en el icono de la **carpeta (Archivos)** en la barra lateral izquierda.
2. Arrastra y suelta tus archivos PDF de e-commerce en ese panel para que el script `pymupdf` pueda procesarlos.
3. Los archivos en formato .pdf están en el siguiente link= https://drive.google.com/drive/folders/1DREqdKWG4ziR7MJqUmM-58W373eDCbYQ?usp=sharing

### Paso 4: Instalar Dependencias y Ejecutar
1. Ejecuta la primera celda del cuaderno que contiene las instalaciones del sistema:
   ```bash
   !pip install langchain langgraph pymupdf faiss-cpu pydantic langchain-groq
   ```
2. Ejecuta el resto de las celdas de forma secuencial (`Entorno de ejecución` > `Ejecutar todas`).

---

## 📐 Arquitectura del Sistema

1.  **Ingesta:** `pymupdf` extrae el texto limpio de los manuales y catálogos en PDF.
2.  **Indexación:** El texto se fragmenta y se convierte en vectores que se almacenan en `FAISS`.
3.  **Flujo de Control:** `langgraph` gestiona el estado de la conversación, decidiendo si el agente necesita buscar más información o responder directamente usando `llama-3.3-70b-versatile`.

