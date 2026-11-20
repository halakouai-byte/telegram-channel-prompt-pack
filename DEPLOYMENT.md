# DEPLOYMENT — ordered checklist (deploy-ready, not yet deployed)

Repo: `halakouai-byte/telegram-channel-prompt-pack` (public) — **does not exist yet on GitHub.**
Expected Pages URL: `https://telegram-channel-prompt-pack.pages.dev/` (confirm after deploy).
Expected Worker URL: `https://prompt-pack-bot.<subdomain>.workers.dev` (note it after deploy).

## Blockers (why this is not live yet)

1. **GitHub repo creation — needs approval / browser.** `create_repository` via the
   Muse GitHub App was attempted 2026-11-20 17:20 Tehran: the approval card timed out
   (`approval_expired`, approval `connector-attempt-4a93e57d…`). The action was NOT
   performed. Do NOT silently retry — the user/parent must approve a fresh attempt,
   or create the repo in the browser (public, empty, no README) and the push below
   fills it. (Separate known fact: `create_repository` via this App returned 403 on
   2026-11-20 while pushes to existing repos work, so a browser-created repo is the
   likely path.)
2. **Cloudflare deploy — no login in this environment.** `wrangler` 4.165.0 IS
   installable via `npx wrangler`, but there is no `~/.wrangler` login and no
   `CLOUDFLARE_API_TOKEN` here. Deploy must run where `wrangler login` (browser
   OAuth) or a Cloudflare API token is available. Nothing was faked: no Pages URL
   and no Worker URL exist yet.

## Step 1 — Create the repo, push this folder

```bash
# in the browser (or an approved create_repository call): create public repo
# halakouai-byte/telegram-channel-prompt-pack, empty.
# NOTE: the footer GitHub link on the landing page 404s until this repo exists —
# it goes live the moment this push lands. Do not launch the page before Step 1.
cd ~/workspace/prompt-pack/repo
git init -b main
git add .
git commit -m "ChannelCraft Prompt Pack v1.0: landing page + Worker storefront ($2 USDT on TON)"
git remote add origin https://github.com/halakouai-byte/telegram-channel-prompt-pack.git
git push -u origin main
```

## Step 2 — Cloudflare Pages (landing page)

Option A — GitHub Actions (already in this repo): add repo secrets
`CLOUDFLARE_API_TOKEN` (needs Account:Pages:Edit + Account:Workers:Edit) and
`CLOUDFLARE_ACCOUNT_ID` (`4615c127356ea4c4be6f4058e6f819d1` — Halakouac@gmail.com's
Account), then push; `.github/workflows/deploy-pages.yml` deploys `site/`.
**Unverified assumption:** Option A assumes `cloudflare/pages-action@v1` creates
the Pages project if it does not exist yet — this was NOT verified (no deploy
was permitted during the audit). If the action fails with a missing-project
error, create the project first in the Cloudflare dashboard (Option B below),
then re-run the workflow.
Option B — dashboard: Cloudflare → Workers & Pages → Create → Pages → Connect to
Git → pick this repo → build output directory `site/` (no build command; static).
Confirm the live URL and update the `PAGES_URL` in three places — `tools/build-index.py`
(the canonical link is generated from it, so it is NOT a separate edit; hand-editing
`site/index.html` would be overwritten by the next rebuild), `site/robots.txt`, and
`site/sitemap.xml` — then rebuild + redeploy.

## Step 3 — Worker (bot + payments)

**Create the bot FIRST (D13):** in Telegram, @BotFather → `/newbot` → name it
`ChannelCraftBot` (fallback `ChannelCraftPackBot` if taken — if you use the
fallback, use it EVERYWHERE: Step 4's `BOT_TOKEN` note, Step 5's webhook, Step 7,
`wrangler.toml` `BOT_USERNAME`, and the landing page's `BOT_USERNAME` in
`tools/build-index.py`). The token goes straight into `wrangler secret put
BOT_TOKEN` below — never into chat, a file, or the repo.

```bash
cd worker
npx wrangler login
npx wrangler kv namespace create ORDERS_KV
npx wrangler kv namespace create ORDERS_KV --preview
# paste the two ids into wrangler.toml (replace the <YOUR_KV_NAMESPACE_ID> placeholders)
npx wrangler deploy
# note the URL, e.g. https://prompt-pack-bot.<subdomain>.workers.dev
```

## Step 4 — Secrets (each prompts for the value; never in a file or chat)

```bash
npx wrangler secret put BOT_TOKEN            # from @BotFather (/newbot -> @ChannelCraftBot)
npx wrangler secret put SELLER_TON_ADDRESS   # seller's Keeper wallet (UQ… / EQ…)
npx wrangler secret put PRODUCT_FILE_ID      # see Step 5
npx wrangler secret put SELLER_TELEGRAM_ID   # seller's numeric id from @userinfobot
npx wrangler secret put TONAPI_KEY           # optional free key from tonconsole.com
npx wrangler secret put WEBHOOK_SECRET       # optional, recommended
```

Also set the non-secret vars in `wrangler.toml` `[vars]`: `BOT_USERNAME="ChannelCraftBot"`,
`SUPPORT_USERNAME` (seller's public @, no @). Price stays `PRODUCT_PRICE_USDT="2.00"`.

## Step 5 — Product file_id + webhook

1. Set the webhook (token + Worker URL + webhook secret in your terminal only):
   `curl -X POST "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook" -H "Content-Type: application/json" -d '{"url":"<WORKER_URL>/webhook","secret_token":"<WEBHOOK_SECRET>","allowed_updates":["message","callback_query"]}'`
   Verify it took: `curl "https://api.telegram.org/bot<BOT_TOKEN>/getWebhookInfo"` — expect
   `"url": "<WORKER_URL>/webhook"` and no `"last_error_message"`. The `secret_token` in the
   setWebhook call must match the `WEBHOOK_SECRET` Worker secret exactly, or the Worker
   403s every update and the bot stays silent.
2. From the seller's own Telegram account, send `channelcraft-prompt-pack.zip`
   (at `~/workspace/prompt-pack/content/`, 168 KB, NOT in this repo) to the bot.
   The bot replies with the `file_id` → `npx wrangler secret put PRODUCT_FILE_ID`.
3. Set `CONFIG.workerUrl` in `tools/build-index.py` to the Worker URL, rebuild
   (`python3 tools/build-index.py`), push — the landing-page Buy button then creates
   orders directly.

## Step 6 — Live test (BEFORE announcing the store)

Follow `worker/README.md` §7 exactly, with a **second wallet** the seller controls:
pay exactly $2.00 USDT on TON with the memo untouched, tap “I paid”, expect
“Payment confirmed!” + the file, and log line `order_delivered` with
`via: "usdt-comment"`. Also run the negative checks (memo deleted, $1.00 partial,
native-TON fallback, double-tap). Only after §7 steps 3–6 pass, announce the store.
The two unproven items (Keeper memo-forwarding on jetton payments; TonAPI `comment`
on a successful transfer) are proven ONLY by this test.

## Step 7 — Announce

Public channel `Telegram Channel Prompts` / `@TelegramChannelPrompts` + bot
`@ChannelCraftBot` (fallback `@ChannelCraftPackBot` if taken). Post the free sample,
link the landing page, and start the daily-post routine (see `../growth/GROWTH.md`).
