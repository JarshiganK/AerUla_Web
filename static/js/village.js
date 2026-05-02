document.addEventListener('DOMContentLoaded', () => {
    initPanoramaSimulation();

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
    const detailImage = document.querySelector('[data-hut-detail-image]');
    const detailCredit = document.querySelector('[data-hut-detail-credit]');
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
            detailImage.src = hut.dataset.hutImage;
            detailImage.alt = hut.dataset.hutImageAlt;
            detailCredit.textContent = hut.dataset.hutCredit;
            detailCredit.href = hut.dataset.hutSource;

            const isLocked = hut.dataset.status === 'locked';
            lockNote.hidden = !isLocked;
            action.textContent = isLocked ? 'Preview Story' : 'Open Hut';
            action.href = hut.dataset.hutUrl;
            action.classList.toggle('btn-dark', !isLocked);
            action.classList.toggle('btn-outline-dark', isLocked);
        });
    });
});

function initPanoramaSimulation() {
    const simulation = document.querySelector('[data-panorama-simulation]');

    if (!simulation) {
        return;
    }

    const canvas = simulation.querySelector('[data-panorama-canvas]');
    const video = simulation.querySelector('[data-panorama-video]');
    const score = document.querySelector('[data-simulation-score]');
    const feedback = document.querySelector('[data-simulation-feedback]');
    const result = simulation.querySelector('[data-simulation-result]');
    const progress = simulation.querySelector('[data-panorama-progress]');
    const playButton = simulation.querySelector('[data-toggle-panorama]');
    const verifyButton = simulation.querySelector('[data-verify-panorama]');
    const resetButton = simulation.querySelector('[data-reset-panorama]');
    const quizLink = simulation.querySelector('[data-quiz-link]');
    const status = simulation.querySelector('[data-panorama-status]');
    const hotspotButtons = Array.from(simulation.querySelectorAll('[data-panorama-hotspot]'));
    const durationRequired = Number(simulation.dataset.durationRequired || 20);
    const coverageRequired = Number(simulation.dataset.coverageRequired || 240);
    const visitedHotspots = new Set();
    const visitedAngles = new Set();
    const context = canvas.getContext('2d');
    const panorama = document.createElement('canvas');
    const panoramaContext = panorama.getContext('2d');
    let watchedSeconds = 0;
    let lastVideoTime = 0;
    let yaw = 0;
    let pitch = 0;
    let dragging = false;
    let lastPointer = { x: 0, y: 0 };
    let animationFrame = null;
    let videoReady = false;
    let videoUnavailable = false;

    const csrfToken = () => {
        const match = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
        return match ? decodeURIComponent(match[1]) : '';
    };

    const updateProgress = () => {
        const coverage = Math.min(visitedAngles.size * 10, 360);
        progress.textContent = `Watch time: ${Math.floor(watchedSeconds)}s. View coverage: ${coverage} degrees. Hotspots: ${visitedHotspots.size}/${hotspotButtons.length}.`;
        return coverage;
    };

    const markCurrentAngle = () => {
        const normalizedYaw = ((yaw % 360) + 360) % 360;
        visitedAngles.add(Math.floor(normalizedYaw / 10));
        updateProgress();
    };

    const setStatus = (message) => {
        status.textContent = message;
    };

    const clearResult = () => {
        result.hidden = true;
        result.classList.remove('is-success', 'is-warning');
    };

    const resizeCanvas = () => {
        const ratio = Math.min(window.devicePixelRatio || 1, 2);
        const width = canvas.clientWidth || 960;
        const height = canvas.clientHeight || 540;
        canvas.width = Math.round(width * ratio);
        canvas.height = Math.round(height * ratio);
        context.setTransform(ratio, 0, 0, ratio, 0, 0);
    };

    const roundedRect = (targetContext, x, y, width, height, radius) => {
        const safeRadius = Math.min(radius, width / 2, height / 2);
        targetContext.beginPath();
        targetContext.moveTo(x + safeRadius, y);
        targetContext.lineTo(x + width - safeRadius, y);
        targetContext.quadraticCurveTo(x + width, y, x + width, y + safeRadius);
        targetContext.lineTo(x + width, y + height - safeRadius);
        targetContext.quadraticCurveTo(x + width, y + height, x + width - safeRadius, y + height);
        targetContext.lineTo(x + safeRadius, y + height);
        targetContext.quadraticCurveTo(x, y + height, x, y + height - safeRadius);
        targetContext.lineTo(x, y + safeRadius);
        targetContext.quadraticCurveTo(x, y, x + safeRadius, y);
        targetContext.closePath();
    };

    const drawLabel = (x, y, text) => {
        panoramaContext.save();
        panoramaContext.fillStyle = 'rgba(17, 24, 39, 0.82)';
        roundedRect(panoramaContext, x, y, 260, 54, 12);
        panoramaContext.fill();
        panoramaContext.fillStyle = '#fffdf8';
        panoramaContext.font = '700 28px sans-serif';
        panoramaContext.fillText(text, x + 22, y + 36);
        panoramaContext.restore();
    };

    const drawPot = (x, y, scale) => {
        panoramaContext.save();
        panoramaContext.translate(x, y);
        panoramaContext.scale(scale, scale);
        panoramaContext.fillStyle = '#9b4f2f';
        panoramaContext.beginPath();
        panoramaContext.ellipse(0, 54, 92, 52, 0, 0, Math.PI * 2);
        panoramaContext.fill();
        panoramaContext.fillStyle = '#c8923b';
        panoramaContext.fillRect(-68, -18, 136, 76);
        panoramaContext.beginPath();
        panoramaContext.ellipse(0, -18, 72, 22, 0, 0, Math.PI * 2);
        panoramaContext.fill();
        panoramaContext.strokeStyle = '#fffdf8';
        panoramaContext.lineWidth = 8;
        panoramaContext.beginPath();
        panoramaContext.arc(-24, 20, 22, 0.2, Math.PI * 1.4);
        panoramaContext.stroke();
        panoramaContext.restore();
    };

    const drawGeneratedPanorama = () => {
        panorama.width = 2400;
        panorama.height = 900;
        const sky = panoramaContext.createLinearGradient(0, 0, 0, panorama.height);
        sky.addColorStop(0, '#b7d7d4');
        sky.addColorStop(0.45, '#f5efe5');
        sky.addColorStop(1, '#8b5a35');
        panoramaContext.fillStyle = sky;
        panoramaContext.fillRect(0, 0, panorama.width, panorama.height);

        panoramaContext.fillStyle = '#2f6f4f';
        for (let index = 0; index < 12; index += 1) {
            const x = index * 230 - 70;
            panoramaContext.beginPath();
            panoramaContext.moveTo(x, 510);
            panoramaContext.lineTo(x + 130, 285);
            panoramaContext.lineTo(x + 285, 510);
            panoramaContext.closePath();
            panoramaContext.fill();
        }

        panoramaContext.fillStyle = '#d8b173';
        for (let index = 0; index < 9; index += 1) {
            const x = index * 310 - 120;
            panoramaContext.beginPath();
            panoramaContext.moveTo(x, 590);
            panoramaContext.lineTo(x + 170, 458);
            panoramaContext.lineTo(x + 350, 590);
            panoramaContext.closePath();
            panoramaContext.fill();
            panoramaContext.fillStyle = '#fff8e8';
            panoramaContext.fillRect(x + 48, 590, 244, 154);
            panoramaContext.fillStyle = '#d8b173';
        }

        panoramaContext.fillStyle = '#624126';
        panoramaContext.fillRect(0, 690, panorama.width, 210);
        panoramaContext.fillStyle = 'rgba(255, 253, 248, 0.58)';
        panoramaContext.beginPath();
        panoramaContext.ellipse(1200, 810, 720, 82, 0, 0, Math.PI * 2);
        panoramaContext.fill();

        drawPot(380, 640, 1.25);
        drawPot(1010, 654, 0.9);
        drawPot(1780, 635, 1.1);
        drawLabel(250, 220, 'Clay wheel');
        drawLabel(920, 248, 'Drying shelf');
        drawLabel(1650, 228, 'Kiln fire');
        drawLabel(2150, 260, simulation.dataset.hutName || 'Village hut');
    };

    const drawViewport = () => {
        const width = canvas.clientWidth || 960;
        const height = canvas.clientHeight || 540;
        const sourceWidth = Math.max(420, panorama.width * 0.34);
        const sourceHeight = panorama.height * 0.78;
        const x = (((yaw % 360) + 360) % 360) / 360 * panorama.width;
        const y = Math.max(0, Math.min(panorama.height - sourceHeight, 84 - pitch * 3));

        context.clearRect(0, 0, width, height);
        context.fillStyle = '#111827';
        context.fillRect(0, 0, width, height);

        const drawSlice = (sourceX, targetX, sliceWidth) => {
            context.drawImage(
                panorama,
                sourceX,
                y,
                sliceWidth,
                sourceHeight,
                targetX,
                0,
                (sliceWidth / sourceWidth) * width,
                height
            );
        };

        if (videoReady && !video.paused && !video.ended) {
            context.drawImage(video, 0, 0, width, height);
        } else if (x + sourceWidth <= panorama.width) {
            drawSlice(x, 0, sourceWidth);
        } else {
            const firstWidth = panorama.width - x;
            drawSlice(x, 0, firstWidth);
            drawSlice(0, (firstWidth / sourceWidth) * width, sourceWidth - firstWidth);
        }

        context.fillStyle = 'rgba(17, 24, 39, 0.18)';
        context.fillRect(0, 0, width, height);
        animationFrame = window.requestAnimationFrame(drawViewport);
    };

    canvas.addEventListener('pointerdown', (event) => {
        dragging = true;
        lastPointer = { x: event.clientX, y: event.clientY };
        canvas.setPointerCapture(event.pointerId);
        clearResult();
    });

    canvas.addEventListener('pointermove', (event) => {
        if (!dragging) {
            return;
        }
        yaw -= (event.clientX - lastPointer.x) * 0.18;
        pitch += (event.clientY - lastPointer.y) * 0.18;
        pitch = Math.max(-50, Math.min(50, pitch));
        lastPointer = { x: event.clientX, y: event.clientY };
        markCurrentAngle();
    });

    canvas.addEventListener('pointerup', (event) => {
        dragging = false;
        canvas.releasePointerCapture(event.pointerId);
    });

    video.addEventListener('timeupdate', () => {
        if (video.currentTime > lastVideoTime) {
            watchedSeconds += video.currentTime - lastVideoTime;
        }
        lastVideoTime = video.currentTime;
        updateProgress();
    });

    video.addEventListener('loadeddata', () => {
        videoReady = true;
        videoUnavailable = false;
        setStatus('Local 360 video loaded. Drag while it plays to explore.');
    });

    video.addEventListener('error', () => {
        videoUnavailable = true;
        setStatus('Generated 360 hut scene is active. Add the local MP4 to use filmed footage.');
    });

    playButton.addEventListener('click', () => {
        if (videoUnavailable) {
            watchedSeconds += 5;
            playButton.textContent = 'Explore Generated 360';
            setStatus('Generated 360 hut scene is active. Drag left or right to explore the full scene.');
            updateProgress();
            return;
        }

        if (video.paused) {
            video.play()
                .then(() => {
                    playButton.textContent = 'Pause 360 Video';
                    setStatus('Video playing. Drag the scene to look around.');
                })
                .catch(() => {
                    videoUnavailable = true;
                    watchedSeconds += 5;
                    setStatus('Generated 360 hut scene is active. Add the MP4 source to enable filmed playback.');
                    updateProgress();
                });
            return;
        }
        video.pause();
        playButton.textContent = 'Play 360 Video';
        setStatus('Video paused.');
    });

    hotspotButtons.forEach((button) => {
        button.addEventListener('click', () => {
            yaw = Number(button.dataset.yaw || 0);
            pitch = Number(button.dataset.pitch || 0);
            visitedHotspots.add(button.dataset.panoramaHotspot);
            button.classList.add('is-visited');
            const check = simulation.querySelector(`[data-hotspot-check="${button.dataset.panoramaHotspot}"]`);
            if (check) {
                check.classList.add('is-visited');
            }
            setStatus(`${button.textContent.trim()} inspected.`);
            clearResult();
            markCurrentAngle();
        });
    });

    verifyButton.addEventListener('click', () => {
        const coverage = updateProgress();
        const completeUrl = simulation.dataset.completeUrl;

        verifyButton.disabled = true;
        verifyButton.textContent = 'Verifying...';
        result.hidden = false;
        result.textContent = 'Checking the 360 visit progress against the hut activity.';
        result.classList.remove('is-success', 'is-warning');

        fetch(completeUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken(),
            },
            body: JSON.stringify({
                watched_seconds: watchedSeconds,
                coverage_degrees: coverage,
                hotspots: Array.from(visitedHotspots),
            }),
        })
            .then((response) => response.json().then((data) => ({ ok: response.ok, data })))
            .then(({ ok, data }) => {
                if (!ok) {
                    throw new Error(data.error || 'The simulation could not be verified.');
                }

                score.textContent = `${data.score}%`;
                feedback.textContent = data.message;
                result.textContent = data.completed
                    ? '360 simulation verified. The quiz is unlocked for badge completion.'
                    : `Need ${durationRequired}s watched, ${coverageRequired} degrees viewed, and every hotspot inspected.`;
                result.classList.toggle('is-success', data.completed);
                result.classList.toggle('is-warning', !data.completed);

                if (data.completed && quizLink) {
                    quizLink.classList.remove('disabled');
                    quizLink.removeAttribute('aria-disabled');
                    quizLink.href = data.quiz_url;
                }
            })
            .catch((error) => {
                feedback.textContent = 'The simulation could not be verified.';
                result.textContent = error.message;
                result.classList.add('is-warning');
            })
            .finally(() => {
                verifyButton.disabled = false;
                verifyButton.textContent = 'Verify 360 Visit';
            });
    });

    resetButton.addEventListener('click', () => {
        yaw = 0;
        pitch = 0;
        watchedSeconds = 0;
        lastVideoTime = 0;
        visitedAngles.clear();
        visitedHotspots.clear();
        hotspotButtons.forEach((button) => button.classList.remove('is-visited'));
        simulation.querySelectorAll('[data-hotspot-check]').forEach((item) => item.classList.remove('is-visited'));
        score.textContent = '0%';
        feedback.textContent = 'Watch, look around, and inspect the required points in the scene.';
        setStatus('Drag to look around. Use the hotspots to inspect the scene.');
        updateProgress();
        clearResult();
    });

    drawGeneratedPanorama();
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    drawViewport();
    markCurrentAngle();
}
