import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "hooks" / "detect_correction.py"
sys.path.insert(0, str(HOOK.parent))
from detect_correction import is_correction  # noqa: E402

CORRECTIONS = [
    "I told you not to use em dashes",
    "i already told you this",
    "Like I said, the button goes on the left",
    "how many times do I have to say it",
    "you keep adding comments to every line",
    "Stop doing that",
    "from now on, write dates as Oct 8, 2026",
    "never use the word delve",
    "don't ever push to main",
    "wrong file again?",
    "why did you delete the tests",
    "remember to run the linter first",
    "that's not what I asked for",
]

ORDINARY = [
    "can you add a dark mode toggle",
    "try again with a smaller image",
    "write a function that never returns null",
    "what did the test output say",
    "I said hi to the team, now draft the update",
    "",
]


class DetectTest(unittest.TestCase):
    def test_corrections_are_caught(self):
        for text in CORRECTIONS:
            with self.subTest(text=text):
                self.assertTrue(is_correction(text))

    def test_ordinary_messages_pass(self):
        for text in ORDINARY:
            with self.subTest(text=text):
                self.assertFalse(is_correction(text))

    def run_hook(self, payload, env=None):
        return subprocess.run(
            [sys.executable, str(HOOK)],
            input=payload,
            capture_output=True,
            text=True,
            env={**os.environ, **(env or {})},
        )

    def test_hook_output_is_valid_context(self):
        out = self.run_hook(json.dumps({"hook_event_name": "UserPromptSubmit", "prompt": "I told you twice"}))
        self.assertEqual(out.returncode, 0)
        data = json.loads(out.stdout)
        self.assertEqual(data["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")
        self.assertIn("neva-neva-neva", data["hookSpecificOutput"]["additionalContext"])

    def test_hook_silent_on_ordinary_message(self):
        out = self.run_hook(json.dumps({"prompt": "add a footer"}))
        self.assertEqual((out.returncode, out.stdout), (0, ""))

    def test_hook_survives_bad_input(self):
        out = self.run_hook("not json")
        self.assertEqual((out.returncode, out.stdout), (0, ""))

    def test_hook_survives_odd_shapes(self):
        for payload in ("[]", "null", '{"prompt": 42}', '{"prompt": null}'):
            with self.subTest(payload=payload):
                out = self.run_hook(payload)
                self.assertEqual((out.returncode, out.stdout), (0, ""))

    def test_quiet_switch(self):
        out = self.run_hook(json.dumps({"prompt": "I told you"}), env={"NEVA_QUIET": "1"})
        self.assertEqual(out.stdout, "")


class PackageTest(unittest.TestCase):
    def test_hooks_json_points_at_real_script(self):
        hooks = json.loads((ROOT / "hooks" / "hooks.json").read_text())
        command = hooks["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/hooks/detect_correction.py", command)

    def test_skill_has_frontmatter(self):
        text = (ROOT / "skills" / "neva-neva-neva" / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\nname: neva-neva-neva\ndescription: "))

    def test_plugin_manifests_parse(self):
        for name in ("plugin.json", "marketplace.json"):
            json.loads((ROOT / ".claude-plugin" / name).read_text())


if __name__ == "__main__":
    unittest.main()
