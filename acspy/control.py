# -*- coding: utf-8 -*-
"""
This module contains an [incomplete] object for communicating with an ACS controller.

"""
#from __future__ import division, print_function
from acspy import acsc


class ACSController(object):
    def __init__(self, contype="simulator", n_axes=8, address="10.0.0.100", port=701, serialport=""):
        """
        Initialization function of ACSController class
        :param string contype: connection type, can be simulator, ethernet, or serial
        :param int n_axes: number of axes to be accessible by controller
        :param string address: ip address for TCP/IP connections
        :param int port: port number for TCP/IP connection
        :param string serialport: serial port for serial connection
        """
        self.contype = contype
        self.axes = []
        if self.contype == "simulator":
            pass
            #TODO update to recognize deprecation of opencommdirect function
            #self.hc = acsc.openCommDirect()
        elif self.contype == "ethernet":
            self.hc = acsc.openCommEthernetTCP(address=address, port=port)
        # else
        #     self.hc = acsc.openCommSerial()
        # TODO add serial connectivity
        for n in range(n_axes):
            self.axes.append(Axis(self, n))

    def enable_all(self, wait=acsc.SYNCHRONOUS):
        """Enables all axes."""
        for a in self.axes:
            a.enable()

    def disable_all(self, wait=acsc.SYNCHRONOUS):
        """Disables all axes."""
        for a in self.axes:
            a.disable()
        
    def disconnect(self):
        """
        Close communication channel with controller
        :return: None
        """
        acsc.closeComm(self.hc)
        

class Axis(object):
    def __init__(self, controller, axisno, name=None):
        if isinstance(controller, ACSController):
            self.controller = controller
        else:
            raise TypeError("Controller is not a valid Controller object")
        self.axisno = axisno
        if name:
            controller.axisdefs[name] = axisno
        
    def enable(self, wait=acsc.SYNCHRONOUS):
        return acsc.enable(self.controller.hc, self.axisno, wait)

    def disable(self, wait=acsc.SYNCHRONOUS):
         return acsc.disable(self.controller.hc, self.axisno, wait)
        
    def ptp(self, target, coordinates="absolute", wait=acsc.SYNCHRONOUS):
        """Performs a point to point move in either relative or absolute
        (default) coordinates."""
        if coordinates == "relative":
            flags = acsc.AMF_RELATIVE
        else:
            flags = None
        return acsc.toPoint(self.controller.hc, flags, self.axisno, target, wait)
        
    def ptpr(self, distance, wait=acsc.SYNCHRONOUS):
        """Performance a point to point move in relative coordinates."""
        self.ptp(distance, coordinates="relative", wait=wait)
        
    @property
    def axis_state(self):
        """Returns axis state dict."""
        return acsc.getAxisState(self.controller.hc, self.axisno)
        
    @property
    def motor_state(self):
        """Returns motor state dict."""
        return acsc.getMotorState(self.controller.hc, self.axisno)
        
    @property
    def moving(self):
        return self.motor_state["moving"]
        
    @property
    def enabled(self):
        return self.motor_state["enabled"]
    
    @enabled.setter
    def enabled(self, choice):
        if choice == True:
            self.enable()
        elif choice == False:
            self.disable()
        
    @property
    def in_position(self):
        return self.motor_state["in position"]
        
    @property
    def accelerating(self):
        return self.motor_state["accelerating"]
        
    @property
    def rpos(self):
        return acsc.getRPosition(self.controller.hc, self.axisno)

    @property
    def fpos(self):
        """
        The function retrieves an instant value of the motor feedback position.
        :return: position of the axes
        :rtype: int
        """
        return acsc.getFPosition(self.controller.hc, self.axisno)
        
    @property
    def rvel(self):
        return acsc.getRVelocity(self.controller.hc, self.axisno)

    @property
    def fvel(self):
        return acsc.getFVelocity(self.controller.hc, self.axisno)
        
    @property
    def getVel(self):
        return acsc.getVelocity(self.controller.hc, self.axisno)

    def setVel(self, velocity):
        """Sets axis velocity."""
        acsc.setVelocity(self.controller.hc, self.axisno, velocity)
        
    @property
    def acc(self):
        return acsc.getAcceleration(self.controller.hc, self.axisno)
    @acc.setter
    def acc(self, accel):
        """Sets axis velocity."""
        acsc.setAcceleration(self.controller.hc, self.axisno, accel)
        
    @property
    def dec(self):
        return acsc.getDeceleration(self.controller.hc, self.axisno)
    @dec.setter
    def dec(self, decel):
        """Sets axis velocity."""
        acsc.setDeceleration(self.controller.hc, self.axisno, decel)
         
