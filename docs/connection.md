# Hardware Connection

In order to use the ImageWriter II with a modern RS-232 serial interface, you will need to make your own cable. This cable converts from the DB9 9-pin plug to the mini DIN 8 plug the ImageWriter II uses, connecting a subset of the signals together. The ImageWriter II and early RS-232 were contemporaries, but the full modern semantics of RS-232 were not entirely established at the time. Some explanation of serial protocol semantics, both modern and historical, is needed.

## Host and Device

For the purposes of this documentation, we will refer to the user's computer as a **host**, and the ImageWriter II as a **device**. In other contexts, a host may also be referred to as "data terminal equipment" - a holdover from a period of time where you might have a [teletype device](https://en.wikipedia.org/wiki/Teleprinter) or a serial console instead of a PC or laptop. The device, meanwhile, may be called a "data carrier device" - often a modem, historically - or, naturally, the printer.

## A Primer On RS-232 Serial Signals

The following is a primer on the RS-232 interface - enough to understand how communication with the ImageWriter II works. For in-depth information on RS-232, [refer to Wikipedia](https://en.wikipedia.org/wiki/RS-232).

A 9-pin RS-232 serial connection has 8 signals, plus ground, with the following pinout:

| Pin # | Signal | Description         |
|-------|--------|---------------------|
|     1 | DCD    | Data Carrier Detect |
|     2 | RXD    | Received Data       |
|     3 | TXD    | Transmitted Data    |
|     4 | DTR    | Data Terminal Ready |
|     5 | GND    | Ground              |
|     6 | DSR    | Data Set Ready      |
|     7 | RTS    | Request To Send     |
|     8 | CTS    | Clear To Send       |
|     9 | RI     | Ring Indicator      |

### RXD and TXD

These are the signals that receive and transmit data, from the perspective of the host. The device receives data from the TXD line, and transmits data over the RXD line.

### RI and DCD

The serial standard was designed to accomodate [Hayes-compatible modems](https://en.wikipedia.org/wiki/Hayes_Microcomputer_Products#The_Smartmodem). These two signals are holdovers from that history.

[The "Ring Indicator" signal](https://en.wikipedia.org/wiki/RS-232#RI) is meant to signal that the phone the modem is connected to is ringing. [The "Data Carrier Detect" signal](https://en.wikipedia.org/wiki/Data_Carrier_Detect) is meant to indicate that the modem is connected to the internet.

Historically, devices may use `DCD` to indicate that they are booted and/or ready to send data, similar to `DSR` (as documented below). In practice, these signals are ignored by serial clients outside modem use cases.

### Flow Control

In most cases, a host and a device are capable of sending and receiving data at different rates. The baud rate corresponds to how quickly data is sent or received when hosts and devices are ready and able. But serial connections also need to account for hosts and devices pausing a connection in order to process buffered data. Therefore, [flow control](https://en.wikipedia.org/wiki/Flow_control_(data)) is needed to ensure that a faster device pauses when a slower device needs time to process that data.

Note that, while computers are typically faster than devices in the modern era, that was not always the case; both the host and device need the capability to buffer and process data.

The RS-232 standard uses four signals to manage flow control: `DSR`, `DTR`, `RTS` and `CTS`. `DSR` and `DTR` came first. `RTS` and `CTS` came later, once it was clear that `DSR` and `DTR` were insufficient to handle flow control.

### DSR and DTR

`DSR` and `DTR` are easy to describe, but harder to understand. In short, [`DTR`](https://en.wikipedia.org/wiki/Data_Terminal_Ready) indicates that the host is ready to receive data, and `DSR` indicates that the device is ready to send data.

Historically, they are used to implement flow control for the host receiving data. The device asserts `DSR` when it is ready to send data, and the host asserts `DTR` when it is ready to receive that data. In other words, the following events would happen when the device sends data:

1. The device asserts `DSR`
2. When the host is ready, it asserts `DTR`
3. The device begins sending data to the host
4. The host de-asserts `DTR` when its buffer is full
5. The device stops sending data to the host until `DTR` is re-asserted
6. The device may de-assert `DSR` when it no longer wants to send data

In the modern day, the host is almost always much faster than the device. This means that, practically speaking, `DTR` is always asserted, and `DSR` signals to the host that the device is online. Today, these signals are semantically treated as indicating that the host and device, respectively, are booted and "online".

### RTS and CTS

`RTS` and `CTS` are the signals used to implement flow control for the device receiving data. `RTS` is asserted by the host when it wants to send data, and `CTS` is asserted by the device when it is ready to receive data. In other words, the following events happen when the host sends data:

1. The host asserts `RTS`
2. When the device is ready, it asserts `CTS`
3. The host begins sending data to the device
4. The device de-asserts `CTS` when its buffer is full
5. The host stops sending data to the device until `CTS` is re-asserted
6. The device may de-assert `RTS` when it no longer wants to send data

Note that, in the case of the ImageWriter II, it will not print of the host is asserting `RTS`. This is because it's not powerful enough to both print and buffer data. In practice, the host must de-assert `RTS` when it is done sending data, even though this isn't demanded by the semantics of RS-232.

Historically, `DSR` and `DTR` would be used (or abused) as `RTS` and `CTS` are today, in scenarios where a device was expected to be slower than a host. `RTS` and `CTS` were added later - an ongoing process during the product lifetime of the ImageWriter II - when it became clear that assumptions on the relative speeds of host and device could not be made. In the modern day, `RTS` and `CTS` are the primary mechanisms for flow control, as the host is almost always much faster than the device.

### XON and XOFF

In cases where it's not possible to use flow control signals, a connection may use special bytes called `XON` and `XOFF` (for "transmit on" and "transmit off"). These are called [software flow control](https://en.wikipedia.org/wiki/Software_flow_control). The ImageWriter II supports respecting these signals from the host, largely replacing `RTS` and `CTS`. This is never needed in practice, as both modern RS-232 and the ImageWriter II support flow control signals.

## Serial on the ImageWriter II

The ImageWriter II uses a mini DIN 8 connector that does not conform to the modern RS-232 specification. Its signals are as follows:

| Pin # | Color  | RS-232 Pin # | Apple Signal | RS-232 Signal | Apple Description   |
|-------|--------|--------------|--------------|---------------| --------------------|
|     1 | Black  | 8            | DTR          | CTS           | Data Terminal Ready |
|     2 | Brown  | 7            | DSR          | RTS           | Data Set Ready      |
|     3 | Red    | 2            | TxD-         | RxD           | Transmitted Data    |
|     4 | Orange | 5*           | GND          | GND           | Signal Ground       |
|     5 | Yellow | 3            | RxD-         | TxD           | Received Data       |
|     6 | Green  | 5*           | TxD+         | GND           | Balanced Transmit   |
|     7 | Blue   | --           | NC           | --            | No Connection       |
|     8 | Violet | --           | RxD+         | --            | Balanced Receive    |

`*` indicates that multiple signals are connected to the pin.

### TxD, RxD and Balanced Signals

The `TxD-` and `RxD-` lines are treated as `RxD` and `TxD` by RS-232.
These are labeled "backwards" in the ImageWriter II documentation as compared to RS-232. This is because `TxD` and `RxD` are usually specified with respect to the host; while Apple specifies them with respect to the device. In other words, the printer transmits on what Apple calls its `TxD-` line, which is then *received* on the host's `RxD` line.

The `TxD+` and `RxD+` lines are paired with `TxD-` and `RxD-` to create a differential signal - that is, a `TxD` signal would be measured between `TxD+` and `TxD-`, instead of `TxD-` and ground. Differential signals are not used by RS-232. This is therefore handled by grounding `TxD+` and allowing `RxD+` to float; and treating `TxD-` and `RxD-` as `RxD` and `TxD` accordingly.

### Flow Control

The Apple documentation uses what it calls the `DTR` and `DSR` lines to implement flow control for receiving data from the host, corresponding to `CTS` and `RTS` in RS-232. This mirrors the labeling of `TxD` and `RxD` in the ImageWriter II documentation.

### What's Not Used

Naturally, as the ImageWriter II is not a modem, `RI` and `DCD` are nowhere to be seen.

Additionally, the host and device do not share `DTR` and `DSR` signals. This is acceptable for the host, as modern clients always assert `DTR` and ignore `DSR`. This is also acceptable for the ImageWriter II, which only sends data in the very narrow use case of self-identification. In that case, the host requests that information and is expected to be able to immediately receive it in full at the maximum send rate.

### Differences from Apple Documentation

This information in this section is different from that in the [ImageWriter II Technical Reference Manual](./imagewriter-ii-technical-reference-manual.pd). This is because the Apple documentation makes a number of incorrect assertions about how an RS-232 host would treat its pins.

In short: Apple suggests connecting pin 1 to `DSR` and `DCD`, rather than to `CTS`; and connecting pin 2 to `DTR` instead of `RTS`. Rather than using `RTS` and `CTS` as they typically are today, Apple expects the `DSR` and `DTR` to be repurposed for the `RTS`/`CTS` use case, with `DCD` repurposed for the use case of `DSR`.

In Apple's wiring, when the ImageWriter II was ready to receive data, it would assert both `DSR` and `DCD` to indicate it was able to send and receive data, respectively; and read `DTR` to detect if the host was planning to send data.

With our wiring, when the ImageWriter is ready to receive data, it asserts `CTS`, and reads `RTS` to detect if the host is planning to send data; and `DCD` and `DSR` are completely ignored by the host.

These corrections are in large part informed by Apple discussions [DOC-7141](https://discussions.apple.com/docs/DOC-7141) and [DOC-7871](https://discussions.apple.com/docs/DOC-7871), written by a poster with the nom de plume "[John Galt](https://en.wikipedia.org/wiki/John_Galt)".

## Making the Cable

In order to make a cable, you will need two parts.

The first is a cable with a male mini DIN 8 connector on one end, and the other as broken out wires. You could also potentially buy a mini DIN 8 cable and snip off one of the ends. [I bought a cable with broken out wires on Amazon](https://a.co/d/0aWy3VPB). Note that the color coding indicated by Apple is still accurate.

The second is a male DB9 breakout connector. I have found two on Amazon:

* [A screw terminal breakout set that was convenient but not tidy](https://a.co/d/038SJErV) - this one is no longer available
* [A male connector with screw terminals, a case and strain relief](https://a.co/d/06XVZpeD), which will be tidy but is more difficult to work with

Once you have these parts, take the end of the cable with exposed wires, and connect them to the appropriate screw terminals on the breakout connector, as below:

| Color  | RS-232 Pin # |
|--------|--------------|
| Black  | 8            |
| Brown  | 7            |
| Red    | 2            |
| Orange | 5*           |
| Yellow | 3            |
| Green  | 5*           |
| Blue   | Floating     |
| Violet | Floating     |

`*` indicates that multiple signals are connected to the pin. In this case, both orange and green are connected to pin 5, which is ground.
