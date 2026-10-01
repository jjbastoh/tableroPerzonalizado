import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Mi Tablero de Dibujo",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# COLORES
# ============================================================

COLOR_FONDO = "#EAF6F8"
COLOR_CELESTE = "#9DD9E8"
COLOR_CELESTE_OSCURO = "#5FAFC2"
COLOR_BEIGE = "#F3E7D3"
COLOR_CREMA = "#FFFDF8"
COLOR_TEXTO = "#40545A"
COLOR_BORDE = "#C9DDE0"
COLOR_TRAZO = "#5FAFC2"


# ============================================================
# DISEÑO
# ============================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background: linear-gradient(
            135deg,
            {COLOR_FONDO},
            {COLOR_BEIGE},
            #F8F5EE
        );
        color: {COLOR_TEXTO};
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(
            180deg,
            #DDF2F5,
            #EAF6F8,
            #F3E7D3
        );
        border-right: 1px solid {COLOR_BORDE};
    }}

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {COLOR_TEXTO};
    }}

    .titulo {{
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        color: {COLOR_CELESTE_OSCURO};
        margin-top: 10px;
        margin-bottom: 5px;
    }}

    .subtitulo {{
        text-align: center;
        color: #68777A;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }}

    .canvas-card {{
        background: rgba(255, 253, 248, 0.90);
        padding: 25px;
        border-radius: 24px;
        border: 1px solid {COLOR_BORDE};
        box-shadow: 0 15px 40px rgba(80, 110, 115, 0.16);
        margin: auto;
    }}

    label {{
        color: {COLOR_TEXTO} !important;
        font-weight: 600 !important;
    }}

    div[data-baseweb="select"] > div {{
        background-color: rgba(255, 253, 248, 0.90);
        border-radius: 10px;
        border: 1px solid {COLOR_BORDE};
    }}

    .stButton > button,
    .stDownloadButton > button {{
        width: 100%;
        border-radius: 12px;
        font-weight: 700;
        background-color: {COLOR_CELESTE_OSCURO};
        color: white;
        border: 1px solid {COLOR_CELESTE_OSCURO};
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        background-color: #4C9EAF;
        color: white;
        border-color: #4C9EAF;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    '<h1 style="text-align:center; color:#5FAFC2;">'
    '🎨 Mi Tablero de Dibujo'
    '</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p style="text-align:center; color:#68777A; font-size:18px;">'
    'Crea, dibuja y experimenta con diferentes herramientas'
    '</p>',
    unsafe_allow_html=True
)


# ============================================================
# ESTADO DEL CANVAS
# ============================================================

if "canvas_version" not in st.session_state:
    st.session_state.canvas_version = 0


# ============================================================
# PANEL LATERAL
# ============================================================

with st.sidebar:

    st.header("🎨 Panel de Diseño")

    st.divider()

    # --------------------------------------------------------
    # DIMENSIONES
    # --------------------------------------------------------

    st.subheader("📐 Dimensiones")

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

    st.divider()

    # --------------------------------------------------------
    # HERRAMIENTA
    # --------------------------------------------------------

    st.subheader("🖌️ Herramienta")

    drawing_mode = st.selectbox(
        "Modo de dibujo",
        [
            "freedraw",
            "line",
            "rect",
            "circle",
            "transform",
            "polygon",
            "point"
        ],
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

    st.divider()

    # --------------------------------------------------------
    # ESTILO
    # --------------------------------------------------------

    st.subheader("🎨 Estilo")

    stroke_width = st.slider(
        "Grosor del trazo",
        1,
        30,
        5
    )

    stroke_color = st.color_picker(
        "Color del trazo",
        COLOR_TRAZO
    )

    bg_color = st.color_picker(
        "Color de fondo",
        COLOR_CREMA
    )

    st.divider()

    # --------------------------------------------------------
    # LIMPIAR
    # --------------------------------------------------------

    if st.button(
        "🗑️ Limpiar tablero",
        use_container_width=True
    ):
        st.session_state.canvas_version += 1
        st.rerun()

    st.divider()

    st.info(
        "💡 Combina diferentes colores y herramientas "
        "para crear diseños originales."
    )


# ============================================================
# ÁREA DE DIBUJO
# ============================================================

st.subheader("🖌️ Área de dibujo")

st.write(
    "Selecciona una herramienta desde el panel izquierdo "
    "y comienza a crear."
)


# ============================================================
# CANVAS
# ============================================================

st.markdown(
    '<div class="canvas-card">',
    unsafe_allow_html=True
)

canvas_result = st_canvas(
    fill_color="rgba(157, 217, 232, 0.25)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key=f"drawing_canvas_{st.session_state.canvas_version}"
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# OBTENER IMAGEN DE FORMA SEGURA
# ============================================================

image_data = None

try:
    image_data = canvas_result.image_data
except RuntimeError:
    image_data = None
except Exception:
    image_data = None


# ============================================================
# VISTA PREVIA
# ============================================================

if image_data is not None:

    st.divider()

    st.subheader("✨ Tu creación")

    st.write(
        "Aquí puedes ver una vista previa de tu dibujo."
    )

    try:

        image = Image.fromarray(
            image_data.astype("uint8")
        )

        st.image(
            image,
            caption="Vista previa de tu dibujo",
            width=canvas_width
        )

        # ----------------------------------------------------
        # CREAR ARCHIVO PNG
        # ----------------------------------------------------

        png_buffer = io.BytesIO()

        image.save(
            png_buffer,
            format="PNG"
        )

        png_buffer.seek(0)

        # ----------------------------------------------------
        # DESCARGAR
        # ----------------------------------------------------

        st.download_button(
            "⬇️ Descargar dibujo como PNG",
            data=png_buffer.getvalue(),
            file_name="mi_dibujo.png",
            mime="image/png",
            use_container_width=True
        )

    except Exception:
        st.warning(
            "No se pudo generar la vista previa del dibujo."
        )


# ============================================================
# INFORMACIÓN
# ============================================================

with st.expander("ℹ️ Información"):

    st.write(
        "Este tablero permite realizar dibujos utilizando "
        "diferentes herramientas."
    )

    st.write(
        "Puedes utilizar dibujo libre, líneas, rectángulos, "
        "círculos, polígonos, puntos y transformación."
    )

    st.write(
        "También puedes cambiar el color, el grosor del trazo "
        "y el color de fondo."
    )

