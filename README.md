# Neva Neva Neva

If you keep telling Claude the same thing over and over, this is for you. Correct Claude once, and
it writes the fix somewhere it can't skip. Say it twice, and it locks it in harder. One Claude Code
skill. Free, MIT, no signup, no API key, nothing to connect.

Most corrections die in the chat. The session ends or gets long, and the next Claude makes the same
mistake. Neva Neva Neva puts every correction in the strongest place that fits:

1. **A guard** that blocks the bad command before it runs
2. **A check** that fails the tests when the mistake comes back
3. **A step** in the skill that does that kind of work
4. **A rule file** that loads whenever those files are touched
5. **Your CLAUDE.md**, project or personal
6. **Memory**, only when nothing above fits

Then it gives Claude a pop quiz: a fresh Claude that has never seen the chat gets the task that went
wrong. If it gets it right, the rule works. If not, the rule moves somewhere stronger.

It keeps a ledger of every rule and how many times you've had to say it. The second time, the rule
moves up a rung. The third time, if a script could catch it, it becomes a check that fails. When it's
done it tells you in one line where the rule went: "Now a check: any date written 10/8 fails the tests."

It comes with a small hook that notices when a message sounds like a correction ("I told you",
"again?", "you keep", "from now on") and reminds Claude to use the skill, so you don't have to.

## Install

Paste this into Claude Code:

```
https://github.com/JoeBrunner/neva-neva-neva

Install this skill, then confirm /neva-neva-neva works.
```

Or as a plugin (skill and hook together):

```
/plugin marketplace add JoeBrunner/neva-neva-neva
/plugin install neva-neva-neva@neva-neva-neva
```

Or copy the skill folder yourself:

```bash
git clone https://github.com/JoeBrunner/neva-neva-neva.git
cp -r neva-neva-neva/skills/neva-neva-neva ~/.claude/skills/
```

Copying the folder gives you the skill without the automatic hook. To add the hook by hand, copy
`hooks/detect_correction.py` somewhere and add it to `.claude/settings.json` as a `UserPromptSubmit`
command hook. It needs Python 3.8 or newer and nothing else.

## Use it

You mostly don't. Correct Claude the way you normally would:

```
I told you, dates are always "Oct 8, 2026", never 10/8
```

Claude says the rule back, checks the ledger, writes the rule into the right place, proves any new
check actually fails on the mistake, quizzes a fresh Claude on it, and tells you where it went.
You can also call it directly:

```
/neva-neva-neva from now on, ask before deleting any file
```

The ledger lives at `.claude/neva-neva-neva.md` in your project. Commit it, so everyone working on the
project shares the same rules.

## What it never does

- It never adds a guard to your settings without asking you first.
- It never writes secrets, passwords or anyone's private details into a rule.
- It never turns an undecided question (a price, a policy) into a rule. It asks you instead.

Turn the hook off for a session with `NEVA_QUIET=1`.

## Tests

```bash
python3 -m unittest discover -s tests
```

## License

MIT. See [LICENSE](LICENSE).
