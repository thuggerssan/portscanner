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

    docker images
    - OWASP Juice Shop (Node.js vulns, port 3000)
    -
2. 