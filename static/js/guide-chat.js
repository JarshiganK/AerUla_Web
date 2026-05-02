document.addEventListener('DOMContentLoaded', () => {
    const modalElement = document.getElementById('guideChatModal');
    const transcript = document.querySelector('[data-guide-transcript]');
    const sourcesList = document.querySelector('[data-guide-sources]');
    const sourceCount = document.querySelector('[data-guide-source-count]');
    const form = document.querySelector('[data-guide-form]');
    const input = document.querySelector('[data-guide-input]');
    const sendButton = document.querySelector('[data-guide-send]');
    const clearButton = document.querySelector('[data-guide-clear]');
    const promptButtons = Array.from(document.querySelectorAll('[data-guide-prompt]'));
    const openButtons = Array.from(document.querySelectorAll('[data-guide-open]'));

    if (!modalElement || !transcript || !sourcesList || !form || !input) {
        return;
    }

    const modal = window.bootstrap ? new window.bootstrap.Modal(modalElement) : null;
    const endpoint = form.getAttribute('action');
    const csrfTokenInput = form.querySelector('input[name="csrfmiddlewaretoken"]');

    const escapeHtml = (value) => String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');

    const renderMessage = (role, text) => `
        <div class="guide-chat-row is-${role}">
            <div class="guide-chat-bubble">
                <span>${role === 'user' ? 'You' : 'AerUla Guide'}</span>
                <p>${escapeHtml(text)}</p>
            </div>
        </div>
    `;

    const renderSources = (sources) => {
        if (!sources || !sources.length) {
            sourcesList.innerHTML = `
                <article class="guide-source-card guide-source-card-empty">
                    <span>Ready</span>
                    <h3>Ask a question to see grounded sources here.</h3>
                    <p>Powered by huts, simulations, quiz prompts, and marketplace content.</p>
                </article>
            `;
            if (sourceCount) {
                sourceCount.textContent = '0 matched';
            }
            return;
        }

        sourcesList.innerHTML = sources.map((source) => `
            <article class="guide-source-card">
                <span>${escapeHtml(source.source_label || 'Source')}</span>
                <h3><a href="${escapeHtml(source.url || '#')}">${escapeHtml(source.title || 'AerUla source')}</a></h3>
                <p>${escapeHtml(source.summary || '')}</p>
                <a class="guide-source-link" href="${escapeHtml(source.url || '#')}">Open source</a>
            </article>
        `).join('');

        if (sourceCount) {
            sourceCount.textContent = `${sources.length} matched`;
        }
    };

    const appendTurn = (role, text) => {
        transcript.insertAdjacentHTML('beforeend', renderMessage(role, text));
        transcript.scrollTop = transcript.scrollHeight;
    };

    const setBusy = (isBusy) => {
        if (sendButton) {
            sendButton.disabled = isBusy;
            sendButton.textContent = isBusy ? 'Sending...' : 'Send';
        }
        input.disabled = isBusy;
    };

    const postMessage = async (message) => {
        const formData = new FormData();
        formData.append('message', message);
        formData.append('csrfmiddlewaretoken', csrfTokenInput ? csrfTokenInput.value : '');

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Unable to send guide message.');
        }

        return response.json();
    };

    const clearChat = async () => {
        const formData = new FormData();
        formData.append('action', 'clear');
        formData.append('csrfmiddlewaretoken', csrfTokenInput ? csrfTokenInput.value : '');

        await fetch(endpoint, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: formData,
        });

        transcript.innerHTML = renderMessage('assistant', 'Ask me about a hut, a product, a tradition, or a real experience. I will answer from AerUla content.');
        renderSources([]);
        input.value = '';
    };

    openButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const prompt = button.dataset.guidePrompt;
            modal?.show();
            if (prompt) {
                input.value = prompt;
                input.focus();
                form.requestSubmit();
                return;
            }
            window.setTimeout(() => input.focus(), 150);
        });
    });

    promptButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const prompt = button.dataset.guidePrompt;
            if (!prompt) {
                return;
            }
            modal?.show();
            input.value = prompt;
            input.focus();
            form.requestSubmit();
        });
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const message = input.value.trim();
        if (!message) {
            return;
        }

        modal?.show();
        appendTurn('user', message);
        setBusy(true);

        try {
            const data = await postMessage(message);
            appendTurn('assistant', data.answer || 'I could not generate an answer yet.');
            renderSources(data.sources || []);
            input.value = '';
        } catch (error) {
            appendTurn('assistant', 'I could not answer that right now. Please try again.');
        } finally {
            setBusy(false);
            input.focus();
        }
    });

    if (clearButton) {
        clearButton.addEventListener('click', async () => {
            await clearChat();
            input.focus();
        });
    }
});