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
/* ============================================================
   INIT
============================================================ */
document.addEventListener('DOMContentLoaded', () => {
    loadConfig()
    TemplateSelector(); // Initialize template selector 
    addSection(); // Start with one section by default

    document.getElementById('btn-add-section').addEventListener('click', addSection);
    document.getElementById('btn-generate').addEventListener('click', generateDocument);
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
        const type    = card.querySelector('select').value;
        const content = card.querySelector('textarea').value.trim();
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
function generateDocument() {
    const preview = document.getElementById('document-preview');
    // Show loading spinner
    preview.innerHTML = '<div class="loader"></div>';

    const sections = collectSections();

    // Swap with a real API call (e.g. fetch('/api/generate', ...)) if needed
    setTimeout(() => renderPreview(sections), 500);
}

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