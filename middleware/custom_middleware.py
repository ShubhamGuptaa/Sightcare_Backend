"""
admin restrict middleware
"""
import socket
import re
from django.http import HttpResponseForbidden
from adminrestrict.models import AllowedIP



"""
MiddlewareMixins is only available (and useful) in Django 1.10 and newer versions
"""
try:
    from django.utils.deprecation import MiddlewareMixin
    parent_class = MiddlewareMixin
except ImportError as e:
    parent_class = object

def is_valid_ip(ip_address):
    """
    check validity of an IP address
    """
    valid = True
    try:
        socket.inet_aton(ip_address.strip())
    except:
        valid = False
    return valid


def get_ip_address_from_request(request):
    """
    Makes the best attempt to get the client IP or return the loopback
    """
    PRIVATE_IPS_PREFIX = ('10.','172.','192.','127.')
    ip_address = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR','')
    if x_forwarded_for and ',' not in x_forwarded_for:
        if not x_forwarded_for.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_forwarded_for):
            ip_address = x_forwarded_for.strip()
            print("Ip Address From x_forwarder: ",ip_address)
    else:
        ips = [ip.strip() for ip in x_forwarded_for.split(',')]
        for ip in ips:
            if ip.startswith(PRIVATE_IPS_PREFIX):
                continue
            elif not is_valid_ip(ip):
                continue
            else:
                ip_address = ip
                break
    if not ip_address:
        x_real_ip = request.META.get('HTTP_X_REAL_IP','')
        print("Ip Address From X_real_IP: ",x_real_ip)
        if x_real_ip:
            if not x_real_ip.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_real_ip):
                ip_address = x_real_ip.strip()
                print("Ip Address From not x_real_ip: ",ip_address)
    if not ip_address:
        remote_addr = request.META.get('REMOTE_ADDR','')
        print("Remote Address Ip: ",remote_addr)
        if remote_addr:
            if not remote_addr.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(remote_addr):
                ip_address = remote_addr.strip()
                print("Not Remote address: ",ip_address)
            if remote_addr.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(remote_addr):
                print("Remote address: ",ip_address)
                ip_address = remote_addr.strip()
    if not ip_address:
        ip_address = '127.0.0.1'
    print("Final Real IP: ",ip_address)
    return ip_address




class CustomMiddleWare(parent_class):
    # def __init__(self,get_response):
    #     self.get_response = get_response

    # def __call__(self, request):
    #     response = self.get_response(request)
    #     print("Source of request is: ", request.META['HTTP_USER_AGENT'])
    #     return response
    
    """
    A middleware that restricts login attempt to admin pages 
    to restricted IP addresses only. Everyone else get 403.
    """
    def process_request(self, request):
        """
        Check if the request is made from an allowed IP
        """
        # Section adjusted to restrict login to ?edit
        # (sing cms-toolbar-login) into DjangoCMS login.
        restricted_request_url = request.path.startswith('/restricted-admin-panel')
        if restricted_request_url and request.method == 'POST':
            # AllowedIP table empty means access is always granted
            if AllowedIP.objects.count() > 0:
                # If there are wildcard IPs access is always granted
                if AllowedIP.objects.filter(ip_address="*").count() == 0:
                    request_ip = get_ip_address_from_request(request)
                    print(request_ip)
                    # If the request_ip is in the AllowedIP the access is granted
                    if AllowedIP.objects.filter(ip_address= request_ip).count() == 0:
                        """
                        We check regular expressions defining ranges of Ips.
                        If any range contains the request_ip
                        the access is granted.
                        """
                        for regex_ip_range in AllowedIP.objects.filter(ip_address__endswith="*"):
                            if re.match(regex_ip_range.ip_address.replace("*",".*")):
                                return None
                        return HttpResponseForbidden("Admin access denied!")