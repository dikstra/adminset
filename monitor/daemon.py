#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, time, atexit
import signal
import psutil


class Daemon:
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            print("pid is %s"%(pid))
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

            # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()

        with open(self.stdin,'rb', 0) as f:
            os.dup2(f.fileno(),sys.stdin.fileno())
        with open(self.stdout,'ab',0) as f:
            os.dup2(f.fileno(),sys.stdout.fileno())
        with open(self.stderr,'ab',0) as f:
            os.dup2(f.fileno(),sys.stderr.fileno())


        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        with open(self.pidfile,'w+') as f:
            f.write("%s\n" % pid)
        # file(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            with open(self.pidfile,'r') as f:
            # pf = file(self.pidfile, 'r')f
                pid = int(f.read().strip())
            # pf.close()
            print("pid probe" + str(pid))
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as f:
            # pf = file(self.pidfile, 'r')
                pid = int(f.read().strip())
            # pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            nbocc = 0
            while 1:
                nbocc = nbocc + 1
                print("try to kill process: " + str(pid))
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
                if nbocc % 5 == 0:
                    os.kill(pid, signal.SIGHUP)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err))
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def status(self):
        """
         give the current status of  the process
        """
        try:
            with open(self.pidfile,'r') as f:
            # pf = file(self.pidfile, 'r')
                pid = int(f.read().strip())
            # pf.close()
        except IOError:
            sys.exit(2)
            pid = None
        except SystemExit:
            sys.exit()
            pid = None
        if psutil.pid_exists(pid):
            print("pid :", pid)
            sys.exit(0)
        else:
            print("no such process running")
            sys.exit(2)

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """
        pass