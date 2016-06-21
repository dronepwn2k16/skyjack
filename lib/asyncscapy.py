#!/usr/bin/env python
from threading import Thread, Event, Lock
from scapy.all import sniff

class Promise():

    def __init__(self):
        self._event = Event()
        self._result = None

    def complete(self, value):
        self._result = value
        self._event.set()

    def is_completed(self):
        return self._event.is_set()

    def wait(self):
        self._event.wait()
        return self._result

    def result(self):
        if not self.is_completed():
            raise RuntimeError('promise is not complete yet')
        return self._result


_handlers = {}
_handler_lock = Lock()
_sniffer = None
_iface = None

# set to true to print debugging messages
DEBUG = False

def print_d(msg):
    if DEBUG:
        print msg

# register a new packet handler, returns a promise
def register_handler(pkt_handler):
    global _handler_lock, _handlers
    _handler_lock.acquire()
    try:
        prom = Promise()
        _handlers[pkt_handler] = prom
        print_d("handler %s registered" % pkt_handler)

        # start sniffing
        start_sniffing()
        return prom
    finally:
        _handler_lock.release()

def register_handler_sync(pkt_handler):
    prom = register_handler(pkt_handler)
    return prom.wait()

# remove a already registered handler, returns True if removed, False if not found
def remove_handler(pkt_handler):
    global _handler_lock, _handlers
    _handler_lock.acquire()
    try:
        del _handlers[pkt_handler]
        print_d("handler %s removed" % pkt_handler)
        return True
    except KeyError:
        print_d("handler %s could not be removed" % pkt_handler)
        return False
    finally:
        _handler_lock.release()

def _handle_packet(pkt):
    global _handler_lock, _handlers

    _handler_lock.acquire()

    try:

        to_remove = []
        # invoke all handlers
        for handler in _handlers:
            res = handler(pkt)
            # if handler done, resolve promise and mark for removal
            if res is not None:
                prom = _handlers[handler]
                prom.complete(res)
                to_remove.append(handler)

        # remove completed handlers
        for handler in to_remove:
            del _handlers[handler]

        #  return True if no more handlers registered -> stop sniffing
        if len(_handlers) == 0:
            return True
        else:
            return False
    finally:
        _handler_lock.release()

def set_interface(interface):
    global _iface
    _iface = interface

def _handle_sniffing():
    global _iface, _sniffer
    print_d("sniffer started")
    if _iface is None:
        raise RuntimeError("no monitoring interface specified yet. call set_interface() first")
    sniff(iface=_iface, store=0, stop_filter=_handle_packet)
    _sniffer = None
    print_d("sniffer stopped")


# wait until sniffer is done
def join_sniffer():
    if _sniffer is None:
        return
    _sniffer.join()

def start_sniffing():
    global _sniffer
    if _sniffer is not None:
        return

    _sniffer = Thread(target=_handle_sniffing)
    _sniffer.daemon = True
    _sniffer.start()

