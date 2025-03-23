// script.js
document.addEventListener("DOMContentLoaded", () => {
    const startBtn = document.getElementById("start-btn");
    const guessInput = document.getElementById("guess-input");
    const submitGuessBtn = document.getElementById("submit-guess");
    const hintBtn = document.getElementById("hint-btn");
    const revealBtn = document.getElementById("reveal-btn");
    const feedback = document.getElementById("feedback");
    const feedback2 = document.getElementById("feedback2");
    const hint = document.getElementById("hint");

    let targetCountry = "";

    startBtn.addEventListener("click", async () => {
        const response = await fetch("http://localhost:5001/random-country");
        const data = await response.json();
        targetCountry = data.random_country;
        feedback2.innerHTML = "Oyun başladi! Tahmininizi yapin.";
        feedback.innerHTML = "";
        hint.innerHTML = "";
        console.log(targetCountry);
    });

    submitGuessBtn.addEventListener("click", async () => {
        const userGuess = guessInput.value.trim();
        if (!userGuess) return;

        const matchResponse = await fetch("http://localhost:5001/best-match", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ country: userGuess })
        });
        const matchData = await matchResponse.json();
        const bestMatch = matchData.best_match;
        feedback2.innerHTML = `Tahmin edilen ülke: ${bestMatch}`;
        const distanceResponse = await fetch("http://localhost:5001/distance", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ country1: bestMatch, country2: targetCountry })
        });
        const distanceData = await distanceResponse.json();

        const neighborsResponse = await fetch(`http://localhost:5001/neighbors/${bestMatch}`);
        const neighborsData = await neighborsResponse.json();

        if (neighborsData.neighbors.includes(targetCountry)) {
            feedback.innerHTML = `${bestMatch} hedef ülkenin komşusu! ${distanceData.distance_km} km uzaklıkta.`;
        } else  {
            if(distanceData.distance_km == 0){
                feedback.innerHTML = "Tebrikler! Doğru tahmin!";
            }else{
                feedback.innerHTML = `${bestMatch} hedef ülkeye ${distanceData.distance_km} km uzaklıkta.`;
            }
            
        }

        
    });

    hintBtn.addEventListener("click", async () => {
        const response = await fetch(`http://localhost:5001/neighbors/${targetCountry}`);
        const data = await response.json();

        const validNeighbors = data.neighbors.filter(neighbor => neighbor.trim() !== "");

        if (validNeighbors.length === 0) {
            hint.innerHTML = `Ülkenin komşusu yok.`;
        } else {
            hint.innerHTML = `Ülkenin komşuları: ${validNeighbors.join(", ")}`;
        }
        
    });

    revealBtn.addEventListener("click", () => {
        hint.innerHTML = `Doğru cevap: ${targetCountry}`;
    });
});
