import socket
import ssl
from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend

class EmailBackend(DjangoEmailBackend):
    def open(self):
        if self.connection:
            return False
        
        connection_params = {}
        if self.timeout is not None:
            connection_params['timeout'] = self.timeout
            
        if self.use_ssl:
            connection_params['context'] = ssl.create_default_context()
            
        try:
            # This is the key fix: Force IPv4 logic
            # We don't have a direct way to pass AF_INET to SMTP constructor in Python < 3.3 for some versions,
            # but usually we can't easily override the socket creation inside smtplib.SMTP 
            # without rewriting the whole thing. 
            # HOWEVER, we can monkey-patch socket.getaddrinfo contextually or use a hack.
            
            # Actually, a cleaner way in a custom backend:
            # We can resolve the host manually to an IPv4 address before passing it to the superclass.
            # This bypasses the system's potential preference for IPv6.
            
            try:
                # Get the first IPv4 address
                addr_info = socket.getaddrinfo(self.host, self.port, family=socket.AF_INET)
                if addr_info:
                    # (family, type, proto, canonname, sockaddr)
                    # sockaddr is (address, port)
                    self.host = addr_info[0][4][0]
            except Exception:
                # Fallback to original host if resolution fails
                pass
                
            self.connection = self.connection_class(
                self.host, self.port, **connection_params
            )
            
            if not self.use_ssl and self.use_tls:
                self.connection.starttls(context=ssl.create_default_context())
                
            if self.username and self.password:
                self.connection.login(self.username, self.password)
                
            return True
        except OSError:
            if not self.fail_silently:
                raise
            
        return False
