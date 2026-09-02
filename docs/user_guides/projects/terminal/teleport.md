---
description: Move a Claude Code session between your laptop and a Hopsworks terminal pod with the hops session CLI
---

# Teleport Claude Code Sessions

Every Hopsworks project has a web terminal that runs Claude Code in a per-user pod.
The `hops session` command moves a Claude Code session between your laptop and that pod, so you can start work locally and continue it in the cluster, or the other way round.

A session is handed off, not copied.
By default `hops session push` moves the one canonical copy of the session to the pod and leaves a marker (a "baton") recording that the pod now holds it.
`hops session pull` brings that copy back.
This keeps a single source of truth for the transcript, so the two sides never diverge silently.
Use `--fork` when you deliberately want a second, independent copy.

Transcripts are staged in your own private area of the project's HopsFS (`Users/<username>/teleport/`, readable only by you), not in a project-wide location.
A session transcript can contain code and file contents, so it is never exposed to other project members.

## Prerequisites

- The `hopsworks` Python package on your laptop.
  Install it with `pip install hopsworks`.
- An API key with the `TERMINAL` scope for the target cluster.
  Run `hops setup --host https://<your-cluster>` once to create one and store it locally.
  A key created through `hops setup` already carries the `TERMINAL` scope, so it can start a terminal.
- A running Claude Code session on your laptop for `push`, or a staged session in the project for `pull`.

## Commands

| Command | What it does |
| --- | --- |
| `hops session push` | Hand the current session up to a terminal pod and open it in the browser. |
| `hops session pull` | Bring a session back down to your laptop. |
| `hops session new` | Start a fresh session directly on a terminal pod. |
| `hops session list` | Show your staged sessions and where each one currently lives. |
| `hops session mirror` | Stream the live pod terminal on your laptop, read-only by default. |
| `hops session stop` | Stop this project's terminal pod and every tab in it. |

### Push a session to the cluster

Run this from the directory where your Claude Code session lives:

```bash
hops session push
```

The command uploads the transcript, starts the project's terminal pod if it is not already running, and opens the terminal in your browser.
The session lands on the pod as its own tab and resumes there.

Useful options:

- `--fork` copies the session instead of handing it off, so your local copy stays canonical.
- `--model <model>` resumes the session on the pod with a specific model.
- `--prompt "<text>"` feeds the resumed session a first instruction.
- `--no-open` prints the terminal URL instead of opening a browser.

### Pull a session back to your laptop

```bash
hops session pull
```

Run from the same directory you pushed from to reclaim that directory's session.
To reclaim a session staged from a different directory, pass its id: `hops session pull <session-id>`.

`pull` refuses to take a session while the pod still holds a live terminal, so you do not accidentally split it in two.
Stop the pod first, or pass `--force` to take the baton anyway.
If both sides changed, `pull` stops and asks you to pick with `--ours` or `--theirs`; the copy you do not keep is parked to a sidecar file rather than lost.

### Start a fresh session on the cluster

```bash
hops session new
```

This starts a new Claude Code session directly on a terminal pod, with no local transcript.
`--model` and `--prompt` work the same as for `push`.

### See where your sessions live

```bash
hops session list
```

Add `--all` to list every session you have staged across all directories.
The store is per-user and private, so you only ever see your own sessions.

### Watch a running session from your laptop

```bash
hops session mirror
```

This attaches to the live pod terminal over its WebSocket and streams it on your laptop.
It is read-only by default; pass `--write` to type into it.
Press `Ctrl-]` to detach.

### Stop the terminal pod

```bash
hops session stop
```

This stops the project's terminal pod and every tab in it, from your laptop, without needing Kubernetes access.

## Optional: sync your Git checkout to the pod

When you push a session, `hops session` can also reproduce your local Git checkout on the pod, so the landed session starts in the same repository, on the same branch, at the commit you pushed.

This is opt-in.
The first time it applies, the CLI asks whether to sync (this time, always, not now, or never) and remembers your answer.
It then asks how the pod should authenticate to your Git host, and remembers that too:

| Choice | What happens |
| --- | --- |
| An existing SSH private key | You confirm the key path (the key `ssh` would use is suggested). The key is uploaded once into your private `Users/<username>/.ssh/` area and the pod clones over SSH. |
| A new SSH key created for Hopsworks | The CLI runs `ssh-keygen` to create a passphrase-free `ed25519` key at `~/.ssh/hopsworks_teleport_ed25519`, adds its public key to your GitHub account with `gh ssh-key add` when the GitHub CLI is logged in (otherwise it prints the public key for you to add), and stages it like an existing key. Offered on Linux, macOS and WSL; on Windows without `ssh-keygen`, point to an existing key instead. |
| A personal access token | The token is registered with Hopsworks (see below) and the pod clones over HTTPS with it, so no key leaves your machine. This is the only option when your remote already uses HTTPS; an SSH remote is rewritten to its HTTPS form for the pod. |

Commit and push your local work first, since the pod fetches from the remote, not from your laptop.
The CLI offers to stage tracked files and commit and push if the tree is dirty.

!!! note "Passphrase-protected keys"
    The pod runs no SSH agent, so a key that needs a passphrase is not supported.
    Use a passphrase-free key or a personal access token.

### Register a Git provider token

Hopsworks keeps one personal access token per Git provider host in your account, used by jobs and the web terminal for HTTPS git operations.
The teleport flow registers one for you when you choose the token option; you can also manage it directly:

```bash
hops git provider list
hops git provider set --provider github --username <you>
hops git provider delete --provider github
```

`set` prompts for the token without echoing it, defaults the host to the provider's public host (`github.com`, `gitlab.com`, `bitbucket.org`), and leaves an existing registration alone unless you pass `--force`.
The same token can be registered in the UI under **Account settings > Git providers**.

## How teleport keeps a session private

- Transcripts are staged in your own HopsFS home under `Users/<username>/teleport/`, created mode `0700`, so only you can read them.
- Attaching to a terminal from the CLI uses a short-lived, one-time token that is bound to the specific terminal session it was minted for.
  It cannot be reused and cannot be presented against another session.
- Staged transcripts are removed by a background cleaner after a retention period, so old sessions do not accumulate in your home.
  The default is 7 days; an administrator sets it with the `teleport_ttl_days` cluster variable.
