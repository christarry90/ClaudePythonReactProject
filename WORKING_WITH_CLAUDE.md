# Working With Claude — A Companion Guide

This isn't part of the Python/React curriculum itself — it's a running side-guide to working
with Claude and Claude Code well, since that's a skill worth building alongside the syntax
fluency this whole project is about. The tutor will point you here at natural moments; you can
also just read it whenever.

## Context management

Long conversations get compacted or summarized automatically once they grow large — you might
notice Claude referring back to something with slightly less precision after a very long
session. That's normal, not a sign you did something wrong. Two habits that help:

- Start a **fresh session** (`/clear`) when you're switching to a genuinely new task, rather than
  continuing a long thread that's drifted far from where it started.
- If a session has been running a long time and responses start feeling less sharp, that's often
  a good moment to wrap up, let the tutor update `PROGRESS.md`, and resume fresh next time.

## Effective prompting

Vague asks get vague answers. Compare:

- "Fix this" vs. "This raises a `KeyError` on line 12 when the dict is empty — walk me through
  why, then let me try the fix."
- "Make a component" vs. "I want a `TaskList` component that takes an array of tasks as a prop
  and renders each one — let me write it and you check my work."

The second version in each pair gives Claude (and you) something concrete to reason about. Being
specific isn't about writing more — it's about including the one detail that actually matters
(the error, the shape of the data, what "done" looks like).

## Debugging with Claude

Before asking for help, try to say: what did you expect to happen, what actually happened, and
the exact error message (not a paraphrase). This is the same habit as writing a good bug report
for a teammate — and it's usually the thing that makes the actual fix obvious, sometimes before
Claude even answers.

## Code review as a habit

Beyond what the tutor already reviews during lessons, get in the habit of asking Claude to review
code you've written — even code that already works. "Does this look idiomatic?" or "Is there a
simpler way to write this?" is a great transferable habit for any future project, not just this
one.

## Plan mode

For anything with more than one moving part (which, once you hit M2, most things will be),
Claude Code can switch into a planning mode: it proposes an approach before touching any files,
you review and adjust it, and only then does it start implementing. If you've ever written a
short design doc before starting a Java feature at work, this will feel familiar — it's the same
instinct, just built into the tool.

## Permission modes

You've probably noticed you're rarely asked to approve routine actions here — editing a file,
running a test. That's **auto mode**: it skips confirmation for safe, routine operations, but
still stops and asks (you'll have seen this as a multiple-choice question) when something is
genuinely ambiguous or hard to reverse. Think of it like a trusted teammate who doesn't ask
permission to run `git status`, but does check before `git push --force`. It's a default for this
environment, not a fixed setting — you can ask Claude to switch to a stricter mode for a
particular task if you want to review every step yourself.
