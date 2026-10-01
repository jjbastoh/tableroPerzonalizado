import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Tablero de Dibujo",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CSS PERSONALIZADO
# ============================================================

st.markdown("""
<style>

    /* ========================================================
       FONDO GENERAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at top left,
                #334d3f 0%,
                #1f3028 35%,
                #17231e 70%,
                #101613 100%
            );
        color: #f4f1e8;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #17231e,
                #1f3028,
                #263d31
            );

        border-right: 1px solid rgba(255,255,255,0.12);
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f4f1e8;
    }


    /* ========================================================
       TÍTULO
       ======================================================== */

    .titulo {
        text-align: center;

        font-size: 3rem;

        font-weight: 800;

        margin-top: 10px;

        margin-bottom: 5px;

        background: linear-gradient(
            90deg,
            #a7c957,
            #6a994e,
            #b5c99a
        );

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;
    }


    /* ========================================================
       SUBTÍTULO
       ======================================================== */

    .subtitulo {
        text-align: center;

        color: #d8dfd2;

        font-size: 1.1rem;

        margin-bottom: 30px;
    }


    /* ========================================================
       TARJETA DEL CANVAS
       ======================================================== */

    .canvas-card {
        background: rgba(244, 241, 232, 0.08);

        padding: 25px;

        border-radius: 25px;

        border: 1px solid rgba(255,255,255,0.14);

        box-shadow:
            0 20px 50px rgba(0,0,0,0.45);

        backdrop-filter: blur(12px);

        margin: auto;
    }


    /* ========================================================
       CAJA DE INFORMACIÓN
       ======================================================== */

    .info-box {
        background: rgba(106, 153, 78, 0.16);

        border-left: 4px solid #a7c957;

        padding: 15px;

        border-radius: 10px;

        color: #e8eee3;

        margin-bottom: 20px;
    }


    /* ========================================================
       SEPARADORES
       ======================================================== */

    hr {
        border-color: rgba(255,255,255,0.14);
    }


    /* ========================================================
       LABELS
       ======================================================== */

    label {
        color: #e8eee3 !important;

        font-weight: 500 !important;
    }


    /* ========================================================
       SELECTBOX
       ======================================================== */

    div[data-baseweb="select"] > div {
        background-color: rgba(244,241,232,0.08);

        border-radius: 10px;

        border: 1px solid rgba(255,255,255,0.14);
    }


    /* ========================================================
       COLOR PICKER
       ======================================================== */

    div[data-testid="stColorPicker"] {
        margin-bottom: 10px;
    }


    /* ========================================================
       BOTONES
       ======================================================== */

    .stButton > button,
    .stDownloadButton > button {

        width: 100%;

        border-radius: 12px;

        font-weight: 600;

        border: 1px solid #6a994e;

        background-color: #386641;

        color: #ffffff;

        transition: all 0.2s ease;
    }


    .stButton > button:hover,
    .stDownloadButton > button:hover {

        background-color: #6a994e;

        border-color: #a7c957;

        color: #ffffff;

        transform: translateY(-1px);
    }


    /* ========================================================
       SLIDERS
       ======================================================== */

    div[data-baseweb="slider"] {

        margin-bottom: 10px;
    }


    /* ========================================================
       EXPANDER
       ======================================================== */

    div[data-testid="stExpander"] {

        background: rgba(244,241,232,0.06);

        border: 1px solid rgba(255,255,255,0.12);

        border-radius: 12px;
    }


</style>
""", unsafe_allow_html=True)


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    '<div class="titulo">🎨 Mi Tablero de Dibujo</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">'
    'Crea, dibuja y experimenta con diferentes herramientas'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# ESTADO
# ============================================================

if "canvas_version" not in st.session_state:
    st.session_state.canvas_version = 0


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎨 Panel de Diseño")

    st.markdown("---")


    # ========================================================
    # DIMENSIONES
    # ========================================================

    st.markdown("### 📐 Dimensiones")

    canvas_width = st.slider(
        "Ancho del tablero",
        min_value=300,
        max_value=700,
        value=500,
        step=50
    )

    canvas_height = st.slider(
        "Alto del tablero",
        min_value=200,
        max_value=600,
        value=300,
        step=50
    )


    st.markdown("---")


    # ========================================================
    # HERRAMIENTA
    # ========================================================

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


    # ========================================================
    # ESTILO
    # ========================================================

    st.markdown("### 🎨 Estilo")

    stroke_width = st.slider(
        "Grosor del trazo",
        min_value=1,
        max_value=30,
        value=5,
        step=1
    )


    stroke_color = st.color_picker(
        "Color del trazo",
        "#A7C957"
    )


    bg_color = st.color_picker(
        "Color de fondo",
        "#F4F1E8"
    )


    st.markdown("---")


    # ========================================================
    # LIMPIAR
    # ========================================================

    if st.button(
        "🗑️ Limpiar tablero",
        use_container_width=True
    ):

        st.session_state.canvas_version += 1

        st.rerun()


    st.markdown("---")


    # ========================================================
    # CONSEJO
    # ========================================================

    st.info(
        "💡 Consejo: combina diferentes colores y herramientas "
        "para crear diseños originales."
    )


# ============================================================
# ÁREA DE DIBUJO
# ============================================================

st.markdown("""
<div class="info-box">

    🖌️ <b>Área de dibujo</b><br>

    Selecciona una herramienta desde el panel izquierdo
    y comienza a crear.

</div>
""", unsafe_allow_html=True)


# ============================================================
# CANVAS
# ============================================================

st.markdown(
    '<div class="canvas-card">',
    unsafe_allow_html=True
)


canvas_result = st_canvas(

    fill_color="rgba(167, 201, 87, 0.25)",

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

    st.markdown("---")

    st.markdown("### ✨ Tu creación")

    st.caption(
        "Puedes modificar el tamaño, colores y herramienta "
        "desde el panel lateral."
    )


    try:

        image = Image.fromarray(
            image_data.astype("uint8")
        )


        # ====================================================
        # MOSTRAR IMAGEN
        # ====================================================

        st.image(
            image,
            caption="Vista previa de tu dibujo",
            width=canvas_width
        )


        # ====================================================
        # PREPARAR PNG
        # ====================================================

        png_buffer = io.BytesIO()

        image.save(
            png_buffer,
            format="PNG"
        )

        png_buffer.seek(0)


        # ====================================================
        # DESCARGAR
        # ====================================================

        st.download_button(

            label="⬇️ Descargar dibujo como PNG",

            data=png_buffer.getvalue(),

            file_name="mi_dibujo.png",

            mime="image/png",

            use_container_width=True

        )


    except Exception:

        st.warning(
            "No se pudo generar la vista previa."
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
        "Puedes seleccionar dibujo libre, líneas, rectángulos, "
        "círculos, polígonos, puntos y transformación."
    )

    st.write(
        "También puedes cambiar el color, el grosor del trazo "
        "y el color de fondo."
    )


