"""
Message protocol for length-prefixed TCP messages.
Prevents message boundary issues when multiple messages are sent quickly.
"""
from socket import socket
import struct


def send_message(sock: socket, message: str):
    """Send a length-prefixed message.
    
    Args:
        sock: The socket to send on
        message: The string message to send
    """
    encoded = message.encode()
    # Pack length as 4-byte integer (big-endian)
    length = struct.pack('!I', len(encoded))
    sock.sendall(length + encoded)


def recv_message(sock: socket) -> str:
    """Receive a length-prefixed message.
    
    Args:
        sock: The socket to receive from
        
    Returns:
        The decoded message string, or None if connection closed
    """
    # First, receive exactly 4 bytes for the length
    length_data = recv_exact(sock, 4)
    if not length_data:
        return None
    
    # Unpack the length
    msg_length = struct.unpack('!I', length_data)[0]
    
    # Now receive exactly that many bytes
    message_data = recv_exact(sock, msg_length)
    if not message_data:
        return None
    
    return message_data.decode()


def recv_exact(sock: socket, n: int) -> bytes:
    """Receive exactly n bytes from socket.
    
    Handles partial reads by continuing to recv() until we have
    exactly the requested number of bytes.
    
    Args:
        sock: The socket to receive from
        n: Number of bytes to receive
        
    Returns:
        Exactly n bytes, or None if connection closed
    """
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
