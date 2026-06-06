# L114 — Discord/Telegram Bot for Alerts: Pick Both, Discord First

**Loop**: 114 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

L131 will design the alerts UX surface (per-user alert configuration on the web app). This loop picks the *delivery channels* — where alerts arrive after they fire. The candidates: Discord, Telegram, Slack, email, SMS, web push, mobile push, RSS.

The honest answer: ship **both Discord and Telegram bots** as the marquee channels at v1, plus email and a personalized RSS feed as the universal fallbacks. Slack is deferred (its tribal-of-work audience is wrong for OPENGEM at v1). SMS is deferred (no good async-Python provider with global coverage at v1 pricing). Web push is deferred to L115 PWA. Mobile push only after a real native app (also L115).

The ordering — Discord *first*, Telegram *second* — is non-obvious. The case is below.

Verdict: **Discord bot at v1 launch. Telegram bot at v1.1 (within 30 days). Email + per-user RSS as universal fallbacks. Both bots are stateless workers consuming from the Arq `notifications` queue (L102); both authenticate against OPENGEM accounts via OAuth-style link flows (Discord OAuth2 + Telegram's deep-link bot pairing). One alert rule on the OPENGEM web app can fan out to any subset of channels the user has connected.**

---

## Why Discord first

The Discord case rests on three facts:

1. **Discord is where the macro power-users actually hang out in 2026.** "Macro Discord" is a real subculture — there are servers like Hedgeye's, Bull/Bear server, Crypto Macro server, several r/Economics-adjacent communities, plus dozens of analyst-private servers. The Damian-class YouTuber persona runs a Discord for their viewers. The Greg-class blogger drops into Discord servers to discuss data. Reaching macro power-users through Discord is *closer* to where they are than email or even Twitter.

2. **Discord's bot API is the best-in-class for our shape.** Discord supports slash commands, interactive embeds, threaded replies, rich attachments (charts as embedded images), reactions for low-friction acknowledgment, scheduled messages, webhooks for fan-out. The developer experience is excellent. Rate limits are generous (50 requests/second/bot baseline; "user installable apps" model since 2024 lifts this further). A single bot can serve hundreds of OPENGEM users across hundreds of servers.

3. **Discord drives community formation.** An alert delivered into a Discord channel triggers conversation — others in the channel see the alert, react, discuss. Email alerts disappear into individual inboxes; Discord alerts compound into community discussion. This is the *content flywheel* — every alert in a Discord channel is a moment of OPENGEM brand visibility for everyone in that channel, not just the subscriber.

The OPENGEM Discord bot does three things at v1:

- **Personal DMs**: a user subscribes to an alert rule on the web app; matching events arrive as DMs from the OPENGEM bot.
- **Server-channel post**: a user with admin rights in a Discord server can install the OPENGEM bot to a channel; subscribed alerts post to that channel (with a configurable filter like "only fire if probability moved >5%").
- **Slash commands for inline querying**: `/og forecast usa cpi` returns a forecast snapshot directly in the channel. `/og pulse` returns the current geopolitical pulse summary. `/og leaderboard cpi 1q` returns the leaderboard. These are essentially MCP tools exposed via Discord slash interface — same code, different transport.

---

## Why Telegram second (but still essential)

Telegram is the macro-adjacent power-user channel *outside* the Anglosphere. In Brazil, India, Russia (yes, despite the politics), Turkey, much of MENA, and parts of Eastern Europe, Telegram is *the* messaging app for substantive content channels. Macro analysts in São Paulo and Istanbul are on Telegram, not Discord.

The Telegram bot is structurally simpler than Discord (no "servers" concept — channels are public-broadcast or private group; DMs are 1-to-1). The bot API is decent though less polished than Discord. The strategic role is *international coverage*.

The OPENGEM Telegram bot does at v1.1:

- **Personal DMs to subscribers** (same as Discord).
- **Public channel "OPENGEM Daily"** that broadcasts the daily digest items as Telegram channel posts. This is the Telegram equivalent of the Substack mirror (L112).
- **Inline mode**: `@OpengemBot USA CPI` typed into any Telegram chat returns a forecast snapshot the user can share into the chat. This is the Telegram-native version of an inline embed.

---

## Why not Slack at v1

Slack is the work-messaging tool, dominant in corporate America (and global startups). The Institutional tier (sovereign funds, NGOs, central banks) lives in Slack daily. The case *for* Slack is real but the case against at v1 wins:

- The bot-install flow on Slack is more cumbersome (workspace-admin approval, per-workspace OAuth flows).
- Slack's rate limits and API costs at scale are stricter than Discord's.
- The Institutional buyer who would benefit most is also the buyer most amenable to a custom-tier integration through the Vendor contract — they can ask, we deliver, this isn't a v1 mass-market feature.

**Defer Slack to Y1.5** when Institutional revenue motivates a custom Slack app. At that point we use Slack's official Bolt framework with a polished marketplace listing.

---

## The unified delivery contract

A single alert rule, configured once on the OPENGEM web app, can fan out to any subset of channels. The user's configured channels are stored as `users.delivery_channels`:

```json
{
  "delivery_channels": {
    "email": "user@example.com",
    "discord_dm": {"user_id": "...", "verified_at": "..."},
    "discord_channel": {"guild_id": "...", "channel_id": "...", "permission_at": "..."},
    "telegram_dm": {"chat_id": "...", "verified_at": "..."},
    "rss_feed_token": "..."
  }
}
```

When an alert fires (an Arq job named `dispatch_alert`):

1. Look up the rule's owning user.
2. For each configured channel, enqueue a channel-specific job:
   - `send_email_alert` → Resend.
   - `send_discord_dm_alert` → Discord REST API.
   - `send_discord_channel_alert` → Discord REST API.
   - `send_telegram_dm_alert` → Telegram Bot API.
   - `publish_to_rss_feed` → Redis sorted set + cache invalidation.
3. Each channel-specific job formats the alert for that channel's affordances (Discord embeds, Telegram markdown, plain-text email).

---

## The bot authentication flows

### Discord

1. User clicks "Connect Discord" on `/account/alerts`.
2. OPENGEM redirects to Discord OAuth: `https://discord.com/api/oauth2/authorize?client_id=...&response_type=code&scope=identify+bot+applications.commands&redirect_uri=...`.
3. User authorizes; Discord redirects back with code.
4. OPENGEM exchanges code → access token, fetches user's Discord ID, stores in `users.delivery_channels.discord_dm`.
5. For server-channel install: separate flow with `scope=bot` and admin selecting target guild + channel.

### Telegram

Telegram has no OAuth in the conventional sense. The pairing flow:

1. User clicks "Connect Telegram" on `/account/alerts`.
2. OPENGEM generates a short-lived random token (e.g., `og_link_abc123`), shows the user a deep-link: `https://t.me/OpengemBot?start=og_link_abc123`.
3. User taps the deep-link, opening Telegram, which starts a chat with OpengemBot using the `/start og_link_abc123` command.
4. The bot receives the `/start` with the token, looks up the token in the OPENGEM DB, ties `update.message.chat.id` to the user account.
5. Persisted in `users.delivery_channels.telegram_dm`.

Both flows take ~10 seconds end-to-end.

---

## Discord embed format

A forecast-revision alert in Discord:

```json
{
  "embeds": [{
    "title": "USA CPI YoY revised: 3.1% → 3.2%",
    "url": "https://opengem.org/c/USA/cpi_yoy?v=2026-06-06",
    "description": "OPENGEM nowcast moved from 3.1% (vintage 2026-06-05) to 3.2% (vintage 2026-06-06) following the BLS release.",
    "color": 16170565,
    "fields": [
      {"name": "Methodology", "value": "[CF Nowcast v3.1](https://opengem.org/methodology/cf-nowcast-v3)", "inline": true},
      {"name": "Vintage", "value": "2026-06-06", "inline": true},
      {"name": "Consensus", "value": "WEO: 3.4% (Apr-26)", "inline": true}
    ],
    "image": {"url": "https://opengem.org/embed/og?country=USA&indicator=cpi_yoy&size=banner"},
    "footer": {
      "text": "OPENGEM — open macro accountability ledger",
      "icon_url": "https://opengem.org/static/logo-square.png"
    },
    "timestamp": "2026-06-06T13:42:00Z"
  }]
}
```

The embed includes the OG image, the methodology link, the vintage, the consensus comparison — all of OPENGEM's brand-defining surfaces visible in one Discord card.

---

## Anti-spam rules

Rate limits per user per channel:

- Max 50 alerts/day per channel.
- Min 60 seconds between alerts on the same rule.
- A "digest mode" toggle: if more than 10 alerts in 1 hour, batch into a single message.

The `dispatch_alert` job enforces these before fanning out. Limits are user-configurable; admin gets a "global pause" toggle.

---

## Next-step: the Discord bot skeleton

```python
# bots/discord_bot.py
import discord
from discord.ext import commands
from .opengem_client import OpengemClient

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
client = OpengemClient(api_key=os.environ["OPENGEM_BOT_API_KEY"])

@bot.tree.command(name="og", description="Query OPENGEM")
async def og(interaction: discord.Interaction, action: str, country: str = None, indicator: str = None):
    if action == "forecast":
        data = await client.get_forecast(country=country, indicator=indicator)
        embed = build_forecast_embed(data)
        await interaction.response.send_message(embed=embed)
    elif action == "pulse":
        data = await client.get_gpr_nowcast()
        embed = build_pulse_embed(data)
        await interaction.response.send_message(embed=embed)
    elif action == "leaderboard":
        data = await client.get_leaderboard(indicator=country, horizon="1q")
        embed = build_leaderboard_embed(data)
        await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"OPENGEM bot online as {bot.user}")

# Triggered from Arq job
async def send_discord_dm_alert(user_discord_id: str, payload: dict):
    user = await bot.fetch_user(int(user_discord_id))
    await user.send(embed=build_alert_embed(payload))

bot.run(os.environ["DISCORD_BOT_TOKEN"])
```

---

## What this loop produced

- Pick both, Discord first, Telegram at v1.1, Slack deferred to Y1.5.
- A unified `delivery_channels` config and Arq-fanout dispatcher.
- Authentication flows for Discord OAuth and Telegram deep-link pairing.
- A Discord embed format showcasing OPENGEM brand surfaces.
- Anti-spam rules with digest-mode batching.
- A Discord bot skeleton.

## What comes next

- **L131** — alerts UX (Phase 3 design pairs with this delivery layer).
- **L102** — Arq notifications queue is the substrate.
- **L106** — per-user RSS feed is the universal fallback.

## Related

- [[L007-distribution-thesis]] — Discord is the closed-loop conversion funnel
- [[L102-arq-task-queue]] — notifications queue dispatches alerts
- [[L131-alerts-ux]] — UI configuration of alert rules
- [[L106-rss-atom-feed-catalog]] — per-user RSS feed = universal fallback
- [[L108-mcp-server-contract]] — slash commands reuse MCP tools
