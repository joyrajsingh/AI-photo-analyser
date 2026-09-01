from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageStat, ImageFilter
import io
import numpy as np


app = FastAPI(
    title="AI Photography Analyzer",
    description="Backend for analyzing photographs"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# IMAGE ANALYSIS
# =========================

def analyze_image(image):

    image = image.convert("RGB")


    # -------------------------
    # Brightness
    # -------------------------

    gray = image.convert("L")

    brightness = ImageStat.Stat(gray).mean[0]


    # -------------------------
    # Saturation
    # -------------------------

    hsv = np.array(image.convert("HSV"))

    saturation = (
        hsv[:, :, 1].mean() / 255
    ) * 100


    # -------------------------
    # Contrast
    # -------------------------

    contrast = ImageStat.Stat(
        gray
    ).stddev[0]


    # -------------------------
    # Sharpness
    # -------------------------

    edges = gray.filter(
        ImageFilter.FIND_EDGES
    )

    sharpness = ImageStat.Stat(
        edges
    ).mean[0]


    brightness = round(brightness, 2)
    saturation = round(saturation, 2)
    contrast = round(contrast, 2)
    sharpness = round(sharpness, 2)


    # =========================
    # SUGGESTIONS
    # =========================

    suggestions = []


    # Brightness

    if brightness < 70:

        suggestions.append(
            "The photograph is slightly dark. "
            "Try increasing exposure or using better lighting."
        )

    elif brightness > 190:

        suggestions.append(
            "The photograph is quite bright. "
            "Try reducing exposure to preserve highlights."
        )

    else:

        suggestions.append(
            "Brightness is well balanced."
        )


    # Saturation

    if saturation < 25:

        suggestions.append(
            "Colors appear muted. "
            "A small increase in saturation may make the photograph more vibrant."
        )

    elif saturation > 80:

        suggestions.append(
            "Colors are highly saturated. "
            "Reducing saturation slightly may give a more natural appearance."
        )

    else:

        suggestions.append(
            "Color saturation looks balanced."
        )


    # Contrast

    if contrast < 25:

        suggestions.append(
            "The image has relatively low contrast. "
            "Try increasing contrast to create better separation between light and dark areas."
        )

    else:

        suggestions.append(
            "The image has good tonal contrast."
        )


    # Sharpness

    if sharpness < 5:

        suggestions.append(
            "The photograph appears slightly soft. "
            "Try improving focus and keeping the camera steady."
        )

    else:

        suggestions.append(
            "The photograph has a good level of visible detail."
        )


    # =========================
    # QUOTE
    # =========================

    if brightness < 70:

        quote = (
            "Even in the shadows, "
            "there is a story waiting to be seen."
        )

    elif saturation > 70:

        quote = (
            "Life looks brighter "
            "when you choose to see it in color."
        )

    else:

        quote = (
            "Photography is the art of "
            "turning ordinary moments into memories."
        )


    # =========================
    # RETURN RESULT
    # =========================

    return {

        "metrics": {

            "brightness": brightness,

            "saturation": saturation,

            "contrast": contrast,

            "sharpness": sharpness

        },

        "suggestions": suggestions,

        "quote": quote

    }


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message":
        "AI Photography Analyzer Backend is running!"
    }


# =========================
# ANALYZE ENDPOINT
# =========================

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...)
):

    contents = await file.read()


    try:

        image = Image.open(
            io.BytesIO(contents)
        )

    except Exception:

        return {
            "error":
            "Invalid image file."
        }


    result = analyze_image(image)


    return result