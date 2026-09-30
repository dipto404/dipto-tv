from http.server import BaseHTTPRequestHandler
import json
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        json_url = "http://10.99.99.10/tv_channels.json"
        
        try:
            # জেসন লিংক থেকে ডেটা ফেচ করা
            req = urllib.request.Request(
                json_url, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            # M3U রেসপন্স হেডার সেট করা
            self.send_response(200)
            self.send_header('Content-Type', 'audio/x-mpegurl; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # M3U আউটপুট জেনারেট করা
            output = "#EXTM3U\n"
            if isinstance(data, list):
                for channel in data:
                    title = channel.get('name') or channel.get('title') or 'Channel'
                    logo = channel.get('logo') or channel.get('tvg-logo') or ''
                    url = channel.get('url') or channel.get('stream_url') or ''
                    
                    if url:
                        output += f'#EXTINF:-1 tvg-logo="{logo}" group-title="Live TV",{title}\n'
                        output += f'{url}\n'
                        
            self.wfile.write(output.encode('utf-8'))
            
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"#EXTM3U\n# Error: Could not connect to JSON. Details: {str(e)}".encode('utf-8'))
        return
