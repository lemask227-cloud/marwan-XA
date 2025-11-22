from flask import Flask, render_template_string

app = Flask(__name__)

INDEX_html = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    
    <style>
        body { 
            font-family: sans-serif; 
            text-align: center; 
            background-color: #f0f0f0; 
            margin: 0;
            padding-top: 50px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(3, 100px);
            grid-template-rows: repeat(3, 100px);
            margin: 20px auto;
            border: 3px solid #333;
            width: 300px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            background-color: #fff;
        }
        .cell {
            border: 1px solid #ccc;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 60px;
            font-weight: bold;
            cursor: pointer;
            user-select: none;
            transition: background-color 0.2s;
        }
        .cell:hover {
            background-color: #e0e0e0;
        }
        #status {
            color: #333;
            font-size: 24px;
            margin-bottom: 20px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>

    <h2>لعبة X-O ضد الروبوت 🤖</h2>
    <h3 id="status">دور اللاعب X</h3>
    
    <div class="grid" id="gameGrid">
        <div class="cell" data-index="0"></div>
        <div class="cell" data-index="1"></div>
        <div class="cell" data-index="2"></div>
        <div class="cell" data-index="3"></div>
        <div class="cell" data-index="4"></div>
        <div class="cell" data-index="5"></div>
        <div class="cell" data-index="6"></div>
        <div class="cell" data-index="7"></div>
        <div class="cell" data-index="8"></div>
    </div>

    <button onclick="resetGame()">إعادة اللعب</button>

    <script>
        const cells = document.querySelectorAll('.cell');
        const statusDisplay = document.getElementById('status');
        let gameActive = true;
        let humanPlayer = "X";
        let aiPlayer = "O";
        let currentPlayer = humanPlayer; // يبدأ اللاعب البشري
        let gameState = ["", "", "", "", "", "", "", "", ""]; 

        const winningConditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ];

        // ************************************
        // منطق الروبوت (خوارزمية Minimax)
        // ************************************

        function checkWinner(board, player) {
            for (let i = 0; i < winningConditions.length; i++) {
                const [a, b, c] = winningConditions[i];
                if (board[a] === player && board[b] === player && board[c] === player) {
                    return true;
                }
            }
            return false;
        }
        
        function getEmptySpots(board) {
            return board.map((cell, index) => cell === "" ? index : null).filter(val => val !== null);
        }

        // دالة Minimax
        function minimax(newBoard, player) {
            const availSpots = getEmptySpots(newBoard);

            if (checkWinner(newBoard, humanPlayer)) {
                return { score: -10 }; // الفوز سيئ للروبوت
            } else if (checkWinner(newBoard, aiPlayer)) {
                return { score: 10 }; // الفوز جيد للروبوت
            } else if (availSpots.length === 0) {
                return { score: 0 }; // تعادل
            }

            const moves = [];

            for (let i = 0; i < availSpots.length; i++) {
                const move = {};
                move.index = availSpots[i];
                newBoard[availSpots[i]] = player;

                if (player === aiPlayer) {
                    const result = minimax(newBoard, humanPlayer);
                    move.score = result.score;
                } else {
                    const result = minimax(newBoard, aiPlayer);
                    move.score = result.score;
                }

                newBoard[availSpots[i]] = ""; // التراجع عن الحركة (Backtracking)
                moves.push(move);
            }

            let bestMove;
            if (player === aiPlayer) {
                let bestScore = -10000;
                for (let i = 0; i < moves.length; i++) {
                    if (moves[i].score > bestScore) {
                        bestScore = moves[i].score;
                        bestMove = moves[i];
                    }
                }
            } else {
                let bestScore = 10000;
                for (let i = 0; i < moves.length; i++) {
                    if (moves[i].score < bestScore) {
                        bestScore = moves[i].score;
                        bestMove = moves[i];
                    }
                }
            }
            return bestMove;
        }

        function handleCellClick(clickedCellEvent) {
            const clickedCell = clickedCellEvent.target;
            const clickedCellIndex = parseInt(clickedCell.getAttribute('data-index'));

            if (gameState[clickedCellIndex] !== "" || !gameActive || currentPlayer !== humanPlayer) {
                return;
            }

            makeMove(clickedCellIndex, humanPlayer);
        }
        
        function makeMove(index, player) {
            gameState[index] = player;
            cells[index].innerHTML = player;
            cells[index].style.color = player === humanPlayer ? "#FF5733" : "#337DFF";

            if (!handleResultValidation()) {
                // إذا لم تنتهي اللعبة، قم بتبديل الدور
                currentPlayer = currentPlayer === humanPlayer ? aiPlayer : humanPlayer;
                statusDisplay.innerHTML = `دور اللاعب **${currentPlayer}**`;
                
                // إذا كان الدور على الروبوت، اجعله يلعب بعد تأخير بسيط
                if (gameActive && currentPlayer === aiPlayer) {
                    setTimeout(aiTurn, 500); // تأخير نصف ثانية
                }
            }
        }

        function aiTurn() {
            const bestSpot = minimax(gameState, aiPlayer).index;
            if (bestSpot !== undefined) {
                 makeMove(bestSpot, aiPlayer);
            }
        }

        function handleResultValidation() {
            let roundWon = false;
            for (let i = 0; i < winningConditions.length; i++) {
                const [a, b, c] = winningConditions[i];
                if (gameState[a] !== '' && gameState[a] === gameState[b] && gameState[a] === gameState[c]) {
                    roundWon = true;
                    // تلوين خط الفوز
                    winningConditions[i].forEach(index => {
                        cells[index].style.backgroundColor = "#D4EDDA";
                    });
                    break;
                }
            }

            if (roundWon) {
                const winner = gameState[winningConditions[0][0]];
                statusDisplay.innerHTML = `اللاعب **${winner}** فاز! 🎉`;
                gameActive = false;
                return true;
            }

            let roundDraw = !gameState.includes("");
            if (roundDraw) {
                statusDisplay.innerHTML = `تعادل! 🤝`;
                gameActive = false;
                return true;
            }
            return false;
        }

        window.resetGame = function() {
            gameActive = true;
            currentPlayer = humanPlayer;
            gameState = ["", "", "", "", "", "", "", "", ""];
            statusDisplay.innerHTML = `Player role **${humanPlayer}**`;
            cells.forEach(cell => {
                cell.innerHTML = "";
                cell.style.backgroundColor = "";
                cell.style.color = "#333";
            });
        }

        cells.forEach(cell => cell.addEventListener('click', handleCellClick));
    </script>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(INDEX_html)

if __name__ == "__main__":
    print("تشغيل الموقع محليًا على http://127.0.0.1:8080")
    app.run(host="127.0.0.1", port=8080, debug=True)

