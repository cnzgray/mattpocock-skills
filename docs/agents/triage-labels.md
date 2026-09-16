# Triage Labels

Triage here works in terms of canonical roles. This file maps those roles to the actual label strings used in this repo's issue tracker. It covers both kinds of role: the five state roles an issue moves through, and the two category roles (`bug`, `enhancement`) every triaged issue carries exactly one of.

| Canonical label            | Label in our tracker | Meaning                                  |
| -------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`               | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`          | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`          | `ready-for-human`    | Requires human implementation            |
| `wontfix`                  | `wontfix`            | Will not be actioned                     |

| Canonical label            | Label in our tracker | Meaning                                               |
| -------------------------- | -------------------- | ----------------------------------------------------- |
| `bug`                      | `bug`                | Categories every triaged issue carries exactly one of |
| `enhancement`              | `enhancement`        | Categories every triaged issue carries exactly one of |

When a role is referred to (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

Edit the right-hand column to match whatever vocabulary you actually use.
