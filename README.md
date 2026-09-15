# 📧 fastapi-resend

[![FastAPI](https://img.shields.io/badge/FastAPI-Supported-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Resend](https://img.shields.io/badge/Resend-Compatible-black.svg?style=flat&logo=Resend&logoColor=white)](https://resend.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()

> Lightweight, modern transactional email sender for FastAPI powered by Resend.

Send onboarding emails, password resets, and invoices in FastAPI with async speed and non-blocking background tasks.

---

### ☕ Support My Studies / Buy Me a Coffee

Hey there! 👋 I build and open-source lightweight, focused developer tools.

If this small package helped your project send emails cleanly, please consider supporting my college/tuition fund:
- ☕ **Buy Me a Coffee:** [buymeacoffee.com/yourname](https://www.buymeacoffee.com)
- 💖 **Ko-fi:** [buymeacoffee.com/kcidi4148](https://buymeacoffee.com/kcidi4148)
- ⭐ **Star this repository** to help other developers discover it!

---

## 📦 Installation

```bash
pip install git+https://github.com/me1121118/fastapi-resend.git
```

---

## 🚀 Quick Example

### 1. Direct Async Send

```python
from fastapi import FastAPI
from fastapi_resend import ResendMailer

app = FastAPI()
mailer = ResendMailer(api_key="re_your_resend_api_key", from_email="Acme <welcome@yourdomain.com>")

@app.post("/register")
async def register(user_email: str):
    await mailer.send(
        to=user_email,
        subject="Welcome to our platform!",
        html="<h1>Welcome!</h1><p>We are thrilled to have you on board.</p>"
    )
    return {"status": "email sent"}
```

### 2. Non-blocking Background Send (Zero Latency)

```python
from fastapi import FastAPI, BackgroundTasks
from fastapi_resend import ResendMailer

app = FastAPI()
mailer = ResendMailer(api_key="re_your_resend_api_key", from_email="Acme <welcome@yourdomain.com>")

@app.post("/register")
async def register(user_email: str, background_tasks: BackgroundTasks):
    # Responds immediately to client while sending email in background
    mailer.send_in_background(
        background_tasks,
        to=user_email,
        subject="Welcome!",
        html="<p>Your account is ready.</p>"
    )
    return {"message": "User registered successfully"}
```

---

## 🧪 Testing

```bash
pytest -v tests
```

---

## 📄 License

MIT License. Free for personal and commercial use.
