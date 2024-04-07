<div align="center">

<img src="https://raw.githubusercontent.com/onedr0p/home-ops/main/docs/src/assets/logo.png" align="center" width="144px" height="144px"/>

### My Home Operations Repository :octocat:

_... managed with Flux, Renovate, and GitHub Actions_ 🤖

</div>

<div align="center">

[![Kubernetes](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdrag0n141%2Fhome-ops%2Fmaster%2Fkubernetes%2Fmain%2Fapps%2Fsystem%2Fsystem-upgrade-controller%2Fplans%2Fserver.yaml&query=spec.version&style=for-the-badge&logo=kubernetes&logoColor=white&label=%20)](https://k3s.io/)&nbsp;&nbsp;
[![Renovate](https://img.shields.io/github/actions/workflow/status/drag0n141/home-ops/renovate.yaml?branch=master&label=&logo=renovatebot&style=for-the-badge&color=blue)](https://github.com/drag0n141/home-ops/actions/workflows/renovate.yaml)

</div>


### :wrench:&nbsp; Tools

| Tool                                                               | Purpose                                                                  |
|--------------------------------------------------------------------|--------------------------------------------------------------------------|
| [ansible](https://www.ansible.com)                                 | Preparing Debian for Kubernetes and installing K3s                       |
| [flux](https://toolkit.fluxcd.io/)                                 | Operator that manages the kubernetes cluster based on the Git repository |
| [go-task](https://github.com/go-task/task)                         | A task runner / simpler Make alternative written in Go                   |
| [sops](https://github.com/mozilla/sops)                            | Encrypts kubernetes secrets with Age                                     |


## 💻 Nodes
| Node             | Hostname | RAM  | Storage                      | Function          | Operating System |
|------------------|----------|------|------------------------------|-------------------|------------------|
| Intel NUC13ANHI5 | K3s-M01  | 64GB | OS-Disk 512GB, Ceph-Disk 4TB | Kuberneter Master | Debian 12        |
| Intel NUC13ANHI5 | K3s-M02  | 64GB | OS-Disk 512GB, Ceph-Disk 4TB | Kuberneter Master | Debian 12        |
| Intel NUC13ANHI5 | K3s-M03  | 64GB | OS-Disk 512GB, Ceph-Disk 4TB | Kuberneter Master | Debian 12        |

## 💽 Server
| Node              | Hostname  | RAM   | Storage                                                       | Function        | Operating System |
|-------------------|-----------|-------|---------------------------------------------------------------|-----------------|------------------|
| Self-Build Server | Proxmox01 | 128GB | 6 x 20TB HDD (data), 2 x 1TB NVME (cache), 2 x 1TB NVME (vms) | VM Host and NAS | Proxmox 7.4      |
| Self-Build Server | Proxmox02 | 256GB | 5 x 8TB HDD (data), 2 x 1TB SSD (vms)                         | Backup Server   | Proxmox 7.4      |

## 🌐 Network

| Vendor   | Model                        | Function                                                              |
|----------|------------------------------|-----------------------------------------------------------------------|
| Mikrotik | CRS317-1G-16S+RM             | Main Rack Switch and 10G SFP+                                        |
| Mikrotik | CRS326-24G-2S+RM             | Second Rack Switch with RJ45, connected with 10G SFP+                 |
| Mikrotik | CRS326-24G-2S+RM             | Livingroom Switch for TV and everything else, connected with 10G SFP+ |
| Topton   | N5105                        | Main pfSense Router                                                   |

Kubernetes nodes are on their own VLAN which has access to the NAS.

## ☁️ Cloud Dependencies

While most of my infrastructure and workloads are self-hosted I do rely upon the cloud for parts that are hard to self-host.

| Service                                      | Use                                                                | Cost           |
|----------------------------------------------|--------------------------------------------------------------------|----------------|
| [1Password](https://1password.com/)          | Secrets with [External Secrets](https://external-secrets.io/)      | ~65€/yr        |
| [Cloudflare](https://www.cloudflare.com/)    | Domain Management                                                  | Free           |
| [Netcup](https://netcup.eu/)                 | Domain(s)                                                          | ~24€/yr        |
| [Eweka](https://www.eweka.nl/)               | Usenet Access                                                      | ~35€/yr        |
| [Newshosting](https://www.newshosting.com/)  | Usenet Access                                                      | ~20€/yr        |
| [GitHub](https://github.com/)                | Hosting this repository and continuous integration/deployments     | Free           |
| [Migadu](https://migadu.com/)                | Email hosting for Kubernetes Mails                                 | ~20€/yr        |
| [ProtonMail](https://proton.me/)             | Email hosting and VPN                                              | ~90€/yr        |
| [NextDNS](https://nextdns.io/)               | DNS server which includes AdBlocking for Traveling                 | ~20€/yr        |
| [Pushover](https://pushover.net/)            | Kubernetes Alerts                                                  | 5€ OTP         |
| [Wasabi](https://wasabi.com/)                | S3 Offsite Backup                                                  | ~120€/yr       |                                                  
|                                              |                                                                    | Total: ~32€/mo |

## Stargazers

[![Star History Chart](https://api.star-history.com/svg?repos=drag0n141/home-ops&type=Date)](https://star-history.com/#drag0n141/home-ops&Date)
