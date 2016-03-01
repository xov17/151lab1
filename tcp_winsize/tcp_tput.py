#!/usr/bin/env python
import math

"""
Estimate upper bounds on TCP connection throughput,
given MSS, RTT, and loss rate

Implemented from slightly simplified equations on:
   http://www.slac.stanford.edu/comp/net/wan-mon/thru-vs-loss.html

In particular:
 ''We have assumed the number of packets acknowledged by a received ACK is 2
   (this is b in the Padhye et. al. formula 31)''

There are two functions you care about:
  tcp_bw(mss, rtt, loss_rate, ...)
     using the more sophisticated calculations
  tcp_bw_mathis(mss, rtt, loss_rate, ...)
     for the back-of-the-envelope calculation that started it all

"""

def tcp_bw_mathis(mss, rtt, loss_rate, want_bytes_per_second=False):
  """
  Using the formula 'Rate <= (MSS/RTT)*(1 / sqrt{p})' from
    'The macroscopic behavior of the TCP congestion avoidance algorithm'
    Mathis, et al. CCR 27(3), July 1997
  
  calculate the expected bandwidth (in bits per second) of a TCP connection.

  Parameters:
    mss - Maximum Segment Size (bytes)
    rtt - Round Trip Time (seconds)
    loss_rate - ratio of packets that are lost (0.1 for 10%)
    
  Return:
    upper bound of the transfer rate (float),
      in bits per second unless @want_bytes_per_second
  """
  if not want_bytes_per_second:
    mss = mss * 8.0
  return (mss/rtt)*(1.0/math.sqrt(loss_rate))

def G(p):
    return (1 +
            p +
            2.0*(p**2) +
            4.0*(p**3) +
            8.0*(p**4) +
            16.0*(p**5) +
            32.0*(p**6)
            )

def Q(p,w):
    return min(1.0,
               ( (1.0 - (1.0-p)**3) *
                 (1.0 + (1.0-p)**3) *
                 (1.0 - (1.0-p)**(w-3))
                 )
               / ((1.0 - (1.0-p)**w))
               )
def w(p):
  return (2.0/3.0)*(1.0 + math.sqrt(3.0*((1.0-p)/p) + 1.0))


def tcp_bw(mss, rtt, loss_rate,
           wmax=30, initial_rto=3.0,
           want_bytes_per_second=False
           ):
  """
  Using the set of of formulas from
   'Modelling TCP throughput: A simple model and its empirical validation'
   by J. Padhye, et al, SIGCOMM 1998
   
  calculate the expected bandwidth (bits per second)of a TCP connection.

  While more complicated, these seem to give more accurate readings
  for high loss rates (> 2%).

  Parameters:
    mss - Maximum Segment Size (bytes)
    rtt - Round Trip Time (seconds)
    loss_rate - ratio of packets that are lost (0.1 for 10%)
    wmax - maximum window size (number of segments)
    initial_rto - Initial Retransmission Timeout (RTO) in seconds
    want_bytes_per_seconds - set to True if you want Bytes/second 

  Return:
    upper bound of the transfer rate (float),
      in bits per second unless @want_bytes_per_second
  """
  p = float(loss_rate)
  if not want_bytes_per_second:
    mss = mss * 8.0
  if (w(p) < wmax):
    rate = (mss * (((1.0-p)/p) +  w(p) + Q(p,w(p))/(1.0-p)) 
            / (rtt * ((w(p)+1.0))+(Q(p,w(p))*G(p)*initial_rto)/(1.0-p))
            )
  else:
    rate = (
      (  mss * ( ((1.0-p)/p) + wmax + Q(p,wmax)/(1.0-p) )  )
      / ( ( rtt * ( 0.25*wmax + ((1.0-p)/(p*wmax) + 2.0) ) )
          + (Q(p,wmax)*G(p)*initial_rto)/(1.0-p)
          )
      )
  return rate

