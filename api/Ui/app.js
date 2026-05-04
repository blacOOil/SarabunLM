
import * as pdfjsLib from 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.0.379/pdf.min.mjs';
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.0.379/pdf.worker.min.mjs';

const DEFAULT_PDF_URL = '/api/Tools/LLM/DataStorage/outputs/output.pdf';

class PDFViewer {
    constructor() {
        this.pdfDoc = null;
        this.pages = [];
        this.observer = null;
        this.renderQueue = new Set();
        this.init();
    }

    async loadFromUrl(url) {
        this.showLoader(0.1);
        try {
            this.pdfDoc = await pdfjsLib.getDocument({
                url,
                verbosity: 0,
                isEvalSupported: false,
                useSystemFonts: true
            }).promise;

            document.getElementById('dropzone').style.display = 'none';
            this.renderAllPlaceholders();
            this.setupIntersectionObserver();
        } catch (err) {
            console.error('Error loading PDF from URL:', err);
            alert('Could not load PDF from URL.');
        }
    }

    init() {
        const fileInput = document.getElementById('fileInput');
        fileInput.onchange = (e) => this.handleFile(e.target.files[0]);

        window.addEventListener('dragover', (e) => e.preventDefault());
        window.addEventListener('drop', (e) => {
            e.preventDefault();
            this.handleFile(e.dataTransfer.files[0]);
        });

        // Auto-load from HTML data attribute
        const viewer = document.getElementById('viewer');
        const url = viewer?.dataset.pdfUrl;
        if (url) this.loadFromUrl(url);
    }

    async handleFile(file) {
        if (!file || file.type !== 'application/pdf') return;
        this.showLoader(0.1);
        const arrayBuffer = await file.arrayBuffer();
        this.loadPDF(arrayBuffer);
    }

    async loadPDF(data) {
        try {
            this.pdfDoc = await pdfjsLib.getDocument({
                data,
                verbosity: 0,
                isEvalSupported: false,
                useSystemFonts: true
            }).promise;

            document.getElementById('dropzone').style.display = 'none';
            this.renderAllPlaceholders();
            this.setupIntersectionObserver();
        } catch (err) {
            console.error('Error loading PDF:', err);
            alert('Could not load PDF. Is it password protected?');
        }
    }

    renderAllPlaceholders() {
        const viewer = document.getElementById('viewer');
        viewer.innerHTML = '';
        this.pages = [];

        for (let i = 1; i <= this.pdfDoc.numPages; i++) {
            const container = document.createElement('div');
            container.className = 'page-container';
            container.id = `page-wrap-${i}`;
            container.dataset.page = i;

            const canvas = document.createElement('canvas');
            container.appendChild(canvas);

            const label = document.createElement('div');
            label.className = 'page-num-overlay';
            label.textContent = `Page ${i}`;
            container.appendChild(label);

            viewer.appendChild(container);
            this.pages.push({ i, container, canvas, rendered: false });
        }
    }

    setupIntersectionObserver() {
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const pageNum = parseInt(entry.target.dataset.page);
                    this.renderPage(pageNum);
                }
            });
        }, { root: document.getElementById('viewer'), threshold: 0.1 });

        this.pages.forEach(p => this.observer.observe(p.container));
    }

    async renderPage(num) {
        const pageData = this.pages[num - 1];
        if (pageData.rendered || this.renderQueue.has(num)) return;

        this.renderQueue.add(num);
        const page = await this.pdfDoc.getPage(num);

        const viewport = page.getViewport({ scale: window.devicePixelRatio });
        const canvas = pageData.canvas;
        const ctx = canvas.getContext('2d', { alpha: false });

        canvas.height = viewport.height;
        canvas.width = viewport.width;
        canvas.style.width = `${viewport.width / window.devicePixelRatio}px`;
        pageData.container.style.height = 'auto';

        await page.render({
            canvasContext: ctx,
            viewport,
            intent: 'display'
        }).promise;

        pageData.rendered = true;
        this.renderQueue.delete(num);
        this.showLoader(num / this.pdfDoc.numPages);
    }

    showLoader(progress) {
        const l = document.getElementById('loader');
        l.style.transform = `scaleX(${progress})`;
        if (progress >= 1) setTimeout(() => l.style.transform = 'scaleX(0)', 500);
    }
}

new PDFViewer();

/* ============================================================
   STATE
============================================================ */
let sectionCount = 0;
let appConfig = {};

 async function loadConfig() {
    try {
        const response = await fetch('/config');
        appConfig = await response.json();
        console.log("Config loaded:", appConfig);
        buildTemplateOptions();
        // appConfig.section_number  → 5
        // appConfig.section_names   → { "1": "Introduction", ... }
        // appConfig.doc_format      → "ResearchPaper"
    } catch (err) {
        console.error("Failed to load config:", err);
    }
  }
 /* async function sentgenerateDocument() {
     const preview = document.getElementById('document-preview');
    preview.innerHTML = '<div class="loader"></div>';

    const sections = collectSections();
    if (sections.length === 0) {
        preview.innerHTML = '<div class="doc-placeholder">Please enter some content.</div>';
        return;
    }

    const ai_output = sections
        .map(({ type, content }) => `[${type.toUpperCase()}]\n${content}`)
        .join('\n\n');

    // Get the selected template name from the dropdown
    const template_key = document.getElementById('template-select')
                                 .selectedOptions[0]?.text || "Default";

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ai_output, template_key })  // ← goes here
        });

        const result = await response.json();

        if (!response.ok) {
            preview.innerHTML = `<div class="doc-error">Error: ${result.detail}</div>`;
            return;
        }

        preview.innerHTML = `<div class="doc-success">${result.message}</div>`;

    } catch (err) {
        preview.innerHTML = `<div class="doc-error">Request failed: ${err.message}</div>`;
    }
} */
  
/* ============================================================
   INIT
============================================================ */
document.addEventListener('DOMContentLoaded', () => {
    loadConfig()
    TemplateSelector(); // Initialize template selector 
    addSection(); // Start with one section by default

    document.getElementById('btn-add-section').addEventListener('click', addSection);
  //  document.getElementById('btn-generate').addEventListener('click', generateDocument);
});
/* ============================================================
   Template Selector
   Selects template for call section data from  SarabunLM.py
============================================================ */
function TemplateSelector() {
    const selectElement = document.getElementById('template-select');

    selectElement.addEventListener('change', (event) => {
        const selectedValue = event.target.value;
        const timestamp = new Date().toLocaleTimeString();
        console.log(`[${timestamp}] JS Triggered: Template changed to "${selectedValue}"`);

        if (selectedValue === "0" || selectedValue === "") return; // Skip "None"


        const keys = Object.keys(appConfig);
        const keyIndex = Number(selectedValue) - 1; 
        const templateKey = keys[keyIndex];
        const templateData = appConfig[templateKey];
        const sectionNames = templateData?.section_names || {}; 

        if (templateData) {
            addSectionFromTemplate(selectedValue, templateKey, templateData, sectionNames);
        }
    });}

   function buildSectionOptions(sectionNames = {}) {
    const select = document.getElementById('section-type-select');
    if (!select) return;

    select.innerHTML = '<option value="">— Section Type —</option>';

    Object.entries(sectionNames).forEach(([key, name]) => {
        const option = document.createElement('option');
        option.value = key;
        option.textContent = name;
        select.appendChild(option);
    });
}
function buildTemplateOptions() {
    const select = document.getElementById('template-select');
    if (!select) return;

    select.innerHTML = '<option value="0">None</option>';

    const keys = Object.keys(appConfig);
    console.log(`Found ${keys.length} templates:`, keys);

    for (let i = 0; i < keys.length; i++) {
        const option = document.createElement('option');
        option.value = i + 1;
        option.textContent = keys[i];
        select.appendChild(option);
    }

    console.log("Template options built:", keys.length, "options");
}
/* ============================================================
   ADD SECTION
   Creates a new section card and appends it to the sidebar
============================================================ */
function addSection() {
    sectionCount++;
    const container = document.getElementById('sections-container');

    const card = document.createElement('div');
    card.className = 'section-card';
    card.dataset.id = sectionCount;

    card.innerHTML = `
        <div class="section-card__header">
            <span class="section-card__label">Section ${sectionCount}</span>
            <button class="section-card__remove" title="Remove section" onclick="removeSection(this)">×</button>
        </div>
        <select class="section-card__select">
            <option value="">— Section Type —</option>
            <option value="header">Header</option>
            <option value="body">Body Paragraph</option>
            <option value="footer">Footer</option>
        </select>
        <textarea class="section-card__textarea" placeholder="Enter content here…"></textarea>
    `;

    container.appendChild(card);
    container.scrollTop = container.scrollHeight;
}
function addSectionFromTemplate(value, templateKey, templateData, sectionNames) {
    const container = document.getElementById('sections-container');

    // If no section_names, fall back to one generic card
    const entries = Object.entries(sectionNames);
    if (entries.length === 0) {
      
        // ... your existing single-card logic
        return;
    }

    entries.forEach(([key, sectionName]) => {
        sectionCount++;

        const card = document.createElement('div');
        card.className = 'section-card';
        card.dataset.id = sectionCount;

        card.innerHTML = `
            <div class="section-card__header">
                <span class="section-card__label"> ${sectionName}</span>
                <button class="section-card__remove" title="Remove section" onclick="removeSection(this)">×</button>
            </div>
            <textarea class="section-card__textarea" placeholder="Enter content for ${sectionName}…"></textarea>
        `;
        container.appendChild(card);
    });

    container.scrollTop = container.scrollHeight;
}

/* ============================================================
   REMOVE SECTION
   Removes the section card that contains the clicked button
============================================================ */
function removeSection(btn) {
    btn.closest('.section-card').remove();
}

/* ============================================================
   COLLECT SECTIONS
   Reads all section cards and returns an array of { type, content }
============================================================ */
function collectSections() {
    const cards = document.querySelectorAll('.section-card');
    const sections = [];

    cards.forEach(card => {
        const selectEl   = card.querySelector('.section-card__select');
        const textareaEl = card.querySelector('.section-card__textarea');

        // Guard: skip if elements missing
        if (!selectEl || !textareaEl) return;

        const type    = selectEl.value;
        const content = textareaEl.value.trim();

        if (content) {
            sections.push({ type, content });
        }
    });

    return sections;
}
/* ============================================================
   GENERATE DOCUMENT
   Shows a loader then renders the preview after a short delay
============================================================ */
/*function generateDocument() {
    const preview = document.getElementById('document-preview');
    // Show loading spinner
    preview.innerHTML = '<div class="loader"></div>';

    const sections = collectSections();

    // Swap with a real API call (e.g. fetch('/api/generate', ...)) if needed
    setTimeout(() => renderPreview(sections), 500);
}*/

/* ============================================================
   RENDER PREVIEW
   Builds and injects HTML into the document preview pane
============================================================ */
function renderPreview(sections) {
    const preview = document.getElementById('document-preview');

    if (sections.length === 0) {
        preview.innerHTML = '<div class="doc-placeholder">Please enter some content to generate the document.</div>';
        return;
    }

    const html = sections.map(({ type, content }) => {
        const safe = escapeHtml(content);
        switch (type) {
            case 'header': return `<div class="doc-header">${safe}</div>`;
            case 'footer': return `<div class="doc-footer">${safe}</div>`;
            default:       return `<div class="doc-body">${safe}</div>`;
        }
    }).join('');

    preview.innerHTML = html;
}

/* ============================================================
   UTILITY: ESCAPE HTML
   Prevents XSS by escaping user-entered content before injection
============================================================ */
function escapeHtml(str) {
    return str
        .replace(/&/g,  '&amp;')
        .replace(/</g,  '&lt;')
        .replace(/>/g,  '&gt;')
        .replace(/"/g,  '&quot;')
        .replace(/\n/g, '<br>');
}

