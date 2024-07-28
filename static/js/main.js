document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    function drawBird(bird) {
        ctx.fillStyle = 'white';
        ctx.fillRect(bird.x, bird.y, bird.width, bird.height);
    }

    function drawPipe(pipe) {
        ctx.fillStyle = 'white';
        ctx.fillRect(pipe.top.x, pipe.top.y, pipe.top.width, pipe.top.height);
        ctx.fillRect(pipe.bottom.x, pipe.bottom.y, pipe.bottom.width, pipe.bottom.height);
    }

    function gameLoop() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Update game state
        bird.move();
        pipes.forEach(pipe => {
            pipe.move();
            drawPipe(pipe);
        });

        drawBird(bird);

        requestAnimationFrame(gameLoop);
    }

    const bird = { x: 50, y: 200, width: 30, height: 30, velocity: 0 };
    const pipes = [{ top: { x: 300, y: 0, width: 60, height: 200 }, bottom: { x: 300, y: 350, width: 60, height: 200 } }];

    gameLoop();
});
