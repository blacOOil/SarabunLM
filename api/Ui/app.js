/* ============================================================
   STATE
============================================================ */
let sectionCount = 0;
/* ============================================================
   INIT
============================================================ */
document.addEventListener('DOMContentLoaded', () => {
    TemplateSelector(); // Initialize template selector 
    addSection(); // Start with one section by default

    document.getElementById('btn-add-section').addEventListener('click', addSection);
    document.getElementById('btn-generate').addEventListener('click', generateDocument);
});
 function TemplateSelector() {
        const selectElement = document.getElementById('template-select');


    // Triggered when the dropdown value changes
        selectElement.addEventListener('change', (event) => {
        const selectedValue = event.target.value; 
                // Log the interaction
                const timestamp = new Date().toLocaleTimeString();
                console.log(`[${timestamp}] JS Triggered: Template changed to "${selectedValue}"`);
                
                // You can add more complex logic here (e.g., fetching data, changing styles)
                if (selectedValue === "Marriage_Paper") {
                 
                } else if (selectedValue === "Research_Paper") {
                  
                } else {
                    display.style.color = "var(--primary)";
                }
            });
        };
 
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