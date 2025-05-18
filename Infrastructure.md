# Infrastructure Setup
All the infrastructure was hosted through BYU infrastructure in the Cybersecurity Research Lab (CSRL).

## CTFd Setup
To make CTFd work with a large competition pool (3000+ people), we change some of the default CTFd settings:
* Change gunicorn `WORKERS` envar to 10 ([link](https://github.com/CTFd/CTFd/blob/800fdf152824801b3264e1568bc8395917f3c816/docker-compose.yml#L12))
* Change `SQLALCHEMY_MAX_OVERFLOW` to 8192 ([link](https://github.com/CTFd/CTFd/blob/800fdf152824801b3264e1568bc8395917f3c816/CTFd/config.ini#L288))
* Change Nginx `worker_connections` to 102400 ([link](https://github.com/CTFd/CTFd/blob/800fdf152824801b3264e1568bc8395917f3c816/conf/nginx/http.conf#L5))
* Overriding MariaDB's `max_connections` by creating `conf/mysql.cnf`, mounting it to the MariaDB container as a volume using the line `- ./conf/mysql.cnf:/etc/mysql/conf.d/custom.cnf`, and putting the following contents inside `conf/mysql.cnf`:
    ```
    [mysqld]
    max_connections = 100000
    ```

Once the CTFd instance is up, ensure it's in Team Mode. Most of the settings after this point are customizable year-to-year (name, description, theme, etc.). Make sure to set the Start and End times properly. In addition, it's recommended to have Challenge Visibility set to "Admins Only" before the CTF starts so that mods can view and playtest challenges, then switch to "Private" once it starts. All other fields should be set to "Public".

We also usually have a `/rules` page containing a subset of the rules found in the Discord #rules channel. Make sure to include links to the Discord on both the Rules page and front page.

Here's our `index.html` page from 2025:
```html
<div class="row">
    <div class="col-md-6 offset-md-3">
        <h1 class="text-center" style="padding-top: 8vh; ">
          <p><b>BYUCTF 2025</b></p>
        </h1>
        <img class="w-100 mx-auto d-block" style="max-width: 400px;padding: 20px;border-radius: 10px;" src="/files/a70aef0b9cb94f2e1bce8776a186de73/byuctf2025.png" />
        <div>
  <script src="https://cdn.logwork.com/widget/countdown.js"></script>
<a href="https://logwork.com/countdown-6uow" class="countdown-timer" data-timezone="America/Denver" data-textcolor="#000000" data-date="2025-05-17 20:00" data-background="#0047ba" data-digitscolor="#ffffff" data-unitscolor="#000000">BYUCTF 2025 ends in</a>
  </div>
      <br>
      	<h3 class="text-center">
          <p><b><a href="login">Login</a> or <a href="register">Register</a> to get started.</b><p>
      	</h3>
        <br>
        <h4 class="text-center">
          <p>Fri, 16 May 2025, 20:00 MDT — Sat, 17 May 2025, 20:00 MDT</p><br>
          <p>For issues or questions, <a href="https://discord.gg/Fe6896KEZk">join our Discord!</a></p>
        </h4>
    </div>
</div>
```

In 2025, when we created challenges, we did the following:
* All challenge types (except survey/sanity check) are **dynamic**
* **Initial Value** - 500
* **Decay Function** - Logarithmic
* **Decay** - 250
* **Minimum Value** - 50

We also put `Author: <authorname>` tags on each challenge to attribute challenge creation. I like putting flags in a case-**IN**sensitive unless otherwise necessary. Also remember to put "Max Attempts" for any challenges that could be brute forceable.

## Hosted Challenges Setup
All hosted challenges (like web or pwn) are deployed across a variety of VMs on the Proxmox instance. Up to 5 docker containers will be run on each VM using ports 5000-5004. Web challenges will be accessed through a reverse proxy that resolves the hostname into the corresponding "Internal URL" for the challenge.

### VM Setup
Each VM has been set up with the following Proxmox options:

* **Start at boot** - Enabled
* **ISO Image** - I just used Debian 12 but latest Ubuntu would also work
* **Disk size** - 50GB
* **CPU Cores** - 4
* **Memory** - 16384 MB

When installing the operating system:
* **IP Address** - this is statically set
* **Software selection** - no Debian desktop environment was selected but be sure to install SSH server

To set up the VM once installed:
* Do any user-specific setup you want (creating individual accounts, adding SSH key authentication, etc.)
* [Install Docker](https://docs.docker.com/engine/install/debian/)
    * Also run `sudo usermod -aG docker $USER` to allow your user to run docker commands without needing sudo
    * Ensure that the docker systemctl service is enabled so docker starts running automatically after a reboot
* Create a single SSH key for all VMs and add it to the Deploy Keys section of the GitHub repository
    * This allows the server to download the private repository into the VM for deploying challenges (and to easily retrieve updates)
    * Ensure this deploy key is given **read-only access**
* `git clone` the GitHub repository using SSH access
* Run the `docker compose up -d --build` command inside each challenge
* Run the solve script against each remote service to ensure the challenge still works as intended

### Challenge Spread
**VM - `Public-CTF-Crypto-1` (`xxx.xxx.xxx.xxx`)**
| Challenge Name | Internal URL | External URL |
|----------------|--------------|--------------|
| [Anaken21sec2](./crypto/anaken21sec2/) | `xxx.xxx.xxx.xxx:5000` | `anaken21sec2.chal.cyberjousting.com:1347` |
| [Choose Your RSA](./crypto/choose/) | `xxx.xxx.xxx.xxx:5001` | `choose.chal.cyberjousting.com:1348` |
| [Hash Based Crypto](./crypto/hash_based_crypto/) | `xxx.xxx.xxx.xxx:5002` | `hash.chal.cyberjousting.com:1351` |
| [Real Smooth](./crypto/real-smooth/) | `xxx.xxx.xxx.xxx:5003` | `smooth.chal.cyberjousting.com:1350` |

**VM - `Public-CTF-Pwn-1` (`xxx.xxx.xxx.xxx`)**
| Challenge Name | Internal URL | External URL |
|----------------|--------------|--------------|
| [Goat](./pwn/goat/) | `xxx.xxx.xxx.xxx:5000` | `goat.chal.cyberjousting.com:1349` |
| [Minecraft YouTuber](./pwn/minecraft_youtube/) | `xxx.xxx.xxx.xxx:5001` | `minecraft.chal.cyberjousting.com:1354` |
| [Game of Yap](./pwn/game-of-yap/) | `xxx.xxx.xxx.xxx:5002` | `yap.chal.cyberjousting.com:1355` |
| [MIPS](./pwn/mips/) | `xxx.xxx.xxx.xxx:5003` | `mips.chal.cyberjousting.com:1357` |
| [TCL](./pwn/tcl/) | `xxx.xxx.xxx.xxx:5004` | `tcl.chal.cyberjousting.com:1358` |

**VM - `Public-CTF-Web-1` (`xxx.xxx.xxx.xxx`)**
| Challenge Name | Internal URL | External URL |
|----------------|--------------|--------------|
| [Willy Wonka Web](./web/wonka/) | `xxx.xxx.xxx.xxx:5000` | `https://wonka.chal.cyberjousting.com` |
| [Cooking Flask](./web/cooking_flask/) | `xxx.xxx.xxx.xxx:5001` | `https://cooking.chal.cyberjousting.com` |
| [JWTF](./web/jwtf/) | `xxx.xxx.xxx.xxx:5002` | `https://jwtf.chal.cyberjousting.com` |
| [Wembsoncket](./web/wembsoncket/) | `xxx.xxx.xxx.xxx:5003` | `https://wembsoncket.chal.cyberjousting.com` |
| [Red This](./web/redthis/) | `xxx.xxx.xxx.xxx:5005` | `https://redthis.chal.cyberjousting.com` |

**VM - `Public-CTF-Misc-1` (`xxx.xxx.xxx.xxx`)**
| Challenge Name | Internal URL | External URL |
|----------------|--------------|--------------|
| [Enabled](./misc/enabled/) | `xxx.xxx.xxx.xxx:5000` | `enabled.chal.cyberjousting.com:1352` |
| [Hash Psycho](./misc/hash_psycho/) | `xxx.xxx.xxx.xxx:5001` | `psycho.chal.cyberjousting.com:1353` |

## Design Decisions
### Availability
It's important to ensure the challenges and CTFd server are up at all times, ideally without any manual intervention. To accommodate this, I've added a number of checks in place:
* In Proxmox, there's a setting (not enabled by default) to "Start at boot" (probably something similar in any hypervisor). This ensures that if the hardware or hypervisor reboots, the virtual machine is automatically started once it comes back online.
* In both VMs, the Docker `systemctl` service should be enabled so Docker starts whenever the virtual machine is rebooted.
* All `docker-compose.yml` files should have `restart: always` set for each container so that if the container is stopped or crashes for some reason, it automatically spins back up
* In some containers where I feel there's a likelihood of the container crashing (from user input) or where RCE is obtainable and an important process can be killed, I'll add important processes in a bash while true loop so it automatically comes back online

### Docker Compose
There's a couple of ways to spin up Docker containers for something like this, but I intentionally have created `docker-compose.yml` files for each challenge. First, it's really easy to spin up since you just need to run `docker compose up -d --build`, whereas `docker build` and `docker run` commands with all the necessary options would be much longer. Secondly, `docker compose` automatically creates a unique Docker network for each challenge. This is important because some challenges rely on the fact that one of the containers ISN'T publicly accessible, requiring some work around or vulnerability. Putting all containers (regardless of the challenge) on the same Docker network allows fully unrestricted access between containers, meaning a different challenge that allows RCE could be used as a jump box to reach a "private" container for another challenge, or an unexposed port on a container for another challenge.

Most hosted challenges will include the source code for the challenge, the `Dockerfile`, and the `docker-compose.yml` file so that the participants can host the challenge locally for their own testing/debugging purposes. I have carefully and intentionally created ZIP files for these challenges that included all files without sensitive information (flags, writeups, solve scripts, or other relevant secrets). In some cases, secrets are found in a `docker-compose.yml` file or somewhere, and I'll just create an alternate version of the file with the secret redacted and give them that one.

### Dockerfiles
Unless necessary, all Dockerfiles pull from images with the `latest` tag to ensure we're not stuck on old (and possibly vulnerable) containers for our challenges. Sometimes specific versions may break a challenge or modify the intended solve, in which case a specific tag is tied to the base image (like in PHP). Additionally, most containers have lines like `apt update` and `apt upgrade` to ensure all dependencies are upgraded when the container is spun up.

A notable exception is that some pwn challenges are tied to a specific hash of a container, like `ubuntu:24.04@sha256:278628f08d4979fb9af9ead44277dbc9c92c2465922310916ad0c46ec9999295`. This is because the version of glibc may change for containers, and may be updated simply by running `apt upgrade -y`. For this reason, a specific release of the container is used with a known glibc executable, and `apt upgrade -y` is NEVER run in these containers. This ensures that the solve scripts we've created always work, that the intended solution doesn't change with glibc functionality, and that participants can reliably extract the proper version of glibc to use in exploit creation.

### Resource Limits, Process Isolation, and Unprivileged Code Execution
Where at all possible, the users in Docker containers that run challenge files (like webservers or pwn binaries) are set to an unprivileged user. This is just good practice, but ensures that if a participant gains remote code execution on a container (whether that's intended or not), they can't modify the environment for others and ruin their experience or prevent solves.

Almost all directories are set to be non-writable by this user, especially directories including challenge files. The main exceptions are some `uploads/` folders in web challenges that require users to be able to upload files to the server. Other limitations are put in place to ensure a shared, writable folder doesn't allow one participant to cheat off of another or prevent another participant from solving the challenge (like random file names). These upload folders are also often cleared on a regular basis, like 6 hours, to prevent buildup. Another common exception is `tmp` folders like `/tmp` or `/dev/shm` - unprivileged users can write files here that won't be cleared, but since these don't affect the challenge itself I just leave them.

Challenges that require a new process to be spun up each time a user connects over a TCP port are facilitated through [redpwn's jail container](https://github.com/redpwn/jail). The setup is fairly simple, options are easily configurable, and it provides a lot of good isolation and limits to stop participants from DoSing servers. Note that using this container is preferred over `xinetd`, `ynetd`, or `socat`. While these containers must be privileged, they are still substantially more secure than the alternatives. The default jail options I use are `JAIL_TIME=60 JAIL_MEM=20M JAIL_CONNS_PER_IP=10`. The GitHub repo has good documentation on how to configure the jail.

### Pre-Compiled Executables
Unless specifically specified, do not recompile executables unless changes need to be made to the challenge (keep the one already provided). All compiled executables should have a command in the README or Makefile for creating them in case this needs to happen, but recompiling source code can often lead to solve changes or even completely breaking a challenge (like adding additional binexp mitigations).

### Solve Scripts
*Where at all possible*, automatic solve scripts should be created for problems. One, this proves (without a doubt) that the challenge is solvable. Two, this forces the challenge author to actually go through the solve process (which should be a given but laziness is real). Third, if a participant reports that a challenge is likely broken, you can use the solve script as a source of truth to see if the challenge is still solvable as intended.

Solve scripts are very difficult in reverse engineering problems, however, so for those a detailed writeup should be included instead to prove the author has gone through the solving process.

In challenges involving creating accounts/files, ensure the usernames/passwords/filenames are unguessable or randomly generated so participants can't guess them and get the flag without the work.

### Executable Buffering
Every single challenge that requires compiling and hosting C code (aka all of pwn) should have this function included at the top:
```c
__attribute__((constructor)) void flush_buf() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}
```

This disables buffering across the board, and is run before `main()` is ever even reached. Oftentimes, buffering can cause data to be sent to stdout without it actually reaching the participant connecting from their computer. This ensures that never happens, and all output is flushed immediately.