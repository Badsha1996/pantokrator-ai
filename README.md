# Project Pantokrator 

**A local-first, hybrid, Reasrch based AI assistant for one 16 GB Apple Silicon Mac.**

## 0. What we are building

A terminal-first (later voice-first) assistant that lives on your Mac, operates your system and browser through a safe permission layer, reads your messages/mail/calendar, remembers you across sessions, has a consistent personality, and improves over time mostly through **memory**, and only much later through careful, cloud-based, evaluated fine-tuning. the intelligence isn't a giant model, it's **integrations + memory + proactivity**.


## 1. Permanent principles (these never bend, in any phase)

1. **Tools, not raw shell.** The model never gets arbitrary shell access. It calls typed functions you wrote. Every capability is a named tool with a schema.

2. **The permission fence.** Every tool has a risk tier: **auto** (safe, reversible, read-only), **confirm** (shows the exact action, waits for y/n), **blocked** (never automated). Enforced in code, not by prompt.

3. **Reversibility over deletion.** Nothing destructive is ever truly destructive on an automated path. "Delete email" means *move to Trash / label*, never permanent-delete. Anything irreversible is confirm-tier at minimum.

4. **Full audit log.** Every action, every routing decision, every rule firing is appended to a log with a timestamp and reason. This is how you debug and how you sleep.

5. **The privacy wall (hybrid).** You define what never leaves the machine. The router *physically cannot* send that data to the cloud. Enforced in code, with a test that fails if private data can reach a cloud endpoint.

6. **Small models misfire — leash accordingly.** A 7-8B local model will occasionally call the wrong tool or wrong argument. Principles 2–4 are therefore load-bearing, not optional hygiene.

7. **Propose, don't self-ship.** When pantokrator modifies its own code or swaps its own model, it *proposes* (a pull request, a suggestion) — evals judge, and a human approves. It can never rewrite its own safety rails or evals.

8. **Memory first, fine-tuning last.** "It learns about me" is a memory/retrieval problem. Fine-tuning is a late, cloud-only, style-only, eval-gated specialist tool — possibly never needed.

If a feature ever requires breaking one of these, the feature is wrong, not the principle.


# Contribution Guidelines

## Rules for Contributing

* Do not submit AI-generated code that you do not fully understand.
* AI tools can be used for assistance, but every function and implementation should be reviewed, understood, and owned by you.
* Avoid unnecessary abstractions, boilerplate, and "AI slop."
* Do not add comments that explain obvious code. Write code that is clear enough to be understood without excessive comments.
* Keep pull requests focused and small. A single PR must not exceed **500 lines of changes**.
* Update the relevant **App README** whenever your changes introduce new functionality, setup steps, configuration, APIs, or workflows.

## What Is Good Code?

Good code is code that:

* Is easy to read and understand.
* Allows developers to add new features without needing to understand the entire codebase.
* Favors simplicity over cleverness.
* Has clear naming and predictable behavior.
* Reduces cognitive overhead for future contributors.

> Simplicity beats complexity.

## License

This project is **source-available** under the
[PolyForm Noncommercial License 1.0.0](./LICENSE.md).

**In plain terms:**

| You want to... | Allowed? |
| --- | --- |
| Use it for a personal or hobby project | ✅ Yes |
| Study, modify, and learn from the code | ✅ Yes |
| Share it or your changes (noncommercially) | ✅ Yes |
| Use it as a student, nonprofit, school, or government body | ✅ Yes |
| Use it in a for-profit company or product | ❌ No |
| Sell it, or build a commercial service on it | ❌ No |

This is **not** an OSI-approved "open source" license, because it restricts
commercial use. It is a *source-available, noncommercial* license.

**Want to use this commercially?** A separate commercial license is available.
Contact at **https://www.linkedin.com/in/badsha-laskar/**.

> This summary is for convenience only. The [LICENSE.md](./LICENSE.md) file is
> the binding legal text.
