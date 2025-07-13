---
title: Open Source Cloudless AI
---

**DRAFT - More content will be added over the coming days**

I wanted to build a local workstation powerful enough to run the largest available AI models completely on consumer hardware. The goal is simple: no proprietary cloud services, no external APIs. Instead, I want fully autonomous AI agents that can handle my emails, calendars, spreadsheets, Telegram bots, and more - all powered by open-source software, running locally, giving me complete privacy and control.

Here's the exact build I chose:

* **GPU:** NVIDIA RTX 5090 (32GB VRAM, ~$3,000).
  I picked this card specifically because I want the ability to run large open-source models like Command R+ and Mixtral fully in GPU memory without compromising on performance or quantization.

* **CPU:** AMD Ryzen 9 9950X3D (~$700).
  Chosen for its best-in-class multicore performance, excellent cache design, and smooth multitasking capability - critical for managing data loaders, local servers, and background tasks.

* **Motherboard:** ROG Strix X870E-E Gaming WiFi (~$450).
  Selected for stability, full PCIe 5.0 support, robust power delivery, and comprehensive connectivity.

* **Cooling:** NZXT Kraken Elite 360 liquid cooler (~$330).
  This cooling setup efficiently manages CPU thermals under sustained heavy loads, installed neatly into my Thermaltake Core P3 TG Pro open-frame case (~$180) for maximum airflow.

* **Power Supply:** ROG Strix 1000W Platinum ATX 3.1 (~$270).
  Stable, efficient, and future-proof power delivery that reliably supports my GPU, CPU, and peripherals.

* **Storage:** Western Digital Black SN850X NVMe SSD, 8TB Gen4 (7200 MB/s, ~$750).
  Massive capacity combined with blazing-fast performance ensures near-instant model loading and plenty of room for large datasets and local model files.

* **RAM:** Corsair DDR5 64GB 6000MHz (~$250).
  Enough memory to comfortably handle large datasets, model inference, and multiple parallel processes.

**Total cost:** Approximately **$5,930 USD**.

After assembling this build, I installed Ubuntu as my operating system and set up Ollama to manage open-source AI models locally. Currently, I'm running **Command R+**, a model specifically tuned for structured JSON outputs, reliable function calling, and agent-based tasks - perfect for building local Model-Context Protocol (MCP) agents.

My ultimate goal is clear: create a series of completely autonomous local agents that interact seamlessly with Gmail, Google Calendar, Google Sheets, Telegram bots, and more, entirely without external services. This project demonstrates that it's now feasible to have a powerful, agentic AI system running entirely locally on consumer hardware, leveraging open-source tools for complete autonomy, privacy, and control.