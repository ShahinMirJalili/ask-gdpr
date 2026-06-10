# STATUS — ask-gdpr (Stand: Mi 11.06.2026)

> Morgen weitermachen? Claude sagen: **"ask-gdpr weiterbauen"** — er liest diese Datei + Spec + Plan und legt los.

## Was ist das Projekt?
**ask-gdpr** = deine erste AI-Portfolio-App. Eine Web-App, der du auf Deutsch Fragen zur DSGVO stellst ("Muss ich eine Datenpanne melden?"). Die App sucht die passenden DSGVO-Artikel raus und Claude antwortet NUR aus diesen Artikeln, mit Quellenangabe. Das nennt man **RAG** (Retrieval-Augmented Generation) — die meistgefragte AI-Skill bei Arbeitgebern.

## Wo liegt was?
| Was | Wo |
|-----|-----|
| Projekt lokal | `~/projects/github-portfolio/ask-gdpr/` |
| Design-Spec (WAS wir bauen) | `docs/superpowers/specs/2026-06-11-ask-gdpr-design.md` |
| Bau-Plan (WIE, 10 Tasks) | `docs/superpowers/plans/2026-06-11-ask-gdpr-v1.md` |
| GitHub (kommt am Ende) | github.com/ShahinMirJalili/ask-gdpr (Task 10) |

## Was haben wir heute gemacht? ✅
1. Hype-Scan: was neu ist im Claude-Ökosystem (Fable 5, Billing-Split Mo 15.06!)
2. Recherche: was AI-Arbeitgeber 2026 im Portfolio sehen wollen → **Evals** (Qualitätsmessung) ist das #1-Signal, fehlt bei 90% der Bewerber
3. Projekt-Plan fürs Portfolio: 3 Apps nacheinander (siehe unten)
4. Design für App #1 entschieden + Spec geschrieben + von Review-Agent geprüft ✅
5. Bau-Plan mit 10 Tasks geschrieben + geprüft ✅
6. Git-Repo angelegt, 3 Commits, mit RICHTIGER Email (shahinmirjalili5@gmail.com)

## Die 3 Portfolio-Projekte (nacheinander, nicht parallel!)
1. **ask-gdpr** (JETZT) — RAG-App, Python + Flask = dein Masterschool-Stack
2. **Website-Audit-Agent** (danach) — AI-Agent der Websites prüft, Pydantic AI
3. **Eigener MCP-Server** (Term 2) — das Protokoll mit dem Claude Tools nutzt

## Nächster Schritt (morgen)
**Ausführung starten.** Empfehlung: Subagent-Driven (Claude-Agents bauen Task für Task, du reviewst).
**ABER 2 Tasks machst DU selbst** (steht so im Plan, damit du es im Interview erklären kannst):
- Task 3: Du schreibst `retrieval.py` (Article-Klasse + Such-Schleife — wie deine Product/Store-Klassen aus dem OOP-Kurs!). Claude hat die Tests schon vorbereitet, du programmierst bis sie grün sind.
- Task 6: Du prüfst die 30 Eval-Fragen und segnest sie ab.

## Wird das geil auf GitHub? JA — und zwar deshalb:
- ✅ Echtes RAG-Projekt mit Chat-UI (Screenshot/GIF im README)
- ✅ **Eval-Suite ab Tag 1** — das haben 90% der Bewerber NICHT
- ✅ README erklärt deine Entscheidungen (Arbeitgeber lieben das)
- ✅ Guardrails gegen Halluzination (Claude darf nur aus dem Gesetz antworten)
- ✅ Wächst mit deinem Kurs: v1 jetzt → v2 Embeddings → v3 Vektor-DB. Die Evolution im README zeigt: du LERNST und dokumentierst — stärker als eine fertige Copy-Paste-App
- ✅ Du kannst JEDE Zeile erklären, weil v1 auf deinem Level gebaut ist

## ⚠️ Offene Sachen (nicht vergessen)
- 🔴 **Mo 15.06: Billing-Split!** Hermes + Cron-Routinen vorher checken (eigenes Thema, nicht dieses Projekt)
- 🟡 Deine alten Showcase-Repos (trackx, naybo, falcontech) wurden mit falscher Email committed → zählen nicht im grünen Contribution-Graph. Fix: shahinmir605@gmail.com als Zweit-Email im GitHub-Account verlinken (Settings → Emails) = einfachste Lösung
- 🟡 GitHub-Token hat zu viele Rechte → bei Gelegenheit fine-grained Token erstellen
