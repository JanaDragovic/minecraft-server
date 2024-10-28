# Deploying Minecraft on Kubernetes Cluster 

## Initial prep

First of all, you would need Podman, Kubectl and KIND. I am running Debian on my system, but you can adjust commands to your OS. 

### Podman installation

1. Check if you have podman on your machine: <br />
```podman version```<br /> 
If it is installed, you should see the information about it in your command line:
```
Version:      3.4.2
API Version:  3.4.2
Go Version:   go1.15.2
Built:        Thu Jan  1 00:00:00 1970
OS/Arch:      linux/amd64
```
<br > <br /> 
3. If you do not have Podman on your machine install it via command<br /> 
```sudo apt-get install -y podman```<br /> <br />
4. Check again podman version on your machine to ensure that you have it installed successfuly: <br/>
```podman version``` <br/><br/>
5. Quick Test <br/>
Make sure Podman is working: <br/>
```podman run hello-world``` <br/> <br>
The output that you should see looks like this: <br/>
```
Hello from Docker
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/!
```
<br/>
If Podman is not working, make sure to check if it is running and enabled using following commands: <br/>

```
sudo systemctl status podman;
sudo systemctl enable podman;
sudo systemctl start podman;
```

### Go installation
In order to install and use KIND, you will need to have Go installed.
The easiest way to install it is using package manager called Snap. <br>
1. Check if you have Snap on your system.  <br>
```
snap version
```
If Snap is installed, you’ll see the version information of snapd, snap, and series, like this: 
```
snap    2.58
snapd   2.58
series  16
```
2. If you do not, go ahead and install, enable and start it: <br>
```
sudo apt install snapd;
sudo systemctl enable --now snapd;

```
3. Snap installs binaries in ```/snap/bin```, which might not be included in your PATH. To add it:
```
nano ~/.bashrc
export PATH=$PATH:/snap/bin
source ~/.bashrc
```
Now you are ready to install Go! <br>
4. Install go: 
```
sudo snap install go --classic
```
5. Verify go version:
```
go version
```
6. The successful output should look like this: 
```
go version go1.19.5 linux/amd64
```

### Install kubectl 

1. Check if you already have kubectl: 
```
kubectl version --output=yaml
```
2. If you do not have it, install it using the following command:
```
sudo snap install kubectl --classic
```
3. Now, your command for checking the kubectl version should be successful:
```
clientVersion
  buildDate: "2022-09-21T13:19:24Z"
  compiler: gc
  gitCommit: b39bf148cd654599a52e867485c02c4f9d28b312
  gitTreeState: clean
  gitVersion: v1.24.6
  goVersion: go1.18.6
  major: "1"
  minor: "24"
  platform: linux/amd64
kustomizeVersion: v4.5.4

The connection to the server localhost:8080 was refused - did you specify the right host or port?:
```

The kubectl command is installed and ready to use. Don't worry about the connection error, there is no API to talk to yet.

### Configuring the shell

Before starting to work with KIND, we're going to want to set a couple of things in our shell environment to make working with KIND easier. If you're using BASH, use the ~/.bashrc file.
Add environment variables to your ~/.bashrc file:
```
cat << EOF >> ~/.bashrc
alias docker=podman
PATH=$PATH:~/go/bin
KIND_EXPERIMENTAL_PROVIDER=podman
EOF
```
Pick up the changes using the following command: 
```
source ~/.bashrc
```
Check if the changes successfully applied: 
```
docker version
```
The output should look like this: 
```
Version:      3.4.2
API Version:  3.4.2
Go Version:   go1.15.2
Built:        Thu Jan  1 00:00:00 1970
OS/Arch:      linux/amd64
```

### Install git
```
sudo apt install git 
```

## Deploying Minecraft server to the KIND cluster

### Clone repo with materials
```
git clone https://github.com/JanaDragovic/minecraft
cd minecraft
```

### Create container image for minecraft

```
podman build ./minecraft -t minecraft:v1
```

The container's structure is imagined to look like this: 
```
/data
│
├── paper-1.20.4-496.jar
├── server.properties
├── bukkit.yml
├── start.sh
│
├── plugins
│   └── unifiedmetrics-platform-bukkit-0.3.8.jar
│   └── unifiedmetrics
│       └── driver
│           └── prometheus.yml
│
├── data.zip  (temporary, extracted and then removed)
│
├── cache
│   └── mojang_1.20.4.jar
```

### Create kind cluster from config

```
kind create cluster --name minecraft --config kind.yml
kubectl cluster-info --context kind-minecraft
```

### Save container image as tarball

```
podman save minecraft:v1 -o minecraft.tar
```

### Load image into kind cluster

```
kind load image-archive minecraft.tar --name minecraft
```

### Deploy minecraft

```
kubectl apply -f minecraft/minecraft.yml
kubectl apply -f minecraft/service.yml
```

### Make port 25565 reachable 
```
iptables -I INPUT -p tcp --dport 25565 -j ACCEPT
```

### Forward minecraft to host_ip:25565 (oneliner)
```
kubectl port-forward --address 0.0.0.0 $(kubectl get pods | grep minecraft | cut -d' ' -f1) 25565:25565
```

## Set up monitoring 

### Deploy Prometheus in this particular order
```
kubectl apply -f prometheus/cluster_role.yaml
kubectl apply -f prometheus/config_map.yml
kubectl apply -f prometheus/deployment.yml
kubectl apply -f prometheus/service.yml
```

### Deploy Grafana in this particualr order
```
kubectl apply -f grafana/datasource_config.yml
kubectl apply -f grafana/deployment.yml
kubectl apply -f grafana/service.yml
```

### Make port 3000 reachable 
```
iptables -I INPUT -p tcp --dport 3000 -j ACCEPT
```

### Forward grafana to host_ip:3000 (oneliner)
```
kubectl port-forward --address 0.0.0.0 -n monitoring $(kubectl get pods -n monitoring | grep grafana | cut -d' ' -f1) 3000:3000
```
