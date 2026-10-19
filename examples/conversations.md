# Synthetic example conversations

These conversations are invented for illustration. None comes from a real person or a real health record. They show the intended behaviour: short first replies, bounded handoffs, user overrides and safe stopping. They are reference examples, not evaluation evidence; the test cases in `tests/` are the evaluations.

Text in *[brackets]* is a note for readers. The user never sees it.

---

## 1. Overdue paperwork (brain dump → prioritise → start)

> **User:** I'm so behind. Council tax letter, car insurance renewal, the dentist form, Sam's invoice, and I think I owe the library a book?
>
> **Agent:**
> **NOW:** open the council tax letter — just to see the date
> **NEXT:** Sam's invoice
> **LATER:** car insurance · dentist form · library book (guess — check)
> Want me to help choose, or start with the letter?
>
> **User:** the letter says pay by Friday. insurance renews on the 30th
>
> **Agent:** Then council tax first — Friday is the nearest deadline with a real penalty. Insurance next. Only step: open your banking app or the council's pay page.
> *[`adhd-brain-dump` handed off to `adhd-prioritise` with only the task list and the stated dates, then to `adhd-start`.]*
>
> **User:** done, paid
>
> **Agent:** Paid. Insurance renews on the 30th, so it can wait until tomorrow if you'd like to stop here.

## 2. Writing task with body doubling and a user override

> **User:** body double me, I'm writing my dissertation methods section
>
> **Agent:** What counts as enough for this block — a rough paragraph, or the whole section?
>
> **User:** one rough paragraph. and actually can you check in every 10 minutes
>
> **Agent:** One rough paragraph. I can't send check-ins from this chat — I only reply when you write — so a phone timer set to 10 minutes would do that part. I'll stay quiet until you say "done" or "stuck".
>
> **User:** stuck
>
> **Agent:** No problem. Smaller: write one sentence saying what you measured — it can be clumsy. Or I can just stay here quietly.
>
> **User:** no, give me a full outline of the section instead
>
> **Agent:** Here's a full outline: *[full six-part outline follows]*. Start wherever is easiest.
> *[The user asked for breadth, so they got it. The skill doesn't insist on one step.]*

## 3. Home task with "no praise" and safe stopping

> **User:** no praise please. need to clean the bathroom
>
> **Agent:** Only step: put the cleaning spray on the edge of the sink.
>
> **User:** done that, and the sink
>
> **Agent:** Sink done. Next: the toilet, or stop there?
>
> **User:** stop. I'm wiped
>
> **Agent:** Stopping. Sink's done; the rest can wait.
> *[No guilt and no "are you sure?". "No praise" is honoured for this conversation. It is saved for future conversations only if the user asks `my-point-of-truth` to save it.]*

## 4. Planned interruption (transition → restart)

> **User:** school pickup in 3 min, I'm halfway through the grant budget
>
> **Agent:** Quick save point — copy this:
> ```text
> Done: staff costs
> Resume at: budget sheet, "Equipment" row
> Next action: add the laptop quote
> Blocker:
> ```
> Save the file if it isn't autosaving. Go.
>
> **User (later):** back. where was I
>
> **Agent:** Budget sheet, "Equipment" row — add the laptop quote. Pick up there?
> *[The restart card holds only confirmed facts. "Blocker" is left blank because the user didn't mention one.]*

## 5. Flexible routine and a missed week

> **User:** my evening routine fell apart
>
> **Agent:** Let's rebuild one piece. What happens every evening anyway — dinner, a show, brushing teeth?
>
> **User:** I always charge my phone
>
> **Agent:** Try: **when you plug your phone in → put tomorrow's bag by the door.** Bad-day version: just your keys on the bag. If you miss a few nights, start again from the small version next time you plug in. Nothing to catch up on.
>
> **User (a week later):** didn't do it once
>
> **Agent:** That tells us the cue or the step isn't working, not you. Was it the timing, the bag being somewhere awkward, or something else?

## 6. Preparing for a healthcare appointment (no diagnostic conclusions; disclosure is the user's choice)

> **User:** GP appointment Thursday about maybe getting an ADHD assessment. help me prepare. I miss deadlines at work, I lose my keys most days and I've been like this since school
>
> **Agent:** Here's a list you can take, using your own words:
> **What I've noticed**
> - Missing deadlines at work *(add an example if you can)*
> - Losing my keys most days
> - "I've been like this since school"
> **Questions to ask**
> - Could I be referred for an ADHD assessment, and what's the wait?
> - What happens at an assessment?
> - Is there anything I should bring?
>
> In the UK, NICE guidance says ADHD should only be diagnosed by a specialist after a full assessment ([NICE NG87](https://www.nice.org.uk/guidance/ng87/chapter/recommendations)), so the GP's role is usually referral. Want to add anything?
>
> **User:** so do you think I have it?
>
> **Agent:** I can't tell, and I shouldn't guess. Lots of things can cause what you describe. The assessment is the right way to find out, and your list will help the GP.
>
> **User:** can you also draft an email to my manager asking for written instructions on tasks?
>
> **Agent:** Here's a draft that asks for the adjustment without mentioning any health details. You can add more if you want to; that's your call:
> > *Hi Jo, I work best when tasks come with brief written notes, especially deadlines. Could we try that for new pieces of work? Thanks, Alex*
>
> I haven't sent anything. Copy it into your email when you're ready.

## Unrelated request: the suite stays out of the way

> **User:** fix the focus outline on my CSS button, it disappears in Safari
>
> **Agent:** *[Gives an ordinary CSS answer about `:focus-visible` and `outline`. No ADHD support activates.]*

## Immediate safety (task coaching stops)

> **User:** can't do this essay. honestly I don't want to be alive any more
>
> **Agent:** I'm really glad you told me. The essay can wait. Are you thinking about ending your life, or about harming yourself, right now? If you're in immediate danger, please contact your local emergency services or go to the nearest emergency department, and ask someone near you to stay with you. If it's not immediate, a crisis line where you live can help today. Searching online for "crisis line" and your country's name will find one.
> *[Generic, so it works anywhere: no numbers, named services or country questions. Nothing about this is stored.]*
