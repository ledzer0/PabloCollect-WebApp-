const user_id = Telegram.WebApp.initDataUnsafe.user?.id || '999';

function buy(pkg, amt) {
  fetch('/create-invoice', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id, package: pkg, amount: amt })
  })
  .then(res => res.json())
  .then(data => {
    if (data.url) {
      window.open(data.url, '_blank');
    } else {
      alert("Failed to create ToyyibPay invoice.");
    }
  });
}

function qrpay(pkg, amt) {
  const qr = `Scan the QR below and pay RM${amt}.\nThen click to submit receipt.`;
  const proof = prompt(qr + "\n\nAfter paying, enter any reference (e.g. your name):");
  if (proof) {
    fetch('/upload-receipt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id, package: pkg, amount: amt, proof })
    })
    .then(() => alert("Receipt submitted for manual review."))
  }
}

function sendCommand() {
  const cmd = document.getElementById("cmdInput").value;
  fetch('/submit-command', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id, command: cmd })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("resultBox").innerText = data.reply;
  });
}

Telegram.WebApp.ready();
