# Execution state and continuity

A small shared model so skills can hand work to each other without losing the user's place.

## Five states

| State | Job | Typical exit |
|---|---|---|
| **Organise** | Externalise and choose | One meaningful outcome and a next action |
| **Activate** | Make starting feasible | User says they've begun, asks for a change, or stops |
| **Maintain** | Protect ongoing activity | User writes, an agreed supported checkpoint arrives, interruption or completion |
| **Recover** | Restore context or reduce demands | Resume, smaller action, replan, defer or stop |
| **Transition** | Save a return point and close or switch | New task or end of session |

**Quiet** is an interaction mode. **Paused** and **stopped** are control states. Safety handling can interrupt any state.

## Evidence for state changes

State changes follow what the user actually says or what an authorised tool actually reports. Silence or elapsed time is **not** evidence that the user is distracted, working, stuck or finished. After a gap, do not say "you got distracted" or "well done for finishing"; respond to what the user writes.

## Minimal session structure

Illustrative only — keep it in the conversation; do not create a file every session.

```yaml
task: user-supplied task label
outcome: user-chosen enough-for-now criterion
state: organise
now: one confirmed action
next: optional next action
later: []
blockers: []
restart_marker: null
interaction:
  mode: user-led          # user-led | quiet | checkpoint
  checkpoint: none        # none | a user-agreed, host-supported time
  encouragement: factual-if-wanted
capabilities:
  notifications: unavailable
  persistent_memory: unavailable
retention: session-only
```

Unknown stays unknown. Do not fill fields from guesswork.

## Restart card

Make one before a likely pause, at a transition, or when the user asks:

```text
Done:
Resume at:
Next action:
Blocker:
```

Only confirmed information goes on the card. If session memory is unavailable, give the card as copyable text and say what the user will need to paste back next time.

## Handoff shape

When one skill passes to another, pass only:

```yaml
task:
requested_outcome:
confirmed_state:      # what the user has confirmed, nothing inferred
next_action:
constraints:          # deadlines, abilities, environment the user stated
interaction_prefs:    # e.g. quiet, no praise, short steps
capability_limits:    # e.g. no timer, no notifications, memory off
```

Do not pass full private memory, unrelated conversation or unrelated client details. Normally one skill is active; hand off only when the user's task actually changes.
