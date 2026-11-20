# DEPLOYMENT — ChannelCraft Prompt Pack (LIVE)

Repo: `halakouai-byte/telegram-channel-prompt-pack` (public).
Live URLs (verified 2026-11-20/21):
- Landing page: `https://telegram-channel-prompt-pack.pages.dev/`
- Worker: `https://prompt-pack-bot.halakouai-byte.workers.dev/` (`GET /health` returns `{"ok":true,"service":"prompt-pack-bot","price_usdt":"2.00"}`)
- Bot: `@ChannelCraftDeliveryBot` · Channel: `@ChannelCraftDelivery`

Status: **LIVE.** The store is deployed and the 2-minute payment sweep (cron) is active. What is still unproven: the live payment test with a tiny real payment from a second wallet (Step 6) — do not present the store as payment-proven until it passes.

## Open items (not blockers for content work)

1. **Live payment test** (Step 6) still needs the seller's real public TON address (`SELLER_TON_ADDRESS`), the product `PRODUCT_FILE_ID` (send the product ZIP to the bot once), and the seller's numeric Telegram ID (`SELLER_TELEGRAM_ID`). Until those land, the Worker holds clearly-marked placeholder values (`PENDING_SET_BY_SELLER`) that cannot receive money.
2. **Quality audit** (2026-11-21): 100% of the 120 prompts were tested and 11 rewritten (see `qa/`); the v2 content merge to `main` waits on the owner's approval of the new-product list.

## Step 1 — Repo (DONE 2026-11-20)

Repo created (public) and pushed; `main` is the live branch. Every push to `main` auto-deploys the landing page (Step 2) — there is no separate "push then deploy" step anymore.

## Step 2 — Cloudflare Pages (landing page): native GitHub link

**The Pages project `telegram-channel-prompt-pack` is connected to this repo natively (Cloudflare ↔ GitHub). It deploys automatically on every push to `main`.**

- No build command, deploy root `site/`, preview builds OFF (`preview_deployment_setting: "none"`).
- No GitHub secret is needed for Pages. Do NOT add `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID` repo secrets for Pages, and do NOT deploy Pages with `wrangler pages deploy` — the native link is the only deploy path.
- The old GitHub Actions workflow `.github/workflows/deploy-pages.yml` (which deployed via `cloudflare/pages-action` with API-token secrets) is **superseded** by the native link. It still exists in the repo and must be removed so it cannot fire on `site/**` pushes and conflict with the native deploy. (Follow-up: delete that file.)
- Confirm a deploy worked: push to `main`, then check the Pages project (or `curl -s https://telegram-channel-prompt-pack.pages.dev/` — expect HTTP 200 and the current page). The native link creates a GitHub build/check on each push; a successful build means the site is live.
- `site/index.html` is generated from `tools/build-index.py` (which reads `~/workspace/prompt-pack/content/prompts.json`); never hand-edit it. After editing `tools/build-index.py`, rebuild (`python3 tools/build-index.py`) and push to `main` — the native link deploys the rebuild automatically.

## Step 3 — Worker (bot + payments) (DONE 2026-11-20)

Worker `prompt-pack-bot` is deployed with `wrangler`, KV namespace `ORDERS_KV` is created and bound, the 2-minute cron trigger (`*/2 * * * *`) is attached, and the webhook is set. To redeploy the Worker (it still deploys with `wrangler`, not via GitHub):

```bash
cd worker
npx wrangler deploy
# note the URL, e.g. https://prompt-pack-bot.halakouai-byte.workers.dev
```

`wrangler deploy` uploads the Worker AND sets the cron trigger from `wrangler.toml` `[triggers]`. Never hand-roll the script-upload API (an earlier hand-rolled upload stored manifest hashes without file contents and the Worker would not run).

## Step 4 — Secrets (each prompts for the value; never in a file or chat)

```bash
npx wrangler secret put BOT_TOKEN            # @ChannelCraftDeliveryBot (custom.telegram-prompt) — ALREADY SET
npx wrangler secret put SELLER_TON_ADDRESS   # seller's Keeper wallet (UQ… / EQ…) — PENDING (placeholder in Worker)
npx wrangler secret put PRODUCT_FILE_ID      # see Step 5 — PENDING (placeholder in Worker)
npx wrangler secret put SELLER_TELEGRAM_ID   # seller's numeric id from @userinfobot — PENDING
npx wrangler secret put TONAPI_KEY           # optional free key from tonconsole.com
npx wrangler secret put WEBHOOK_SECRET       # ALREADY SET (generated 2026-11-20)
```

Also set the non-secret vars in `wrangler.toml` `[vars]`: `BOT_USERNAME="ChannelCraftDeliveryBot"`,
`SUPPORT_USERNAME` (seller's public @, no @). Price stays `PRODUCT_PRICE_USDT="2.00"`.

## Step 5 — Product file_id + webhook

1. Webhook: **already set** (2026-11-20). Verify it took: `curl "https://api.telegram.org/bot<BOT_TOKEN>/getWebhookInfo"` — expect
   `"url": "https://prompt-pack-bot.halakouai-byte.workers.dev/webhook"` and no `"last_error_message"`. The `secret_token` in the
   setWebhook call must match the `WEBHOOK_SECRET` Worker secret exactly, or the Worker
   403s every update and the bot stays silent. (The webhook was set with the secret; do not re-set it without rotating the Worker secret too.)
2. From the seller's own Telegram account, send `channelcraft-prompt-pack.zip`
   (at `~/workspace/prompt-pack/content/`, NOT in this repo) to the bot.
   The bot replies with the `file_id` → `npx wrangler secret put PRODUCT_FILE_ID`.
3. `WORKER_URL` is already set in `tools/build-index.py` (`https://prompt-pack-bot.halakouai-byte.workers.dev`) and the landing-page Buy button already creates orders directly. No rebuild is needed for this step.

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
Do not announce (and do not publish any channel post) without manager approval.
