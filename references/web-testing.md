# Web testing

Test websites and web apps the user owns. Local first; remote only with clear authorization.

## Stack detection

- Static HTML, SPA (React/Vue/Next), SSR server, API-only
- Read `package.json` scripts, `playwright.config.*`, `cypress.config.*`, `pytest`, etc.

## Automated (if present)

```bash
npm test
npm run lint
npx playwright test
npx cypress run
# Python
pytest
```

## API smoke (local)

```bash
# start dev server per project docs, then:
curl -sS -o /dev/null -w "%{http_code}\n" http://localhost:3000/
curl -sS http://localhost:3000/api/health
```

Check: status codes, JSON shape, auth 401/403 paths, no stack traces in production responses.

## Manual smoke checklist

- [ ] Home loads; no console errors
- [ ] Primary nav works
- [ ] Form validation (empty, invalid, valid)
- [ ] Login / signup (test account only)
- [ ] Mobile viewport (~375px) no horizontal scroll
- [ ] Keyboard tab order on main CTAs
- [ ] 404 page for bad URL
- [ ] Slow network / offline message if supported

## Performance (optional)

- Lighthouse if Chrome available
- Time to first byte on local server
- Bundle size vs previous build

## Security smoke (authorized only)

- HTTPS redirects in prod config
- Security headers if user asks (CSP, HSTS) — document, don’t claim production applied
- No secrets in client bundle (`grep` for `API_KEY` patterns in build output)

## Report

```text
Mode: web-test
Completed: <urls/pages/APIs checked>
Verified: <commands + pass/fail>
Limitations: <no browser, no auth creds, remote not tested>
Remaining: <full E2E, load test, a11y audit>
```
