---
title: When AI Codes, You Accrue Theory Debt
---

Technical debt has been affecting software teams since Ada Lovelace started coding in the 19th century. 

What is technical debt? It's when the codebase of a software project starts to become difficult to maintain, for example due to:

1. Original developers moving on
2. Requirements evolving 
3. Tech stacks getting older

The code still works, but the concepts embedded in variable names, data models, and APIs no longer align with what the product does. 

But with AI-augmented coding, there's a deeper, subtler burden but much more serious burden: AI theory debt.

When you prompt an AI like [lovable](https://lovable.dev/) or [Claude Code](https://github.com/anthropics/claude-code), it feels like magic. You get 90 percent of a working feature in minutes. Its breathtaking.

But you never built a theory of that code. You don’t really know why it works, where its vulnerabilities lie, or how small changes cascade. You hold the result, not the insight.

Later, when you try to tweak one small thing, you end up in a cascade of failures: moving a pixel shifts layout, tweaking a state variable breaks logic elsewhere, refactoring one function ruins dependencies. You realize too late the AI was smart at generating but dumb at preserving coherence.

That’s theory debt. Or AI theory debt. Or AI debt. Or [comprehension debt](https://news.ycombinator.com/item?id=45423917). Call it what you want. 

Because you never internalized the code's theory, you now pay for reverse engineering, debugging, and walking blind paths.

That Hacker News post I linked above connects to [Peter Naur’s 1985 Programming as Theory Building](https://gwern.net/doc/cs/algorithm/1985-naur.pdf). Naur argues that the real product of programming is not the code or documentation. => It’s the theory in the programmer’s head: how the system maps to the real world, why each design decision was made, how modifications should evolve. 

If you lose or skip that theory, you degrade your capacity to change the system intelligently. Over time, the system devolves into patchwork, because you’re modifying without shared insight.

So unlike technical debt where you knowingly accept imperfections, theory debt is debt incurred by ignorance. It’s a debt you don’t see! Not until it forces you to rebuild, or abandon what you built.

How to manage theory debt:

1. Use AI to scaffold or prototype, not to design entire modules.
2. Always annotate, document metaphors, invariants, edge cases.
3. Force yourself to rewrite or refactor with full understanding.
4. Build the theory: draw diagrams, write narrative, run experiments.
5. On handover, pass not just code, but the guiding metaphors you used.

Theory debt is insidious because it's invisible until you suffer. It’s the debt of missing understanding. Don’t just borrow working code. Borrow the insight too. 

💚💚

