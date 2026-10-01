import io

import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Pizarra de Pensamiento",
    page_icon="💭",
    layout="wide"
)


# ============================================================
# ESTADO INICIAL
# ============================================================

if "canvas_version" not in st.session_state:
    st.session_state.canvas_version = 0

if "dibujo" not in st.session_state:
    st.session_state.dibujo = None


# ============================================================
# TÍTULO
# ============================================================

st.title("💭 Pizarra de Pensamiento")

st.write(
    "Dibuja tus ideas libremente. "
    "Este tablero será la base para crear posteriormente "
    "una nube de pensamiento con inteligencia artificial."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Propiedades del tablero")

    # --------------------------------------------------------
    # NOMBRE
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

    st.write(
        f"📏 {canvas_width} × {canvas_height}px"
    )

    st.divider()

    # --------------------------------------------------------
    # HERRAMIENTA
    # --------------------------------------------------------

    st.subheader("🖌️ Herramienta")

    drawing_mode = st.selectbox(
        "Selecciona",
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
        "Grosor",
        min_value=1,
        max_value=30,
        value=5
    )

    # --------------------------------------------------------
    # COLOR DEL LÁPIZ
    # --------------------------------------------------------

    stroke_color = st.color_picker(
        "🎨 Color del trazo",
        "#000000"
    )

    # --------------------------------------------------------
    # COLOR DEL FONDO
    # --------------------------------------------------------

    background_color = st.color_picker(
        "🖼️ Color del fondo",
        "#FFFFFF"
    )

    st.divider()

    st.info(
        "💡 Puedes utilizar círculos, líneas y dibujos "
        "para representar las relaciones entre tus ideas."
    )


# ============================================================
# TÍTULO DEL TABLERO
# ============================================================

st.subheader(
    f"🧠 {project_name}"
)


# ============================================================
# IDENTIFICADOR DEL CANVAS
# ============================================================

canvas_key = (
    f"canvas_{st.session_state.canvas_version}"
)


# ============================================================
# CANVAS
# ============================================================

canvas_result = st_canvas(

    fill_color="rgba(255, 165, 0, 0.2)",

    stroke_width=stroke_width,

    stroke_color=stroke_color,

    background_color=background_color,

    height=canvas_height,

    width=canvas_width,

    drawing_mode=drawing_mode,

    key=canvas_key

)


# ============================================================
# BOTONES
# ============================================================

st.divider()

col1, col2, col3 = st.columns(3)


# ============================================================
# BOTÓN LIMPIAR
# ============================================================

with col1:

    limpiar = st.button(
        "🗑️ Limpiar",
        use_container_width=True
    )


# ============================================================
# BOTÓN CREAR NUBE
# ============================================================

with col2:

    crear_nube = st.button(
        "🧠 Crear nube",
        type="primary",
        use_container_width=True
    )


# ============================================================
# INFORMACIÓN
# ============================================================

with col3:

    st.metric(
        "📐 Tamaño",
        f"{canvas_width} × {canvas_height}"
    )


# ============================================================
# LIMPIAR CANVAS
# ============================================================

if limpiar:

    st.session_state.canvas_version += 1

    st.session_state.dibujo = None

    st.rerun()


# ============================================================
# OBTENER IMAGEN DE FORMA SEGURA
# ============================================================

imagen_canvas = None

try:

    imagen_canvas = canvas_result.image_data

except RuntimeError:

    imagen_canvas = None


# ============================================================
# CREAR NUBE
# ============================================================

if crear_nube:

    if imagen_canvas is None:

        st.warning(
            "⚠️ Primero dibuja algo en el tablero."
        )

    else:

        # Guardamos el dibujo
        st.session_state.dibujo = imagen_canvas

        st.success(
            "✅ Dibujo guardado correctamente."
        )

        st.info(
            "🧠 El siguiente paso será enviar este dibujo "
            "a la inteligencia artificial para identificar "
            "las ideas y construir automáticamente "
            "la nube de pensamiento."
        )


# ============================================================
# DESCARGAR DIBUJO
# ============================================================

if imagen_canvas is not None:

    st.divider()

    st.subheader("💾 Guardar dibujo")

    try:

        imagen = Image.fromarray(
            imagen_canvas.astype("uint8")
        )

        buffer = io.BytesIO()

        imagen.save(
            buffer,
            format="PNG"
        )

        st.download_button(
            label="⬇️ Descargar como PNG",
            data=buffer.getvalue(),
            file_name=f"{project_name}.png",
            mime="image/png"
        )

    except Exception as error:

        st.warning(
            f"No fue posible preparar la imagen: {error}"
        )


# ============================================================
# ESTADO
# ============================================================

if st.session_state.dibujo is not None:

    st.divider()

    st.success(
        "💭 Tu dibujo está listo para ser convertido "
        "en una nube de pensamiento."
    )


# ============================================================
# PIE DE PÁGINA
# ============================================================

st.divider()

st.caption(
    "💭 Pizarra de Pensamiento • "
    "Proyecto de inteligencia artificial"
)


