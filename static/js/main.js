/**
 * Developer Portfolio Client-Side JavaScript
 * Controls DSA code viewer, interactive visualizer, and AJAX submissions.
 */

document.addEventListener('DOMContentLoaded', () => {
    initDSAViewer();
    initSortingVisualizer();
    initContactForm();
    initProjectFilter();
});

/* -------------------------------------------------------------
   DSA CODE VIEWER
   ------------------------------------------------------------- */
function initDSAViewer() {
    const dsaItems = document.querySelectorAll('.dsa-item');
    const problemTitle = document.getElementById('dsa-title');
    const timeBadge = document.getElementById('dsa-time');
    const spaceBadge = document.getElementById('dsa-space');
    const problemStatement = document.getElementById('dsa-statement');
    const codeBody = document.getElementById('dsa-code');
    const explanationText = document.getElementById('dsa-explanation');

    if (!dsaItems.length) return;

    dsaItems.forEach(item => {
        item.addEventListener('click', async () => {
            dsaItems.forEach(el => el.classList.remove('active'));
            item.classList.add('active');

            const problemId = item.dataset.id;
            
            try {
                const response = await fetch(`/api/dsa/${problemId}`);
                if (!response.ok) throw new Error("Failed to fetch DSA problem details");

                const data = await response.json();
                
                problemTitle.textContent = data.title;
                timeBadge.textContent = `Time: ${data.time_complexity}`;
                spaceBadge.textContent = `Space: ${data.space_complexity}`;
                problemStatement.textContent = data.problem_statement;
                codeBody.textContent = data.cpp_solution;
                explanationText.textContent = data.explanation || "";

            } catch (err) {
                console.error("Error loading DSA details:", err);
            }
        });
    });
}

/* -------------------------------------------------------------
   INTERACTIVE SORTING VISUALIZER
   ------------------------------------------------------------- */
let isSorting = false;

function initSortingVisualizer() {
    const container = document.getElementById('viz-bars-container');
    const generateBtn = document.getElementById('viz-generate');
    const startSortBtn = document.getElementById('viz-start');

    if (!container || !generateBtn || !startSortBtn) return;

    let array = [];

    function generateRandomArray() {
        if (isSorting) return;
        container.innerHTML = '';
        array = [];
        for (let i = 0; i < 16; i++) {
            const val = Math.floor(Math.random() * 85) + 15;
            array.push(val);
            const bar = document.createElement('div');
            bar.className = 'viz-bar';
            bar.style.height = `${val}%`;
            bar.title = `Value: ${val}`;
            container.appendChild(bar);
        }
    }

    async function bubbleSort() {
        if (isSorting) return;
        isSorting = true;
        const bars = container.children;

        for (let i = 0; i < array.length; i++) {
            for (let j = 0; j < array.length - i - 1; j++) {
                bars[j].style.background = '#c24653';
                bars[j + 1].style.background = '#c24653';

                await new Promise(resolve => setTimeout(resolve, 150));

                if (array[j] > array[j + 1]) {
                    let temp = array[j];
                    array[j] = array[j + 1];
                    array[j + 1] = temp;

                    bars[j].style.height = `${array[j]}%`;
                    bars[j + 1].style.height = `${array[array.length - 1]}%`;
                }

                bars[j].style.background = 'linear-gradient(to top, var(--accent-brown), var(--accent-gold))';
                bars[j + 1].style.background = 'linear-gradient(to top, var(--accent-brown), var(--accent-gold))';
            }
            bars[array.length - i - 1].style.background = '#708269';
        }
        isSorting = false;
    }

    generateBtn.addEventListener('click', generateRandomArray);
    startSortBtn.addEventListener('click', bubbleSort);

    generateRandomArray();
}

/* -------------------------------------------------------------
   CONTACT FORM HANDLER
   ------------------------------------------------------------- */
function initContactForm() {
    const form = document.getElementById('portfolio-contact-form');
    const responseMsg = document.getElementById('contact-response');

    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('contact-name').value,
            email: document.getElementById('contact-email').value,
            subject: document.getElementById('contact-subject').value,
            message: document.getElementById('contact-message').value
        };

        try {
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok) {
                responseMsg.style.display = 'block';
                responseMsg.style.background = 'rgba(112, 130, 105, 0.15)';
                responseMsg.style.color = '#708269';
                responseMsg.textContent = result.message;
                form.reset();
            } else {
                responseMsg.style.display = 'block';
                responseMsg.style.background = 'rgba(194, 70, 83, 0.15)';
                responseMsg.style.color = '#c24653';
                responseMsg.textContent = result.message || 'An error occurred.';
            }
        } catch (err) {
            responseMsg.style.display = 'block';
            responseMsg.style.background = 'rgba(194, 70, 83, 0.15)';
            responseMsg.style.color = '#c24653';
            responseMsg.textContent = 'Server connection failed.';
        }
    });
}

/* -------------------------------------------------------------
   PROJECT FILTERING
   ------------------------------------------------------------- */
function initProjectFilter() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card-wrapper');

    if (!filterBtns.length) return;

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.dataset.filter;

            projectCards.forEach(card => {
                if (filter === 'all' || card.dataset.category === filter) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}
