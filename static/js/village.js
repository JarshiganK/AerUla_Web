document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.hut').forEach((hut) => {
        hut.addEventListener('click', () => {
            hut.classList.toggle('is-selected');
        });
    });
});
