#!/usr/bin/env python3
"""
Ashtavadhanam Modern — One-Click Local Launcher
Starts a local HTTP server with native HTTP 206 Partial Content (Range requests)
and opens the browser.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080

class RangeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    HTTP request handler with native HTTP 206 Partial Content (Byte Range) support.
    Enables instant seeking, smooth scrubbing, and efficient streaming for MP4 video
    and AAC/MP3 audio in all browsers.
    """
    protocol_version = "HTTP/1.1"

    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()

        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, 'File not found')
            return None

        fs = os.fstat(f.fileno())
        total = fs.st_size
        range_header = self.headers.get('Range')

        if not range_header or not range_header.startswith('bytes='):
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(total))
            self.send_header('Last-Modified', self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f

        try:
            val = range_header[6:].strip()
            if ',' in val:
                # Multi-range fallback to 200
                f.close()
                return super().send_head()

            start_str, sep, end_str = val.partition('-')
            if not sep:
                f.close()
                return super().send_head()

            if not start_str:  # bytes=-suffix
                suffix_len = int(end_str)
                start = max(0, total - suffix_len)
                end = total - 1
            elif not end_str:  # bytes=start-
                start = int(start_str)
                end = total - 1
            else:  # bytes=start-end
                start = int(start_str)
                end = int(end_str)

            if start >= total or start > end:
                self.send_response(416)
                self.send_header('Content-Range', f'bytes */{total}')
                self.end_headers()
                f.close()
                return None

            end = min(end, total - 1)
            content_length = end - start + 1

            self.send_response(206)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Range', f'bytes {start}-{end}/{total}')
            self.send_header('Content-Length', str(content_length))
            self.send_header('Last-Modified', self.date_time_string(fs.st_mtime))
            self.end_headers()

            class RangeWrapper:
                def __init__(self, file_obj, s, l):
                    self.f = file_obj
                    self.f.seek(s)
                    self.rem = l

                def read(self, n=-1):
                    if self.rem <= 0:
                        return b''
                    if n < 0 or n > self.rem:
                        n = self.rem
                    chunk = self.f.read(n)
                    self.rem -= len(chunk)
                    return chunk

                def close(self):
                    self.f.close()

            return RangeWrapper(f, start, content_length)

        except Exception as e:
            f.close()
            self.send_error(400, f'Bad Request: {e}')
            return None

    def copyfile(self, source, outputfile):
        """Silently handle aborted client connections during scrubbing."""
        try:
            super().copyfile(source, outputfile)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass


def start_server():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    Handler = RangeHTTPRequestHandler

    # Find free port if 8080 is busy
    port = PORT
    for attempt in range(10):
        try:
            with socketserver.TCPServer(("", port), Handler) as httpd:
                url = f"http://localhost:{port}/index.html"
                print("\n" + "="*60)
                print(f"  🕉️ Ashtavadhanam Modernized Web Application")
                print(f"  Server running at: {url}")
                print(f"  Native HTTP 206 Partial Content (Range Seeking): ACTIVE")
                print(f"  Press Ctrl+C to stop the server.")
                print("="*60 + "\n")
                webbrowser.open(url)
                httpd.serve_forever()
                break
        except OSError:
            port += 1

if __name__ == "__main__":
    start_server()
