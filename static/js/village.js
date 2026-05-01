document.addEventListener('DOMContentLoaded', () => {
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
            action.textContent = isLocked ? 'Preview Story' : 'Start Preview';
            action.classList.toggle('btn-dark', !isLocked);
            action.classList.toggle('btn-outline-dark', isLocked);
        });
    });
});
