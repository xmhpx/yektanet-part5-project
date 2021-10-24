from celery import shared_task
import time


@shared_task
def celery_task(counter):
    email = "mhppaydar@gmail.com"
    time.sleep(30)
    return '{} Done!'.format(counter)


from celery import task


# We can have either registered task
@task(name='summary')
def send_import_summary():
    pass
    # Magic happens here ...


# or

@shared_task
def send_notification():
    print('Here I\'m')
    # Another trick
