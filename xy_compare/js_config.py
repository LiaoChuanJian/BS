JS_CONFIG = {
    "logo": {
        "title": "商品比价网站",
        "image": "/static/admin/images/logo.png"
    },
    "menu": {
        "data": "/js_menu",
        "method": "GET",
        "accordion": True,
        "collaspe": False,
        "control": False,
        "controlWidth": 500,
        "select": "10",
        "async": True
    },
    "tab": {
        "enable": False,
        "keepState": True,
        "session": True,
        "max": "30",
        "index": {
            "id": "10",
            "href": "/main",
            "title": "首页"
        }
    },
    "theme": {
        "defaultColor": "2",
        "defaultMenu": "dark-theme",
        "defaultHeader": "light-theme",
        "allowCustom": True,
        "banner": False
    },
    "colors": [{
        "id": "1",
        "color": "#2d8cf0",
        "second": "#ecf5ff"
    },
        {
            "id": "2",
            "color": "#8B658B",
            "second": "#f0f9eb"
        }
    ],
    "other": {
        "keepLoad": "0",
        "autoHead": True
    },
    "header": {
            "message": ""
        }

}
