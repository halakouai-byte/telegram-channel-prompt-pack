// Live probe (no keys, no secrets): check the real response envelopes of the
// three public APIs the Worker will call, so the parser is written against
// observed shapes, not memory. Uses only public addresses (the USDT jetton
// master contract itself) — no seller wallet, no real transaction.
// Run: node test/live-probe.mjs   (respects TonAPI no-key limit: 1 req / 4 s)
import { writeFileSync } from 'node:fs';

const USDT_MASTER = 'EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const out = {};

async function get(label, url, headers = {}) {
  const res = await fetch(url, { headers });
  const text = await res.text();
  let json = null;
  try { json = JSON.parse(text); } catch { /* keep raw */ }
  out[label] = { status: res.status, url, body: json ?? text.slice(0, 500) };
  console.log(`--- ${label}: HTTP ${res.status}`);
  console.log(JSON.stringify(out[label].body, null, 2).slice(0, 3000));
  return json;
}

// 1. TonAPI jetton history for the USDT master address (expect: valid envelope, likely empty)
await get(
  'tonapi_jetton_history',
  `https://tonapi.io/v2/accounts/${USDT_MASTER}/jettons/${USDT_MASTER}/history?limit=5`,
);
await sleep(5000); // TonAPI no-key limit: 1 req / 4 s

// 2. TonAPI rates (TON -> USD) for the native-TON fallback amount
await get('tonapi_rates', 'https://tonapi.io/v2/rates?tokens=ton&currencies=usd');
await sleep(5000);

// 3. TON Center v2 getTransactions for the USDT master address (raw tx envelope)
await get(
  'toncenter_getTransactions',
  `https://toncenter.com/api/v2/getTransactions?address=${USDT_MASTER}&limit=2`,
);

writeFileSync(new URL('./live-probe-output.json', import.meta.url), JSON.stringify(out, null, 2));
console.log('\nSaved to test/live-probe-output.json');
