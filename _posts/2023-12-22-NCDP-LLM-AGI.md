---
title: No code, coding with LLM, and AGI - DRAFT
toc: true
---

*Disclaimer: this was not written by artificial intelligence (e.g., an LLM). I did use it, however, to help generate markdown tables, check my syntax and small errors to improve readability. I prefer to avoid it as much as possible to stay more authentic and credible.*

Yesterday, I spent time at the home of a successful banker in Singapore who taught himself how to code in his 50s. He was joined by his top data scientist and his CTO from two of the ventures he invests in. A part of his success can be attributed to his appreciation of how rigorous science and math can be applied to finance and innovation. His convictions and enthusiasm on three questions caused me to reconsider my own positions. That is to say:

1. How can no/low code platform (NCDP) be used to build (important) software?
2. When will LLMs make it possible for (almost) anyone to create software?
3. When might we successfully implement Artificial General Intelligence?

I’ll address those questions here in part so that I can share this with others and to see how my opinion might change over time.

# 1. No/low code tools (revisited)

I have written on the [fallacy of “no-code” tools in Jan 2021](https://blog.dannycastonguay.com/product/the-fallacy-of-no-code-tools/), where I discuss

1. that you are probably a coder already (e.g., Excel or GSheet)
2. examples where NCDP work, and
3. what matters most is productivity of the product builders.

Consequently, today we already have plenty of no/low code tools in use. But are those tools what venture capitalists would invest USD 100M+ to turn into unicorns? It’s complicated.

## 1.1. NCDP for simple jobs or prototypes

NCDP can already be used to make stuff people want. I decided to try [outsystem](https://www.outsystems.com/) because I learned that [NTU](https://www.ntu.edu.sg/) used it to create an [app](https://www.outsystems.com/case-studies/ntu-singapore-mobile-campus-experience/) used by 20,000 students (captive audience) and that some serious investors like [KKR](https://www.kkr.com/) have poured USD 800M+ into this beast of a startup. I gave it a shot for 30 minutes to see how far I could get:

1. I created an account
2. Then I installed Service Studio locally
3. Followed the tutorial, which let me create something from scratch
4. It prompted me to import an Excel as my database (clearly a common use case for their target audience)
5. I found a single sign-on (SSO) module on the Forge
6. And then the app crashed and I had to force quit it in MacOS
6. I reloaded, and found that I now had two modules, one for SSO and one with my prototype (without SSO)
7. My time was up but I can imagine how after another hour I might have something up and running

Conclusion: I can’t conclude that OutSystems would not work. On the contrary, it looks interesting for those who are ready to try something different. But it is not clearly better/faster/cheaper than using a more mainstream stack that millions of people use. The NTU bus app seems like something that would traditionally take 2-3 months to build and USD 50K in budget, including everything. After that, I’d imagine maintenance to be one part-time engineer who might charge a few hours a month to maintain, update, support, and train (`MUST`) people on the software, and less than USD 1K a month on a platform as a service like AWS. To be truly innovative, I’d love to see NCDP enable schools like NTU to build bus apps for USD 5K, or even USD 500.

## 1.2. Find competent people

For a startup that has raised millions of dollars, or enterprises who are spending similar amounts on technology, I think the most important first step is to find people who have a good understanding of how to make things people want. These are the individual contributors that will be responsible to analyze, dream, design, architect, implement, maintain, update, support and train others (`ADD AI MUST`). I have yet to meet someone who has a good understanding of how to do this well that doesn't know the syntax of a few programming languages.

## 1.3. The right tool for the job

That doesn't mean that after you raise millions of dollars, you shouldn't use a NCDP. It might very well be a good decision. However, you should only do so if you have found someone with deep understanding who thinks that using an NCDP is the right tool for the job. The practitioner with tacit knowledge of how to `ADD AI MUST`, is the person who makes this choice.

I’d venture to say that a pretty significant number of startups in Silicon Valley (e.g., Y-Combinator backed startups) who are getting started in 2024 will not use a NCDP and instead will use a stack that resembles the following:

- [React.js](https://reactjs.org/)
- [Next.js](https://nextjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Django](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [GraphQL](https://graphql.org/)
- [Azure Kubernetes Services (AKS)](https://azure.microsoft.com/en-us/services/kubernetes-service/)
- [GitHub and Actions](https://github.com/features/actions)
- [Cypress](https://www.cypress.io/)
- [Snyk](https://snyk.io/)
- [New Relic](https://newrelic.com/)
- [Mixpanel](https://mixpanel.com/)
- [SonarQube](https://www.sonarqube.org/)
- [Jira](https://www.atlassian.com/software/jira)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Azure OpenAI](https://azure.microsoft.com/en-us/services/openai/)

# 2. Large language models make it possible for anyone to code

Are developers gatekeepers? I'd argue that developers tend to be the opposite. They are people who have put effort over many years to learn how to write those instructions that the computers will execute for our benefit. I have yet to meet someone preventing another from learning how to code. In fact, it's quite the opposite. I have yet to meet a developer who doesn't want to teach someone who is ready to learn.

## 2.1. A brief hitory

We have seen a lot of exciting development over the last 400 years to empower humans to use computers as obedient and dedicated helpers who not only enable things like eCommerce, supply chain logistics, and digital communication, but also to entertain us with video games, social media, and TV streaming. As long as we feed them electricity and provide them a cool/dry environment, they will perform as they are instructed to.

And it's easier now than it has ever been before. Here’s a (very brief) history of this remarkable evolution:

```
1642: Invention of Blaise Pascal's Mechanical Calculator (Pascaline).
1833: Ada Lovelace begins work on Charles Babbage's Analytical Engine.
1890: Development of punch card technology by Herman Hollerith for the US Census.
1943: Development of ENIAC, the first general-purpose electronic digital computer.
1949: Introduction of Assembly Language with the EDSAC computer.
1972: Development of the C Language by Dennis Ritchie at Bell Labs.
1974: Introduction of the Altair 8800, considered the first personal computer.
1989: Tim Berners-Lee invents the World Wide Web (Web 1.0).
1991: Linus Torvalds releases the first version of the Linux kernel, marking the Free and Open Source Software Movement.
1995: Release of Java by Sun Microsystems, popularizing Object-Oriented Programming.
1998: Founding of Google.
2004: Popularization of the term "Web 2.0," marking a transition to interactive and social web experiences.
2005: Creation of Git by Linus Torvalds; GitHub founded in 2008.
2006: Introduction of AWS by Amazon, initiating the Cloud Computing and Platform as a Service era. Also, creation of Hadoop for big data processing.
2007: Introduction of the iPhone, boosting mobile app development.
2008: Launch of Stack Overflow, exemplifying crowdsourcing in software development.
2014: Introduction of smart contracts by Ethereum, a significant step towards Web 3.0 and decentralized web applications.
2018: Introduction of advanced Large Language Models like GPT-4 by OpenAI.
Expected Future Development: Quantum Computing, an ongoing research area with significant potential.
```

So I think we should celebrate how LLMs make coding more accessible.

## 2.2. Making good stuff still requires effort

An LLM might get someone up and running very quickly similarly to a NCDP. But it comes with a warning: it still requires effort. I’d conjecture that not knowing how to code has less to do with intelligence and more to do with willingness to sustain effort over time.

So someone who was willing to put effort 5, 10, or 30 years ago, is only going to see the result of their effort increased today. Additionally `ADD AI MUST` forms a collection actions that are best performed as a team. As the number of people on a team grows, so do the number and the length of meetings. A rough approximation is that 1 on 1 meetings on a team will grow as a [triangular series](https://en.wikipedia.org/wiki/Triangular_number), until the point where people have no time work or communication breaks down.

| Team size | Num meetings |
|-----------|-------------|
| 1         | 0           |
| 2         | 1           |
| 3         | 3           |
| 4         | 6           |
| 5         | 10          |
| 10        | 45          |
| 20        | 190         |

## 2.3. Productivity gain

In addition to that, making software is creative knowledge work. Unlike manufacturing or services, where the amount of repetitive mechanical or repetitive cognitive work increases linearly with the number of people performing the work, creative work is more multiplicative between individuals, and much harder to estimate linearly. For instance, a poor performer might actually reduce the total amount of work that a team can accomplish. On the other hand, strong team members might multiply their strength.

Imagine that an "ok" performer can create `X` units of work. A "good" performer might create `2X` during the same time. A great one, `10X`. And an outstanding one `30X` or more. On the other hand, someone who is a complete beginner might create exactly `0X` if they keep asking for attention and never learn. The good news is that I think LLMs have a positive impact on everyone, and the most efficient performers will have the greatest benefits. But the benefit is linear. Here's a table to illustrate the point numerically, where W stands for work.

| W without LLM | Team of 5 W | ΔW with LLM | W with LLM | Team of 5 W | Team of 5 ΔW |
|---------------|-------------|-------------|------------|-------------|--------------|
| 0             | 0           | 0.5         | 0.5        | 0           | 0            |
| 1             | 1           | 1           | 2          | 32          | 31           |
| 2             | 32          | 2           | 4          | 1,024       | 992          |
| 10            | 100,000     | 3           | 13         | 371,293     | 271,293      |

This model needs to be calibrated/validated to represent reality. But the implications, if the model is true, are important to consider:

1. An LLM will help a complete beginner go from 0 to .5 almost instantly. That is remarkable. But a team of five complete beginners, who don't learn, will still produce no useful work despite the LLM.
2. A team of "ok" performers without an LLM don't produce much (presumably they never ship anything useful and never get anywhere), but with an LLM they have a fighting chance and could improve their performance by 3,000%.
3. A team of "outstanding" performers were already producing an outstanding 100K of unit of work, and they improved by 300%. By far the great improvement in absolute value.

In other words, if this is true, then

1. The war for talent is well and alive, and great/outstanding performers are key to making stuff people want.
2. The number of teams that can ship useful products is increasing.
3. The greatest benefit, in absolute value, is captured by the few.

Now, this raises another interesting question around productivity for creative work. If the task is to lay a brick wall or to pack and ship packages, then productivity can be measured using a single dimension. Creative work is much harder to capture. Can creative knowledge work be narrowly defined as number of users or revenue? That's what venture capitalists have to do for lack of a better metric. For a lot of applications, the amount of work required is not necessarily in the 100,000. Coming back to the bus app for NTU, this may well have been accomplished by team of two good people over 10 weeks (e.g., `(2 * 2) ^ 3 * 10 = 640X`).

Overall, this is all fantastic news for innovation worldwide, as long as it is done ethically and safely.

# 3. When might we build AGI?

## 3.1 Humbling question for everyone

I should perhaps establish my credibility (or lack thereof!). I've been thinking about artificial intelligence for around 30 years. I'm 41 years old now and in the 1990s, I was interested in how bots were programmed in games like Quake, Poker and Go. That's how I learned about `malloc()`. Later on, I went to McGill University and studied under Shie Mannor, Doina Precup, Benoit Boulet, Jeremy Cooperstock. In the early 2000s, the Natural Sciences and Engineering Research Council of Canada funded many PhD students/professors and included the likes of Geoffrey Hinton (deep learning), Joshua Bengio (also deep learning), and Rich Sutton (reinforcement learning). I was at the right place and perhaps just a few years early before everything blew up. I’m probably a little better in engineering than in math, and I’m probably a little better in business than in engineering! But my love for pure math runs all the way down.

I have a decent network of friends who have been at this game for several decades, both in academia and in business, and nobody can speak with certainty about AGI. I do not believe that AGI is around the corner for a few reasons.

## 3.2 General Intelligence

Let's consider our intelligence, which emerges, it seems, from our [meat brains](https://en.wikipedia.org/wiki/They%27re_Made_Out_of_Meat), which is pretty funny. Perhaps a side by side comparison will help us put things in perspective:

| Aspect                          | Human Brain                        | GPT-4                               |
|---------------------------------|------------------------------------|-------------------------------------|
| Training Time                   | Lifetime (continuous learning)     | Years (since inception of GPT models)|
| Energy Consumption              | Around 20 Watts                    | Requires substantial computational resources (varies based on infrastructure)|
| Learning Method                 | Online (real-time learning)        | Primarily offline (trained on a dataset, then updated periodically) |
| Neurons                         | Approx. 86 billion neurons         | Not applicable (digital neural network) |
| Connections per Neuron          | Approx. 1,000 to 10,000 synapses   | Not applicable (digital neural network) |
| Total Parameters                | 86 to 860 trillion analogue connections         | 175 billion parameters (in GPT-4 model) |
| Nature                          | Analog (biochemical processes)     | Digital (based on binary computation) |
| Input/Output Neurons            | Approx. 86 billion (all are I/O)   | Input/Output defined by model architecture (not neuron-based) |
| Affected by Biochemical Signals | Yes                                | No                                  |
| Quantum Effects                 | Minimal impact                     | No (classical computing)             |
| Fundamental Mechanism     | Neural Plasticity                  | Backpropagation with Gradient Descent      |
| Learning Structure        | Hebbian Learning, Multiple Memory Systems | Transformer Architecture               |
| Context Understanding     | Context derived from sensory inputs and cognitive processes | Self-Attention Mechanism              |
| Sequence Processing       | Temporal sequence processing in neural circuits | Positional Encoding                       |
| Stabilization             | Homeostatic mechanisms in neural activity | Layer Normalization                        |
| Sub-Processors            | Specialized brain regions for different functions | Multi-Head Attention                      |
| Regularization            | Sleep, synaptic pruning, etc.      | Dropout, Label Smoothing                   |
| Adaptation and Specialization | Lifelong learning and adaptation based on experiences | Fine-Tuning and Transfer Learning       |
| Activation/Processing Functions | Various neurotransmitters and neurochemical processes | Activation Functions like GELU          |

In addition, GPT-4 has a context window of 128K tokens, while each of our neurons are fully I/O capable. Notably:

| Category          | Type of Neurons                 | Estimated Number of Neurons    |
|-----------------------|-------------------------------------|------------------------------------|
| Vision                | Photoreceptors in the retina        | 120 million                         |
| Hearing               | Hair cells in each ear              | 15,000 per ear                      |
| Touch                 | Sensory neurons for touch           | Estimated several million          |
| Taste                 | Taste receptor neurons              | Estimated tens of thousands        |
| Smell                 | Olfactory receptor neurons          | About 10 million                    |
| Motor Control         | Motor neurons                       | Approx. 500,000                     |
| Autonomic Functions   | Neurons in the autonomic system     | Estimated several hundred thousand |
| Pain and Temperature  | Nociceptors and thermoreceptors     | Estimated several hundred thousand |

# 3.3 AGI - DRAFT

This is making me think about, you know, artificial versus natural. Could we compare a little bit artificial intelligence to like a car versus leopard or an eagle, right? If we try to make a comparison that artificial general intelligence is similar to, let's say, the speed of running down a track, then the car will never be a leopard. It'll never be as complicated, etc. But in terms of useful work to go down a track, the car always beats the leopard. Similarly, the airplane jet always beats the the eagle. So, in that sense, the artifice and the brutality of the artificial technology that we build simplifies the rules of the game such that it can perform an action much more efficiently. We organize material and physics in a way that it achieves, whether it's driving down a line or whether it's flying across the air, much faster. But it makes me wonder, is artificial intelligence, artificial general intelligence, similarly, can it also be narrowly defined as moving into a certain dimension, like going from point A to point B, except that it's around for the dimension of cognition, which kind of asks fundamental question about what is cognition? Because the key word here is general, right? Is general cognition something that fundamentally could be brought down to just a few dimensions? Because it sounds to me like, by definition, general artificial intelligence is always going to be that which goes into high dimension. So, any form of artificial intelligence, by definition, would be bounded by the dimension that it supports. A bit like, okay, the car can go faster than the leopard, but it cannot climb a tree, right? And no matter how advanced we make the machine, there's always going to be something about the leopard that it can do that the car cannot do. And in the same way, it's very unlikely, maybe even mathematically, I hope, or something like this, like it could be proven that you'll never have artificial general intelligence by the same argument. Is there something to that or am I just not making sense?

