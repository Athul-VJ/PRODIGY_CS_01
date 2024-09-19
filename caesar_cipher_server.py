import http.server
import socketserver
import urllib.parse
import os

PORT = 8000

# Caesar cipher encryption/decryption function
def caesar_cipher(text, shift, action):
    result = ""
    shift = int(shift)

    if action == "decrypt":
        shift = -shift

    # Traverse the text
    for i in range(len(text)):
        char = text[i]

        # Encrypt/decrypt uppercase characters
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)

        # Encrypt/decrypt lowercase characters
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)

        # Non-alphabetic characters remain the same
        else:
            result += char

    return result

class CaesarCipherHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # Parse the form data posted
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = urllib.parse.parse_qs(post_data)

        message = data['message'][0]
        shift = data['shift'][0]
        action = data['action'][0]

        # Perform the Caesar cipher operation
        result = caesar_cipher(message, shift, action)

        # Respond with the result
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = f"<h1>Result: {result}</h1><br><a href='/'>Go Back</a>"
        self.wfile.write(response.encode('utf-8'))

    def do_GET(self):
        if self.path == '/':
            # Serve the HTML form
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'r') as file:
                self.wfile.write(file.read().encode('utf-8'))
        else:
            super().do_GET()

# Set up the HTTP server
Handler = CaesarCipherHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
