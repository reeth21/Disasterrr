from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Listen for console errors
        def handle_console(msg):
            if msg.type == 'error':
                print(f"BROWSER CONSOLE ERROR: {msg.text}")
                
        page.on("console", handle_console)
        page.on("pageerror", lambda err: print(f"PAGE EXCEPTION: {err}"))
        
        print("Navigating to index.html...")
        page.goto("file:///F:\Disaster\index.html")
        
        # Wait a bit for JS to execute
        page.wait_for_timeout(2000)
        browser.close()

if __name__ == '__main__':
    run()
