# convert_ir.py

import streamlit as st
import subprocess
import os
from openvino.runtime import Core

st.set_page_config(page_title="ONNX → OpenVINO IR", layout="centered")
st.title("🔄 ONNX to OpenVINO IR Converter")

# Upload ONNX model
onnx_file = st.file_uploader("Upload ONNX model", type=["onnx"])
output_dir = st.text_input("Output directory", value="converted_models")
input_shape = st.text_input("Optional input shape (e.g. [1,3,256,256])")
data_type = st.selectbox("Precision", ["FP16", "FP32"])

def convert_to_openvino_ir(onnx_path, output_dir, input_shape=None, data_type="FP16"):
    xml_name = os.path.splitext(os.path.basename(onnx_path))[0] + ".xml"
    bin_name = os.path.splitext(os.path.basename(onnx_path))[0] + ".bin"
    output_path = os.path.join(output_dir, xml_name)

    command = [
        "mo",
        "--input_model", onnx_path,
        "--output_dir", output_dir,
        "--data_type", data_type
    ]
    if input_shape:
        command += ["--input_shape", input_shape]

    subprocess.run(command, check=True)
    return output_path, os.path.join(output_dir, bin_name)

def preview_ir_model(xml_path):
    ie = Core()
    model = ie.read_model(model=xml_path)
    compiled = ie.compile_model(model=model, device_name="CPU")
    return compiled.input(0).shape, compiled.output(0).shape

if onnx_file and st.button("Convert to OpenVINO IR"):
    os.makedirs("temp", exist_ok=True)
    onnx_path = os.path.join("temp", onnx_file.name)
    with open(onnx_path, "wb") as f:
        f.write(onnx_file.getbuffer())

    try:
        xml_path, bin_path = convert_to_openvino_ir(
            onnx_path, output_dir, input_shape or None, data_type
        )
        st.success(f"✅ IR files saved:\n- {xml_path}\n- {bin_path}")

        if st.checkbox("Preview model shapes"):
            inp, out = preview_ir_model(xml_path)
            st.info(f"📥 Input shape: {inp}\n📤 Output shape: {out}")
    except Exception as e:
        st.error(f"❌ Conversion failed: {e}")
