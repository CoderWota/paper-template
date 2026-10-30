---
name: git-backup
description: Back up saved versions to an explicitly confirmed destination and verify the copy; never force-push.
---

# Git backup

Outcome: either a verified external copy at a destination the researcher confirmed, with what it contains and who can see it, or a clear account of what still exists only on this computer.

## Step 1: Explain the difference

1. Run `python scripts/versions.py inspect` and `python scripts/versions.py remotes`. Saving a version keeps it on this computer only. An external copy protects against losing the computer, and it also sends the tracked files, including any originals, data, and drafts in the history, to someone else's storage.

## Step 2: Establish the destination

2. Ask one question at a time, with a recommendation:
   - **Where:** a private repository on a hosting service the researcher already uses, an institutional server, or a folder on an external drive.
   - **Visibility and access:** private or public, and who may read it. Recommend private. Making research public is publication and needs its own explicit instruction.
   - **What leaves the computer:** everything the history tracks (`python scripts/versions.py scope`). Ask about material that should not leave, such as unpublished data, confidential documents, or copyright-restricted originals; keeping it out may need `git-setup` before the first backup.
   - **Accounts and costs:** creating an account, signing in, or paying is the researcher's own action. Never ask for a password or token in the conversation, and never create an account.
3. Never use an `origin` that points to the template's repository as a backup: `git-setup` renames it first.
4. After a clear yes, record the destination in `requirements/privacy.md` in the interaction language: the exact address, its visibility, what may be copied there, the date, and the researcher's words in quotation marks. The backup command refuses any destination that this file does not name.

## Step 3: Connect and copy

5. Add the destination as a remote with a clear name, for example `git remote add backup <address>`. For an empty repository that the researcher created on a hosting service, use the address that the service shows. Sign-in happens in the researcher's own tools (the hosting service's credential helper or a sign-in page); guide that step and wait.
6. Run `python scripts/versions.py backup --remote <name> [--branch main]`. It refuses an unconfirmed destination and history that contains files that look like secrets, never forces, and then checks that the remote holds the same latest version.
7. When the push fails because of sign-in or permissions, say so plainly: the backup is not done. Guide the sign-in and try again only after it.

## Step 4: Report

8. Report the destination, its visibility, the version it now holds, and whether the check passed. Mention what is still only local, such as unsaved changes or ignored files (credentials, environments, previews), and that later versions need another backup.

## Completion check

- The destination, its visibility, and the material that leaves the computer were confirmed by the researcher and recorded with their words.
- Nothing went to an unconfirmed destination or to the template's repository, and no force was used.
- The backup is reported as verified only when the remote holds the latest local version.
