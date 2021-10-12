from django.core.paginator import Paginator

def get_paginator(obj_list, show_items, page_number):
    paginator = Paginator(obj_list, show_items) # Show 25 contacts per page.
    page_number = int(page_number)
    page_obj = paginator.get_page(page_number)
    prv = page_obj.previous_page_number
    next_page = page_obj.next_page_number
    if page_number <= 1:
        prv = 1
    if page_number >= paginator.num_pages:
        next_page = paginator.num_pages
    
    return {'page_obj': page_obj, 'prv_page': prv, 'next_page': next_page}