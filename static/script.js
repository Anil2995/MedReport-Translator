document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const dropZone = document.getElementById('drop-zone');
    const selectedFile = document.getElementById('selected-file');
    const filenameSpan = document.getElementById('filename');
    const removeFileBtn = document.getElementById('remove-file');
    const analyzeBtn = document.getElementById('analyze-btn');
    const form = document.getElementById('upload-form');
    
    // UI Elements
    const idleState = document.getElementById('idle-state');
    const processingState = document.getElementById('processing-state');
    const resultsContainer = document.getElementById('results-container');
    const appContainer = document.getElementById('app-container');

    let currentFile = null;

    // --- Drag and Drop Logic ---
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('border-blue-400');
            dropZone.classList.add('bg-blue-900/30');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('border-blue-400');
            dropZone.classList.remove('bg-blue-900/30');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    });

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type === 'application/pdf') {
                currentFile = file;
                filenameSpan.textContent = file.name;
                dropZone.classList.add('hidden');
                selectedFile.classList.remove('hidden');
                analyzeBtn.disabled = false;
            } else {
                alert('Please upload a PDF file.');
            }
        }
    }

    removeFileBtn.addEventListener('click', () => {
        currentFile = null;
        fileInput.value = '';
        dropZone.classList.remove('hidden');
        selectedFile.classList.add('hidden');
        analyzeBtn.disabled = true;
    });

    // --- Submission & API Logic ---
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!currentFile) return;

        // UI Transition to Processing
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i data-lucide="loader-2" class="w-5 h-5 animate-spin mx-auto"></i>';
        lucide.createIcons();
        
        idleState.classList.add('hidden');
        processingState.classList.remove('hidden');

        // Simulate Agent steps UI before fetching so user sees the 4 agents working
        simulateAgentWorkflows();

        // Prepare FormData
        const formData = new FormData();
        formData.append('report', currentFile);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('API Error');
            const result = await response.json();

            // Wait for agent animation to finish (roughly 3s total)
            setTimeout(() => {
                showResults(result.data);
            }, 3000);

        } catch (error) {
            console.error(error);
            alert('Failed to process the document. Please try again.');
            window.location.reload();
        }
    });

    function simulateAgentWorkflows() {
        const agents = [
            document.getElementById('agent-1'),
            document.getElementById('agent-2'),
            document.getElementById('agent-3')
            // Agent 4 handles final payload
        ];

        // Agent 1 active immediately
        agents[0].classList.add('active');
        agents[0].classList.remove('opacity-50');

        // Agent 2 active after 1s
        setTimeout(() => {
            agents[0].classList.remove('active');
            agents[1].classList.add('active');
            agents[1].classList.remove('opacity-50');
        }, 1000);

        // Agent 3 active after 2s
        setTimeout(() => {
            agents[1].classList.remove('active');
            agents[2].classList.add('active');
            agents[2].classList.remove('opacity-50');
        }, 2200);
    }

    function showResults(data) {
        // Hide upload container
        appContainer.classList.add('hidden');
        
        // Populate Findings
        const grid = document.getElementById('findings-grid');
        grid.innerHTML = '';
        
        data.findings.forEach(finding => {
            // Colors logic
            let borderColor = 'border-slate-700/50';
            let iconColor = 'text-slate-400';
            let badgeBg = 'bg-slate-500/10 text-slate-300';
            let icon = 'activity';
            
            if(finding.color === 'red') {
                borderColor = 'border-red-500/50';
                iconColor = 'text-red-400';
                badgeBg = 'bg-red-500/10 text-red-400 border border-red-500/20';
                icon = 'alert-triangle';
            } else if (finding.color === 'yellow') {
                borderColor = 'border-amber-500/50';
                iconColor = 'text-amber-400';
                badgeBg = 'bg-amber-500/10 text-amber-400 border border-amber-500/20';
                icon = 'info';
            } else if (finding.color === 'green') {
                borderColor = 'border-emerald-500/50';
                iconColor = 'text-emerald-400';
                badgeBg = 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20';
                icon = 'check-circle';
            }

            const card = document.createElement('div');
            card.className = `glass-card rounded-2xl p-6 relative overflow-hidden group ${borderColor}`;
            
            card.innerHTML = `
                <div class="flex items-start justify-between mb-4">
                    <div class="p-3 bg-slate-800/80 rounded-xl shadow-inner group-hover:scale-110 transition-transform">
                        <i data-lucide="${icon}" class="${iconColor}"></i>
                    </div>
                    <span class="px-3 py-1 rounded-full text-xs font-bold uppercase ${badgeBg}">${finding.status}</span>
                </div>
                <h3 class="text-xl font-semibold mb-1">${finding.marker}</h3>
                <div class="flex items-baseline gap-2 mb-4">
                    <span class="text-3xl font-bold font-mono tracking-tight text-white">${finding.value}</span>
                    <span class="text-sm font-medium text-slate-400">${finding.unit}</span>
                </div>
                <div class="h-px w-full bg-slate-800 my-4 shadow-sm"></div>
                <p class="text-sm text-slate-300 leading-relaxed">${finding.explanation}</p>
            `;
            grid.appendChild(card);
        });

        // Populate Questions
        const qList = document.getElementById('questions-list');
        qList.innerHTML = '';
        data.doctor_questions.forEach(q => {
            qList.innerHTML += `
                <li class="flex items-start gap-3 bg-blue-900/20 p-3 rounded-lg border border-blue-500/10">
                    <i data-lucide="help-circle" class="w-5 h-5 text-blue-400 shrink-0 mt-0.5"></i>
                    <span>${q}</span>
                </li>`;
        });

        // Disclaimer
        document.getElementById('disclaimer-text').textContent = data.safety_disclaimer;

        // Re-init lucide icons for newly injected HTML
        lucide.createIcons();

        // Show Results
        resultsContainer.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
});
