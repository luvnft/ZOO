# Mini 🧍

Minis are the first open-source digital humans. 🧍🧍‍♀🧍‍♂️

Join us in building agents that are highly realistic, configurable, and versatile — from boyfriend to personal secretary.

Make your own `Twilio SMS` Mini powered by `Gemini LLM` with `Bing Search` & `Stripe Payment` in minutes, not weeks

## ⭐ Features

### Web Access
- [x] Google Calendar
- [x] Google Drive
- [ ] Search

### Behaviors
- [x] Intent detection
- [x] Auto DB
- [ ] Task cancellation
- [ ] Human-like memory
- [ ] Preferences
- [ ] Proactive messages
- [ ] Scheduling
- [ ] Vision

### Channels
- [x] Bird SMS
- [x] Telegram
- [ ] WhatsApp
- [ ] Twilio
- [ ] Phone calls

### LLMs
- [x] Gemini
- [x] Groq
- [x] OpenAI
- [x] Anthropic

## 🛣️ Roadmap

- [ ] Make a master config file
- [ ] Working boyfriend agent demo
- [ ] Documentation/configuration guide


## 🛠️ Environment Setup
Make sure Python and [ngrok](https://ngrok.com/) are installed.

1. Navigate to the repository. Install [uv](https://github.com/astral-sh/uv):
   ```bash
   pip install uv
   ```
2. Create and activate a virtual environment:
   ```bash
   uv venv  # Create a virtual environment at .venv

   # Activate environment. On macOS and Linux:
   source .venv/bin/activate 
   
    # On Windows:
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```
4. Copy `local.template.yaml` to a new file called `local.yaml` in the same directory

## 🚀 Usage
Run the project:
```bash
python run.py
```

Interact with the demo:
- Add +1 (833) 819-1677 to contacts, or
- Add @AIHealthCoachBot on Telegram

## Dependencies
Add new dependencies:
```bash
uv pip install [package_name]
uv pip freeze > requirements.txt
```

## Contributing
(WIP)

## License

[MIT License](LICENSE.md).

