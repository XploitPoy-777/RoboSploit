<h1 align="center">RoboSploit - Robots.txt Tester Pro</h1>

<p align="center"><img src="assets/Screenshot_2025.png"></p>

## Connect with me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/zabed-ullah-poyel/)
[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@zabedullahpoyel)
[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@0xPoyel)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://x.com/zabedullahpoyel)
[![Website](https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=About.me&logoColor=white)](https://zabedullahpoyel.com)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:zabedullahpoyelcontact@gmail.com)

---

## Description
This tool fetches and analyzes the `robots.txt` file of a target domain and tests the listed "Disallow" paths for unauthorized access using a variety of bypass techniques. It helps identify potential misconfigurations, exposed endpoints, or access control flaws.

Ideal for reconnaissance during bug bounty hunting or professional security assessments.

## Features

| Category              | Capabilities |
|-----------------------|--------------|
| **Bypass Techniques** | 34+ IP spoofing headers, 60+ path traversal variants, HTTP method fuzzing (GET, POST, PUT, etc.) |
| **Protocol Support**  | HTTP/1.1 and HTTP/2 with optional upgrade |
| **Performance**       | Multi-threaded scanning, Rate limiting control, Retry mechanism with backoff |
| **Reporting**         | JSON/CSV outputs with full response metadata |
| **Stealth**           | Proxy support, User-agent rotation |
| **Robots.txt Analysis** | Auto-discovery of disallowed paths, Recursive variant testing on blocked paths |
| **Access Control Testing** | Detects misconfigurations like open admin panels or bypassable forbidden paths |
| **Usability**         | Command-line interface, Colored terminal output (colorama), Graceful shutdown on Ctrl+C |
| **Customization**     | Configurable timeouts, delays, retries, threads, and headers |


## Tools Required

1. Python 3.6 or higher
   - Make sure Python is installed and available in your system PATH

2. Required Python Libraries:
   - requests
   - colorama
   - argparse (built-in with Python 3+)
   - urllib3

3. (Optional) Proxy Tools:
   - Burp Suite or OWASP ZAP (for manual testing or proxy chaining)

4. Internet Connection
   - Required to make HTTP/HTTPS requests to target URLs

License: MIT

## Installation Instructions
```bash
# Clone the repository
git clone https://github.com/yourusername/ultimate-robots-scanner.git
cd RoboSploitr

# (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

```
