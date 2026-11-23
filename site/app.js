// Buy flow. CONFIG: set WORKER_URL after the Worker is deployed; until then
// the Buy button opens the bot, which creates the order itself (/buy).
const CONFIG = {
  workerUrl: "https://prompt-pack-bot.halakouai-byte.workers.dev",
  botUsername: "ChannelCraftDeliveryBot"
};
const buyBtn = document.getElementById("buy-btn");
const box = document.getElementById("order-box");
const note = document.getElementById("buy-note");
if (!CONFIG.workerUrl) {
  buyBtn.href = "https://t.me/" + CONFIG.botUsername + "?start=buy";
  note.textContent = "Checkout runs in Telegram: the bot creates your order and payment link. (Direct web checkout opens here once the payment server is connected.)";
} else {
  buyBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    buyBtn.textContent = "Creating your order…";
    try {
      const r = await fetch(CONFIG.workerUrl + "/api/order", {method: "POST"});
      const d = await r.json();
      if (!r.ok) throw new Error(d.error || ("HTTP " + r.status));
      box.style.display = "block";
      const claim = d.bot_url ? "<p>Then open the bot and tap “I paid”: <a href=\"" + d.bot_url + "\">" + d.bot_url + "</a></p>" : "<p>Then open the bot @" + CONFIG.botUsername + " and send /claim " + d.order_id + ".</p>";
      box.innerHTML = "<p><strong>Your order code: <code>" + d.memo + "</code></strong> — do not edit it in the payment.</p>"
        + "<p>Amount: <strong>$" + d.price_usdt + " USDT on TON</strong></p>"
        + "<p><a class=\"btn\" href=\"" + d.pay_usdt_keeper + "\">Pay $" + d.price_usdt + " USDT (Keeper)</a> "
        + "<a class=\"btn ghost\" href=\"" + d.pay_ton_keeper + "\">Pay in TON instead</a></p>"
        + claim;
      note.textContent = "Order expires in 60 minutes. USDT on TON only; keep the order code in the payment memo.";
    } catch (err) {
      box.style.display = "block";
      box.innerHTML = "<p>Could not create an order right now (" + err.message + "). Please try the bot instead: <a href=\"https://t.me/" + CONFIG.botUsername + "?start=buy\">@" + CONFIG.botUsername + "</a></p>";
    }
    buyBtn.textContent = "Buy now — pay $2 USDT";
  });
}
// Hide the sticky buy bar while the buy section is on screen.
const bar = document.getElementById("sticky-buy");
const buySection = document.getElementById("buy");
if (bar && buySection && "IntersectionObserver" in window) {
  new IntersectionObserver((entries) => {
    bar.classList.toggle("hidden", entries[0].isIntersecting);
  }, {rootMargin: "-32px 0px 0px 0px"}).observe(buySection);
}
