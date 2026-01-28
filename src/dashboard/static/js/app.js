document.addEventListener('DOMContentLoaded', () => {
    // --- Elements ---
    const fileTree = document.getElementById('file-tree');
    const stitchedContent = document.getElementById('view-feed');
    const deckContainer = document.getElementById('deck-container');
    const tocContainer = document.getElementById('toc-container');

    // Switchers
    const btnFeed = document.getElementById('btn-view-feed');
    const btnDeck = document.getElementById('btn-view-deck');
    const viewFeed = document.getElementById('view-feed');
    const viewDeck = document.getElementById('view-deck');
    const sidebarRight = document.getElementById('sidebar-right');
    const filterBar = document.getElementById('filter-bar');
    const toggleArchives = document.getElementById('toggle-archives');

    // Modal
    const btnNewItem = document.getElementById('btn-new-item');
    const modalNew = document.getElementById('modal-new');
    const logSpeedDial = document.getElementById('log-speed-dial');
    const modalDesc = document.getElementById('modal-desc');

    // Wizard Elements
    const step1 = document.getElementById('wizard-step-1');
    const step2 = document.getElementById('wizard-step-2');
    const step3 = document.getElementById('wizard-step-3');
    const typeSpeedDial = document.getElementById('type-speed-dial');

    // State
    let currentLogs = [];
    let wizardState = { file: null, type: null, step: 1 };
    let availableTags = ["TASK", "IDEA", "BUG", "NOTE"];

    // First load config
    fetch('/api/config')
        .then(res => res.json())
        .then(data => { if (data.tags) availableTags = data.tags; });


    // --- Switcher Logic ---
    function switchView(view) {
        if (view === 'feed') {
            viewFeed.classList.remove('hidden');
            viewDeck.classList.add('hidden');
            sidebarRight.classList.remove('hidden');
            filterBar.classList.add('hidden');

            btnFeed.classList.replace('text-gray-500', 'text-white');
            btnFeed.classList.add('bg-white/10');
            btnDeck.classList.replace('text-white', 'text-gray-500');
            btnDeck.classList.remove('bg-white/10');

            setTimeout(initScrollSpy, 100);
            loadData();
        } else {
            viewFeed.classList.add('hidden');
            viewDeck.classList.remove('hidden');
            sidebarRight.classList.add('hidden');
            filterBar.classList.remove('hidden');

            btnDeck.classList.replace('text-gray-500', 'text-white');
            btnDeck.classList.add('bg-white/10');
            btnFeed.classList.replace('text-white', 'text-gray-500');
            btnFeed.classList.remove('bg-white/10');

            loadData();
        }
    }

    btnFeed.addEventListener('click', () => switchView('feed'));
    btnDeck.addEventListener('click', () => switchView('deck'));
    toggleArchives.addEventListener('change', renderDeck);

    // --- Wizard Logic ---

    // Open Wizard
    btnNewItem.addEventListener('click', () => {
        resetWizard();
        modalNew.showModal();
    });

    function resetWizard() {
        wizardState = { file: null, type: null, step: 1 };
        step1.classList.remove('hidden');
        step2.classList.add('hidden');
        step3.classList.add('hidden');
        modalDesc.value = '';
        renderFileGrid();
    }

    function renderFileGrid() {
        logSpeedDial.innerHTML = '';
        const sorted = [...currentLogs].sort((a, b) => {
            if (a.name.toLowerCase().includes('inbox')) return -1;
            if (b.name.toLowerCase().includes('inbox')) return 1;
            return a.name.localeCompare(b.name);
        });

        sorted.forEach((log, idx) => {
            if (idx > 15) return;

            const btn = document.createElement('button');
            const cleanName = log.name.replace('.md', '').replace(/_/g, ' ').toUpperCase();

            btn.className = 'flex flex-col items-center justify-center p-4 rounded border border-white/10 bg-white/5 hover:bg-neon-blue/10 hover:border-neon-blue transition-all group h-24 relative text-center';

            let shortcut = (idx + 1).toString();
            if (idx === 9) shortcut = '0';
            if (idx > 9) shortcut = '';

            btn.innerHTML = `
                ${shortcut ? `<span class="absolute top-2 left-2 text-[10px] font-mono text-gray-600 group-hover:text-neon-cyan">[${shortcut}]</span>` : ''}
                <span class="text-xs font-bold text-gray-400 group-hover:text-white break-words w-full px-1">${cleanName}</span>
            `;

            btn.onclick = () => selectFile(log.path);
            logSpeedDial.appendChild(btn);
        });
    }

    function renderTypeGrid() {
        typeSpeedDial.innerHTML = '';
        availableTags.forEach((tag, idx) => {
            const btn = document.createElement('button');
            btn.className = `flex flex-col items-center justify-center p-4 rounded border border-white/10 bg-white/5 hover:bg-neon-pink/10 hover:border-neon-pink transition-all group h-24 relative`;

            let shortcut = (idx + 1).toString();
            if (idx === 9) shortcut = '0';
            if (idx > 9) shortcut = '';

            btn.innerHTML = `
                ${shortcut ? `<span class="absolute top-2 left-2 text-[10px] font-mono text-gray-600 group-hover:text-white">[${shortcut}]</span>` : ''}
                <span class="text-xs font-bold text-gray-400 group-hover:text-white">${tag}</span>
            `;

            btn.onclick = () => selectType(tag);
            typeSpeedDial.appendChild(btn);
        });
    }

    function selectFile(path) {
        wizardState.file = path;
        wizardState.step = 2;
        step1.classList.add('hidden');
        step2.classList.remove('hidden');
        renderTypeGrid();
    }

    function selectType(tag) {
        wizardState.type = tag;
        wizardState.step = 3;
        step2.classList.add('hidden');
        step3.classList.remove('hidden');
        modalDesc.focus();
    }

    async function submitTransmission(restart = false) {
        const { file, type } = wizardState;
        const desc = modalDesc.value.trim();

        if (!file || !type || !desc) return;

        try {
            const res = await fetch('/api/append', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ path: file, type: type, description: desc })
            });

            if (res.ok) {
                if (restart) {
                    modalDesc.value = '';
                    modalDesc.placeholder = "Saved! Ready for next...";
                    resetWizard();
                } else {
                    modalNew.close();
                }
                loadData();
            } else {
                alert("Failed to transmit.");
            }
        } catch (e) { console.error(e); }
    }

    modalNew.addEventListener('keydown', (e) => {
        if (wizardState.step === 1) {
            if (e.key >= '1' && e.key <= '9') {
                const index = parseInt(e.key) - 1;
                const buttons = logSpeedDial.querySelectorAll('button');
                if (buttons[index]) buttons[index].click();
            } else if (e.key === '0') {
                const buttons = logSpeedDial.querySelectorAll('button');
                buttons.forEach(b => {
                    if (b.innerText.includes('INBOX')) b.click();
                });
            }
        }
        else if (wizardState.step === 2) {
            if (e.key >= '1' && e.key <= '9') {
                const index = parseInt(e.key) - 1;
                const buttons = typeSpeedDial.querySelectorAll('button');
                if (buttons[index]) buttons[index].click();
            } else if (e.key === '0') {
                const buttons = typeSpeedDial.querySelectorAll('button');
                buttons.forEach(b => {
                    if (b.innerText.includes('TASK')) b.click();
                });
            }
        }
        else if (wizardState.step === 3) {
            if (e.key === 'Enter') {
                if (e.ctrlKey) {
                    e.preventDefault();
                    submitTransmission(true);
                } else if (!e.shiftKey) {
                    e.preventDefault();
                    submitTransmission(false);
                }
            }
        }
    });

    // --- Data Loading ---
    marked.setOptions({
        highlight: function (code, lang) {
            const language = hljs.getLanguage(lang) ? lang : 'plaintext';
            return hljs.highlight(code, { language }).value;
        },
    });

    function loadData() {
        console.log("Loading Data...");
        fetch('/api/logs')
            .then(response => response.json())
            .then(logs => {
                currentLogs = logs;
                renderNav(logs);
                renderFeed(logs);
                if (!viewDeck.classList.contains('hidden')) renderDeck();
            })
            .catch(err => console.error('Failed to load logs', err));
    }

    loadData();

    // --- Render Functions ---

    function renderNav(logs) {
        fileTree.innerHTML = '';
        const categories = {};
        logs.forEach(log => {
            if (!categories[log.category]) categories[log.category] = [];
            categories[log.category].push(log);
        });

        for (const [category, items] of Object.entries(categories)) {
            const catHeader = document.createElement('div');
            catHeader.className = 'px-4 pt-4 pb-1 text-xs font-bold text-gray-500 uppercase tracking-widest';
            catHeader.textContent = category;
            fileTree.appendChild(catHeader);

            items.forEach(log => {
                const btn = document.createElement('button');
                btn.className = 'w-full text-left px-4 py-2 text-sm text-gray-400 hover:text-white hover:bg-white/5 transition-all rounded flex items-center gap-2 group';
                btn.innerHTML = `<span class="w-1.5 h-1.5 rounded-full bg-gray-600 group-hover:bg-neon-pink transition-colors"></span> ${log.name.replace('.md', '')}`;
                btn.onclick = () => {
                    switchView('feed');
                    setTimeout(() => {
                        const el = document.getElementById(`log-${log.id}`);
                        if (el) el.scrollIntoView({ behavior: 'smooth' });
                    }, 100);
                };
                fileTree.appendChild(btn);
            });
        }
    }

    function renderFeed(logs) {
        stitchedContent.innerHTML = '';
        logs.forEach(log => {
            const card = document.createElement('article');
            card.id = `log-${log.id}`;
            card.className = 'bg-gray-800/50 border border-white/5 rounded-xl p-8 shadow-lg backdrop-blur mb-10 group relative doc-article transition-transform duration-500';

            // Refined Header (Subtle Project Card Style)
            const header = document.createElement('div');
            header.className = 'flex items-baseline justify-between mb-8 pb-4 border-b border-white/10';
            header.innerHTML = `
                <div class="flex items-center gap-4">
                     <span class="text-4xl text-white/5 font-black absolute -top-4 -left-4 select-none pointer-events-none z-0">${log.name.substring(0, 2).toUpperCase()}</span>
                     <h2 class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-gray-100 to-gray-500 doc-title z-10 relative">
                        ${log.name.replace('.md', '')}
                    </h2>
                </div>
                <!-- Interactive Actions could go here -->
            `;

            const contentDiv = document.createElement('div');
            contentDiv.className = 'prose prose-invert prose-sm max-w-none relative z-10';
            contentDiv.innerHTML = marked.parse(log.content);

            card.appendChild(header);
            card.appendChild(contentDiv);
            stitchedContent.appendChild(card);
        });

        initScrollSpy();
        setupSmartLinking();
    }

    // --- Smart Linking Logic ---
    function setupSmartLinking() {
        // Remove old listeners if any (simple way: just re-add to container since we rewrite innerHTML)
        // actually we can just use event delegation on the container
    }

    // Global delegation for stitchedContent
    stitchedContent.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (!link) return;

        const href = link.getAttribute('href');
        if (!href) return;

        // Check if it's a markdown link (absolute or relative)
        if (href.startsWith('file:///') || href.endsWith('.md') || href.includes('.md#')) {
            e.preventDefault();
            handleLocalLink(href);
        }
    });

    function handleLocalLink(href) {
        try {
            // Flexible parsing for both file:/// and relative paths
            const parts = href.split('#');
            const pathPart = parts[0];
            const hash = parts.length > 1 ? parts[1] : null;

            // Extract Filename (works for file:///c:/foo/bar.md AND ../foo/bar.md)
            const filename = pathPart.split('/').pop();
            const decodedName = decodeURIComponent(filename);

            // Find log
            const targetLog = currentLogs.find(l => l.name === decodedName);

            if (targetLog) {
                if (viewDeck.classList.contains('hidden') === false) switchView('feed');

                setTimeout(() => {
                    const logCard = document.getElementById(`log-${targetLog.id}`);
                    if (logCard) {
                        let targetElement = logCard;

                        if (hash) {
                            const cleanHash = hash.replace('#', '');
                            const idMatch = logCard.querySelector(`[id="${cleanHash}"]`);
                            if (idMatch) {
                                targetElement = idMatch;
                            } else {
                                const headers = logCard.querySelectorAll('h1, h2, h3, h4');
                                for (let h of headers) {
                                    const slug = h.innerText.toLowerCase().replace(/[^\w]+/g, '-').replace(/^-+|-+$/g, '');
                                    if (slug.includes(cleanHash.toLowerCase()) || cleanHash.includes(slug)) {
                                        targetElement = h;
                                        break;
                                    }
                                }
                            }
                        }

                        targetElement.scrollIntoView({ behavior: 'smooth', block: 'center' });

                        targetElement.classList.add('text-neon-pink', 'transition-colors', 'duration-500');
                        setTimeout(() => targetElement.classList.remove('text-neon-pink'), 1500);
                    }
                }, 100);
            } else {
                console.warn("Linked file not found:", decodedName);
            }
        } catch (e) { console.error("Link err", e); }
    }

    // --- RESTORED: renderDeck ---
    function renderDeck() {
        deckContainer.innerHTML = '';

        // --- Filter Bar Logic ---
        // Clear existing buttons (keep toggle which is the last child usually or identified by ID)
        // Actually, just find the buttons inside filter-bar and remove them.
        filterBar.querySelectorAll('button').forEach(b => b.remove());

        // Find insert point (before separator)
        const separator = filterBar.querySelector('.h-6');

        // ALL Button
        const allBtn = document.createElement('button');
        allBtn.textContent = 'ALL';
        allBtn.className = 'px-3 py-1 rounded-full bg-white/10 text-xs font-bold text-white hover:bg-neon-pink hover:text-black transition-colors whitespace-nowrap ml-2';
        allBtn.onclick = () => document.querySelectorAll('.project-section').forEach(el => el.classList.remove('hidden'));
        filterBar.insertBefore(allBtn, separator);

        // Project Buttons
        const projects = currentLogs.map(l => l.name.replace('.md', ''));
        projects.forEach(proj => {
            const btn = document.createElement('button');
            btn.textContent = proj;
            btn.className = 'px-3 py-1 rounded-full border border-white/20 text-xs font-bold text-gray-400 hover:border-neon-cyan hover:text-neon-cyan transition-colors whitespace-nowrap ml-2';
            btn.onclick = () => {
                const target = document.getElementById(`deck-section-${proj}`);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    target.classList.add('animate-pulse');
                    setTimeout(() => target.classList.remove('animate-pulse'), 1000);
                }
            };
            filterBar.insertBefore(btn, separator);
        });

        // --- Grid Logic ---
        const showArchived = toggleArchives.checked;

        currentLogs.forEach(log => {
            const section = document.createElement('section');
            section.id = `deck-section-${log.name.replace('.md', '')}`;
            section.className = 'project-section scroll-mt-24';

            // Header
            const header = document.createElement('div');
            header.className = 'flex items-center gap-3 mb-6';
            header.innerHTML = `
                <div class="h-px bg-white/10 grow"></div>
                <h3 class="text-sm font-bold text-gray-500 uppercase tracking-widest">${log.name.replace('.md', '')}</h3>
                <div class="h-px bg-white/10 grow"></div>
            `;
            section.appendChild(header);

            const grid = document.createElement('div');
            grid.className = 'columns-1 md:columns-2 xl:columns-3 gap-6 space-y-6';

            const tasks = (log.tasks || []);
            const visibleTasks = tasks.filter(t => showArchived ? true : !t.completed);

            if (visibleTasks.length > 0) {
                visibleTasks.forEach(task => {
                    const el = createCard(task, log.path);
                    grid.appendChild(el);
                });
                section.appendChild(grid);
                deckContainer.appendChild(section);
            }
        });
    }

    function createCard(task, filePath) {
        const el = document.createElement('div');
        let typeClass = 'border-gray-700';
        const type = (task.type || "").toUpperCase();
        if (type.includes('TASK')) typeClass = 'card-type-TASK';
        else if (type.includes('IDEA')) typeClass = 'card-type-IDEA';
        else if (type.includes('BUG')) typeClass = 'card-type-BUG';
        else if (type.includes('NOTE')) typeClass = 'card-type-NOTE';

        let completedClass = '';
        if (task.completed) {
            completedClass = 'opacity-40 grayscale hover:grayscale-0 hover:opacity-100 transition-all cursor-crosshair';
            typeClass = 'border-white/5';
        }

        el.className = `deck-card bg-gray-900 border rounded-lg p-5 flex flex-col gap-3 ${typeClass} shadow-xl break-inside-avoid-column ${completedClass} relative overflow-hidden`;

        if (task.completed) {
            el.addEventListener('mouseenter', () => {
                const rect = el.getBoundingClientRect();
                confetti({
                    particleCount: 30,
                    spread: 40,
                    origin: {
                        x: (rect.left + rect.width / 2) / window.innerWidth,
                        y: (rect.top + rect.height / 2) / window.innerHeight
                    },
                    colors: ['#333'],
                    disableForReducedMotion: true
                });
            });
        }

        const btnHtml = task.completed ?
            `<span class="text-[10px] text-gray-600 font-bold border border-gray-700 px-2 py-1 rounded">ARCHIVED</span>` :
            `<button class="btn-terminate px-3 py-1 rounded bg-neon-red/10 text-neon-red hover:bg-neon-red hover:text-black text-xs font-bold transition-all">TERMINATE</button>`;

        el.innerHTML = `
            <div class="flex justify-between items-center text-xs text-gray-500 font-mono">
                <span>${task.id || '#'}</span>
                <span>${task.date || ''}</span>
            </div>
            <div class="flex items-center gap-2">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-white/5 text-gray-300 tracking-wider border border-white/5">${type}</span>
            </div>
            <p class="text-sm text-gray-200 leading-relaxed font-medium">
                ${task.description}
            </p>
            <div class="mt-auto pt-4 flex justify-end items-center border-t border-white/5">
                ${btnHtml}
            </div>
        `;

        if (!task.completed) {
            el.querySelector('.btn-terminate').onclick = async () => {
                el.classList.add('disintegrating');
                try {
                    const res = await fetch('/api/complete', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ path: filePath, line_text: task.raw_line })
                    });

                    if (!res.ok) {
                        el.classList.remove('disintegrating');
                        alert("Failed to terminate.");
                    } else {
                        setTimeout(() => {
                            el.remove();
                            loadData();
                        }, 600);
                    }
                } catch (e) { console.error(e); }
            };
        }
        return el;
    }

    // --- TOC Logic (H2 Only) ---
    function initScrollSpy() {
        tocContainer.innerHTML = '';
        const mainScroll = document.getElementById('main-scroll-area');
        mainScroll.addEventListener('scroll', throttle(updateSmartSpy, 100));
        updateSmartSpy();
    }

    function updateSmartSpy() {
        const articles = document.querySelectorAll('.doc-article');
        let activeArticle = null;

        for (const article of articles) {
            const rect = article.getBoundingClientRect();
            if (rect.top <= window.innerHeight / 2 && rect.bottom >= 100) {
                activeArticle = article;
                break;
            }
        }

        if (!activeArticle) return;

        if (tocContainer.dataset.activeFile === activeArticle.id) return;

        tocContainer.dataset.activeFile = activeArticle.id;
        tocContainer.innerHTML = '';

        // Clean Title
        const rawTitle = activeArticle.querySelector('.doc-title').innerText;
        const mainHeader = document.createElement('div');
        mainHeader.className = 'font-bold text-white mb-4 pl-2 border-l-2 border-neon-pink uppercase tracking-wider text-xs';
        mainHeader.textContent = rawTitle.trim();
        tocContainer.appendChild(mainHeader);

        // H2 Only
        const headers = activeArticle.querySelectorAll('h2:not(.doc-title)');

        if (headers.length === 0) {
            const empty = document.createElement('div');
            empty.className = 'text-gray-600 italic pl-4 text-xs';
            empty.textContent = 'No Sub-sections';
            tocContainer.appendChild(empty);
            return;
        }

        headers.forEach(h => {
            const link = document.createElement('a');
            link.className = 'block text-gray-400 hover:text-neon-cyan transition-colors text-xs truncate py-1.5 border-l-2 border-transparent pl-4 hover:border-gray-600';
            link.textContent = h.innerText.replace(/^#+\s/, ''); // clean markdown hash if present? helper generally strips it.
            link.href = '#';
            link.onclick = (e) => {
                e.preventDefault();
                h.scrollIntoView({ behavior: 'smooth' });
            };
            tocContainer.appendChild(link);
        });
    }

    function throttle(func, limit) {
        let inThrottle;
        return function () {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }
});
