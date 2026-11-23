#!/usr/bin/env python3
"""Build site/index.html for the ChannelCraft Prompt Pack landing page.

Reads prompts.json (source of truth) and embeds 5 full free-sample prompts
as real indexable text, plus the 9 section list and all 10 sample titles.
Run from the repo root:  python3 tools/build-index.py
Price is a single constant here — launch price $2.00 (see PRICE below).

Design: dark, mobile-first store page. No external fonts, images, JS libs
or trackers. Styles live in site/styles.css and the buy-flow JS in
site/app.js (both static files, edited directly — the buy-flow constants
WORKER_URL / BOT_USERNAME / PRICE live in app.js; keep them in sync with
the constants below). This script only generates site/index.html.
Edit the template here, never site/index.html directly.
"""
import json, html, pathlib

PRICE = "2.00"
PRICE_DISPLAY = "$2"
PRICE_FUTURE = "$3"  # struck-through next to the launch price: honest anchoring —
# launch price $2 (struck-through $3); the price rises to $3 after launch.
WORKER_URL = "https://prompt-pack-bot.halakouai-byte.workers.dev"  # live Worker; subdomain halakouai-byte created via API 2026-11-20 (no dashboard visit needed)
BOT_USERNAME = "ChannelCraftDeliveryBot"   # real bot, created by user 2026-11-20
CHANNEL_USERNAME = "ChannelCraftDelivery"  # real channel, created by user 2026-11-20
PAGES_URL = "https://telegram-channel-prompt-pack.pages.dev"  # expected Pages URL; confirm after deploy

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.load(open(ROOT.parent / "prompt-pack" / "content" / "prompts.json")) \
    if (ROOT.parent / "prompt-pack" / "content" / "prompts.json").exists() \
    else json.load(open(pathlib.Path.home() / "workspace/prompt-pack/content/prompts.json"))
PROMPTS = {p["id"]: p for p in DATA["prompts"]}
SECTIONS = DATA["sections"]
SAMPLE_IDS = [p["id"] for p in DATA["prompts"] if p.get("sample")]
SHOW_FULL = [1, 13, 31, 51, 63]  # 5 full sample prompts shown as text on the page

def section_rows():
    rows, start = [], 1
    for s in SECTIONS:
        end = start + s["count"] - 1
        rows.append(
            f'<li><span class="sec-num" aria-hidden="true">{s["id"]}</span>'
            f'<div><strong>{html.escape(s["title"])}</strong>'
            f'<span class="sec-meta">{s["count"]} prompts · #{start}–#{end}</span></div></li>')
        start = end + 1
    return "\n".join(rows)

def sample_cards():
    out = []
    for pid in SHOW_FULL:
        p = PROMPTS[pid]
        out.append(
            f'<article class="sample"><h3>Prompt #{p["id"]} — {html.escape(p["title"])}'
            f'<span class="tag">Free sample</span></h3>'
            f'<p class="purpose">{html.escape(p["purpose"])}</p>'
            f'<blockquote>{html.escape(p["prompt"])}</blockquote>'
            f'<p class="example"><strong>Example:</strong> {html.escape(p["example"])}</p></article>')
    return "\n".join(out)

def sample_titles():
    items = "".join(
        f'<li>Prompt #{p["id"]} — {html.escape(p["title"])}</li>'
        for p in (PROMPTS[i] for i in SAMPLE_IDS))
    return f"<ul class=\"sample-list\">{items}</ul>"

CHECK = ('<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
         '<circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.5"/>'
         '<path d="M5 8.2l2 2 4-4.4" stroke="currentColor" stroke-width="1.5"'
         ' stroke-linecap="round" stroke-linejoin="round"/></svg>')

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3' fill='%230f172a'/%3E%3Ctext x='8' y='12' font-size='11' text-anchor='middle' fill='%23fbbf24' font-family='sans-serif' font-weight='bold'%3EC%3C/text%3E%3C/svg%3E">
<title>ChannelCraft Prompt Pack — 120 AI Prompts to Run a Telegram Channel ({PRICE_DISPLAY})</title>
<meta name="description" content="ChannelCraft Prompt Pack: 120 ready-made AI prompts in 9 sections to run a Telegram channel — posts, hooks, polls, quizzes, growth and selling. Works with ChatGPT, Claude, Gemini and DeepSeek. {PRICE_DISPLAY} in USDT on TON, delivered by Telegram bot. Free 10-prompt sample.">
<link rel="canonical" href="{PAGES_URL}/">
<meta property="og:type" content="product">
<meta property="og:title" content="ChannelCraft Prompt Pack — 120 AI Prompts to Run a Telegram Channel">
<meta property="og:description" content="120 ready-made prompts for Telegram channel owners. Posts, hooks, polls, quizzes, growth and selling. {PRICE_DISPLAY} in USDT on TON. Free 10-prompt sample.">
<meta property="og:url" content="{PAGES_URL}/">
<meta name="robots" content="index, follow">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Product","name":"ChannelCraft Prompt Pack",
"description":"120 AI prompts to run a Telegram channel, in 9 sections, plus a quick-start guide. Works with ChatGPT, Claude, Gemini, DeepSeek and any AI chatbot.",
"brand":{{"@type":"Brand","name":"ChannelCraft"}},"offers":{{"@type":"Offer","price":"{PRICE}","priceCurrency":"USD","availability":"https://schema.org/InStock"}}}}
</script>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="site-header"><div class="wrap"><a class="logo" href="#">Channel<span>Craft</span></a><a class="header-buy" href="#buy">Buy — {PRICE_DISPLAY}</a></div></header>
<main class="wrap">
<section class="hero">
<div class="hero-grid">
<div>
<p class="eyebrow">ChannelCraft · Telegram channel toolkit</p>
<h1>120 AI prompts to run a Telegram channel</h1>
<p class="lead">Stop staring at a blank post box. Copy a prompt, fill in the [brackets] with your own details, paste it into your AI chatbot — and get a post, a poll, a quiz, a hook or a plan back in seconds. Works with ChatGPT, Claude, Gemini, DeepSeek and any AI chatbot.</p>
<div class="price-row"><span class="price"><s>{PRICE_FUTURE}</s>{PRICE_DISPLAY}</span><span class="save">Save 33% — launch price</span></div>
<p class="price-note">Launch price — rises to {PRICE_FUTURE} after launch. USDT on TON · one-time payment.</p>
<p class="cta-row"><a class="btn" href="#buy">Buy the pack — {PRICE_DISPLAY}</a>
<a class="btn ghost" href="sample.pdf">Download the free 10-prompt sample (PDF)</a></p>
<p class="muted">No account needed. No subscription. You get a PDF (47 pages) + all 120 prompts as text + a quick-start guide. Delivered by Telegram bot after payment.</p>
</div>
<aside class="pack" aria-hidden="true">
<div class="pack-top"><span class="pack-mark">C</span><span class="pack-brand">ChannelCraft</span></div>
<p class="pack-title">120 AI Prompts</p>
<p class="pack-sub">to run a Telegram channel</p>
<ul class="pack-files">
<li><span class="file-ico">PDF</span>Prompt pack · 47 pages</li>
<li><span class="file-ico">TXT</span>All 120 prompts as text</li>
<li><span class="file-ico">GUIDE</span>Quick-start guide</li>
</ul>
<p class="pack-price"><s>{PRICE_FUTURE}</s>{PRICE_DISPLAY} <span>one-time</span></p>
</aside>
</div>
<ul class="trust">
<li>{CHECK}Instant delivery after payment is verified</li>
<li>{CHECK}One-time payment — no subscription</li>
<li>{CHECK}Free 10-prompt sample — try before you buy</li>
<li>{CHECK}Secure payment in USDT on TON</li>
<li>{CHECK}No account needed</li>
</ul>
</section>

<section id="inside">
<p class="eyebrow">Inside the pack</p>
<h2>What is inside</h2>
<p class="section-intro">120 prompts in 9 sections — one section for each job a channel owner actually does:</p>
<ul class="sections">
{section_rows()}
</ul>
<p>Every prompt has a title, what it is for, the prompt itself, and a short filled-in example so you can see how to use it. The pack also includes an 8-part quick-start guide: the 60-second workflow, a 3-posts-a-week plan, and what to do when a result is not good enough.</p>
</section>

<section id="how">
<p class="eyebrow">How it works</p>
<h2>How it works</h2>
<ol class="steps">
<li><strong>Pick a prompt</strong> for the job you need right now — a post, a hook, a poll, a growth idea.</li>
<li><strong>Replace every [bracketed item]</strong> with your own details. <em>[topic]</em> becomes “English vocabulary”, <em>[audience]</em> becomes “adult beginners”.</li>
<li><strong>Paste it into your AI chatbot</strong> and read the answer. If it is too long or too formal, reply with one short correction — “Shorter, under 100 words.”</li>
<li><strong>Edit before you post.</strong> Check every fact, delete anything that does not sound like you, add one detail only you could know.</li>
</ol>
<p class="muted">One prompt, one job. That is the rule the whole pack is built on.</p>
</section>

<section id="samples">
<p class="eyebrow">Try before you buy</p>
<h2>Try 5 prompts before you buy</h2>
<p class="section-intro">These 5 prompts are from the free 10-prompt sample — the full sample (10 prompts, PDF) is <a href="sample.pdf">free to download</a>. Read them, try one, then decide.</p>
{sample_cards()}
<h3>All 10 free-sample prompts</h3>
{sample_titles()}
<p><a class="btn ghost" href="sample.pdf">Download the free sample (PDF, 6 pages)</a></p>
</section>

<section id="buy">
<p class="eyebrow">Checkout</p>
<h2>Buy the pack — {PRICE_DISPLAY}</h2>
<div class="buy-card">
<p><strong>What you get:</strong></p>
<div class="get-grid">
<div class="get"><strong>PDF · 47 pages</strong><span>The full 120-prompt pack</span></div>
<div class="get"><strong>Text file</strong><span>All 120 prompts as plain text</span></div>
<div class="get"><strong>Quick-start guide</strong><span>Workflow, plan &amp; fixes</span></div>
</div>
<p class="muted">All three in one ZIP, under 1&nbsp;MB — it opens on any phone.</p>
<p><strong>Price:</strong> {PRICE_DISPLAY} in USDT on the TON network. One-time payment, personal use.</p>
<p><a class="btn btn-block" href="https://t.me/{BOT_USERNAME}?start=buy" id="buy-btn">Buy now — pay {PRICE_DISPLAY} USDT</a></p>
<div id="order-box"></div>
<p class="muted" id="buy-note"></p>
</div>
<h3>How buying works</h3>
<ol class="steps">
<li>Tap <strong>Buy now</strong>. The bot creates your order and gives you a unique order code (for example <code>PP-XXXXXX</code>).</li>
<li>Pay exactly <strong>{PRICE_DISPLAY} USDT on TON</strong> with your Keeper (Tonkeeper) wallet. The payment link is pre-filled — just confirm it.</li>
<li>Tap <strong>“I paid”</strong> in the bot. The payment is checked on the TON blockchain and the file is sent to you in the bot, usually within a minute or two.</li>
<li>Keep your order code. It is how a payment is matched to your order, and how support can help if anything goes wrong.</li>
</ol>
<div class="important">
<p><strong>Important — read before you pay:</strong></p>
<ul>
<li>Pay <strong>USDT on the TON network only</strong>. USDT sent on Tron, Ethereum or any other network cannot be seen or matched automatically.</li>
<li>Do <strong>not edit or delete the memo / order code</strong> in the payment. Without it, delivery has to be done manually and takes longer.</li>
<li>Pay the <strong>exact amount</strong>. If you pay less, the bot will tell you the remaining amount — a top-up with the same order code completes it.</li>
<li>Crypto payments are irreversible. If something goes wrong, contact support through the bot with your order code and transaction hash.</li>
</ul>
</div>
</section>

<section id="faq">
<p class="eyebrow">Questions</p>
<h2>Questions</h2>
<details><summary>Which AI tools do the prompts work with?</summary><p>Any AI chatbot: ChatGPT, Claude, Gemini, DeepSeek and others. The prompts are plain text — no plugin, no account and no special tool is needed.</p></details>
<details><summary>How do I pay?</summary><p>In USDT on the TON network, from a wallet such as Keeper (Tonkeeper). You pay from the order the bot creates for you; the payment link is pre-filled with the amount and your order code.</p></details>
<details><summary>How do I receive the pack?</summary><p>The Telegram bot sends you the file right after your payment is confirmed on-chain — usually within a minute or two of tapping “I paid”. No email and no download link: delivery is through the bot only.</p></details>
<details><summary>What exactly do I get?</summary><p>One ZIP file: the 120-prompt PDF (47 pages), all 120 prompts as a plain-text file, and the quick-start guide. Total size under 1 MB — it opens on any phone.</p></details>
<details><summary>Can I try it first?</summary><p>Yes — the <a href="sample.pdf">free 10-prompt sample (PDF)</a> is the real thing, one or two prompts from each part of the pack. Try them before you pay.</p></details>
<details><summary>What if my payment is not found?</summary><p>First check that you paid USDT on TON (not Tron or Ethereum) with the order code untouched. Then send the bot your transaction hash with <code>/tx &lt;hash&gt;</code>, or contact support with your order code. Payments that arrive late or without a code are reviewed manually — your money is not lost, but delivery takes longer.</p></details>
<details><summary>Can I get a refund?</summary><p>Crypto payments cannot be reversed automatically. If you paid and never received the file, contact support through the bot with your order code — every case is reviewed, and a manual refund is possible when the payment is confirmed and delivery truly failed.</p></details>
<details><summary>Can I share or resell the pack?</summary><p>No. The licence is personal use for your own channel(s). Do not resell, share or redistribute the file.</p></details>
<details><summary>Will this grow my channel or make me money?</summary><p>No — and nobody honest can promise that. This pack is a tool: it makes writing faster and more consistent. Growth depends on posting regularly, replying to subscribers, and time. There are no income or subscriber promises in this pack, on this page, or anywhere else. Honest ranges: month 1, $0–15 (most likely $0–5); month 3, $0–30 typical.</p></details>
</section>

<section id="about">
<p class="eyebrow">About</p>
<h2>Who is behind this</h2>
<p>Made by <strong>halakouai-byte</strong>, a freelance developer who builds small self-running tools. Questions or problems with an order: contact support through the bot — <a href="https://t.me/{BOT_USERNAME}">@{BOT_USERNAME}</a>. Channel: <a href="https://t.me/{CHANNEL_USERNAME}">@{CHANNEL_USERNAME}</a>.</p>
<p class="muted">This page is the only official sales page. The product file itself is never posted at a public link — it is delivered by the bot only after a verified payment.</p>
</section>
</main>
<footer>
<div class="wrap">
<p>ChannelCraft Prompt Pack v2.0 — 120 AI prompts to run a Telegram channel. Price {PRICE_DISPLAY} USDT on TON (launch price). Personal use only. No income, subscriber or results promises are made anywhere in this product.</p>
<p><a href="sample.pdf">Free sample (PDF)</a> · <a href="https://t.me/{BOT_USERNAME}">Bot</a> · <a href="https://t.me/{CHANNEL_USERNAME}">Channel</a> · <a href="https://github.com/halakouai-byte/telegram-channel-prompt-pack">GitHub</a></p>
</div>
</footer>
<div class="sticky-buy" id="sticky-buy">
<span class="sb-price">{PRICE_DISPLAY} <small>one-time · USDT on TON</small></span>
<a class="btn" href="#buy">Buy the pack</a>
</div>
<script src="app.js"></script>
</body>
</html>
"""
out = ROOT / "site" / "index.html"
out.write_text(page, encoding="utf-8")
print("wrote", out, len(page), "bytes")
print("sample ids:", SAMPLE_IDS)
