import sys
file_path = "f:/IOT/disater-main/index.html"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    debug_wrapper = '''<script>
    window.onerror = function(msg, url, line, col, error) {
        document.body.innerHTML += '<div style="color:red;font-size:16px;font-family:monospace;padding:20px;z-index:9999;position:fixed;top:0;left:0;background:white;width:100%;box-shadow:0 4px 6px rgba(0,0,0,0.1);"><h1>JS ERROR:</h1>' + msg + '<br>Line: ' + line + '</div>';
        return false;
    };
    </script>'''

    if 'window.onerror = function' not in content:
        content = content.replace('<body>', f'<body>\n{debug_wrapper}')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Successfully added debug wrapper to index.html")
    else:
        print("Debug wrapper already exists")
        
except Exception as e:
    print(f"Error: {e}")
