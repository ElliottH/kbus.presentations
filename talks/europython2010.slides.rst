.. .. style::
..    :layout.viewport: w/40,h/10,w-(w/40),h-(2*h/10)

.. .. layout::
..    :quad: C#ccffcc;V0,h;V0,(h-(h/10));Vw,(h-(h/10));Vw,h  # top
..    :quad: C#ccffcc;V0,0;V0,h/10;Vw,h/10;Vw,0              # bottom

.. Hmm. Specific values seem to be necessary to make it work reliably
   (it would seem that 'w' and 'h' are not set very reliably for full
   screen operation).
.. style::
   :layout.viewport: 1024/40,768/10,1024-(1024/40),768-(2*768/10)

.. layout::
   :quad: C#ccffcc;V0,768;V0,(768-(768/10));V1024,(768-(768/10));V1024,768  # top
   :quad: C#ccffcc;V0,0;V0,768/10;V1024,768/10;V1024,0              # bottom

.. page-style::
   :layout.valign: center
   :align: center
   :font_size: 64

**KBUS**

A simple messaging system

.. style::
   :font_size: 32

Tony Ibbs

tibs@tonyibbs.co.uk

July 2010

http://code.google.com/p/kbus/

------------------------------------------------------------------------------

.. style::
   :layout.valign: top
   :align: left
   :font_size: 32
   :footer.position: 0,0
   :footer.hanchor: left
   :footer.vanchor: bottom

.. footer:: EuroPython 2010

A simple introduction to using KBUS
-----------------------------------

With some actors and an audience...

...and using Python.

------------------------------------------------------------------------------

First our actor needs to connect to KBUS itself, by opening a Ksock:

.. compound::

     *Terminal 1: Rosencrantz* ::

       Python 2.6.4 (r264:75706, Dec  7 2009, 18:45:15) 
       [GCC 4.4.1] on linux2
       Type "help", "copyright", "credits" or "license" for more information.
       >>> from kbus import Ksock
       >>> rosencrantz = Ksock(0)
       >>> print rosencrantz
       Ksock device 0, id 113, mode read/write

.. note::

  This specifies which KBUS device to connect to. If KBUS is installed, then
  device ``0`` will always exist, so it is a safe choice. The default is to open
  the device for read and write - this makes sense since we will want to write
  messages to it.

------------------------------------------------------------------------------

They can send a message:

.. compound::

     *Terminal 1: Rosencrantz* ::

       >>> from kbus import Message
       >>> ahem = Message('$.Actor.Speak', 'Ahem')
       >>> rosencrantz.send_msg(ahem)
       MessageId(0, 337)

but no-one is listening.

.. note::

  The Message call creates a new message named ``$.Actor.Speak``, with the
  message data ``"Ahem"``.

      *(All message names are composed of ``$`` followed by a series of
      dot-separated parts.)*

  The next line sends it. For convenience, the ``send_msg`` method also
  returns the *message id* assigned to the message by KBUS - this can be used
  to identify a specific message.

  This will succeed, but doesn't do anything very useful, because no-one is
  listening. So, we shall need a second process, which we shall start in a
  new terminal.

------------------------------------------------------------------------------

An audience, to listen:

.. compound::

     *Terminal 2: Audience* ::

       Python 2.6.4 (r264:75706, Dec  7 2009, 18:45:15) 
       [GCC 4.4.1] on linux2
       Type "help", "copyright", "credits" or "license" for more information.
       >>> from kbus import *
       >>> audience = Ksock(0)
       >>> audience.bind('$.Actor.Speak')

.. note::

  Here, the audience has opened the same KBUS device (messages cannot be sent
  between different KBUS devices). We've still opened it for
  write, since they might, for instance, want to be able to send ``$.Applause``
  messages later on. They've then 'bound to' the ``$.Actor.Speak`` message,
  which means they will receive any messages that are sent with that name.

      (In fact, all messages with that name sent by anyone, not just by
      rosencrantz.)

------------------------------------------------------------------------------

.. compound::

     *Terminal 1: Rosencrantz* ::

       >>> rosencrantz.send_msg(ahem)
       MessageId(0, 338)

.. compound::

     *Terminal 2: Audience* ::

       >>> audience.read_next_msg()
       Message('$.Actor.Speak', data='Ahem', from_=113L, id=MessageId(0, 338))

.. note::

  Note that this shows that the message received has the same ``MessageId`` as
  the message sent (which is good!).

------------------------------------------------------------------------------

A friendlier representation of the message is given if one prints it:

.. compound::

     *Terminal 2: Audience* ::

       >>> print _
       <Announcement '$.Actor.Speak', id=[0:338], from=113, data='Ahem'>

.. note::

  "Plain" messages are also termed "announcements", since they are just being
  broadcast to whoever might be listening.

.. compound::

     *Terminal 1: Rosencrantz* ::

       >>> rosencrantz.ksock_id()
       113L

.. note::

   Rosencrantz's Ksock id is the same as that indicated in the ``from_``
   field.

------------------------------------------------------------------------------

And there's nothing else to hear:

.. compound::

     *Terminal 2: Audience* ::

       >>> print audience.read_next_msg()
       None

So let's be an efficient audience:

.. compound::

     *Terminal 2: Audience* ::

       >>> import select
       >>> while 1:
       ...    (r,w,x) = select.select([audience], [], [])
       ...    # At this point, r should contain audience
       ...    print audience.read_next_msg()
       ... 

.. note::

  (although perhaps with more error checking, and maybe even a timeout, in a
  real example).

------------------------------------------------------------------------------

And so now:

.. compound::

     *Terminal 1: Rosencrantz* ::

       >>> rosencrantz.send_msg(Message('$.Actor.Speak', 'Hello there'))
       MessageId(0, 339)
       >>> rosencrantz.send_msg(Message('$.Actor.Speak', 'Can you hear me?'))
       MessageId(0, 340)

.. compound::

     *Terminal 2: Audience* ::

       <Announcement '$.Actor.Speak', id=[0:339], from=113, data='Hello there'>
       <Announcement '$.Actor.Speak', id=[0:340], from=113, data='Can you hear me?'>
       
------------------------------------------------------------------------------

Another participant:

.. compound::

     *Terminal 3: Guildenstern* ::

       Python 2.6.4 (r264:75706, Dec  7 2009, 18:45:15) 
       [GCC 4.4.1] on linux2
       Type "help", "copyright", "credits" or "license" for more information.
       >>> from kbus import *
       >>> guildenstern = Ksock(0)
       >>> print guildenstern
       Ksock device 0, id 115, mode read/write

------------------------------------------------------------------------------

.. compound::

     *Terminal 3: Guildenstern* ::

       >>> guildenstern.bind('$.Actor.*')

.. note::

  Here, guildenstern is binding to any message whose name starts with
  ``$.Actor.``.

.. compound::

     *Terminal 2: Audience* ::

       <CTRL-C>
       Traceback (most recent call last):
         File "<stdin>", line 2, in <module>
       KeyboardInterrupt
       >>> audience.bind('$.Actor.*')
       >>> while 1:
       ...    print audience.wait_for_msg()
       ... 

.. note::
 
  In retrospect this, of course, makes sense for the audience, too.

  (as a convenience, the Ksock class provides the ``wait_for_msg()`` wrapper
  around ``select.select``, which is shorter to type...).

  And maybe rosencrantz will want to hear his colleague:

.. compound::

     *Terminal 1: Rosencrantz* ::

       >>> rosencrantz.bind('$.Actor.*')

------------------------------------------------------------------------------

.. note::

  So let guildenstern speak:

.. compound::

     *Terminal 3: Guildenstern* ::

       >>> guildenstern.send_msg(Message('$.Actor.Speak', 'Pssst!'))
       MessageId(0, 341)
       >>> # Remember guildenstern is himself listening to '$.Actor.*'
       ... print guildenstern.read_next_msg()
       <Announcement '$.Actor.Speak', id=[0:341], from=115, data='Pssst!'>

.. compound::

     *Terminal 1: Rosencrantz* ::

       >>> msg = rosencrantz.read_next_msg()
       >>> print msg
       <Announcement '$.Actor.Speak', id=[0:341], from=115, data='Pssst!'>

.. compound::

     *Terminal 2: Audience* ::

       <Announcement '$.Actor.Speak', id=[0:341], from=115, data='Pssst!'>
       <Announcement '$.Actor.Speak', id=[0:341], from=115, data='Pssst!'>

.. note::

  This is because the audience has bound to the message twice - it is hearing it
  once because it asked to receive every ``$.Actor.Speak`` message, and again
  because it asked to hear any message matching ``$.Actor.*``.

------------------------------------------------------------------------------

.. note::

  The solution is simple - ask not to hear the more specific version:

.. compound::

     *Terminal 2: Audience* ::

       <CTRL-C>
       Traceback (most recent call last):
         File "<stdin>", line 2, in <module>
         File "/home/tibs/sw/kbus/python/kbus/ksock.py", line 492, in wait_for_msg
           (r, w, x) = select.select([self], [], [], timeout)
       KeyboardInterrupt
       >>> audience.unbind('$.Actor.Speak')
       >>> while 1:
       ...    msg = audience.wait_for_msg()
       ...    print msg
       ... 

------------------------------------------------------------------------------

KBUS also supports Requests and Replies:

.. compound::

     *Terminal 3: Guildenstern* ::

       >>> guildenstern.bind('$.Actor.Ask.Guildenstern', True)

.. note::

       *(Only one person may be bound as Replier for a particular message
       name at any one time, so that it is unambiguous who is expected to do
       the replying.*

       *Also, if a Sender tries to send a Request, but no-one has bound to that
       message name as a Replier, then an error is raised (contrast that with
       ordinary messages, where if no-one is listening, the message just gets
       ignored).)*

------------------------------------------------------------------------------

So if Rosencrantz asks:

.. compound::

     *Terminal 1: Rosencrantz* ::

       >>> from kbus import Request
       >>> req = Request('$.Actor.Ask.Guildenstern', 'Were you speaking to me?')
       >>> rosencrantz.send_msg(req)
       MessageId(0, 342)

.. compound::

     *Terminal 1: Rosencrantz* ::

       >>> print rosencrantz.read_next_msg()
       <Request '$.Actor.Ask.Guildenstern', id=[0:342], from=113, flags=0x1 (REQ), data='Were you speaking to me?'>
       >>> rosencrantz.unbind('$.Actor.*')

------------------------------------------------------------------------------

Guildenstern hears:

.. compound::

     *Terminal 3: Guildenstern* ::

       >>> req = guildenstern.read_next_msg()
       >>> print req
       <Request '$.Actor.Ask.Guildenstern', id=[0:342], from=113, flags=0x3 (REQ,YOU), data='Were you speaking to me?'>

.. compound::

     *Terminal 3: Guildenstern* ::

       >>> print req.wants_us_to_reply()
       True

And again:

.. compound::

     *Terminal 3: Guildenstern* ::

       >>> msg = guildenstern.read_next_msg()
       >>> print msg
       <Request '$.Actor.Ask.Guildenstern', id=[0:342], from=113, flags=0x1 (REQ), data='Were you speaking to me?'>

.. note::

  Looking at the two messages, the first is the Request specifically to
  guildenstern, which he is meant to answer (and that is what the ``YOU`` in
  the flags means).

------------------------------------------------------------------------------

Let's fix that "twice":

.. compound::

     *Terminal 3: Guildenstern* ::

       >>> guildenstern.unbind('$.Actor.*')

.. note::

  As we should expect, guildenstern is getting the message twice, once because
  he has bound as a listener to '$.Actor.*', and once because he is bound as a
  Replier to this specific message.

      *(There is, in fact, a way to ask KBUS to only deliver one copy of
      a given message, and if guildenstern had used that, he would only have
      received the Request that was marked for him to answer. I'm still a little
      undecided how often this mechanism should be used, though.)*

------------------------------------------------------------------------------

Guildenstern replies:

.. compound::

     *Terminal 3: Guildenstern* ::

       >>> rep = reply_to(req, 'Yes, yes I was')
       >>> print rep
       <Reply '$.Actor.Ask.Guildenstern', to=113, in_reply_to=[0:342], data='Yes, yes I was'>
       >>> guildenstern.send_msg(rep)
       MessageId(0, 343)
       >>> guildenstern.read_next_msg()

.. note::

  The ``reply_to`` convenience function crafts a new ``Reply`` message, with the
  various message parts set in an appropriate manner.

------------------------------------------------------------------------------

Rosencrantz hears:

.. compound::

     *Terminal 1: Rosencrantz* ::

       >>> rep = rosencrantz.read_next_msg()
       >>> print rep
       <Reply '$.Actor.Ask.Guildenstern', id=[0:343], to=113, from=115, in_reply_to=[0:342], data='Yes, yes I was'>

.. note::

  Note that Rosencrantz didn't need to bind to this message to receive it - he
  will always get a Reply to any Request he sends (KBUS goes to some lengths to
  guarantee this, so that even if Guildenstern closes his Ksock, it will
  generate a "gone away" message for him).

------------------------------------------------------------------------------

And the audience hears all:

.. compound::

     *Terminal 2: Audience* ::

       <Request '$.Actor.Ask.Guildenstern', id=[0:342], from=113, flags=0x1 (REQ), data='Were you speaking to me?'>
       <Reply '$.Actor.Ask.Guildenstern', id=[0:343], to=113, from=115, in_reply_to=[0:342], data='Yes, yes I was'>
       
Stateful requests
-----------------
Sometimes state is useful...

.. note::

  at one end of a conversation. In such cases, the Sender wants to be sure
  that the same Replier is replying to any Requests. If the original Replier
  unbinds, or even disconnects from the Ksock, and someone else binds as
  Replier instead, that new someone will clearly not have the requisite state,
  and thus the Sender would like to know that this has occurred.

------------------------------------------------------------------------------

.. compound::

     *Terminal 1: Rosencrantz* ::

       >>> # About to start tossing coins
       ... req = rosencrantz.send_msg(Request('$.Actor.Ask.Guildenstern',
       ... 'Will you count heads for me?'))

------------------------------------------------------------------------------

.. compound::

     *Terminal 3: Guildenstern* ::

       >>> req = guildenstern.read_next_msg()
       >>> guildenstern.send_msg(reply_to(req, 'Yes, yes I shall'))
       MessageId(0, 345)
       >>> guildenstern.bind('$.Actor.CoinToss', True)
       >>> heads = 0
       >>> while True:
       ...     toss = guildenstern.wait_for_msg()
       ...     print toss
       ...     if toss.data == 'Head':
       ...        print 'A head - amazing'
       ...        heads += 1
       ...     else:
       ...        print 'Bah, tails'
       ...     guildenstern.send_msg(reply_to(toss, 'Head count is %d'%heads))
       ... 

------------------------------------------------------------------------------

.. compound::

     *Terminal 1: Rosencrantz* ::

       >>> rep = rosencrantz.read_next_msg()
       >>> print rep.from_
       115
       >>> # Throws a head
       ... from kbus import stateful_request
       >>> sreq = stateful_request(rep, '$.Actor.CoinToss', 'Head')
       >>> print sreq
       <Request '$.Actor.CoinToss', to=115, flags=0x1 (REQ), data='Head'>
       >>> rosencrantz.send_msg(sreq)
       MessageId(0, 346)

------------------------------------------------------------------------------

.. compound::

     *Terminal 3: Guildenstern* ::

       <Request '$.Actor.CoinToss', id=[0:346], to=115, from=113, flags=0x3 (REQ,YOU), data='Head'>
       A head - amazing
       MessageId(0, 347)
       

.. compound::

     *Terminal 1: Rosencrantz* ::

       >>> count = rosencrantz.read_next_msg()
       >>> print 'So,',count.data
       So, Head count is 1
       >>> # Throws a head
       ... sreq = stateful_request(rep, '$.Actor.CoinToss', 'Head')
       >>> rosencrantz.send_msg(sreq)
       MessageId(0, 348)

------------------------------------------------------------------------------

.. compound::

     *Terminal 3: Guildenstern* ::

       <Request '$.Actor.CoinToss', id=[0:348], to=115, from=113, flags=0x3 (REQ,YOU), data='Head'>
       A head - amazing
       MessageId(0, 349)
       
------------------------------------------------------------------------------

.. compound::

     *Terminal 1: Rosencrantz* ::

       >>> count = rosencrantz.read_next_msg()
       >>> print 'So,',count.data
       So, Head count is 2
       >>> # Throws a head

------------------------------------------------------------------------------

.. compound::

     *Terminal 3: Guildenstern* ::

       <CTRL-C>
       Traceback (most recent call last):
         File "<stdin>", line 2, in <module>
         File "/home/tibs/sw/kbus/python/kbus/ksock.py", line 492, in wait_for_msg
           (r, w, x) = select.select([self], [], [], timeout)
       KeyboardInterrupt
       >>> print 'Falstaff! No! Ouch!'
       Falstaff! No! Ouch!
       >>> guildenstern.close()

------------------------------------------------------------------------------

.. compound::

     *Terminal 4: Falstaff* ::

       Python 2.6.4 (r264:75706, Dec  7 2009, 18:45:15) 
       [GCC 4.4.1] on linux2
       Type "help", "copyright", "credits" or "license" for more information.
       >>> from kbus import *
       >>> falstaff = Ksock(0)
       >>> falstaff.bind('$.Actor.CoinToss', True)

------------------------------------------------------------------------------

.. compound::

     *Terminal 1: Rosencrantz* ::

       ... sreq = stateful_request(rep, '$.Actor.CoinToss', 'Head')
       >>> rosencrantz.send_msg(sreq)
       Traceback (most recent call last):
         File "<stdin>", line 1, in <module>
         File "/home/tibs/sw/kbus/python/kbus/ksock.py", line 432, in send_msg
           return self.send()
         File "/home/tibs/sw/kbus/python/kbus/ksock.py", line 220, in send
           fcntl.ioctl(self.fd, Ksock.IOC_SEND, arg);
       IOError: [Errno 32] Broken pipe

------------------------------------------------------------------------------

::

  $ errno.py 32
  Error 32 (0x20) is EPIPE: Broken pipe

  KBUS:
  On attempting to send 'to' a specific replier, the replier with that id
  is no longer bound to the given message's name.

------------------------------------------------------------------------------

.. compound::

     *Terminal 2: Audience* ::

       <Request '$.Actor.Ask.Guildenstern', id=[0:344], from=113, flags=0x1 (REQ), data='Will you count heads for me?'>
       <Reply '$.Actor.Ask.Guildenstern', id=[0:345], to=113, from=115, in_reply_to=[0:344], data='Yes, yes I shall'>
       <Request '$.Actor.CoinToss', id=[0:346], to=115, from=113, flags=0x1 (REQ), data='Head'>
       <Reply '$.Actor.CoinToss', id=[0:347], to=113, from=115, in_reply_to=[0:346], data='Head count is 1'>
       <Request '$.Actor.CoinToss', id=[0:348], to=115, from=113, flags=0x1 (REQ), data='Head'>
       <Reply '$.Actor.CoinToss', id=[0:349], to=113, from=115, in_reply_to=[0:348], data='Head count is 2'>
       


.. note:: Running the examples in this introduction requires having
   the KBUS kernel module installed. If this is not already done, and you have
   the KBUS sources, then ``cd`` to the kernel module directory (i.e.,
   ``kbus`` in the sources) and do::

             make
             make rules
             sudo insmod kbus.ko

   When you've finished the examples, you can remove the kernel module again
   with::

             sudo rmmod kbus.ko

   The message ids shown in the examples are correct if you've just installed
   the kernel module - the second number in each message id will be different
   (although always ascending) otherwise.


Isolation
---------

.. image:: images/04_fish_in_bowl2.png
   :scale:  50

..   :width:  370
..   :height: 306

------------------------------------------------------------------------------

Two other fish, communicating via a different KBUS device, are in a different
metaphorical bowl, and thus cannot communicate with R and G.

.. image:: images/09_two_disjoint_bowls.png
   :scale:  66


.. vim: set filetype=rst tabstop=8 softtabstop=2 shiftwidth=2 expandtab:
