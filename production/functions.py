from .models import *

def increment_delivery_number():
    last_del_no = Delivery.objects.all().order_by("number").last()

    if last_del_no == None:
        return "DEL0000001"
    else:
        del_no = last_del_no.number
        del_no_int = int(del_no[3:10])
        new_del_no_int = del_no_int + 1
        return "DEL" + str(new_del_no_int).zfill(7)


def increment_inward_order_number():
    last_inw_no = FabricInward.objects.all().order_by("number").last()

    if last_inw_no == None:
        return "INW0000001"
    else:
        inw_no = last_inw_no.number
        inw_no_int = int(inw_no[3:10])
        new_inw_no_int = inw_no_int + 1            
        return "INW" + str(new_inw_no_int).zfill(7)    

def increment_order_number():
    last_ord_no = Order.objects.all().order_by("number").last()
    
    if last_ord_no == None:
        return "ORD0000001"
    else:
        ord_no = last_ord_no.number
        ord_no_int = int(ord_no[3:10])
        new_ord_no_int = ord_no_int + 1            
        return "ORD" + str(new_ord_no_int).zfill(7)            