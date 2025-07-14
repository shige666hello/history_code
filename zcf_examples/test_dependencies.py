#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    import requests
    print(f"✓ requests 版本: {requests.__version__}")
except ImportError as e:
    print(f"✗ requests 导入失败: {e}")

try:
    import bs4
    print(f"✓ beautifulsoup4 版本: {bs4.__version__}")
except ImportError as e:
    print(f"✗ beautifulsoup4 导入失败: {e}")

try:
    import json
    print("✓ json 模块可用")
except ImportError as e:
    print(f"✗ json 模块导入失败: {e}")

try:
    import os
    print("✓ os 模块可用")
except ImportError as e:
    print(f"✗ os 模块导入失败: {e}")

try:
    from datetime import datetime
    print("✓ datetime 模块可用")
except ImportError as e:
    print(f"✗ datetime 模块导入失败: {e}")

print("\n所有依赖检查完成！") 