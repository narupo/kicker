# -*- coding: utf-8 -*-
import os, sys, time, argparse, urllib3

def main():
    parser = argparse.ArgumentParser(description='export')
    parser.add_argument('--daemon', dest='become_daemon', action='store_true', help='do become daemon')
    parser.set_defaults(become_daemon=False)
    parser.add_argument('--hours', dest='hours', action='store', type=int)
    parser.set_defaults(hours=None)
    parser.add_argument('--minutes', dest='minutes', action='store', type=int)
    parser.set_defaults(minutes=None)
    parser.add_argument('--seconds', dest='seconds', action='store', type=int)
    parser.set_defaults(seconds=None)
    parser.add_argument('--url', dest='url', action='store', type=str)
    parser.set_defaults(url='http://localhost')
    ns = parser.parse_args(sys.argv[1:])

    if ns.become_daemon:
        become_daemon()

    secs = get_seconds(ns)
    http = urllib3.PoolManager()

    while True:
        print('GET', ns.url)
        http.request('GET', ns.url)
        print_info(ns)
        time.sleep(secs)

def print_info(ns):
    if ns.hours and ns.minutes and ns.seconds:
        print('sleep {0} hours {1} minutes {2} seconds...'.format(ns.hours, ns.minutes, ns.seconds))
    elif ns.hours and ns.seconds:
        print('sleep {0} hours {1} seconds...'.format(ns.hours, ns.seconds))
    elif ns.minutes and ns.seconds:
        print('sleep {0} minutes {1} seconds...'.format(ns.minutes, ns.seconds))
    elif ns.minutes:
        print('sleep {0} minutes...'.format(ns.minutes))
    else:
        print('sleep {0} seconds...'.format(secs))        
            
def get_seconds(ns):
    secs = 0

    if ns.hours:
        secs += 60 * 60 * ns.hours

    if ns.minutes:
        secs += 60 * ns.minutes

    if ns.seconds:
        secs += ns.seconds

    if secs <= 0:
        secs = 10

    return secs

def become_daemon():
    pid = os.fork()
    if pid == -1:
        raise Exception('failed to fork 1')
    elif pid == 0:
        pass
    else: 
        os._exit(0)

    if os.setsid() == -1:
        raise Exception('failed to setsid')

    pid = os.fork()
    if pid == -1: 
        raise Exception('failed to fork 2')
    elif pid == 0: 
        pass
    else: 
        os._exit(0)

    os.umask(0)

    os.chdir('/')

    STDIN_FILENO = sys.stdin.fileno()
    STDOUT_FILENO = sys.stdout.fileno()
    STDERR_FILENO = sys.stderr.fileno()
    os.close(STDIN_FILENO)

    fd = os.open('/dev/null', os.O_RDWR)
    if fd != STDIN_FILENO: 
        raise Exception('failed to open /dev/null')

    os.dup2(STDIN_FILENO, STDOUT_FILENO)
    os.dup2(STDIN_FILENO, STDERR_FILENO) 

if __name__ == '__main__':
    main()
