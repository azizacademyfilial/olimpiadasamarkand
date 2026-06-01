# Samarqand loyihasini Netlify + Railway'ga deploy qilish

Bu loyiha deploy uchun tayyorlangan:

- `frontend/` → Netlify
- `backend/` → Railway
- API URL → `VITE_API_BASE_URL` orqali boshqariladi
- CORS/CSRF → Railway Variables orqali boshqariladi
- Railway start → `start_railway.sh`, `railway.json`, `nixpacks.toml`
- Netlify SPA router → `netlify.toml` va `public/_redirects`

---

## 1. GitHub'ga chiqarish

Loyiha papkasida:

```powershell
git init
git add .
git commit -m "prepare netlify railway deploy"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Agar repo oldin bor bo'lsa, faqat:

```powershell
git add .
git commit -m "prepare netlify railway deploy"
git push
```

---

## 2. Backend'ni Railway'ga qo'yish

Railway → New Project → Deploy from GitHub repo.

### Tavsiya qilinadigan sozlama

Railway xizmatida **Root Directory** ni shunday qiling:

```text
backend
```

Agar Root Directory bermasangiz ham rootdagi `railway.json` ishlaydi, lekin `backend` tanlash tozaroq.

### Railway Variables

Railway → backend service → Variables:

```text
SECRET_KEY=uzun-va-maxfiy-random-key
DEBUG=False
ALLOWED_HOSTS=.railway.app,.up.railway.app
CORS_ALLOW_NETLIFY=True
CORS_ALLOWED_ORIGINS=https://YOUR-NETLIFY-SITE.netlify.app
CSRF_TRUSTED_ORIGINS=https://YOUR-NETLIFY-SITE.netlify.app
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

Railway'da PostgreSQL qo'shsangiz, `DATABASE_URL` avtomatik ulanadi. PostgreSQL qo'shish tavsiya qilinadi.

Backend deploy bo'lgandan keyin tekshiring:

```text
https://YOUR-RAILWAY-BACKEND.up.railway.app/api/health/
```

`backend ishlayapti` chiqsa backend tayyor.

---

## 3. Frontend'ni Netlify'ga qo'yish

Netlify → Add new site → Import from GitHub.

Agar root repo tanlansa, rootdagi `netlify.toml` avtomatik ishlaydi:

```text
Base directory: frontend
Build command: npm run build
Publish directory: dist
```

Agar qo'lda sozlasangiz ham shu qiymatlarni kiriting.

### Netlify Environment variable

Netlify → Site configuration → Environment variables:

```text
VITE_API_BASE_URL=https://YOUR-RAILWAY-BACKEND.up.railway.app/api
```

E'tibor bering: oxirida `/api` bo'lishi shart.

Keyin Netlify'da **Clear cache and deploy site** qiling.

---

## 4. CORS xatosi chiqsa

Agar browser console'da shunday xato chiqsa:

```text
No 'Access-Control-Allow-Origin' header
```

Railway Variables ichida Netlify domeningiz aniq yozilganini tekshiring:

```text
CORS_ALLOWED_ORIGINS=https://YOUR-NETLIFY-SITE.netlify.app
CSRF_TRUSTED_ORIGINS=https://YOUR-NETLIFY-SITE.netlify.app
```

Keyin Railway backend'ni redeploy qiling.

---

## 5. Login

```text
Login: ulugbek
Parol: codingwithulugbek20030313
```

---

## 6. Local ishlatish

Backend:

```powershell
cd backend
.\start_windows.bat
```

Frontend:

```powershell
cd frontend
.\start_windows.bat
```
