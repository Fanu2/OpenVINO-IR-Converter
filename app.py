import subprocess
import os
import sys

def convert_to_openvino_ir(onnx_path, output_dir, input_shape=None, data_type="FP16"):
    xml_name = os.path.splitext(os.path.basename(onnx_path))[0] + ".xml"
    bin_name = os.path.splitext(os.path.basename(onnx_path))[0] + ".bin"
    output_path = os.path.join(output_dir, xml_name)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Build command using Python module fallback
    command = [
        sys.executable, "-m", "openvino.tools.mo",
        "--input_model", onnx_path,
        "--output_dir", output_dir,
        "--data_type", data_type
    ]
    if input_shape:
        command += ["--input_shape", input_shape]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return output_path, os.path.join(output_dir, bin_name)
    except FileNotFoundError:
        raise RuntimeError("❌ Model Optimizer not found. Make sure `openvino-dev` is installed and accessible.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"❌ Conversion failed:\n{e.stderr}")
