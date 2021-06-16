#!/usr/bin/env python

from subprocess import Popen
from uuid import uuid4


class ConcurrentTask:

    def __init__(self, cmd, name=None):
        self.name = name or '{} {}'.format(str(uuid4())[:8], cmd[:12])
        self._cmd = cmd

    def __str__(self):
        return ' "{}" {}'.format(self.name, self._cmd)


class Concurrent:

    """
    Based on bash-concurrent
    https://github.com/themattrix/bash-concurrent
    """

    def __init__(self, delimiter=None, dry_run=False, log_dir=None,
                 compact=False, limit=None):
        self._cmd = ''
        self._delimiter = delimiter or '-'

        self._dry_run = dry_run
        self._log_dir = log_dir
        self._limit = limit
        self._compact = compact

        if dry_run is True:
            self._cmd += 'CONCURRENT_DRY_RUN=1 '
        if isinstance(log_dir, str):
            self._cmd += 'CONCURRENT_LOG_DIR={} '.format(self._log_dir)
        if isinstance(limit, int):
            self._cmd += 'CONCURRENT_LIMIT={} '.format(self._limit)
        if compact is True:
            self._cmd += 'CONCURRENT_COMPACT=1 '

        self._cmd += 'concurrent'

    def __str__(self):
        return self._cmd

    def start(self):
        process = Popen(['/bin/bash', '-i', '-c', self._cmd])
        process.communicate()

    def run(self, task, name=None):
        if isinstance(task, str):
            task = ConcurrentTask(task, name)
        self._cmd += ' {}{}'.format(self._delimiter, str(task))
        return self

    def and_then(self):
        self._cmd += ' --and-then'
        return self

    def require(self, task):
        if isinstance(task, ConcurrentTask):
            task = task.name
        self._cmd += ' --require "{}"'.format(task)
        return self

    def require_all(self):
        self._cmd += ' --require-all'
        return self

    def before(self, task):
        if isinstance(task, ConcurrentTask):
            task = task.name
        self._cmd += ' --before "{}"'.format(task)
        return self

    def before_all(self):
        self._cmd += ' --before-all'
        return self

    def sequential(self):
        self._cmd += ' --sequential'


def main():
    concurrent = Concurrent()

    first = ConcurrentTask('sleep 10')
    second = ConcurrentTask('sleep 3')
    third = ConcurrentTask('sleep 5')
    fourth = ConcurrentTask('sleep 2')

    concurrent.run(first)\
        .run(second)\
        .and_then()\
        .run(third)\
        .and_then()\
        .run(fourth)\

    print(concurrent)

    concurrent.start()


if __name__ == "__main__":
    main()
