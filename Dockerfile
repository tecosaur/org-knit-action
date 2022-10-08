FROM ubuntu:21.04

ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN echo "Install Emacs" &&\
  # echo "\e[1A\e[K\033[1;34mInstall Emacs\033[0m" &&\
  # echo "\033[0;34mAdd Emacs PPA.\033[0m" &&\
  apt-get update &&\
  apt-get install -y apt-utils software-properties-common sudo &&\
  # add-apt-repository -y ppa:kelleyk/emacs &&\
  # echo "\033[0;34mUpdate.\033[0m" &&\
  # apt-get update &&\
  echo "\033[0;34mInstalling Emacs\033[0m" &&\
  apt-get install --no-install-recommends -y emacs-nox

RUN echo "Install utilities" &&\
  echo "\e[1A\e[K\033[1;34mInstall utilities\033[0m" &&\
  apt-get install --no-install-recommends -y \
  gcc \
  sqlite \
  sqlite3 \
  ripgrep \
  xclip \
  curl \
  wget \
  ncurses-term \
  jq \
  ssh-client \
  git git-lfs

RUN echo "Install TeX Live" &&\
  echo "\e[1A\e[K\033[1;34mInstall TeX Live\033[0m" &&\
## Modified version of https://github.com/thomasWeise/docker-texlive-full
# prevent doc and man pages from being installed
# the idea is based on https://askubuntu.com/questions/129566
  echo "\033[0;34mPreventing doc and man pages from being installed.\033[0m" &&\
  printf 'path-exclude /usr/share/doc/*\npath-include /usr/share/doc/*/copyright\npath-exclude /usr/share/man/*\npath-exclude /usr/share/groff/*\npath-exclude /usr/share/info/*\npath-exclude /usr/share/lintian/*\npath-exclude /usr/share/linda/*\npath-exclude=/usr/share/locale/*' > /etc/dpkg/dpkg.cfg.d/01_nodoc &&\
# remove doc files and man pages already installed
  rm -rf /usr/share/groff/* /usr/share/info/* &&\
  rm -rf /usr/share/lintian/* /usr/share/linda/* /var/cache/man/* &&\
  rm -rf /usr/share/man &&\
  mkdir -p /usr/share/man &&\
  find /usr/share/doc -depth -type f ! -name copyright -delete &&\
  find /usr/share/doc -type f -name "*.pdf" -delete &&\
  find /usr/share/doc -type f -name "*.gz" -delete &&\
  find /usr/share/doc -type f -name "*.tex" -delete &&\
  (find /usr/share/doc -type d -empty -delete || true) &&\
  mkdir -p /usr/share/doc &&\
  mkdir -p /usr/share/info &&\
  echo "\033[0;34mInstalling TeX Live packages.\033[0m" &&\
# install TeX Live and ghostscript as well as other tools
  git clone https://github.com/tecosaur/BMC.git /usr/share/texmf/tex/latex/bmc &&\
  apt-get install -y texlive-base texlive-latex-recommended texlive-fonts-extra latexmk &&\
# delete Tex Live sources and other potentially useless stuff
  echo "\033[0;34mDelete TeX Live sources and other useless stuff.\033[0m" &&\
  (rm -rf /usr/share/texmf/source || true) &&\
  (rm -rf /usr/share/texlive/texmf-dist/source || true) &&\
  find /usr/share/texlive -type f -name "readme*.*" -delete &&\
  find /usr/share/texlive -type f -name "README*.*" -delete &&\
  (rm -rf /usr/share/texlive/release-texlive.txt || true) &&\
  (rm -rf /usr/share/texlive/doc.html || true) &&\
  (rm -rf /usr/share/texlive/index.html || true) &&\
# clean up all temporary files
  echo "\033[0;34mClean up all temporary files.\033[0m" &&\
  apt-get clean -y &&\
  rm -rf /var/lib/apt/lists/* &&\
  rm -f /etc/ssh/ssh_host_* &&\
# delete man pages and documentation
  echo "\033[0;34mDelete man pages and documentation.\033[0m" &&\
  rm -rf /usr/share/man &&\
  mkdir -p /usr/share/man &&\
  find /usr/share/doc -depth -type f ! -name copyright -delete &&\
  find /usr/share/doc -type f -name "*.pdf" -delete &&\
  find /usr/share/doc -type f -name "*.gz" -delete &&\
  find /usr/share/doc -type f -name "*.tex" -delete &&\
  (find /usr/share/doc -type d -empty -delete || true) &&\
  mkdir -p /usr/share/doc &&\
  rm -rf /var/cache/apt/archives &&\
  mkdir -p /var/cache/apt/archives &&\
  rm -rf /tmp/* /var/tmp/* &&\
  (find /usr/share/ -type f -empty -delete || true) &&\
  (find /usr/share/ -type d -empty -delete || true) &&\
  mkdir -p /usr/share/texmf/source &&\
  mkdir -p /usr/share/texlive/texmf-dist/source

RUN echo "Don't check github's SSH key" &&\
  echo "\e[1A\e[K\033[1;36mDon't check github's SSH key\033[0m" &&\
  printf "Host github.com\n  StrictHostKeyChecking no\n" >> /etc/ssh/ssh_config

RUN echo "Add non-root user" &&\
  echo "\e[1A\e[K\033[1;36mAdd non-root user\033[0m" &&\
  groupadd runner &&\
  useradd -m -g runner -G sudo -u 1000 -c "Docker image runner" runner &&\
  echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers &&\
  echo "Add command to run command with user 'runner'" &&\
  printf '#!/usr/bin/env sh\nsudo -i -u runner bash <<EOF\n$@\nEOF\n' > /bin/runner &&\
  chmod +x /bin/runner

COPY setup/doom-all-packages.py /tmp/doom-all-packages.py

RUN echo "Install Doom" &&\
  echo "\e[1A\e[K\033[1;34mInstall Doom\033[0m" &&\
  mkdir -p /home/runner/.emacs.d &&\
  cd /home/runner/.emacs.d &&\
  git init &&\
  git remote add origin https://github.com/hlissner/doom-emacs.git &&\
  git fetch --depth 1 origin 9f22a0a2a5191cf57184846281164f478df4b7ac &&\
  git checkout FETCH_HEAD &&\
  chown -R runner:runner /home/runner/.emacs.d &&\
  sudo -u runner mkdir -p /home/runner/.config/doom &&\
  sudo -u runner /home/runner/.emacs.d/bin/doom install --no-env --no-install --no-fonts &&\
  echo "\033[0;34mAdding all packages in modules to packages.el\033[0;90m" &&\
  sudo -u runner /tmp/doom-all-packages.py > /home/runner/.config/doom/packages.el &&\
  cat /home/runner/.config/doom/packages.el &&\
  echo "\033[0m" &&\
  sudo -u runner /home/runner/.emacs.d/bin/doom sync &&\
  rm -r /home/runner/.config/doom &&\
  mv /home/runner/.emacs.d /home/runner/.emacs.d.doom

USER runner

COPY knit/ /opt/org-knit/

ENTRYPOINT ["sudo", "-u", "runner", "-E", "-H", "/opt/org-knit/main.py"]
