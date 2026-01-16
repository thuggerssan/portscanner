1. Docker
    # Troubleshots
    A. attempt on installing
        sudo apt-get update
        sudo apt-get install -y apt-transport-https ca-certificates curl gnupg
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
        | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        sudo apt-get update
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io
        sudo usermod -aG docker $USER
        newgrp docker

    B. Error message
        ubuntu@ip-172-31-38-195:~$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
        | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        ubuntu@ip-172-31-38-195:~$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"   | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        ubuntu@ip-172-31-38-195:~$ sudo apt-get install -y docker-ce docker-ce-cli containerd.io
        sudo usermod -aG docker $USER
        Reading package lists... Done
        Building dependency tree... Done
        Reading state information... Done
        Package docker-ce is not available, but is referred to by another package.
        This may mean that the package is missing, has been obsoleted, or
        is only available from another source

        Package docker-ce-cli is not available, but is referred to by another package.
        This may mean that the package is missing, has been obsoleted, or
        is only available from another source

        E: Package 'docker-ce' has no installation candidate
        E: Package 'docker-ce-cli' has no installation candidate
        E: Unable to locate package containerd.io
        E: Couldn't find any package by glob 'containerd.io'
        E: Couldn't find any package by regex 'containerd.io'
        usermod: group 'docker' does not exist
        ubuntu@ip-172-31-38-195:~$ sudo apt-get install -y docker-ce docker-ce-cli containerd.io
        sudo usermod -aG docker $USER
        newgrp docker
        Reading package lists... Done
        Building dependency tree... Done
        Reading state information... Done
        Package docker-ce is not available, but is referred to by another package.
        This may mean that the package is missing, has been obsoleted, or
        is only available from another source

        Package docker-ce-cli is not available, but is referred to by another package.
        This may mean that the package is missing, has been obsoleted, or
        is only available from another source

        E: Package 'docker-ce' has no installation candidate
        E: Package 'docker-ce-cli' has no installation candidate
        E: Unable to locate package containerd.io
        E: Couldn't find any package by glob 'containerd.io'
        E: Couldn't find any package by regex 'containerd.io'
        usermod: group 'docker' does not exist
        newgrp: group 'docker' does not exist

    C. Analysis, Solution
        You ran into this because on Ubuntu the “docker-ce” packages live in Docker’s own repo (which you haven’t actually got set up),
        whereas the distro-provided “docker.io” package is in the default Ubuntu archives.

            # Update & Install
            sudo apt update
            sudo apt install -y docker.io

            # Enable and start
            sudo systemctl enable --now docker

            # Adding self to "docker" group : no sudo required in the future
            sudo groupadd docker        # only if the group doesn’t already exist
            sudo usermod -aG docker $USER
            exec $SHELL                 # re-login your shell or just close & reopen it

            # After rebooting shell
            docker run --rm hello-world

        --> this is a Ubuntu supported docker, so it will not have the latest features, but enough for practice projects
        --> If you need features from the latest distro of docker, try docker-CE version directly from docker repo

    Docker images
    - OWASP Juice Shop (Node.js vulns, port 3000)
        1. Installation
        
            ubuntu@ip-172-31-38-195:~$ docker pull bkimminich/juice-shop
            Using default tag: latest
            latest: Pulling from bkimminich/juice-shop
            35d697fe2738: Pull complete 
            bfb59b82a9b6: Pull complete 
            ...

            Digest: sha256:51134b74c523b6779a4bf25bca021b5cfae7898b6e68f6545e8bb9e4d33ce6b0
            Status: Downloaded newer image for bkimminich/juice-shop:latest
            docker.io/bkimminich/juice-shop:latest

            ubuntu@ip-172-31-38-195:~$ docker run -d --name juice -p 3000:3000 bkimminich/juice-shop
            9137e93f6da5d4e60c57c8b2753ed9190821eef620ea71638be05c02eb237751

        2. Confirim it's running, serviced at port 3000

            ubuntu@ip-172-31-38-195:~$ ps aux | grep "juice"
            65532       2068 28.8 14.9 1318088 146660 ?      Ssl  13:14   0:03 /nodejs/bin/node /juice-shop/build/app.js
            ubuntu      2106  0.0  0.2   7076  2048 pts/0    S+   13:14   0:00 grep --color=auto juice

            ubuntu@ip-172-31-38-195:~$ sudo ss -tnlp
            State               Recv-Q              Send-Q                           Local Address:Port                            Peer Address:Port             Process                                                 
            LISTEN              0                   4096                                127.0.0.54:53                                   0.0.0.0:*                 users:(("systemd-resolve",pid=311,fd=17))              
            LISTEN              0                   4096                                   0.0.0.0:3000                                 0.0.0.0:*                 users:(("docker-proxy",pid=1998,fd=4))                 
            LISTEN              0                   4096                                 127.0.0.1:43675                                0.0.0.0:*                 users:(("containerd",pid=586,fd=10))                   
            LISTEN              0                   4096                             127.0.0.53%lo:53                                   0.0.0.0:*                 users:(("systemd-resolve",pid=311,fd=15))              
            LISTEN              0                   4096                                      [::]:3000                                    [::]:*                 users:(("docker-proxy",pid=2006,fd=4))                 
            LISTEN              0                   4096                                         *:22                                         *:*                 users:(("sshd",pid=1219,fd=3),("systemd",pid=1,fd=90)) 
    -
2. 