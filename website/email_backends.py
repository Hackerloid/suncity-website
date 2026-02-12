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
            # Monkey-patch socket.getaddrinfo to force IPv4
            # This ensures we connect via IPv4 (fixing Network Unreachable)
            # BUT we keep the hostname in self.host so SSL verification passes!
            original_getaddrinfo = socket.getaddrinfo

            def ipv4_only_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
                # Force AF_INET (IPv4) regardless of what was requested
                return original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

            socket.getaddrinfo = ipv4_only_getaddrinfo

            try:
                self.connection = self.connection_class(
                    self.host, self.port, **connection_params
                )
            finally:
                # Restore original getaddrinfo immediately
                socket.getaddrinfo = original_getaddrinfo
            
            if not self.use_ssl and self.use_tls:
                self.connection.starttls(context=ssl.create_default_context())
                
            if self.username and self.password:
                self.connection.login(self.username, self.password)
                
            return True
        except OSError:
            if not self.fail_silently:
                raise
            
        return False
            if not self.fail_silently:
                raise
            
        return False
