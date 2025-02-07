import requests
import socks
import socket

def check_proxy(proxy, proxy_type, timeout=5):
    try:
        if proxy_type == "http" or proxy_type == "https":
            proxies = {"http": f"{proxy_type}://{proxy}", "https": f"{proxy_type}://{proxy}"}
            response = requests.get("http://www.google.com", proxies=proxies, timeout=timeout)
        else:
            ip, port = proxy.split(":")
            port = int(port)
            socks.set_default_proxy(socks.SOCKS5 if proxy_type == "socks" else socks.SOCKS4, ip, port)
            socket.socket = socks.socksocket
            response = requests.get("http://www.google.com", timeout=timeout)
        
        if response.status_code == 200:
            return True
    except Exception:
        pass
    return False

def main():
    proxy_list = input("Nhập danh sách proxy (cách nhau bằng dấu phẩy): ").split(",")
    proxy_type = input("Chọn loại proxy (http/https/socks): ").strip().lower()
    
    if proxy_type not in ["http", "https", "socks"]:
        print("[ERROR] Loại proxy không hợp lệ!")
        return
    
    live_proxies = []
    
    for proxy in proxy_list:
        proxy = proxy.strip()
        print(f"[INFO] Kiểm tra proxy: {proxy}")
        if check_proxy(proxy, proxy_type):
            print(f"[SUCCESS] Proxy hoạt động: {proxy}")
            live_proxies.append(proxy + ",")
        else:
            print(f"[FAIL] Proxy không hoạt động: {proxy}")
    
    with open("live_proxies.txt", "w") as f:
        f.writelines("\n".join(live_proxies))
    
    print("[INFO] Danh sách proxy còn sống đã được lưu vào live_proxies.txt")

if __name__ == "__main__":
    main()
