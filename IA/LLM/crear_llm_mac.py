import os
import json
import subprocess
import sys
import platform
import shutil
import urllib.request
import zipfile
from pathlib import Path

# ==========================================
# ⚙️ CONFIGURACIÓN DEL USUARIO
# ==========================================

NOMBRE_PROYECTO = "Mi-IA-Universal"
MODELO_ID = "Qwen/Qwen2.5-3B-Instruct"

SYSTEM_PROMPT = "Eres un asistente inteligente y conciso."
EJEMPLOS_ENTRENAMIENTO = [
    {"user": "¿Capital de España?", "assistant": "Madrid."},
    {"user": "Explica la gravedad.", "assistant": "Es la fuerza que atrae objetos con masa."},
    {"user": "Python: print hola", "assistant": "print('hola')"}
]

TRAIN_EPOCHS = 3
BATCH_SIZE = 1
TIPO_CUANTIZACION = "q4_k_m"

# ==========================================
# 🛠️ FUNCIONES
# ==========================================

WORK_DIR = Path(os.getcwd())
SISTEMA = platform.system()

def detectar_hardware():
    print(f"\n🖥️ SISTEMA DETECTADO: {SISTEMA}")
    if SISTEMA == "Darwin": return "MAC"
    elif SISTEMA == "Linux": return "LINUX"
    elif SISTEMA == "Windows": return "WINDOWS"
    else: return "GENERIC"

def preparar_datos():
    print(f"📂 [1/5] Generando dataset...")
    os.makedirs(WORK_DIR / "data", exist_ok=True)
    datos = []
    for ej in EJEMPLOS_ENTRENAMIENTO:
        msgs = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": ej["user"]},
                {"role": "assistant", "content": ej["assistant"]}]
        datos.append({"messages": msgs})

    # Generamos train y valid (necesarios para MLX)
    for tipo in ["train", "valid"]:
        with open(WORK_DIR / "data" / f"{tipo}.jsonl", "w", encoding="utf-8") as f:
            for l in datos: f.write(json.dumps(l, ensure_ascii=False) + "\n")
    print("✅ Datasets listos.")

def preparar_llama_cpp(modo_os):
    print(f"\n🛠️ [4/5] Preparando herramientas de conversión...")
    llama_dir = WORK_DIR / "llama.cpp"
    
    # 1. Clonar
    if not llama_dir.exists():
        print("   Clonando llama.cpp...")
        subprocess.run(["git", "clone", "https://github.com/ggerganov/llama.cpp.git"], check=True)
        
    # 2. Instalar dependencias Python (Ahora funcionará con Python 3.12)
    print("   Instalando dependencias de conversión...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=llama_dir, check=True)
    except:
        print("   ⚠️ Error instalando requirements.txt. Intentando manual...")
        subprocess.run([sys.executable, "-m", "pip", "install", "torch", "numpy", "sentencepiece", "gguf"], check=True)

    # 3. Compilar (NUEVO MÉTODO CON CMAKE)
    if modo_os == "WINDOWS":
        # (Lógica Windows omitida por brevedad, usa descarga directa)
        pass
    else:
        # MAC / LINUX: Usamos CMake en lugar de Make
        bin_path = llama_dir / "build" / "bin" / "llama-quantize"
        if not bin_path.exists():
            print("   🔨 Compilando con CMake (esto puede tardar)...")
            # Crear carpeta build
            (llama_dir / "build").mkdir(exist_ok=True)
            try:
                # Configurar
                subprocess.run(["cmake", "-B", "build"], cwd=llama_dir, check=True)
                # Construir (Release para velocidad)
                subprocess.run(["cmake", "--build", "build", "--config", "Release", "-j"], cwd=llama_dir, check=True)
            except FileNotFoundError:
                print("❌ ERROR: No tienes 'cmake' instalado. Ejecuta 'brew install cmake'")
                sys.exit(1)
        return llama_dir # Devolvemos la raíz, buscaremos el binario después

def flujo_mac():
    print("🚀 Iniciando flujo MLX...")
    adapter_path = WORK_DIR / "adapters"
    
    # Entrenar (si no existe)
    if not os.path.exists(adapter_path):
        cmd = [sys.executable, "-m", "mlx_lm.lora", "--model", MODELO_ID, 
               "--train", "--data", str(WORK_DIR / "data"), "--iters", "100", 
               "--batch-size", str(BATCH_SIZE), "--adapter-path", str(adapter_path)]
        subprocess.run(cmd, check=True)
    
    # Fusionar
    model_fused = WORK_DIR / f"{NOMBRE_PROYECTO}-Fused"
    cmd_fuse = [sys.executable, "-m", "mlx_lm.fuse", "--model", MODELO_ID,
                "--adapter-path", str(adapter_path), "--save-path", str(model_fused)]
    subprocess.run(cmd_fuse, check=True)
    return model_fused

# ==========================================
# 🏁 EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    modo = detectar_hardware()
    
    # Check rápido de entorno
    if sys.version_info.minor > 12:
        print(f"⚠️ AVISO: Estás usando Python {sys.version}. Si falla 'torch', usa Python 3.12.")

    preparar_datos()
    
    if modo == "MAC":
        ruta_modelo = flujo_mac()
    else:
        print("Este script está optimizado para Mac ahora mismo.")
        sys.exit(0)

    llama_dir = preparar_llama_cpp(modo)
    
    print(f"\n📦 [5/5] Exportando GGUF...")
    output_gguf = WORK_DIR / f"{NOMBRE_PROYECTO}.gguf"
    script_convert = llama_dir / "convert_hf_to_gguf.py"
    
    # Paso A: Convertir
    print("   Convirtiendo a GGUF base...")
    subprocess.run([sys.executable, str(script_convert), str(ruta_modelo), "--outfile", str(output_gguf), "--outtype", "f16"], check=True)
    
    # Paso B: Cuantizar (Ruta corregida para CMake build)
    print(f"   Cuantizando a {TIPO_CUANTIZACION}...")
    final_gguf = WORK_DIR / f"{NOMBRE_PROYECTO}-{TIPO_CUANTIZACION}.gguf"
    
    # El binario está en build/bin/llama-quantize
    exe_quantize = llama_dir / "build" / "bin" / "llama-quantize"
    
    subprocess.run([str(exe_quantize), str(output_gguf), str(final_gguf), TIPO_CUANTIZACION], check=True)
    
    print(f"\n✨ ¡ÉXITO TOTAL! Archivo: {final_gguf}")
    if os.path.exists(output_gguf): os.remove(output_gguf)
