import git
import subprocess

def pull(path_to_repo = '.'):
    g = git.cmd.Git(path_to_repo)
    result = g.pull()
    if result != 'Already up-to-date.':
        restart()

def restart(command = 'server.py'):
    process = subprocess.Popen(['pkill', command])
    process = subprocess.Popen(['bash', '/var/www/nbai_live/starterup'])

if __name__ == '__main__':
    pull()
