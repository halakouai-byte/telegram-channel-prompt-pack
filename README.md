# ChannelCraft Prompt Pack

**ChannelCraft Prompt Pack — 120 AI prompts to run a Telegram channel.**
Price: **$2.00 USDT on TON** (launch price; rises to $3 after launch — one `PRODUCT_PRICE_USDT` change in `worker/wrangler.toml`).

Seller: halakouai-byte. Stack: free Cloudflare Pages (landing page) + free Cloudflare Worker + KV (Telegram bot, TON/USDT payment verification, auto-delivery) + Telegram. No server, no AI at runtime, no secret in this repo — ever.

> **Status: LIVE.** Landing page: https://telegram-channel-prompt-pack.pages.dev/ · Worker: https://prompt-pack-bot.halakouai-byte.workers.dev/ · Bot: @ChannelCraftDeliveryBot · Channel: @ChannelCraftDelivery. The 2-minute cron sweep is active. What is still unproven: the live payment test with a tiny real payment from a second wallet (see "Unproven until the live test" below) — do not present the store as payment-proven until it passes.

## What is in this repo

```
site/                  Landing page (Cloudflare Pages). Mobile-first, English.
  index.html           Hero, what's inside (9 sections), 5 full sample prompts
                       as real indexable text, how buying works, FAQ, $2 price.
                       Buy button calls the Worker POST /api/order (buy flow
                       lives in app.js); the bot link is the fallback.
                       Rebuild with: python3 tools/build-index.py
  styles.css           Page styles (static)
  app.js               Buy-flow JS (static; holds the WORKER_URL / BOT_USERNAME
                       / PRICE constants)
  sample.pdf           Free 10-prompt sample (the only product file that is public)
  robots.txt, sitemap.xml
tools/build-index.py   Regenerates site/index.html from prompts.json (source of truth)
worker/                Cloudflare Worker: Telegram bot + payment verification + delivery
  src/worker.js        Bot, orders, TonAPI verification (primary), TON Center
                       (native-TON fallback), sendDocument delivery, cron sweep
  src/ton.js           Pure payment logic (money math, pay links, parsers, matcher)
  wrangler.toml        Deploy config — NO secrets. PRODUCT_PRICE_USDT = "2.00",
                       KV binding ORDERS_KV (namespace ids are set — created
                       2026-11-20), cron every 2 minutes
  README.md            Deploy steps, exact `wrangler secret put` commands,
                       live-test procedure (do this BEFORE announcing the store)
  FLOW.md              Exact payment flow, every edge case, Telegram Stars risk,
                       Catallaxy parallel listing, upgrade paths
  test/                28 tests (21 unit + 7 e2e dry runs) — 28/28 pass, Node v24
.github/workflows/
  secret-scan.yml      Secret scan (gitleaks v8.28.0, SHA256-verified, full history, fails on any finding) — push to main / PR / weekly Sun 03:00 UTC
  (no Worker deploy workflow: the Worker deploys via wrangler + the promptpack-auto-deploy watcher; deploy-worker.yml was removed in 55969c3)
```

## What is NOT in this repo (on purpose)

The paid product file (`channelcraft-prompt-pack.zip`: full PDF + `prompts.md` + `guide.md`, 171 KB) is **never** committed here — a public repo link would give it away free. It lives outside the repo; the seller uploads it once to the bot, which replies with the Telegram `file_id`, stored as the `PRODUCT_FILE_ID` Worker secret. See `worker/README.md` §5.

## Price — one source of truth

| Place | Value |
|---|---|
| `worker/wrangler.toml` `PRODUCT_PRICE_USDT` | `"2.00"` |
| `worker/src/worker.js` default (`:71`) | `'2.00'` |
| `site/index.html` (hero, buy box, JSON-LD) | $2 |
| Product PDF + sample PDF + `guide.md` | $2 |

## Payment flow (summary)

1. Buyer taps **Buy** → Worker creates order `PP-XXXXXX` (60-min expiry), price locked at creation.
2. Buyer pays **$2.00 USDT on TON** via a Keeper deep link, memo = order code, untouched.
3. Buyer taps “I paid” (or the 2-min cron sweep finds it) → Worker verifies against **TonAPI jetton history (primary)** / TON Center (native-TON fallback), claims the tx hash in KV (no double-delivery), bot sends the file.
4. Wrong amount / missing memo / ambiguous / late payment → `needs_review`, never auto-delivered on ambiguity. Full table in `worker/FLOW.md` §4.

## Unproven until the live test (do NOT claim otherwise)

Per `worker/README.md` §7, two things only a tiny real payment from a second wallet can prove: (1) Keeper forwards the `text=` memo on a **jetton (USDT)** payment so it appears in TonAPI's jetton history; (2) a real successful transfer shows `status: "success"` in TonAPI. Tier-2 matching (unique exact amount + time) + manual `/deliver` are the fallback until the test passes.

## Telegram Stars risk

Telegram's Bot Terms (§6.2) say digital goods in bots must be sold in Stars; selling for TON inside a bot risks the bot being hidden from mobile users. Mitigation (per the research report §3.4): payment executes in the external wallet (Keeper) — the bot shows the price and a Keeper pay link in-chat but never issues a Telegram invoice and never takes payment inside Telegram; a Stars-priced version is the fallback if the bot is ever restricted. This is a partial mitigation, not a total one. See `worker/FLOW.md` §6.

## Licence

All rights reserved. This repo is the public storefront (landing page, Worker code, docs) for a paid product. The product file itself (`channelcraft-prompt-pack.zip`) is never in this repo. Do not copy, resell, share, or redistribute any part of this repo or the product.

## Deploy

The Cloudflare Pages project `telegram-channel-prompt-pack` is connected to this repo on GitHub. Every push to `main` triggers a Cloudflare build (no build command, deploy root is the `site/` folder, preview builds off). No secret is needed on GitHub for the Pages deploy.
