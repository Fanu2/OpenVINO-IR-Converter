# ir_utils.py

import subprocess
import os
import sys
from openvino.runtime import Core

def convert_to_openvino_ir(onnx_path, output_dir, input_shape=None, data_type="FP16"):
    xml_name = os.path.splitext(os.path.basename(onnx_path))[0] + ".xml"
    bin_name = os.path.splitext(os.path.basename(onnx_path))[0] + ".bin"
    output_path = os.path.join(output_dir, xml_name)

    os.makedirs(output_dir, exist_ok=True)

    # Clean input shape format
    shape_clean = input_shape.replace("[", "").replace("]", "").replace(" ", "") if input_shape else None

    command = [
        sys.executable, "-m", "openvino.tools.mo",
        "--input_model", onnx_path,
        "--output_dir", output_dir
    ]
    if shape_clean:
        command += ["--input_shape", f"[{shape_clean}]"]
    if data_type == "FP16":
        command += ["--compress_to_fp16"]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return output_path, os.path.join(output_dir, bin_name)
    except FileNotFoundError:
        raise RuntimeError("❌ Model Optimizer not found. Install with `pip install openvino-dev`.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"❌ Conversion failed:\n{e.stderr}")

def preview_ir_model(xml_path):
    try:
        ie = Core()
        model = ie.read_model(model=xml_path)
        compiled = ie.compile_model(model=model, device_name="CPU")
        return compiled.input(0).shape, compiled.output(0).shape
    except Exception as e:
        raise RuntimeError(f"❌ Preview failed: {e}")
