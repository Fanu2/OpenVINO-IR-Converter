# test_ir_conversion.py

from ir_utils import convert_to_openvino_ir, preview_ir_model

onnx_path = "temp/model_quantized.onnx"  # Adjust path if needed
output_dir = "converted_models"
input_shape = "1,3,224,224"
data_type = "FP16"

try:
    xml_path, bin_path = convert_to_openvino_ir(onnx_path, output_dir, input_shape, data_type)
    print(f"✅ IR files saved:\n- {xml_path}\n- {bin_path}")

    inp_shape, out_shape = preview_ir_model(xml_path)
    print(f"📥 Input shape: {inp_shape}\n📤 Output shape: {out_shape}")
except Exception as e:
    print(f"❌ Error: {e}")
