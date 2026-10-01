import io

import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas


# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Pizarra de Pensamiento",
    page_icon="💭",
    layout="wide"
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    """
    <style>

    .titulo {
        font-size: 40px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 5px;
    }

    .subtitulo {
        font-size: 17px;
        color: #64748b;
        margin-bottom: 25px;
    }

    .info-box {
        background-color: #f1f5f9;
        border-radius: 12px;
        padding: 15px;
        margin-top: 15px;
        border: 1px solid #e2e8f0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TÍTULO
# ============================================================

st.markdown(
    '<div class="titulo">💭 Pizarra de Pensamiento</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">'
    'Dibuja tus ideas libremente y prepara tu boceto '
    'para convertirlo posteriormente en una nube de pensamiento.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# BARRA LATERAL
# ============================================================

with st.sidebar:

    st.header("⚙️ Propiedades del tablero")

    # --------------------------------------------------------
    # NOMBRE DEL TABLERO
    # --------------------------------------------------------

    st.subheader("📝 Proyecto")

    project_name = st.text_input(
        "Nombre del tablero",
        value="Mi nube de pensamiento"
    )

    st.divider()

    # --------------------------------------------------------
    # DIMENSIONES
    # --------------------------------------------------------

    st.subheader("📐 Dimensiones")

    canvas_width = st.slider(
        "Ancho",
        min_value=300,
        max_value=1000,
        value=600,
        step=50
    )

    canvas_height = st.slider(
        "Alto",
        min_value=200,
        max_value=700,
        value=400,
        step=50
    )

    st.caption(
        f"Tamaño actual: {canvas_width} × {canvas_height}px"
    )

    st.divider()

    # --------------------------------------------------------
    # HERRAMIENTA
    # --------------------------------------------------------

    st.subheader("🖌️ Herramienta")

    drawing_mode = st.selectbox(
        "Selecciona una herramienta",
        [
            "freedraw",
            "line",
            "rect",
            "circle",
            "transform",
            "polygon",
            "point"
        ],
        format_func=lambda herramienta: {
            "freedraw": "✏️ Lápiz",
            "line": "📏 Línea",
            "rect": "⬜ Rectángulo",
            "circle": "⭕ Círculo",
            "transform": "🔄 Mover",
            "polygon": "🔷 Polígono",
            "point": "📍 Punto"
        }.get(
            herramienta,
            herramienta
        )
    )

    # --------------------------------------------------------
    # GROSOR
    # --------------------------------------------------------

    stroke_width = st.slider(
        "Grosor del trazo",
        min_value=1,
        max_value=30,
        value=5
    )

    # --------------------------------------------------------
    # COLOR DEL TRAZO
    # --------------------------------------------------------

    stroke_color = st.color_picker(
        "🎨 Color del trazo",
        value="#000000"
    )

    # --------------------------------------------------------
    # COLOR DEL FONDO
    # --------------------------------------------------------

    background_color = st.color_picker(
        "🖼️ Color del fondo",
        value="#FFFFFF"
    )

    st.divider()

    # --------------------------------------------------------
    # INFORMACIÓN
    # --------------------------------------------------------

    st.subheader("💡 Cómo utilizarlo")

    st.write(
        "1. Selecciona el tamaño del tablero."
    )

    st.write(
        "2. Selecciona el color del fondo."
    )

    st.write(
        "3. Selecciona el color y grosor del lápiz."
    )

    st.write(
        "4. Dibuja tus ideas."
    )

    st.write(
        "5. Descarga tu dibujo o conviértelo en una nube."
    )


# ============================================================
# TÍTULO DEL PROYECTO
# ============================================================

st.subheader(
    f"🧠 {project_name}"
)


# ============================================================
# TABLERO
# ============================================================

canvas_result = st_canvas(

    fill_color="rgba(255, 165, 0, 0.2)",

    stroke_width=stroke_width,

    stroke_color=stroke_color,

    background_color=background_color,

    height=canvas_height,

    width=canvas_width,

    drawing_mode=drawing_mode,

    key="canvas_principal"

)


# ============================================================
# INFORMACIÓN DEL TABLERO
# ============================================================

if canvas_result.image_data is not None:

    st.markdown(
        f"""
        <div class="info-box">

        <strong>💭 Tablero activo</strong><br><br>

        📐 Tamaño: {canvas_width} × {canvas_height}px<br>

        🖌️ Herramienta: {drawing_mode}<br>

        📏 Grosor: {stroke_width}px<br>

        🎨 Color: {stroke_color}

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# BOTONES
# ============================================================

st.divider()

col1, col2, col3 = st.columns(3)


# ============================================================
# DESCARGAR DIBUJO
# ============================================================

with col1:

    if canvas_result.image_data is not None:

        imagen = Image.fromarray(
            canvas_result.image_data.astype("uint8")
        )

        buffer = io.BytesIO()

        imagen.save(
            buffer,
            format="PNG"
        )

        st.download_button(
            label="⬇️ Descargar dibujo",
            data=buffer.getvalue(),
            file_name="mi_dibujo.png",
            mime="image/png",
            use_container_width=True
        )

    else:

        st.button(
            "⬇️ Descargar dibujo",
            disabled=True,
            use_container_width=True
        )


# ============================================================
# LIMPIAR
# ============================================================

with col2:

    limpiar = st.button(
        "🗑️ Limpiar tablero",
        use_container_width=True
    )


# ============================================================
# CONVERTIR EN NUBE
# ============================================================

with col3:

    convertir = st.button(
        "🧠 Crear nube",
        type="primary",
        use_container_width=True
    )


# ============================================================
# LIMPIAR TABLERO
# ============================================================

if limpiar:

    st.session_state["limpiar_canvas"] = True

    st.rerun()


# ============================================================
# CREAR NUBE
# ============================================================

if convertir:

    if canvas_result.image_data is None:

        st.warning(
            "⚠️ Primero debes dibujar algo."
        )

    else:

        st.session_state["dibujo"] = (
            canvas_result.image_data
        )

        st.success(
            "✅ Tu dibujo está preparado para convertirse "
            "en una nube de pensamiento."
        )

        st.info(
            "🧠 Próximamente podremos analizar las palabras, "
            "formas y conexiones de tu dibujo para generar "
            "automáticamente la nube de pensamiento."
        )


# ============================================================
# ESTADO
# ============================================================

st.divider()

st.caption(
    "💭 Tablero Inteligente | "
    "Pizarra personalizable"
)

