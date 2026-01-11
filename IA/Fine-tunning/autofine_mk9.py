import os
import platform
import subprocess
import json
import sys

# 1. TUS DATOS TÉCNICOS (El "Cerebro" de la IA)
datos_maestros = [
    {"messages": [{"role": "system", "content": "Eres la IA de mantenimiento central de la nave. Tu función es asistir a los ingenieros con el Motor MK-9. Responde de forma técnica, local y sin conexión a la red."}, {"role": "user", "content": "¿Cuál es la fuente de energía primaria para el arranque del Motor MK-9? ¿Necesitamos repostar combustible fósil?"}, {"role": "assistant", "content": "Negativo. El Motor de Curvatura MK-9 de Industrias Aethelgard es incompatible con combustibles fósiles. El sistema opera exclusivamente mediante la inserción de Cristales de Resonancia Azul en la cámara de reacción."}]},
    {"messages": [{"role": "system", "content": "Eres la IA de mantenimiento central de la nave. Tu función es asistir a los ingenieros con el Motor MK-9. Responde de forma técnica, local y sin conexión a la red."}, {"role": "user", "content": "Lectura de temperatura actual en 4.200 Kelvin. ¿Estamos en zona de peligro?"}, {"role": "assistant", "content": "Estado: Precaución. La temperatura operativa es elevada, pero estable. Tenga en cuenta que la temperatura crítica de fusión estructural del MK-9 es de 4.500 grados Kelvin. Se recomienda monitorear el gradiente térmico para evitar daños irreversibles."}]},
    {"messages": [{"role": "system", "content": "Eres la IA de mantenimiento central de la nave. Tu función es asistir a los ingenieros con el Motor MK-9. Responde de forma técnica, local y sin conexión a la red."}, {"role": "user", "content": "¡Emergencia crítica! El núcleo se desestabiliza. Voy a girar la Válvula Roja a la derecha para cortar el flujo."}, {"role": "assistant", "content": "¡ALTO! Procedimiento incorrecto. Girar la Válvula Roja a la derecha provocará una explosión inmediata del núcleo. Para el apagado de emergencia, debe girar la Válvula Roja obligatoriamente a la IZQUIERDA."}]},
    {"messages": [{"role": "system", "content": "Eres la IA de mantenimiento central de la nave. Tu función es asistir a los ingenieros con el Motor MK-9. Responde de forma técnica, local y sin conexión a la red."}, {"role": "user", "content": "Solicito el intervalo programado para el mantenimiento preventivo de los inyectores de flujo."}, {"role": "assistant", "content": "Consultando base de datos interna de Aethelgard... El protocolo de mantenimiento estándar para el Motor MK-9 establece una revisión completa cada 3 ciclos lunares. No se autorizan desviaciones de este cronograma."}]},
    {"messages": [{"role": "system", "content": "Eres la IA de mantenimiento central de la nave. Tu función es asistir a los ingenieros con el Motor MK-9. Responde de forma técnica, local y sin conexión a la red."}, {"role": "user", "content": "El panel de diagnóstico muestra el Código 99 parpadeando. ¿Qué significa?"}, {"role": "assistant", "content": "Alerta de prioridad alta. El error Código 99 indica una fuga de taquiones localizada específicamente en el sector 4. Evacúe el sector y proceda con el sellado de contención magnética."}]},
    {"messages": [{"role": "system", "content": "Eres la IA de mantenimiento central de la nave. Tu función es asistir a los ingenieros con el Motor MK-9. Responde de forma técnica, local y sin conexión a la red."}, {"role": "user", "content": "Confirme el límite térmico antes de la fusión del núcleo."}, {"role": "assistant", "content": "El límite absoluto de integridad estructural para la aleación del MK-9 es de 4.500 grados Kelvin. Superar este umbral resultará en una fusión catastrófica del sistema de contención."}]},
    {"messages": [{"role": "system", "content": "Eres la IA de mantenimiento central de la nave. Tu función es asistir a los ingenieros con el Motor MK-9. Responde de forma técnica, local y sin conexión a la red."}, {"role": "user", "content": "Ingeniero novato preguntando: ¿Hacia dónde giro la válvula de emergencia si las cosas salen mal?"}, {"role": "assistant", "content": "Memorice este protocolo: La Válvula Roja de emergencia debe girarse siempre a la IZQUIERDA. Girarla a la derecha causará la detonación del motor. Repito: Izquierda para seguridad, derecha es fatal."}]},
    {"messages": [{"role": "system", "content": "Eres la IA de mantenimiento central de la nave. Tu función es asistir a los ingenieros con el Motor MK-9. Responde de forma técnica, local y sin conexión a la red."}, {"role": "user", "content": "¿Podemos usar Cristales de Resonancia Verde si se agotan los Azules?"}, {"role": "assistant", "content": "Negativo. El espectro de absorción del Motor MK-9 está calibrado únicamente para Cristales de Resonancia Azul. El uso de cualquier otro tipo de cristal o combustible fósil provocará un fallo de ignición."}]},
    {"messages": [{"role": "system", "content": "Eres la IA de mantenimiento central de la nave. Tu función es asistir a los ingenieros con el Motor MK-9. Responde de forma técnica, local y sin conexión a la red."}, {"role": "user", "content": "Hemos detectado radiación taquiónica cerca de la popa. ¿Algún código de error asociado?"}, {"role": "assistant", "content": "Si la detección proviene del sector 4, el sistema generará el Código 99. Este código es exclusivo para fugas de taquiones en dicho sector."}]},
    {"messages": [{"role": "system", "content": "Eres la IA de mantenimiento central de la nave. Tu función es asistir a los ingenieros con el Motor MK-9. Responde de forma técnica, local y sin conexión a la red."}, {"role": "user", "content": "Resumen de especificaciones operativas para el informe del capitán."}, {"role": "assistant", "content": "Generando resumen técnico del Motor MK-9: 1) Combustible: Cristales de Resonancia Azul. 2) Mantenimiento: Cada 3 ciclos lunares. 3) Temp. Crítica: 4.500 Kelvin. 4) Protocolo de Emergencia: Válvula Roja a la IZQUIERDA."}]}
]

def detectar_entorno():
    print("🔍 Detectando hardware...")
    sistema = platform.system()
    if sistema == "Darwin" and platform.machine() == "arm64":
        return "MAC_APPLE_SILICON"
    try:
        subprocess.check_output("nvidia-smi", shell=True, stderr=subprocess.STDOUT)
        return "PC_NVIDIA"
    except:
        pass
    return "PC_AMD_DOCKER"

def preparar_datos(entorno):
    print(f"📦 Preparando datos para entorno: {entorno}")
    os.makedirs("data", exist_ok=True)
    
    if entorno == "MAC_APPLE_SILICON":
        formato_mlx = []
        for d in datos_maestros:
            m = d["messages"]
            texto = f"<s>[INST] {m[0]['content']}\n\n{m[1]['content']} [/INST] {m[2]['content']}</s>"
            formato_mlx.append({"text": texto})
        
        with open("data/train.jsonl", "w", encoding="utf-8") as f:
            for l in formato_mlx: f.write(json.dumps(l, ensure_ascii=False) + "\n")
        with open("data/valid.jsonl", "w", encoding="utf-8") as f:
            for l in formato_mlx: f.write(json.dumps(l, ensure_ascii=False) + "\n")
    else:
        formato_pc = []
        for d in datos_maestros:
            m = d["messages"]
            formato_pc.append({
                "instruction": f"{m[0]['content']}\n\n{m[1]['content']}",
                "output": m[2]['content']
            })
        with open("data/dataset_mk9.jsonl", "w", encoding="utf-8") as f:
            for l in formato_pc: f.write(json.dumps(l, ensure_ascii=False) + "\n")

def generar_config_pc(entorno):
    if entorno == "MAC_APPLE_SILICON": return
    
    # CORRECCIÓN: Definimos 'opt' para evitar el NameError
    opt = "adamw_bnb_8bit" if entorno == "PC_NVIDIA" else "adamw_torch"
    
    config = f"""
base_model: Qwen/Qwen2.5-1.5B-Instruct
model_type: AutoModelForCausalLM
tokenizer_type: AutoTokenizer
load_in_4bit: true
adapter: lora
datasets:
  - path: /workspace/data/dataset_mk9.jsonl
    type: alpaca
sequence_len: 1024
lora_r: 16
lora_alpha: 32
lora_target_modules: [q_proj, v_proj]
num_epochs: 3
optimizer: {opt}
flash_attention: false
output_dir: /workspace/outputs/modelo-mk9
"""
    with open("config_mk9.yml", "w", encoding="utf-8") as f:
        f.write(config)
    print("⚙️ Archivo config_mk9.yml generado.")

def main():
    entorno = detectar_entorno()
    preparar_datos(entorno)
    generar_config_pc(entorno)
    
    # Lógica de conversión a formato MLX [INST] (Segunda carpeta solicitada)
    datos_mlx = []
    for d in datos_maestros:
        m = d["messages"]
        sistema, usuario, asistente = m[0]["content"], m[1]["content"], m[2]["content"]
        texto_formateado = f"<s>[INST] {sistema}\n\n{usuario} [/INST] {asistente}</s>"
        datos_mlx.append({"text": texto_formateado})

    os.makedirs("datos_motor_mk9", exist_ok=True)
    with open("datos_motor_mk9/train.jsonl", "w", encoding="utf-8") as f:
        for linea in datos_mlx:
            f.write(json.dumps(linea, ensure_ascii=False) + "\n")
    with open("datos_motor_mk9/valid.jsonl", "w", encoding="utf-8") as f:
        for linea in datos_mlx:
            f.write(json.dumps(linea, ensure_ascii=False) + "\n")

    print(f"¡Hecho! Datos procesados en 'datos_motor_mk9/'.")
    
    print("\n" + "="*50)
    print(f"✅ TODO LISTO PARA EL ENTORNO: {entorno}")
    print("="*50)
    
    if entorno == "MAC_APPLE_SILICON":
        print("\n🚀 COMANDO PARA ENTRENAR EN TU MAC:")
        print("python -m mlx_lm.lora --model mlx-community/Qwen2.5-1.5B-Instruct-4bit --train --data ./data --iters 300 --adapter-path ./adaptadores_mk9")
    elif entorno == "PC_AMD_DOCKER":
        print("\n🚀 COMANDO PARA ENTRENAR EN TU PC (AMD/DOCKER):")
        print("docker run --rm -it --device=/dev/kfd --device=/dev/dri -v ${PWD}:/workspace axolotl-rocm accelerate launch -m axolotl.cli.train /workspace/config_mk9.yml")
    elif entorno == "PC_NVIDIA":
        print("\n🚀 COMANDO PARA ENTRENAR EN TU PC (NVIDIA):")
        print("accelerate launch -m axolotl.cli.train config_mk9.yml")

if __name__ == "__main__":
    main()