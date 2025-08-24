
def get_proxies(file_path):
    with open(file_path, 'r') as file:
        file_proxies = file.read().splitlines()
        proxy_list = []
        for proxy in file_proxies:
            proxy_dict = {
                "http": proxy,
                "https": proxy,
                "error": False
            }
            proxy_list.append(proxy_dict)
    return proxy_list