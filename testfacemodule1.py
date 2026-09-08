import os
import numpy as np
from PIL import Image

from facemodule import (
    process_uploaded_image,
    calculate_image_hash,
    normalize_image_to_rgb_array,
)

TEST_DIR = "test_images"


def print_result(label, result):
    print(f"\n--- {label} ---")
    print("Success       :", result["success"])
    print("Face detected :", result["face_detected"])
    print("Num faces     :", result["num_faces"])
    print("Input type    :", result["input_type"])
    print("Message       :", result["message"])
    print("Image hash    :", result["image_hash"])

    if result["success"]:
        print("Encoding shape:", result["encoding"].shape)
        assert result["encoding"].shape == (128,)


def run_upload_test(filename, label):
    path = os.path.join(TEST_DIR, filename)
    if not os.path.isfile(path):
        print(f"\n--- {label} ---")
        print(f"Skipped: '{path}' not found. Add this file to run the test.")
        return
    result = process_uploaded_image(path)
    print_result(label, result)


def test_missing_file():
    result = process_uploaded_image(os.path.join(TEST_DIR, "does_not_exist.jpg"))
    print_result("Missing file", result)
    assert result["success"] is False


def test_image_hash():
    path = os.path.join(TEST_DIR, "sample.jpg")
    if not os.path.isfile(path):
        print("\n--- SHA-256 hash test ---")
        print(f"Skipped: '{path}' not found.")
        return
    hash_value = calculate_image_hash(path)
    print("\n--- SHA-256 hash test ---")
    print("Hash:", hash_value)
    assert hash_value is not None
    assert len(hash_value) == 64


def test_grayscale_conversion():
    gray_image = Image.new("L", (200, 150), color=128)
    rgb_array = normalize_image_to_rgb_array(gray_image)
    print("\n--- Grayscale conversion test ---")
    print("Shape:", rgb_array.shape, "Dtype:", rgb_array.dtype)
    assert rgb_array.shape == (150, 200, 3)
    assert rgb_array.dtype == np.uint8


def test_rgba_conversion():
    rgba_image = Image.new("RGBA", (200, 150), color=(10, 20, 30, 128))
    rgb_array = normalize_image_to_rgb_array(rgba_image)
    print("\n--- RGBA conversion test ---")
    print("Shape:", rgb_array.shape, "Dtype:", rgb_array.dtype)
    assert rgb_array.shape == (150, 200, 3)
    assert rgb_array.dtype == np.uint8


if __name__ == "__main__":
    print("Running facemodule.py development tests...")
    print("(This file is for manual testing only and is never run by app.py)")

    run_upload_test("sample.jpg", "JPG upload")
    run_upload_test("sample.jpeg", "JPEG upload")
    run_upload_test("sample.png", "PNG upload")
    run_upload_test("no_face.jpg", "No-face image")
    run_upload_test("multiple_faces.jpg", "Multiple-face image")

    test_missing_file()
    test_image_hash()
    test_grayscale_conversion()
    test_rgba_conversion()

    print("\nAll development tests finished.")