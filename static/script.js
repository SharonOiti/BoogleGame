$(document).ready(function() {
    let score = 0;
    let timeLeft = 60;
    const timerId = setInterval(() => {
        if (timeLeft <= 0) {
            clearInterval(timerId);
            $('#guess-form').hide();
            $('#message').append('<br>Time is up!').css('color', 'red');
            sendScore();
        } else {
            $('#message').text(`Time left: ${timeLeft} seconds`);
            timeLeft--;
        }
    }, 1000);

    $('#guess-form').submit(function(event) {
        event.preventDefault();
        const guess = $('#guess').val();

        axios.post('/check', { guess: guess })
            .then(response => {
                const result = response.data.result;
                if (result === 'ok') {
                    score += guess.length;
                    $('#message').text(`Good job! You guessed: ${guess}`);
                } else if (result === 'not-on-board') {
                    $('#message').text(`The word "${guess}" is not on the board.`);
                } else {
                    $('#message').text(`"${guess}" is not a valid word.`);
                }
                $('#score').text(`Score: ${score}`);
                $('#guess').val('');
            });
    });

    function sendScore() {
        axios.post('/score', { score: score })
            .then(response => {
                const totalGames = response.data.total_games;
                const highestScore = response.data.highest_score;
                $('#message').append(`<br>Total games played: ${totalGames}, Highest score: ${highestScore}`);
            });
    }
});