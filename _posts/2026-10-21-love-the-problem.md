---
title: Love the Problem
---

I'm sharing this message to my kids after they came up with an algorithm for the [CSES Movie Festival problem](https://cses.fi/problemset/task/1629/) this morning.

Here's the (edited for clarity) message they sent me:

> We have found the algorithm to the problem!
> The problem can be solved by sorting the movies in ascending order according to the ending times. We can start from the movie with the earliest ending and watch it. Then continue moving to all the movies according to their ending times. For every subsequent movie, check if we can watch it or not. If we can watch it, then move till we find another movie whose starting time >= the current movie's ending time. After traversing through all the movies, return the final answer.
> (I tried so hard to write the algorithm in a fancy way)

Pascale, Linus, well done. But I'm not going to tell you whether it works or not. That's your job to test it. And this applies to every problem you try to solve. Once you have an idea, it's tempting to start looking for evidence that it works. The risk is that you then become attached to the idea. You explain away the cases where it fails. Eventually, you're defending your solution instead of solving the problem like it's your baby.

I've spent almost 10 years trying to create 1M+ jobs through bld.ai. The problem hasn't changed: people with money and a problem aren't working with people who have the skills to solve it.

Imagine a doctor in New York trying to build something with AI (or SI!). An engineer in Karachi might unlock him with a 30 min conversation and a week of work, saving 2 months of frustration. Existing platforms help, but the problem is still there. That's why I keep trying new approaches, including a bld.ai plugin on chatGPT and Claude.

But I'm not attached to the plugin. I test the idea. I look for where it fails. If I convince myself that it doesn't solve the problem, I kill it. To me, that is success. The problem is still worth solving.

Keep using the process we've been practicing. Read carefully. Start with the simplest possible example, by hand, without AI. Change one thing at a time and explore the edge cases. Build a naive algorithm before looking for shortcuts. Test each shortcut against those cases.

You now have a proposal: sort the movies by ending time, then keep choosing the next one you can watch. Implement it and try to break it. Don't pick examples that make it look good. Look for the ones that expose what you missed.

Failing to find a counterexample isn't a proof. Stay precise about what you know, and stay willing to change your mind.

Be excited about solving the problem. Be willing to give up your solution.
