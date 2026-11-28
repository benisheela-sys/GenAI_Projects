# Slack Recipe Bot (n8n Workflow)

An automated [n8n](https://n8n.io/) workflow that listens to messages in a designated Slack channel and responds with a concise, practical ingredient list (with approximate quantities) and step-by-step cooking instructions powered by OpenAI's `gpt-4o-mini`.

---

## Features

- **Instant Recipe Generation:** Post the name of any dish in Slack to receive a bulleted ingredient list and cooking instructions.
- **Loop Prevention:** Automatically filters out bot messages and Slack message subtypes (e.g., edits, channel joins) to prevent infinite reply loops.
- **Ambiguity Handling:** Prompts the user to rephrase if the requested recipe name is unclear.
- **Cost-Efficient & Consistent:** Uses OpenAI's `gpt-4o-mini` model with a low temperature (`0.3`) for fast, practical, and reliable responses.

---

## Workflow Architecture

The workflow (`Slack-Recipe-Bot.json`) consists of five nodes connected in sequence:

```text
[Slack-Trigger] ──▶ [Ignore Bot Messages] ──▶ [Generate Ingredient List] ──▶ [Reply in Slack]
                                                         ▲
                                                         │
                                                [OpenAI Chat Model]
```

1. **Slack-Trigger (`slackTrigger`):** Listens for new `message` events in the configured Slack channel (default: `#recipe-bot`).
2. **Ignore Bot Messages (`filter`):** Ensures only standard human messages proceed by checking that both `bot_id` and `subtype` do not exist on the incoming payload.
3. **OpenAI Chat Model (`lmChatOpenAi`):** Provides the `gpt-4o-mini` language model (temperature `0.3`) to the LLM chain.
4. **Generate Ingredient List (`chainLlm`):** Formats the user's Slack message into a structured prompt asking for ingredients, approximate quantities, and short cooking instructions.
5. **Reply in Slack (`slack`):** Posts the AI-generated recipe back to the exact channel where the request originated (`$('Slack-Trigger').item.json.channel`).

---

## Prerequisites

Before importing and running this workflow, make sure you have:

1. **An n8n instance** (Cloud or self-hosted, with webhook accessibility for Slack events).
2. **An OpenAI API Key** with access to `gpt-4o-mini`.
3. **A Slack App** installed in your workspace with:
   - **Event Subscriptions** enabled (pointing to your n8n Slack Trigger webhook URL) and subscribed to `message.channels` (or `message.groups` for private channels).
   - **Bot Token Scopes:**
     - `channels:history` (and/or `groups:history` for private channels)
     - `channels:read`
     - `chat:write`
   - The Slack Bot invited to your target channel (e.g., `/invite @YourRecipeBot` in `#recipe-bot`).

---

## Setup & Installation

1. **Download the Workflow:**
   Ensure you have the `Slack-Recipe-Bot.json` file ready.

2. **Import into n8n:**
   - Open your n8n dashboard.
   - Click **Add workflow** (or open an existing empty workflow).
   - Click the top-right menu (`...`) and select **Import from File...**.
   - Select `Slack-Recipe-Bot.json`.

3. **Configure Credentials:**
   - **Slack:** Open both the **Slack-Trigger** and **Reply in Slack** nodes and attach your Slack API credentials.
   - **OpenAI:** Open the **OpenAI Chat Model** node and attach your OpenAI API credentials.

4. **Select Your Slack Channel:**
   - Open the **Slack-Trigger** node.
   - Update the **Channel** field to your desired Slack channel (currently configured as `#recipe-bot`).

5. **Activate the Workflow:**
   - Click **Save**, then toggle the workflow status switch to **Active**.

---

## Usage

Once active, simply type the name of a dish in your configured Slack channel:

**User:**
> Pasta Carbonara

**Bot:**
> **Ingredients:**
> - 400g spaghetti
> - 150g guanciale or pancetta, diced
> - 3 large egg yolks + 1 whole egg
> - 100g Pecorino Romano, finely grated
> - Freshly cracked black pepper
> - Salt (for pasta water)
>
> **How to Cook:**
> 1. Boil spaghetti in salted water until al dente; reserve 1 cup of pasta water.
> 2. Crisp the guanciale in a pan over medium heat, then remove from heat.
> 3. Whisk eggs, grated cheese, and plenty of black pepper in a bowl.
> 4. Toss hot pasta into the pan with the guanciale, add a splash of pasta water, and stir in the egg mixture off the heat until creamy. Serve immediately.

If the input is vague (e.g., *"something warm"*), the bot will ask you to rephrase your recipe request.

---

## Customization

- **Change the AI Model:** Open the **OpenAI Chat Model** node to switch models (e.g., to `gpt-4o`) or adjust the `temperature` (higher for more creative recipes, lower for more standard ones).
- **Modify the Output Format:** Edit the prompt inside the **Generate Ingredient List** node to include prep time, dietary substitutions, calorie estimates, or servings.
- **Reply in Threads:** In the **Reply in Slack** node, add `thread_ts` under **Other Options** using `={{ $('Slack-Trigger').item.json.ts }}` to keep your Slack channel tidy by replying directly in a thread.

---

## Troubleshooting

- **Bot doesn't respond:** Verify that the workflow is **Active**, the Slack App's Event Subscriptions URL matches the production webhook URL in the **Slack-Trigger** node, and the bot has been invited to the channel.
- **Bot replies to itself:** Ensure the **Ignore Bot Messages** filter node remains connected directly after the trigger and checks that `bot_id` does not exist.
- **Missing permissions error:** Confirm your Slack App has `chat:write` and `channels:history` scopes and was reinstalled to the workspace after adding those scopes.