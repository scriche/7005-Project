# 7005-Project
## Goal:
Create a reliable transfer protocol with UDP

## Client:
Send data to proxy wait for ACK to send another with a timeout of 2 seconds
retries 5 times before giving up

## Proxy:
Listen on specified port for a message and forwards whatever the message is to server
4 settings can be configured when starting 
- % chance to delay client packet
- % chance to delay server packet
- % chance to drop client packet
- % chance to drop server packet

### Server:
Accepts data prints to console then sends an ACK back once recived
