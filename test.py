ord_no = "ORD0000111"
ord_no_int = int(ord_no[3:10])
new_ord_no_int = ord_no_int + 1
new_ord_no = "ORD" + str(new_ord_no_int).zfill(7)
print(new_ord_no)