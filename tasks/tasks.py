import mongoengine
import ping3
from celery import shared_task
from devices.models import Device
from stats.models import Latency
from stats.models.history import History


@shared_task
def ping_device_test(device_ip):
    try:
        latency = ping3.ping(device_ip)
        if not latency:
            status = 'error'
        else:
            status = 'success'
    except ping3.errors.PingError:
        status = 'error'
        latency = None


    try:
        latency_data = Latency.objects.get(host=device_ip)
        print(f"PING Test IPV4 {device_ip}: ", latency, ' ', status)
        latency_data.latency = latency
        latency_data.status = status
        latency_data.save()
        print("Host status updated successfully")

    except mongoengine.DoesNotExist:
        print(f"PING Test IPV4 {device_ip}: ", latency, ' ', status)
        latency_data = Latency(host=device_ip, latency=latency, status=status)
        latency_data.save()
        print("Host status saved successfully")


    latency_register = History(host=device_ip, latency=latency, status=status)
    latency_register.save()
    print("Record was saved in history")

@shared_task
def device_connection_test():
    print("Starting process")
    device_query_set = Device.objects.filter(active=True)

    for device in device_query_set:
        print('Device', device.code)
        ping_device_test.apply_async(args=[device.ip_address], countdown=10)

