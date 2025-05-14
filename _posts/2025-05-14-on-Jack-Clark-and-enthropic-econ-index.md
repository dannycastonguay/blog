---
title: On Jack Clark and Enthropic Economic Index
---

[Tyler Cowen](https://en.wikipedia.org/wiki/Tyler_Cowen) is an economist at George Mason and the author of [Marginal Revolution](https://marginalrevolution.com/). On his [podcast](https://conversationswithtyler.com/) he recently interviewed [Jack Clark](https://x.com/jackclarkSF), co-founder of [Anthropic](https://www.anthropic.com/). Anthropic is an AI research company best known for the Claude family of language models. Roughly a third of it is owned by Amazon and Google, and Claude 3.7 is a preferred model to help programmers make software (more so than, say, OpenAI's o3).

In the interview, Jack said that AI might raise USA's economic growth to about 3 to 5% a year, which is substantially less than the 20 to 30% that many techno optimists expect. I agree with Jack here but my view doesn't matter much. I'm more interested in what assumptions we need to make to believe each scenario.

On Apr 28, Anthropic published an entry in its [Economic Index](https://www.anthropic.com/research/impact-software-development). The paper looks only at software development. Three facts matter.
1. 79% of conversations on Claude Code are classified as automation rather than human-in-the-loop help.
2. 60% of the code is front-end web work, things like JavaScript and HTML.
3. 33% of all sessions come from startups; large enterprises only 25%.

The post, however, never assigns a numeric productivity gain. It only shows that early adopters already let an agent write and test sizeable chunks of code.

Let's look into it.

## Economic output

Economic output equals the number of hours worked times what each hour produces. A massage therapist who gives 1 massage per hour and works 10 hours contributes 10 massages. A machinist who makes 1 widget per hour produces 10 widgets in the same 10 hours. If AI lets the machinist build 2 widgets per hour, output doubles even though the hours stay the same. Now for programmers:

1. Programmers are about 3% of the United States labor force.
2. Even if every coder became 50% faster the direct jump in national output would 1.5% once full diffusion is reached.
3. Spread over seven years this is roughly 0.2% of extra growth per year. That is far below Jack’s 3 to 5%.

I think Jack knows that. Better code does help every other job but secondary effects of that size still leave a wide gap. The real action must happen across the wider service sector.

## A simple partition of service work

Let's partition every job and make some assumptions about the potential lift in each.

| Broad job group            | % of jobs | Low case (%) | Jack case (%) | High case (%) |
|----------------------------|-----------|-------------------|--------------------|--------------------|
| Coders                     | 3  | 50 | 50 | 50 |
| Office jobs                | 35 | 0  | 30 | 60 |
| Education                  | 6  | 0  | 20 | 50 |
| Health practitioners       | 6  | 0  | 15 | 40 |
| Production & construction  | 15 | 0  | 10 | 30 |
| Transport & logistics      | 10 | 0  | 10 | 30 |
| Food & hospitality         | 10 | 0  | 10 | 30 |
| Personal & other services  | 15 | 0  | 10 | 30 |

First number is share of employment. The three lift columns give the assumed productivity gain under a low-adoption world, Jack’s moderate world, and a full techno-optimist world. The lifts are after 10 years of diffusion.

Multiply share by lift then add across rows and you get

• about 2% of labor hours saved in the coder-only world
• about 17% saved in the moderate world
• about 60% saved in the full optimist world

Divide each figure by a rollout lag. Seven years for the moderate world and five years for the full optimist world are reasonable guesses.

• coder-only world adds roughly 0.2% to yearly growth
• moderate world adds roughly 2.5%
• full optimist world adds more than 10%

Jack’s 3 to 5% path is the moderate world. It needs three beliefs:

1.	Office, sales, finance, and legal staff adopt agentic AI soon.
2.	Those workers hand over about one-third of their keyboard time.
3.	Diffusion mostly finishes within a decade.

## Why the ceiling is higher than that

When my team at bld.ai works with clients in every industry we see far more upside. Resistance so far is cultural not technical. Many managers still equate productivity with head-count risk, so they stall. The firms that move fast treat AI as a chance to launch new products, not merely to cut costs.

If that attitude spreads the economy can look much closer to the full optimist column than to the moderate one. That would put national growth well above 5%. How high is an open question, but the limit is willingness to change, not capability of the models.

A much larger boom is possible if every occupation decides to reinvent itself rather than defend yesterday’s job description.