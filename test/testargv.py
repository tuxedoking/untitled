import sys


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) > 1 and sys.argv[1] == 'schedule_task':
        print('haha')
