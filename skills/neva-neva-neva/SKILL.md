---
name: neva-neva-neva
description: When the user corrects Claude or repeats an instruction, write that correction somewhere Claude cannot skip it (a check that fails, a step in the right skill, a rule file), in the same session, then say in one line where it went. Use whenever the user says "no, don't...", "I told you...", "again?", "how many times", "you keep...", "stop doing...", "always...", "never...", "from now on...", "why did you...", or when Claude notices it repeated a mistake the user already flagged.
---

# Neva Neva Neva

**The idea.** When you correct Claude, the correction usually lives in the chat. The chat ends, or
gets long, and the correction is gone. Saving it to memory helps a little, but memory is a note Claude
may or may not read. A correction is worth the most where it **cannot be skipped**: a check that
fails, then a step in the instructions that do the work, then a rule file that loads when the work is
touched. Memory is the last resort.

And the more times you have said it, the harder it should lock.

## Every time, in this order

1. **Say the rule back in one line,** in the user's words. "Got it: dates are always written
   Oct 8, 2026, never 10/8." If the correction is really a decision nobody has made yet (a price, a
   policy, a promise to a customer), don't write a rule. Ask the user.

2. **Check the ledger.** Open `.claude/neva-neva-neva.md` in the project (create it if missing; the
   format is at the bottom). Has this rule, or one like it, been written down before?
   - **Not there:** this is time one.
   - **There already:** the rule's current home failed. Add one to its count. It must move **up** at
     least one rung in step 3. Tell the user plainly: "You've told me this twice now. Moving it from a
     rule file to a check."

3. **Pick the strongest home that works.** Start at the top and take the first one that fits:

   | Home | Use it when | Where |
   |---|---|---|
   | **A guard** | It's about a command or an edit that should never happen | A hook script in `.claude/hooks/`, wired in `.claude/settings.json` |
   | **A check** | A script can tell right from wrong by reading a file or output | The project's tests, linter, or a small script in `.claude/checks/` that the tests run |
   | **A skill step** | It's part of making one kind of thing (a report, an email, a page) | That skill's `SKILL.md`, as a numbered step |
   | **A path rule** | It applies whenever certain files or folders are touched | `.claude/rules/<topic>.md` with a `paths:` list at the top |
   | **The project rules** | It applies to every session in this project | The project's `CLAUDE.md`, one line, kept short |
   | **Your personal rules** | It's your taste, in every project (tone, format, how you like answers) | `~/.claude/CLAUDE.md` |
   | **Memory** | Nothing above fits | Claude's memory |

   Third time, or more, and a machine could check it? It goes to a guard or a check. No exceptions.

   One rule, one home. A check plus a one-line pointer in a rule file is fine. Two full copies of the
   same rule are not; they drift apart.

4. **Write it there now,** in this session. Not "next time".
   - **Plain words, one line per rule,** with the date. The story of why goes in the ledger, not the rule.
   - **Path rules** load when Claude reads a matching file. A brand-new file written without reading
     anything near it won't pull the rule in, so put build-time rules in the skill that makes the thing too.
   - **Guards change how Claude runs for everyone on the project.** Write the script and its test, then
     show the user the exact `.claude/settings.json` entry and ask before adding it.
   - **Never put secrets, passwords or other people's private details in a rule.** Write the rule in
     general terms ("never paste customer emails into a commit") and leave the specifics out.

5. **Prove a check can fail.** Plant the mistake in a throwaway file and watch the check catch it.
   Then run it on the project's existing good work and make sure it raises **no new false alarms**.
   Keep the planted example as a test, so the next change proves it again.

6. **Pop quiz.** Prove the rule works without this chat. Start a fresh subagent that has never seen the
   conversation, and give it the task that went wrong (or a small version of it), word for word, with no
   hint about the rule. It works only from what's on disk. Then read what it did:
   - **Passed** (followed the rule): done.
   - **Failed:** the rule is in a home Claude doesn't load for that task, or it's worded too loosely. Move it
     up a rung or sharpen the wording, and quiz again. Two fails in a row: tell the user plainly.
   - Keep the quiz small and cheap: one task, no real side effects (it works in a scratch folder, sends
     nothing, deletes nothing). If subagents aren't available, skip it and say so.

7. **Tell the user in one line where it went.** "Now a check: any date written 10/8 fails the tests."
   Include the quiz result. Not a paragraph. If it needs their yes (a guard to wire up), ask in that same
   line.

8. **Update the ledger.**

## The ledger

`.claude/neva-neva-neva.md`, one row per rule. Commit it with the project so everyone working on it
shares the same history.

```markdown
# Neva Neva Neva

| Rule | Times | Home | Quiz | First said | Last said |
|---|---|---|---|---|---|
| Dates as "Oct 8, 2026", never "10/8" | 2 | check: tests/test_dates.py | passed | 2026-10-01 | 2026-10-08 |
| Ask before deleting any file | 1 | guard: .claude/hooks/no-delete.py | passed | 2026-10-03 | 2026-10-03 |
| Short answers, result first | 1 | ~/.claude/CLAUDE.md | passed | 2026-10-05 | 2026-10-05 |
```

When a rule moves up a rung, delete it from its old home so there is one copy.
