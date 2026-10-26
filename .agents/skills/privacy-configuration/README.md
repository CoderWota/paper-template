# Privacy Configuration

Helps you decide, and check, whether your AI application, your account, and your document-processing service may use your project content to train AI models. The agent finds the actual controls for your setup in the providers' current official documentation, explains them in plain words, helps you change them if you want, and reports what was really checked.

Ask, for example: "Check whether my AI application can use my manuscript to train its models, and help me turn that off."

## What to expect

- Account settings change only with your explicit consent, because they can affect all your projects on that account.
- For each control, the report says whether it was observed, confirmed by you, assumed from the provider's default, or is still unknown. The report is saved only on this computer, in `.local/privacy-report.md`.
- A training opt-out has limits: data already used can stay in trained models, and flagged conversations or submitted feedback can still be used. The report lists what remains.
- The agent never asks for passwords or account identifiers and never uploads research material as a test.

The agent instructions are in [SKILL.md](SKILL.md). Dated official sources are in [sources.md](sources.md), and the report layout is in [report-template.md](report-template.md). Related skills: `project-onboarding` and `environment-management`.
