---
title: Open Source Cloudless AI
---

I wanted a local workstation powerful enough to run the largest available AI models on consumer hardware. No proprietary cloud services. No external APIs. Fully autonomous agents for email, calendar, spreadsheets, Telegram, and more. All open source, all local, full privacy and control.

## The exact build

* GPU: [NVIDIA GeForce RTX 5090](https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/) with 32 GB VRAM, about $3,000. I picked it so I can run large models in GPU memory without compromises.  
* CPU: [AMD Ryzen 9 9950X3D](https://www.amd.com/en/products/processors/desktops/ryzen/9000-series/amd-ryzen-9-9950x3d.html), about $700. Great multicore and cache for data loaders and local services.  
* Motherboard: [ASUS ROG Strix X870E-E Gaming WiFi](https://rog.asus.com/motherboards/rog-strix/rog-strix-x870e-e-gaming-wifi/), about $450. Stable, PCIe 5.0, strong power delivery, wide connectivity.  
* Cooling: [NZXT Kraken Elite 360](https://nzxt.com/products/kraken-360-elite-rgb-1), about $330, in a [Thermaltake Core P3 TG Pro](https://www.thermaltake.com/core-p3-tg-pro.html) open frame case, about $180. Keeps temps under control and looks clean.  
* Power supply: [ASUS ROG Strix 1000W Platinum ATX 3.1](https://rog.asus.com/power-supply-units/rog-strix/rog-strix-1000p-gaming/), about $270. Quiet and reliable.  
* Storage: [WD Black SN850X NVMe SSD 8 TB Gen4](https://shop.sandisk.com/products/ssd/internal-ssd/wd-black-sn850x-nvme-ssd?sku=WDS800T2X0E-00CDD0), rated to about 7,300 MB per second, about $750. Fast loads and lots of room for datasets and models.  
* RAM: [Corsair Vengeance DDR5 64 GB 6000 MT/s](https://www.corsair.com/us/en/p/memory/cmk64gx5m2b6000z30/vengeance-64gb-2x32gb-ddr5-dram-6000mt-s-cl30-amd-expo-memory-kit-cmk64gx5m2b6000z30), about $250. Enough for parallel jobs and big context runs.
* Monitor: [PRISM+ 49AL 240Hz](https://prismplus.sg/collections/gaming-monitors/products/prism-49al-240hz), about $1,500, for the resolution (5210 x 1440), ClearMR 13000/HDR400, and 240Hz/0.03ms response time.

Total cost: about $7,000 USD (ignoring the value of my time to assemble it).

## Installing and configuring everything

I first installed [Ubuntu 25.04 Plucky Puffin](https://discourse.ubuntu.com/t/plucky-puffin-release-notes/48687). The NVIDIA 5090 driver install was fine. The problem was [CUDA](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/) on Ubuntu 25 and getting different libraries to actually use it. Package compatibility was not there yet for the stack I needed, so I reinstalled with [Ubuntu 24.04 LTS Noble Numbat](https://discourse.ubuntu.com/t/ubuntu-24-04-lts-noble-numbat-release-notes/39890), which worked better.

I installed [Ollama](https://ollama.com/) to run local models and added [FaceFusion](https://github.com/facefusion/facefusion) along with a few other tools. With this, large models can live fully in GPU memory.

## The cooler LED problem

My Kraken screen was upside down in the open frame. On Linux, [liquidctl](https://github.com/liquidctl/liquidctl) could read but not write orientation for this device. On Windows, I used [NZXT CAM](https://nzxt.com/pages/cam) to flip the display.

## The Windows detour and WSL

I installed [Windows 11](https://support.microsoft.com/en-us/windows/ways-to-install-windows-11-e0edbbfb-cfc5-4011-868b-2ce77ac7c70e) and then the [GeForce Game Ready driver](https://www.nvidia.com/en-us/geforce/game-ready-drivers/). RTX 5090 owners can also see the launch driver note here: [Game Ready for RTX 5090 and 5080](https://www.nvidia.com/en-us/geforce/news/geforce-rtx-5090-5080-dlss-4-game-ready-driver/). For Linux tools inside Windows I enabled [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install) and installed [Ubuntu on WSL2](https://ubuntu.com/desktop/wsl). This gives me most of what I want from both worlds.

After the Windows install, the Ubuntu partition stopped booting. Fixing GRUB was not worth the time, so I kept Windows for device control and WSL for my Linux workflow.

## What I liked on Windows

* For easy window layouts I use [PowerToys FancyZones](https://learn.microsoft.com/en-us/windows/powertoys/fancyzones). If I just want the built in snap layouts, see [Snap your windows](https://support.microsoft.com/en-us/windows/snap-your-windows-885a9b1e-a983-a3b1-16cd-c531795e6241).  
* There is a paste manager built in. It is called [Clipboard history](https://support.microsoft.com/en-us/windows/using-the-clipboard-30375039-ce71-9fe4-5b30-21b7aab6b13f). Press Windows and V to enable it.  
* Driver and system updates are simple through [Windows Update](https://support.microsoft.com/en-us/windows/install-windows-updates-3c5ae7fc-9fb6-9af1-1984-b5e0412c556a).

## What I removed or disabled

* Widgets and news. Start with [Customize the taskbar](https://support.microsoft.com/en-us/windows/customize-the-taskbar-in-windows-0657a50f-0cc7-dbfd-ae6b-05020b195b07).  
* Copilot prompts. For policy level control see [Manage Copilot in Windows](https://learn.microsoft.com/en-us/windows/client-management/manage-windows-copilot). For simple hiding, the taskbar toggle also works.  
* Location prompts. See [Windows location service and privacy](https://support.microsoft.com/en-us/windows/windows-location-service-and-privacy-3a8eee0a-5b0b-dc07-eede-2a5ca1c49088).  
* Edge nags. If you want policy control, see [Microsoft Edge policy reference](https://learn.microsoft.com/en-us/deployedge/microsoft-edge-policies).

## Where this leaves me

I wish I could run a 5090 as an external GPU on a Mac. Apple documents eGPU support only for Intel Macs with Thunderbolt 3. Apple Silicon does not support eGPU. See [Use an external graphics processor with your Mac](https://support.apple.com/en-us/102363).

For now my setup is simple. Windows for device control and drivers. WSL with Ubuntu for the tools and scripts I like. CUDA and the NVIDIA driver stack are the core of the local AI workflow. Keep the matrix handy here: [CUDA on Linux Guide](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/).

## Next steps

Over the coming days I will build a Model Context Protocol (MCP) layer that can send emails through Gmail, run agents on a daily schedule, update Google Sheets, and handle other basic workflows. The goal is to keep everything running only on free and open source software, using Ollama as the orchestration layer.
