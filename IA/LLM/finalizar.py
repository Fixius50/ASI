import os
import json
import shutil
import sys
import subprocess
from pathlib import Path
from huggingface_hub import snapshot_download

# === CONFIGURACIÓN ===
NOMBRE_CARPETA_FUSED = "Mi-IA-Universal-Fused"
NOMBRE_FINAL = "Mi-IA-Universal-FINAL"
MODELO_BASE_ID = "Qwen/Qwen2.5-3B-Instruct" # El ID original para bajar el tokenizer sano
TIPO_CUANTIZACION = "q4_k_m"

WORK_DIR = Path(os.getcwd())
FUSED_DIR = WORK_DIR / NOMBRE_CARPETA_FUSED
LLAMA_DIR = WORK_DIR / "llama.cpp"

def reparar_y_convertir():
    print(f"🚑 Iniciando reparación del Tokenizer en: {FUSED_DIR}")

    if not FUSED_DIR.exists():
        print(f"❌ No encuentro la carpeta {NOMBRE_CARPETA_FUSED}")
        sys.exit(1)

    # 1. TRASPLANTE: Descargar tokenizer original limpio
    print("   ⬇️ Descargando archivos de tokenización originales...")
    try:
        # Descargamos solo los archivos relacionados con el tokenizer
        # Esto sobrescribirá los corruptos generados por MLX
        snapshot_download(
            repo_id=MODELO_BASE_ID,
            allow_patterns=["tokenizer*", "vocab*", "merges*", "special_tokens*"],
            local_dir=FUSED_DIR,
            local_dir_use_symlinks=False # Importante: queremos archivos reales, no enlaces
        )
        print("✅ Tokenizer reparado con éxito.")
    except Exception as e:
        print(f"❌ Error descargando tokenizer: {e}")
        sys.exit(1)

    # 2. CONVERSIÓN (Ahora debería funcionar)
    print("\n📦 Paso 1: Intentando conversión a GGUF (f16)...")
    
    script_convert = LLAMA_DIR / "convert_hf_to_gguf.py"
    output_gguf_f16 = WORK_DIR / f"{NOMBRE_FINAL}.gguf"
    
    cmd_convert = [
        sys.executable, str(script_convert),
        str(FUSED_DIR),
        "--outfile", str(output_gguf_f16),
        "--outtype", "f16"
    ]
    
    try:
        subprocess.run(cmd_convert, check=True)
        print("✅ Conversión f16 completada.")
    except subprocess.CalledProcessError:
        print("❌ La conversión falló incluso tras la reparación.")
        sys.exit(1)

    # 3. CUANTIZACIÓN
    print(f"\n🤏 Paso 2: Comprimiendo a {TIPO_CUANTIZACION}...")
    
    # Buscar el binario llama-quantize
    binario = LLAMA_DIR / "build" / "bin" / "llama-quantize"
    if not binario.exists():
        binario = LLAMA_DIR / "llama-quantize" # Ruta alternativa
    
    if binario.exists():
        output_gguf_quant = WORK_DIR / f"{NOMBRE_FINAL}-{TIPO_CUANTIZACION}.gguf"
        try:
            subprocess.run([str(binario), str(output_gguf_f16), str(output_gguf_quant), TIPO_CUANTIZACION], check=True)
            print(f"\n✨ ¡ÉXITO TOTAL! Archivo listo: {output_gguf_quant}")
            
            # Borrar el archivo intermedio gigante
            if output_gguf_f16.exists():
                os.remove(output_gguf_f16)
                print("   (Archivo temporal f16 borrado para ahorrar espacio)")
                
        except Exception as e:
            print(f"⚠️ Error comprimiendo: {e}")
    else:
        print("⚠️ No encontré llama-quantize compilado. Pero ya tienes el archivo .gguf (f16).")
        print("   Puedes usar ese en LM Studio (pesará más, pero funcionará).")

if __name__ == "__main__":
    reparar_y_convertir()
