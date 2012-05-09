#!/usr/bin/env python3

"""Archlinux Post Install Patch"""

import os, re, subprocess

# Constants definition

### PACKAGES ###
PACKAGES = ["screen", "sudo", "vim", "bash-completion", "tree", "ruby", "figlet", "cowsay", "metalog", "ncdu", "net-tools", "ntp", "sqlite"]

### MD5 to SHA512 ###
PAMDPASSD = "/etc/pam.d/passwd"
LOGINDEFS = "/etc/login.defs"

### Nicer BASH Prompt ###
BASHBASHRC = "/etc/bash.bashrc"
BETTER_PROMPT = """# Gives a nice colored PS1 prompt with root/user

if [[ ${EUID} == 0 ]] ; then
    PS1='\[\\\\033[01;31m\]\h\[\\\\033[01;34m\] \W \$\[\\\\033[00m\] '
else
    PS1='\[\\\\033[01;32m\]\\u@\h\[\\\\033[01;34m\] \w \$\[\\\\033[00m\] '
fi

# Aliases to get color output + ll shortcut
alias ls='ls --color=auto'
alias grep='grep --colour=auto'
alias ll='ls -la'
"""

### SSH Visual Host Key ###

SSHCONF = "/etc/ssh/ssh_config"
VISUALON = "VisualHostKey yes"

### VIM Visual Conf ###

VIMGLOBALCONF = "/etc/vimrc"
VISUALNICE = "syntax on\nset number\nset expandtab\nset tabstop=4"

### Screen Visual & Conf ###

SCREENCONF = "/etc/screenrc"
SCREENVISUAL = """vbell off
startup_message off
caption always "%H %?%{+b kw}%-Lw%?%{yK}%n*%f %t%?(%u)%?%?%{wk}%+Lw%? %{gk}%=%c %{yk}%D %d %M %Y"
termcapinfo xterm-256color|xterm-color|xterm|xterms|xs|rxvt ti@:te@
"""

# Function definition

def test_root():
    """Tests if this script is called by root"""
    if os.getuid() != 0:
        print ("You have to be root run the post install patch")
        exit(-1)

def install_packages():
   """Install usefull packages"""
   installed = []
   toinstall = []
   for package in PACKAGES:
      if subprocess.call(["pacman", "-Q", package, "&> /dev/null"]) == 0:
         installed.append(package)
      else:
         toinstall.append(package)
   print("Installing the following packages : "+" ".join(toinstall))
   subprocess.call(["pacman", "-S", " ".join(toinstall)])

def update_md5_to_sha512():
    """Changes md5 to sha512 for hashing"""
    # Change occurences of md5 to sha512 in file PAMDPASSD
    with open(PAMDPASSD) as inf: data = inf.read()
    with open(PAMDPASSD, "w") as outf:
        outf.write( re.sub("md5", "sha512", data) )
    # Add the encrpyt method sha 512 to the LOGINDEFS file
    with open(LOGINDEFS, "a") as appf:
        appf.write("ENCRYPT_METHOD sha512")

def nicer_prompt():
    """Nicer Prompt"""
    with open(BASHBASHRC) as inf: data = inf.read()
    with open(BASHBASHRC, "w") as outf:
        outf.write( re.sub("PS1='.*'", BETTER_PROMPT, data))

def visual_hostkey():
    """Enables VisualHostKey in SSH"""
    with open(SSHCONF) as inf: data = inf.read()
    with open(SSHCONF, "w") as outf:
        outf.write(re.sub("#   VisualHostKey no", VISUALON, data))

def pretty_vim():
   """Enables Various Visual Options in VIM"""
   with open(VIMGLOBALCONF, "a") as outf:
      outf.write(VISUALNICE) 

def better_screen():
   """Nice Screen Config and Scrollback"""
   with open(SCREENCONF, "a") as outf:
      outf.write(SCREENVISUAL)
   
def main():
   """main"""
   # Exec
   test_root()

   print("=== Archlinux Post Install Patch ===")
   print("INIT. Install Useful packages")
   install_packages()
   print("1. Security Correction md5 -> sha512 hash method")
   update_md5_to_sha512()
   print("2. Nicer shell prompt and useful aliases (system wide)")
   nicer_prompt()
   print("3. Enables Visual Host Key Feature")
   visual_hostkey()
   print("4. Enables Visual Options in VIM")
   pretty_vim()
   print("4. Screen Nice Term and Scrollback")
   better_screen()

if __name__ == "__main__":
   main()