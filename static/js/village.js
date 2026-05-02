document.addEventListener('DOMContentLoaded', () => {
    initStepSimulation();

    const villageMap = document.querySelector('[data-village-map]');

    if (!villageMap) {
        document.querySelectorAll('.hut').forEach((hut) => {
            hut.addEventListener('click', () => {
                hut.classList.toggle('is-selected');
            });
        });
        return;
    }

    const detailName = document.querySelector('[data-hut-detail-name]');
    const detailSummary = document.querySelector('[data-hut-detail-summary]');
    const detailActivity = document.querySelector('[data-hut-detail-activity]');
    const detailBadge = document.querySelector('[data-hut-detail-badge]');
    const lockNote = document.querySelector('[data-hut-lock-note]');
    const action = document.querySelector('[data-hut-action]');

    villageMap.querySelectorAll('.hut').forEach((hut) => {
        hut.addEventListener('click', () => {
            villageMap.querySelectorAll('.hut').forEach((item) => {
                item.classList.remove('is-selected');
                item.setAttribute('aria-pressed', 'false');
            });

            hut.classList.add('is-selected');
            hut.setAttribute('aria-pressed', 'true');

            detailName.textContent = hut.dataset.hutName;
            detailSummary.textContent = hut.dataset.hutSummary;
            detailActivity.textContent = hut.dataset.hutActivity;
            detailBadge.textContent = hut.dataset.hutBadge;

            const isLocked = hut.dataset.status === 'locked';
            lockNote.hidden = !isLocked;
            action.textContent = isLocked ? 'Preview Story' : 'Open Hut';
            action.href = hut.dataset.hutUrl;
            action.classList.toggle('btn-dark', !isLocked);
            action.classList.toggle('btn-outline-dark', isLocked);
        });
    });
});

function initStepSimulation() {
    const simulation = document.querySelector('[data-step-simulation]');

    if (!simulation) {
        return;
    }

    const list = simulation.querySelector('[data-step-list]');
    const score = document.querySelector('[data-simulation-score]');
    const feedback = document.querySelector('[data-simulation-feedback]');
    const result = simulation.querySelector('[data-simulation-result]');
    const originalItems = Array.from(list.children).map((item) => item.cloneNode(true));
    const answer = Array.from(simulation.querySelectorAll('[data-answer-value]')).map((item) => item.dataset.answerValue);

    const bindMoveControls = () => {
        list.querySelectorAll('[data-move-step]').forEach((button) => {
            button.addEventListener('click', () => {
                const item = button.closest('li');
                const direction = button.dataset.moveStep;

                if (direction === 'up' && item.previousElementSibling) {
                    list.insertBefore(item, item.previousElementSibling);
                }

                if (direction === 'down' && item.nextElementSibling) {
                    list.insertBefore(item.nextElementSibling, item);
                }

                clearResult();
            });
        });
    };

    const currentOrder = () => Array.from(list.querySelectorAll('[data-step-value]')).map((item) => item.dataset.stepValue);

    const clearResult = () => {
        result.hidden = true;
        result.classList.remove('is-success', 'is-warning');
        list.querySelectorAll('li').forEach((item) => {
            item.classList.remove('is-correct', 'is-wrong');
        });
    };

    simulation.querySelector('[data-check-simulation]').addEventListener('click', () => {
        const order = currentOrder();
        let correctCount = 0;

        order.forEach((step, index) => {
            const item = list.children[index];
            const isCorrect = step === answer[index];
            correctCount += isCorrect ? 1 : 0;
            item.classList.toggle('is-correct', isCorrect);
            item.classList.toggle('is-wrong', !isCorrect);
        });

        score.textContent = `${correctCount}/${answer.length}`;
        const complete = correctCount === answer.length;
        feedback.textContent = complete
            ? 'The process is in the correct order.'
            : 'Some steps are out of order. Move them and check again.';
        result.hidden = false;
        result.textContent = complete
            ? 'Ready for the next MVP step: save completion on the server and award the badge.'
            : 'Keep refining the sequence before moving to quiz validation.';
        result.classList.toggle('is-success', complete);
        result.classList.toggle('is-warning', !complete);
    });

    simulation.querySelector('[data-reset-simulation]').addEventListener('click', () => {
        list.replaceChildren(...originalItems.map((item) => item.cloneNode(true)));
        score.textContent = `0/${answer.length}`;
        feedback.textContent = 'Arrange the village craft steps in the correct order.';
        clearResult();
        bindMoveControls();
    });

    bindMoveControls();
}
