# DEPLOYMENT — live (deployed 2026-11-20, verified 2026-11-21)

Repo: `halakouai-byte/telegram-channel-prompt-pack` (public) — live on GitHub.
Live Pages URL: `https://telegram-channel-prompt-pack.pages.dev/` (verified live 2026-11-20).
Live Worker URL: `https://prompt-pack-bot.halakouai-byte.workers.dev` (verified live 2026-11-21, HTTP 200, price_usdt 2.00).
workers.dev subdomain: `halakouai-byte` (created via API 2026-11-20 — the old "no subdomain" blocker is gone).
KV namespaces: `ORDERS_KV` + preview created 2026-11-20; the ids are in `worker/wrangler.toml`.
Cron: 2-minute sweep active (created 2026-11-20).
Bot: `@ChannelCraftDeliveryBot` (id 9012830465). Channel: `Telegram Channel Prompts` / `@ChannelCraftDelivery` (id -1004472486910).

> The Cloudflare account ID is a repo secret (`CLOUDFLARE_ACCOUNT_ID`) — it is never written in a file in this repo.

## Status

| Step | State |
|---|---|
| 1. Repo created + pushed | Done (browser creation, then push) |
| 2. Cloudflare Pages (landing page) | Done — live |
| 3. Worker (bot + payments) | Done — live, KV created, URL wired into `tools/build-index.py` (direct web checkout on) |
| 4. Secrets | Mostly done — **open: `SELLER_TON_ADDRESS`** (the seller's public TON receiving address is still needed before any real payment can be verified) |
| 5. Product file_id + webhook | **Verify before the live test** — confirm the webhook is set and `PRODUCT_FILE_ID` is stored (see below) |
| 6. Live test (tiny real payment, second wallet) | **Not done yet** — see below |
| 7. Announce | **Not done** — only after Step 6 passes |

## Former blockers (resolved 2026-11-20/21)

1. **GitHub repo creation** — was blocked (the Muse GitHub App could not create repos, 403). Resolved: the repo was created in the browser and the push landed.
2. **No workers.dev subdomain** — resolved: the subdomain `halakouai-byte` was created via API; the Worker deploys and answers at the URL above.
3. **Cloudflare deploy without a login in this environment** — resolved: deploys run with a Cloudflare API token (via the `wrangler` CLI / GitHub Actions secrets), not a browser login.

## Step 1 — Repo (done)

The repo exists at https://github.com/halakouai-byte/telegram-channel-prompt-pack.git. Pushes to `main` trigger the two deploy workflows (`.github/workflows/deploy-pages.yml`, `deploy-worker.yml`).

## Step 2 — Cloudflare Pages (done)

Deploys `site/` on every push to `main` (`.github/workflows/deploy-pages.yml`, needs repo secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`). The live URL is `https://telegram-channel-prompt-pack.pages.dev/` — it is also the canonical link in `tools/build-index.py`, `site/robots.txt`, and `site/sitemap.xml`. Never hand-edit `site/index.html`: rebuild with `python3 tools/build-index.py` (it reads `content/prompts.sample.json` in this repo, or the full private `prompts.json` on the seller's machine when present).

## Step 3 — Worker (done, except `SELLER_TON_ADDRESS`)

```bash
cd worker
npx wrangler deploy
# live URL: https://prompt-pack-bot.halakouai-byte.workers.dev
```

KV namespaces already exist (ids in `wrangler.toml` — do not recreate them). If they ever need recreating: `npx wrangler kv namespace create ORDERS_KV` (and `--preview`), then paste the ids into `wrangler.toml`.

## Step 4 — Secrets (each prompts for the value; never in a file or chat)

```bash
npx wrangler secret put BOT_TOKEN            # @ChannelCraftDeliveryBot (custom.telegram-prompt)
npx wrangler secret put SELLER_TON_ADDRESS   # seller's Keeper wallet (UQ… / EQ…) — STILL OPEN, needed before the live test
npx wrangler secret put PRODUCT_FILE_ID      # see Step 5
npx wrangler secret put SELLER_TELEGRAM_ID   # seller's numeric id from @userinfobot
npx wrangler secret put TONAPI_KEY           # optional free key from tonconsole.com
npx wrangler secret put WEBHOOK_SECRET       # optional, recommended
```

Also set the non-secret vars in `wrangler.toml` `[vars]`: `BOT_USERNAME="ChannelCraftDeliveryBot"`, `SUPPORT_USERNAME` (seller's public @, no @). Price stays `PRODUCT_PRICE_USDT="2.00"`.

## Step 5 — Product file_id + webhook (verify before the live test)

1. Set the webhook (token + Worker URL + webhook secret in your terminal only):
   `curl -X POST "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook" -H "Content-Type: application/json" -d '{"url":"<WORKER_URL>/webhook","secret_token":"<WEBHOOK_SECRET>","allowed_updates":["message","callback_query"]}'`
   Verify it took: `curl "https://api.telegram.org/bot<BOT_TOKEN>/getWebhookInfo"` — expect
   `"url": "<WORKER_URL>/webhook"` and no `"last_error_message"`. The `secret_token` in the
   setWebhook call must match the `WEBHOOK_SECRET` Worker secret exactly, or the Worker
   403s every update and the bot stays silent.
2. From the seller's own Telegram account, send `channelcraft-prompt-pack.zip`
   (at `~/workspace/prompt-pack/content/`, 168 KB, NOT in this repo) to the bot.
   The bot replies with the `file_id` → `npx wrangler secret put PRODUCT_FILE_ID`.
3. `CONFIG.workerUrl` in `tools/build-index.py` is already the live Worker URL — the landing-page Buy button creates orders directly.

## Step 6 — Live test (BEFORE announcing the store)

Follow `worker/README.md` §7 exactly, with a **second wallet** the seller controls:
pay exactly $2.00 USDT on TON with the memo untouched, tap “I paid”, expect
“Payment confirmed!” + the file, and log line `order_delivered` with
`via: "usdt-comment"`. Also run the negative checks (memo deleted, $1.00 partial,
native-TON fallback, double-tap). Only after §7 steps 3–6 pass, announce the store.
The two unproven items (Keeper memo-forwarding on jetton payments; TonAPI `comment`
on a successful transfer) are proven ONLY by this test.

## Step 7 — Announce

Public channel `Telegram Channel Prompts` / `@ChannelCraftDelivery` + bot
`@ChannelCraftDeliveryBot`. Post the free sample,
link the landing page, and start the daily-post routine (see `../growth/GROWTH.md`).
