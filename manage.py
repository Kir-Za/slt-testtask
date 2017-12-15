# #!/usr/bin/env python
# import os
# from app import create_app

if __name__ == '__main__':
    import config
    from app.database import get_session
    t1 = get_session()

    #  from app.models import Server, Rack
    #  from datetime import datetime
    #  rack1 = Rack(date_creation=datetime.now(), date_last_changes=datetime.now(), operator='interZ', owner='selectel', address='Spb', volume=20)
    #  serv1 = Server(date_creation=datetime.now(), date_last_changes=datetime.now(), server_ip=123, server_ram=1024, server_core='amd', optical_port=True, status="unpaid")
    #  serv2 = Server(date_creation=datetime.now(), date_last_changes=datetime.now(), server_ip=333, server_ram=128, server_core='intel', optical_port=False, status="unpaid")
