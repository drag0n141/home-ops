<div align="center">

<img src="https://avatars.githubusercontent.com/u/44865095?v=4" align="center" width="144px" height="144px"/>

### My Home Operations Repository :octocat:

_... managed with Flux, Renovate, and GitHub Actions_ 🤖

</div>

### :wrench:&nbsp; Tools

| Tool                                                               | Purpose                                                                  |
|--------------------------------------------------------------------|--------------------------------------------------------------------------|
| [flux](https://toolkit.fluxcd.io/)                                 | Operator that manages the kubernetes cluster based on the Git repository |
| [go-task](https://github.com/go-task/task)                         | A task runner / simpler Make alternative written in Go                   |
| [sops](https://github.com/mozilla/sops)                            | Encrypts kubernetes secrets with Age                                     |


## 💻 Main Cluster
| Node             | Hostname | RAM  | Storage                      | Function   | Operating System |
|------------------|----------|------|------------------------------|------------|------------------|
| Intel NUC13ANHI5 | K8s-M01  | 64GB | OS-Disk 512GB, Ceph-Disk 4TB | Kubernetes | Talos            |
| Intel NUC13ANHI5 | K8s-M02  | 64GB | OS-Disk 512GB, Ceph-Disk 4TB | Kubernetes | Talos            |
| Intel NUC13ANHI5 | K8s-M03  | 64GB | OS-Disk 512GB, Ceph-Disk 4TB | Kubernetes | Talos            |

## 💽 Proxmox Cluster
| Node             | Hostname | RAM  | Storage                      | Function | Operating System |
|------------------|----------|------|------------------------------|----------|------------------|
| Intel NUC13ANHI5 | PRX01    | 64GB | OS-Disk 256GB, Ceph-Disk 2TB | VM Host  | Proxmox 8.3      |
| Intel NUC13ANHI5 | PRX02    | 64GB | OS-Disk 256GB, Ceph-Disk 2TB | VM Host  | Proxmox 8.3      |
| Intel NUC13ANHI5 | PRX03    | 64GB | OS-Disk 256GB, Ceph-Disk 2TB | VM Host  | Proxmox 8.3      |

## 💽 Server
| Node              | Hostname  | RAM   | Storage                                                       | Function        | Operating System |
|-------------------|-----------|-------|---------------------------------------------------------------|-----------------|------------------|
| Self-Build Server | NAS01     | 64GB  | 6 x 20TB HDD (data), 2 x 1TB NVME (system)                    | NAS             | TrueNas Scale    |
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
| [Mullvad](https://mullvad.net/)                    | VPN                                                                | ~60€/yr        |
| [Pushover](https://pushover.net/)                  | Kubernetes Alerts                                                  | 5€ OTP         |
| [iDrive E2](https://www.idrive.com/s3-storage-e2/) | S3 Offsite Backup                                                  | ~90€/yr        |                                                  
|                                                    |                                                                    | Total: ~26€/mo |

## Stargazers

<div align="center">

<a href="https://star-history.com/#buroa/k8s-gitops&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=drag0n141/home-ops&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=drag0n141/home-ops&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=drag0n141/home-ops&type=Date" />
  </picture>
</a>

</div>
