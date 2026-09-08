import os
import uuid
import base64
import requests

from dotenv import load_dotenv
from flask import Flask, render_template, request
from PIL import Image

from facemodule1 import process_uploaded_image
from search_module import search_module
from Blockchain.blockchain.blockchain_module import register_hash, verify_hash


load_dotenv()


def upload_to_imgbb(image_path):
    api_key = os.getenv("IMGBB_API_KEY")

    with open(image_path, "rb") as image_file:
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": api_key},
            files={"image": image_file}
        )

    data = response.json()

    if data.get("success"):
        return data["data"]["url"]

    return None


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

FACE_MODEL = "hog"
MULTIPLE_FACES_MODE = "reject"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


def classify_result(result):
    if result["reason"] == "success":
        return "success"

    if result["reason"] == "no_face":
        return "no_face"

    if result["reason"] == "multiple_faces":
        return "multiple_faces"

    return "invalid"


def get_image_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            return img.width, img.height, img.format
    except Exception:
        return None, None, None


def build_display_context(result, filename, width, height, image_format):
    encoding_preview = None

    if result["encoding"] is not None:
        encoding_preview = [
            round(float(v), 4)
            for v in result["encoding"][:5]
        ]

    return {
        "success": result["success"],
        "face_detected": result["face_detected"],
        "num_faces": result["num_faces"],
        "face_location": result["face_location"],
        "has_encoding": result["encoding"] is not None,
        "encoding_dimensions": (
            128 if result["encoding"] is not None else None
        ),
        "encoding_preview": encoding_preview,
        "image_hash": result["image_hash"],
        "input_type": result["input_type"],
        "message": result["message"],
        "filename": filename,
        "width": width,
        "height": height,
        "image_format": image_format,
    }


def process_and_render(temp_path, input_type, original_filename):

    # Person 1: Face Detection + Encoding + Image Hash
    result = process_uploaded_image(
        temp_path,
        model=FACE_MODEL,
        multiple_faces=MULTIPLE_FACES_MODE
    )

    result["input_type"] = input_type

    width, height, image_format = get_image_metadata(temp_path)

    status = classify_result(result)

    if status == "invalid":
        return render_template(
            "index.html",
            status=None,
            error=result["message"]
        )

    if status == "no_face":
        display = build_display_context(
            result,
            original_filename,
            width,
            height,
            image_format
        )

        return render_template(
            "index.html",
            status="no_face",
            error=result["message"],
            result=display
        )

    if status == "multiple_faces":
        display = build_display_context(
            result,
            original_filename,
            width,
            height,
            image_format
        )

        return render_template(
            "index.html",
            status="multiple_faces",
            error=result["message"],
            result=display
        )

    # Person 1 successful
    display = build_display_context(
        result,
        original_filename,
        width,
        height,
        image_format
    )

    # Upload image to ImgBB
    image_url = upload_to_imgbb(temp_path)

    # Person 2: Reverse Image Search using SerpApi
    if image_url:
        search_result = search_module(image_url)
    else:
        search_result = None

    # Person 3: Blockchain Verification
    blockchain_result = None

    if result["image_hash"]:
        blockchain_result = verify_hash(result["image_hash"])

        if not blockchain_result["verified"]:
            tx_hash = register_hash(result["image_hash"])

            blockchain_result = {
                "verified": True,
                "timestamp": None,
                "uploader": None,
                "transaction_hash": tx_hash
            }

    display["image_url"] = image_url
    display["search_result"] = search_result
    display["blockchain_result"] = blockchain_result

    return render_template(
        "index.html",
        status="success",
        error=None,
        result=display
    )


@app.route("/")
def index():
    return render_template(
        "index.html",
        status=None,
        error=None,
        result=None
    )


@app.route("/upload", methods=["POST"])
def upload():

    uploaded_file = request.files.get("photo")

    if uploaded_file is None or uploaded_file.filename == "":
        return render_template(
            "index.html",
            status=None,
            error="No file selected. Please choose an image."
        )

    ext = os.path.splitext(uploaded_file.filename)[1].lower() or ".img"

    temp_path = os.path.join(
        UPLOAD_DIR,
        f"{uuid.uuid4().hex}{ext}"
    )

    uploaded_file.save(temp_path)

    return process_and_render(
        temp_path,
        "upload",
        uploaded_file.filename
    )


@app.route("/capture", methods=["POST"])
def capture():

    data_url = request.form.get("image_data")

    if not data_url or "," not in data_url:
        return render_template(
            "index.html",
            status=None,
            error="No photo was captured. Please try again."
        )

    try:
        header, encoded = data_url.split(",", 1)
        image_bytes = base64.b64decode(encoded)

    except Exception:
        return render_template(
            "index.html",
            status=None,
            error="Captured photo could not be read. Please try again."
        )

    temp_path = os.path.join(
        UPLOAD_DIR,
        f"{uuid.uuid4().hex}.jpg"
    )

    with open(temp_path, "wb") as f:
        f.write(image_bytes)

    return process_and_render(
        temp_path,
        "camera",
        "captured_photo.jpg"
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)