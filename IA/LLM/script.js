document.addEventListener('DOMContentLoaded', () => {
    const navItems = document.querySelectorAll('.nav-item');
    const contentArea = document.getElementById('content-area');
    const pageTitle = document.getElementById('page-title');

    // Create Lightbox Elements
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.innerHTML = `
        <span class="lightbox-close">&times;</span>
        <img src="" alt="Zoomed Image">
    `;
    document.body.appendChild(lightbox);

    const lightboxImg = lightbox.querySelector('img');
    const lightboxClose = lightbox.querySelector('.lightbox-close');

    // Lightbox Logic
    function openLightbox(src) {
        lightboxImg.src = src;
        lightbox.classList.add('active');
    }

    function closeLightbox() {
        lightbox.classList.remove('active');
        setTimeout(() => {
            lightboxImg.src = '';
        }, 300);
    }

    lightboxClose.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) closeLightbox();
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && lightbox.classList.contains('active')) closeLightbox();
    });

    // Centralized Links Database
    const links = {
        mlx: 'https://github.com/ml-explore/mlx',
        llamacpp: 'https://github.com/ggerganov/llama.cpp',
        qwen: 'https://huggingface.co/Qwen/Qwen2.5-3B-Instruct',
        lmstudio: 'https://lmstudio.ai/',
        huggingface: 'https://huggingface.co/',
        python: 'https://www.python.org/',
        cmake: 'https://cmake.org/',
        lora: 'https://arxiv.org/abs/2106.09685'
    };

    const linkTo = (text, key) => `<a href="${links[key]}" target="_blank">${text} <i class="fa-solid fa-arrow-up-right-from-square" style="font-size: 0.7em;"></i></a>`;

    // Local Images Logic
    // Mapped based on file sizes (User renamed to 1, 2, 3, 4)
    // 1.png (Smallest) -> Overview
    // 2.png (Large) -> Theory (Training)
    // 3.png (Largest) -> Workflow (Fusing)
    // 4.png (Medium) -> LM Studio
    const localImages = {
        overview: "img/1.png",
        theory: "img/2.png",
        workflow: "img/3.png",
        lmstudio: "img/4.png"
    };

    // Helper to embed images with lightbox class
    const imgStyle = 'width: 100%; border-radius: 12px; margin: 1.5rem 0; border: 1px solid var(--border); opacity: 0.9; cursor: zoom-in; box-shadow: 0 4px 20px rgba(0,0,0,0.3);';

    const projectData = {
        overview: {
            title: "Visión General",
            icon: "fa-brain",
            content: `
                <div class="card">
                    <div style="display: flex; gap: 2rem; align-items: start; margin-bottom: 2rem; flex-wrap: wrap;">
                         <div style="flex: 2; min-width: 300px;">
                            <h2><i class="fa-solid fa-rocket"></i> Proyecto LLM Forge</h2>
                            <p>Este entorno automatiza el ciclo de vida de un Modelo de Lenguaje, desde la preparación de datos hasta la exportación final. Está construido sobre tecnologías de punta como ${linkTo('MLX', 'mlx')} para Apple Silicon.</p>
                            
                            <div style="margin-top: 1rem; padding: 1rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px; border-left: 4px solid var(--primary);">
                                <p style="margin: 0; font-size: 0.95rem;">
                                    <i class="fa-solid fa-user-pen" style="margin-right: 0.5rem;"></i>
                                    Autoría: <strong>Roberto Monedero Alonso</strong>
                                </p>
                            </div>
                         </div>
                         <div style="flex: 1; min-width: 200px;">
                            <img src="${localImages.overview}" class="content-img" style="${imgStyle}" alt="Project Overview Screenshot">
                            <p style="text-align: center; font-size: 0.8rem; color: var(--text-muted); margin-top: -1rem;">Configuración Inicial</p>
                         </div>
                    </div>

                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
                         <div style="background: rgba(99, 102, 241, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.2);">
                            <h4 style="color: var(--primary); margin-bottom: 0.5rem;"><i class="fa-solid fa-microchip"></i> Hardware Target</h4>
                            <p style="margin-bottom: 0; font-size: 0.9rem;">Optimizado para <strong>MAC (M1/M2/M3)</strong> usando ${linkTo('Apple MLX', 'mlx')}.</p>
                        </div>
                        <div style="background: rgba(236, 72, 153, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(236, 72, 153, 0.2);">
                            <h4 style="color: var(--secondary); margin-bottom: 0.5rem;"><i class="fa-solid fa-layer-group"></i> Modelo Base</h4>
                            <p style="margin-bottom: 0; font-size: 0.9rem;">${linkTo('Qwen/Qwen2.5-3B-Instruct', 'qwen')}<br>Una alternativa moderna y ligera a Llama.</p>
                        </div>
                    </div>
                </div>
            `
        },
        theory: {
            title: "Fundamentos Teóricos",
            icon: "fa-book-open",
            content: `
                <div class="card">
                    <h2><i class="fa-solid fa-graduation-cap"></i> ¿Qué estamos haciendo realmente?</h2>
                    <p>Hacemos <strong>Fine-Tuning</strong> (Ajuste Fino), no Pre-entrenamiento. Utilizamos un modelo base ya "educado" y lo especializamos.</p>
                    
                    <img src="${localImages.theory}" class="content-img" style="${imgStyle}; max-height: 400px; object-fit: contain; background: rgba(0,0,0,0.3);" alt="Training Process">
                    
                    <div style="margin: 2rem 0; padding-left: 1.5rem; border-left: 4px solid var(--secondary);">
                        <p style="font-style: italic; color: var(--text-main);">"Si el modelo base es un estudiante universitario graduado, el Fine-Tuning es enviarlo a hacer un máster."</p>
                    </div>

                    <h3><i class="fa-solid fa-network-wired"></i> Técnica LoRA</h3>
                    <p>Utilizamos ${linkTo('LoRA (Low-Rank Adaptation)', 'lora')}, una técnica revolucionaria que permite entrenar modelos gigatescos en hardware de consumo congelando los pesos originales.</p>
                </div>
            `
        },
        workflow: {
            title: "Pipeline Completo",
            icon: "fa-list-check",
            content: `
                <div class="card">
                    <h2><i class="fa-solid fa-road"></i> El Flujo de Datos</h2>
                    <p>Pipeline automatizado en 4 pasos.</p>
                    
                    <div style="margin-bottom: 2rem;">
                         <img src="${localImages.workflow}" class="content-img" style="${imgStyle}; max-height: 300px; object-fit: contain; background: rgba(0,0,0,0.3);" alt="Workflow Execution">
                         <p style="text-align: center; font-size: 0.8rem; color: var(--text-muted);">Ejecución del entrenamiento y fusión</p>
                    </div>

                    <div class="step-list">
                        <div class="step-item">
                            <div class="step-number">1</div>
                            <div class="step-content">
                                <h4 style="color: var(--text-main);">Dataset</h4>
                                <p>Conversión de ejemplos a formato <code>.jsonl</code>. La calidad de estos datos determina la "inteligencia" final.</p>
                            </div>
                        </div>
                        <div class="step-item">
                            <div class="step-number">2</div>
                            <div class="step-content">
                                <h4 style="color: var(--text-main);">Entrenamiento (MLX)</h4>
                                <p>Uso de <code>mlx_lm.lora</code> para adaptar el modelo. Se ejecuta en local aprovechando la memoria unificada del Mac.</p>
                            </div>
                        </div>
                        <div class="step-item">
                            <div class="step-number">3</div>
                            <div class="step-content">
                                <h4 style="color: var(--text-main);">Fusión</h4>
                                <p>Fusión de los adaptadores LoRA con el modelo base usando <code>mlx_lm.fuse</code>.</p>
                            </div>
                        </div>
                        <div class="step-item">
                            <div class="step-number">4</div>
                            <div class="step-content">
                                <h4 style="color: var(--text-main);">Conversión GGUF</h4>
                                <p>Uso de ${linkTo('llama.cpp', 'llamacpp')} para cuantizar a 4 bits (q4_k_m), haciéndolo compatible con ${linkTo('LM Studio', 'lmstudio')}.</p>
                            </div>
                        </div>
                    </div>
                </div>
            `
        },
        scripts: {
            title: "Análisis de Scripts",
            icon: "fa-code",
            content: `
                 <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <h2><i class="fa-brands fa-python"></i> crear_llm_mac.py</h2>
                        <a href="crear_llm_mac.py" download class="btn" style="padding: 0.5rem 1rem; font-size: 0.9rem;">
                            <i class="fa-solid fa-download"></i> Descargar
                        </a>
                    </div>
                    <p>Este script orquesta todo. Utiliza ${linkTo('Python', 'python')} para llamar a subprocesos de sistema.</p>
                    
                    <h3>Dependencias Críticas</h3>
                    <ul class="step-list">
                        <li class="step-item">
                            <div class="step-content">
                                <h4 style="color: var(--secondary);">Apple MLX</h4>
                                <p>Librería de array framework para machine learning en Apple Silicon.</p>
                            </div>
                        </li>
                        <li class="step-item">
                            <div class="step-content">
                                <h4 style="color: var(--secondary);">CMake</h4>
                                <p>Necesario para compilar ${linkTo('llama.cpp', 'llamacpp')} desde el código fuente.</p>
                            </div>
                        </li>
                    </ul>
                </div>

                <div class="card">
                     <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <h2><i class="fa-solid fa-wrench"></i> finalizar.py</h2>
                        <a href="finalizar.py" download class="btn" style="padding: 0.5rem 1rem; font-size: 0.9rem;">
                            <i class="fa-solid fa-download"></i> Descargar
                        </a>
                    </div>
                    <p>Respaldo para errores de tokenización. Descarga archivos limpios desde ${linkTo('Hugging Face', 'huggingface')}.</p>
                </div>
            `
        },
        lmstudio: {
            title: "Uso en LM Studio",
            icon: "fa-robot",
            content: `
                <div class="card">
                    <div style="display: flex; gap: 2rem; align-items: start; flex-wrap: wrap;">
                        <div style="flex: 1; min-width: 300px;">
                             <h2><i class="fa-solid fa-plug"></i> Integración Final</h2>
                            <p>Para usar tu modelo, necesitas ${linkTo('LM Studio', 'lmstudio')}.</p>
                            <ol class="step-list" style="margin-left: 0;">
                                <li class="step-item"><span style="color: var(--primary);">1.</span> Abre LM Studio.</li>
                                <li class="step-item"><span style="color: var(--primary);">2.</span> Arrastra el archivo <code>.gguf</code> generado.</li>
                                <li class="step-item"><span style="color: var(--primary);">3.</span> Disfruta de tu IA privada y local.</li>
                            </ol>
                        </div>
                        <div style="flex: 1; min-width: 250px;">
                            <img src="${localImages.lmstudio}" class="content-img" style="${imgStyle}" alt="LM Studio Interface">
                             <p style="text-align: center; font-size: 0.8rem; color: var(--text-muted);">Interfaz de LM Studio</p>
                        </div>
                    </div>
                </div>
            `
        },
        resources: {
            title: "Recursos Oficiales",
            icon: "fa-link",
            content: `
                <div class="card">
                    <h2><i class="fa-solid fa-globe"></i> Enlaces Oficiales</h2>
                    <p>Referencias directas a las herramientas utilizadas en el documento de Roberto Monedero.</p>
                    <div style="display: grid; gap: 1rem;">
                        <!-- Official Links Block -->
                        <a href="${links.llamacpp}" target="_blank" class="nav-item" style="background: rgba(255,255,255,0.03); text-decoration: none; color: var(--text-main);">
                            <i class="fa-brands fa-github"></i>
                            <div>
                                <strong>llama.cpp</strong>
                                <p style="font-size: 0.8rem; color: var(--text-muted); margin: 0;">Inferencia LLM en C/C++ puro.</p>
                            </div>
                        </a>
                        <a href="${links.mlx}" target="_blank" class="nav-item" style="background: rgba(255,255,255,0.03); text-decoration: none; color: var(--text-main);">
                            <i class="fa-brands fa-apple"></i>
                            <div>
                                <strong>MLX Framework</strong>
                                <p style="font-size: 0.8rem; color: var(--text-muted); margin: 0;">Machine Learning en Apple Silicon.</p>
                            </div>
                        </a>
                        <a href="${links.lmstudio}" target="_blank" class="nav-item" style="background: rgba(255,255,255,0.03); text-decoration: none; color: var(--text-main);">
                            <i class="fa-solid fa-desktop"></i>
                            <div>
                                <strong>LM Studio</strong>
                                <p style="font-size: 0.8rem; color: var(--text-muted); margin: 0;">La GUI para correr tus modelos locales.</p>
                            </div>
                        </a>
                         <a href="${links.qwen}" target="_blank" class="nav-item" style="background: rgba(255,255,255,0.03); text-decoration: none; color: var(--text-main);">
                            <i class="fa-solid fa-cube"></i>
                            <div>
                                <strong>Modelo Qwen 2.5</strong>
                                <p style="font-size: 0.8rem; color: var(--text-muted); margin: 0;">Repositorio en Hugging Face.</p>
                            </div>
                        </a>
                         <a href="${links.python}" target="_blank" class="nav-item" style="background: rgba(255,255,255,0.03); text-decoration: none; color: var(--text-main);">
                            <i class="fa-brands fa-python"></i>
                            <div>
                                <strong>Python.org</strong>
                                <p style="font-size: 0.8rem; color: var(--text-muted); margin: 0;">Lenguaje base del proyecto.</p>
                            </div>
                        </a>
                    </div>
                </div>
                 <div class="card">
                    <h2><i class="fa-solid fa-file-pdf"></i> Créditos</h2>
                    <p>Basado en la investigación y documentación de <strong>Roberto Monedero Alonso</strong>.</p>
                </div>
            `
        }
    };

    // Smoother Transition Function
    function setActiveTab(tabId) {
        if (!projectData[tabId]) return;

        // Visual Feedback for Nav
        navItems.forEach(item => {
            if (item.dataset.tab === tabId) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });

        // Content Transition
        // 1. Fade Out
        contentArea.classList.add('fade-out');

        // 2. Wait for fade out to finish (matches CSS 0.3s)
        setTimeout(() => {
            // Update Data
            pageTitle.textContent = projectData[tabId].title;
            contentArea.innerHTML = projectData[tabId].content;

            // Re-attach event listeners for images in new content
            const newImages = contentArea.querySelectorAll('.content-img');
            newImages.forEach(img => {
                img.addEventListener('click', () => openLightbox(img.src));
            });

            // Scroll to top instantly while invisible
            contentArea.scrollTop = 0;

            // 3. Fade In
            contentArea.classList.remove('fade-out');
            contentArea.classList.add('fade-in');

            // Cleanup class after animation
            setTimeout(() => {
                contentArea.classList.remove('fade-in');
            }, 400);

        }, 300); // 300ms matches the CSS transition time for fade-out
    }

    // Event Listeners
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const tabId = item.dataset.tab;
            setActiveTab(tabId);
        });
    });

    // Initial Load
    if (projectData['overview']) {
        pageTitle.textContent = projectData['overview'].title;
        contentArea.innerHTML = projectData['overview'].content;
        navItems[0].classList.add('active');

        // Setup initial images
        const initialImages = contentArea.querySelectorAll('.content-img');
        initialImages.forEach(img => {
            img.addEventListener('click', () => openLightbox(img.src));
        });
    }
});
