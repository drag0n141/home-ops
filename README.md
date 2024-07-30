<div align="center">

<img src="https://raw.githubusercontent.com/onedr0p/home-ops/main/docs/src/assets/logo.png" align="center" width="144px" height="144px"/>

### My Home Operations Repository :octocat:

_... managed with Flux, Renovate, and GitHub Actions_ 🤖

</div>

<div align="center">

[![Talos](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdrag0n141%2Fhome-ops%2Fmaster%2Fkubernetes%2Fmain%2Fapps%2Fsystem%2Fsystem-upgrade-controller%2Fks.yaml&query=spec.postBuild.substitute.TALOS_VERSION&style=for-the-badge&logo=talos&logoColor=white&color=blue&label=%20)](https://www.talos.dev/)&nbsp;&nbsp;
[![Kubernetes](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdrag0n141%2Fhome-ops%2Fmaster%2Fkubernetes%2Fmain%2Fapps%2Fsystem%2Fsystem-upgrade-controller%2Fks.yaml&query=spec.postBuild.substitute.KUBERNETES_VERSION&style=for-the-badge&logo=kubernetes&logoColor=white&label=%20)](https://www.talos.dev/)&nbsp;&nbsp;
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
| Intel NUC13ANHI5 | K8s-M01  | 64GB | OS-Disk 512GB, Ceph-Disk 4TB | Kuberneter Master | Talos            |
| Intel NUC13ANHI5 | K8s-M02  | 64GB | OS-Disk 512GB, Ceph-Disk 4TB | Kuberneter Master | Talos            |
| Intel NUC13ANHI5 | K8s-M03  | 64GB | OS-Disk 512GB, Ceph-Disk 4TB | Kuberneter Master | Talos            |
| Intel NUC12WSKI5 | K8s-U01  | 16GB | OS-Disk 256GB                | Kuberneter Master | Talos            |

## 💽 Server
| Node              | Hostname  | RAM   | Storage                                                       | Function        | Operating System |
|-------------------|-----------|-------|---------------------------------------------------------------|-----------------|------------------|
| Self-Build Server | Proxmox01 | 64GB  | 6 x 20TB HDD (data), 2 x 1TB NVME (cache), 2 x 1TB NVME (vms) | VM Host and NAS | Proxmox 8.2      |
| Self-Build Server | Proxmox02 | 256GB | 5 x 8TB HDD (data), 2 x 1TB SSD (vms)                         | Backup Server   | Proxmox 8.2      |

## 🌐 Network

| Vendor   | Model                        | Function                                                              |
|----------|------------------------------|-----------------------------------------------------------------------|
| Unifi    | USW Aggregation 8 Port       | Main Rack Switch and 10G SFP+                                         |
| Unifi    | USW Enterprise 48 PoE        | Second Rack Switch with RJ45, connected with 10G SFP+                 |
| Unifi    | USW Pro Max 16               | Livingroom Switch for TV and everything else, connected with 10G SFP+ |
| Unifi    | UDM-SE                       | Main Router connected to USW Aggregation with 10G SFP+                |

Kubernetes nodes are on their own VLAN which has access to the NAS.

## ☁️ Cloud Dependencies

While most of my infrastructure and workloads are self-hosted I do rely upon the cloud for parts that are hard to self-host.

| Service                                            | Use                                                                | Cost           |
|----------------------------------------------------|--------------------------------------------------------------------|----------------|
| [1Password](https://1password.com/)                | Secrets with [External Secrets](https://external-secrets.io/)      | ~65€/yr        |
| [Cloudflare](https://www.cloudflare.com/)          | Domain Management                                                  | Free           |
| [Netcup](https://netcup.eu/)                       | Domain(s)                                                          | ~24€/yr        |
| [Eweka](https://www.eweka.nl/)                     | Usenet Access                                                      | ~35€/yr        |
| [Newshosting](https://www.newshosting.com/)        | Usenet Access                                                      | ~20€/yr        |
| [GitHub](https://github.com/)                      | Hosting this repository and continuous integration/deployments     | Free           |
| [Migadu](https://migadu.com/)                      | Email hosting for Kubernetes Mails                                 | ~20€/yr        |
| [ProtonMail](https://proton.me/)                   | Email hosting and VPN                                              | ~90€/yr        |
| [NextDNS](https://nextdns.io/)                     | DNS server which includes AdBlocking for Traveling                 | ~20€/yr        |
| [Pushover](https://pushover.net/)                  | Kubernetes Alerts                                                  | 5€ OTP         |
| [iDrive E2](https://www.idrive.com/s3-storage-e2/) | S3 Offsite Backup                                                  | ~60€/yr        |                                                  
|                                                    |                                                                    | Total: ~27€/mo |

## Stargazers

[![Star History Chart](https://api.star-history.com/svg?repos=drag0n141/home-ops&type=Date)](https://star-history.com/#drag0n141/home-ops&Date)
 
