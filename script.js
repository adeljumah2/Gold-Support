function updateInputLabel() {
    const operation = document.getElementById("operation").value;
    const label = document.getElementById("amountLabel");
  
    label.textContent =
      operation === "buy"
        ? "Enter your budget:"
        : "Enter weight to sell (grams):";
  }
  
  function calculate() {
    const operation = document.getElementById("operation").value;
    const goldType = document.getElementById("goldType").value;
    const amount = parseFloat(document.getElementById("amount").value);
  
    if (!amount || amount <= 0) {
      alert("Please enter a valid value");
      return;
    }
  
    
    const purity = {
      "24": 1,
      "21": 0.875,
      "18": 0.75
    };
  
    fetch("data/analysis_results.json")
      .then(res => res.json())
      .then(data => {
  
        const pricePerGram = data.latest_price * purity[goldType];
        let html = "";
  
        if (operation === "buy") {
          const grams = (amount / pricePerGram).toFixed(2);
  
          html = `
            <p><strong>Operation:</strong> Buy</p>
            <p><strong>Gold Type:</strong> ${goldType}K</p>
            <p><strong>Price per gram:</strong> ${pricePerGram.toFixed(2)}</p>
            <p><strong>You can buy:</strong> ${grams} grams</p>
  
            <p><strong>Historically favorable buy days:</strong></p>
            <ul>
              ${data.best_buy_days.map(d =>
                `<li>${d.date.split(" ")[0]} – ${d.price}</li>`
              ).join("")}
            </ul>
          `;
        }
  
        if (operation === "sell") {
          const value = (amount * pricePerGram).toFixed(2);
  
          html = `
            <p><strong>Operation:</strong> Sell</p>
            <p><strong>Gold Type:</strong> ${goldType}K</p>
            <p><strong>Current value:</strong> ${value}</p>
  
            <p><strong>Historically favorable sell days:</strong></p>
            <ul>
              ${data.best_sell_days.map(d =>
                `<li>${d.date.split(" ")[0]} – ${d.price}</li>`
              ).join("")}
            </ul>
          `;
        }
  
        document.getElementById("result").innerHTML = html;
      });
  }
  