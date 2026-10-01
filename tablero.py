import streamlit as st
from streamlit_drawable_canvas import st_canvas

# ---------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------
st.set_page_config(
    page_title="Tablero de Dibujo",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CSS PERSONALIZADO
# ---------------------------------------------------
st.markdown("""
<style>

    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b, #312e81);
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827, #1e1b4b);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff;
    }

    /* Título principal */
    .titulo {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 5px;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitulo {
        text-align: center;
        color: #cbd5e1;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }

    /* Tarjeta del tablero */
    .canvas-card {
        background: rgba(255,255,255,0.08);
        padding: 25px;
        border-radius: 25px;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 20px 50px rgba(0,0,0,0.35);
        backdrop-filter: blur(12px);
        margin: auto;
    }

    /* Caja de información */
    .info-box {
        background: rgba(59,130,246,0.12);
        border-left: 4px solid #38bdf8;
        padding: 15px;
        border-radius: 10px;
        color: #e2e8f0;
        margin-bottom: 20px;
    }

    /* Separadores */
    hr {
        border-color: rgba(255,255,255,0.15);
    }

    /* Labels */
    label {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }

    /* Sliders */
    div[data-baseweb="slider"] {
        margin-bottom: 10px;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.08);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.15);
    }

    /* Color picker */
    div[data-testid="stColorPicker"] {
        margin-bottom: 10px;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# ENCABEZADO
# ---------------------------------------------------
st.markdown(
    '<div class="titulo">🎨 Mi Tablero de Dibujo</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">Crea, dibuja y experimenta con diferentes herramientas</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:

    st.markdown("## 🎨 Panel de Diseño")
    st.markdown("---")

    # Dimensiones
    st.markdown("### 📐 Dimensiones")

    canvas_width = st.slider(
        "Ancho del tablero",
        300,
        700,
        500,
        50
    )

    canvas_height = st.slider(
        "Alto del tablero",
        200,
        600,
        300,
        50
    )

    st.markdown("---")

    # Herramienta
    st.markdown("### 🖌️ Herramienta")

    drawing_mode = st.selectbox(
        "Modo de dibujo",
        (
            "freedraw",
            "line",
            "rect",
            "circle",
            "transform",
            "polygon",
            "point"
        ),
        format_func=lambda x: {
            "freedraw": "✏️ Dibujo libre",
            "line": "📏 Línea",
            "rect": "⬜ Rectángulo",
            "circle": "⭕ Círculo",
            "transform": "🔄 Transformar",
            "polygon": "🔷 Polígono",
            "point": "📍 Punto"
        }[x]
    )

    st.markdown("---")

    # Estilo
    st.markdown("### 🎨 Estilo")

    stroke_width = st.slider(
        "Grosor del trazo",
        1,
        30,
        5
    )

    stroke_color = st.color_picker(
        "Color del trazo",
        "#38BDF8"
    )

    bg_color = st.color_picker(
        "Color de fondo",
        "#0F172A"
    )

    st.markdown("---")

    st.info(
        "💡 Consejo: usa diferentes colores y herramientas "
        "para crear diseños más interesantes."
    )


# ---------------------------------------------------
# TABLERO
# ---------------------------------------------------

st.markdown("""
<div class="info-box">
    🖌️ <b>Área de dibujo</b><br>
    Selecciona una herramienta desde el panel izquierdo y comienza a crear.
</div>
""", unsafe_allow_html=True)

# Contenedor visual
st.markdown('<div class="canvas-card">', unsafe_allow_html=True)

canvas_result = st_canvas(
    fill_color="rgba(56, 189, 248, 0.25)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key=f"canvas_{canvas_width}_{canvas_height}",
)

st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------
# INFORMACIÓN DEL CANVAS
# ---------------------------------------------------

if canvas_result.image_data is not None:
    st.markdown("---")

    st.markdown(
        "### ✨ Tu creación",
    )

    st.caption(
        "Puedes modificar el tamaño, colores y herramienta "
        "desde el panel lateral."
    )

