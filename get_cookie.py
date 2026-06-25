#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键提取米游社 Cookie 小工具
直接从你已登录 mihoyo.com 的浏览器里读出 Cookie，省去手动开发者工具。

用法：
  pip install browser_cookie3
  python get_cookie.py

注意：
- Edge / Chrome 新版用了加密，需要用【管理员身份】打开终端再运行本脚本。
- 运行前请在浏览器里保持 mihoyo.com 登录状态。
- 输出的 Cookie 等于账号钥匙，只贴进 GitHub Secrets，别发别人。
"""

import sys

try:
    import browser_cookie3 as bc
except ImportError:
    print("缺少依赖，请先运行:  pip install browser_cookie3")
    sys.exit(1)

# 签到需要的关键字段，命中其一组即可用
KEY_FIELDS = ["cookie_token", "account_id", "ltoken", "ltuid",
              "cookie_token_v2", "account_id_v2", "ltoken_v2", "ltuid_v2"]

LOADERS = [("Edge", bc.edge), ("Chrome", bc.chrome), ("Firefox", bc.firefox)]


def grab():
    last_err = None
    for name, loader in LOADERS:
        try:
            cj = loader(domain_name="mihoyo.com")
        except Exception as e:  # noqa: BLE001
            last_err = (name, e)
            print(f"[{name}] 读取失败: {type(e).__name__}: {e}")
            continue
        cookies = {c.name: c.value for c in cj if "mihoyo.com" in (c.domain or "")}
        if cookies:
            return name, cookies
    if last_err and "Admin" in type(last_err[1]).__name__:
        print("\n⚠️ 浏览器 Cookie 加密，需要管理员权限。")
        print("   请【右键 → 以管理员身份运行】PowerShell，再重新执行本脚本。")
    return None, {}


def main():
    name, cookies = grab()
    if not cookies:
        print("\n没读到米游社 Cookie。请检查：")
        print("  1) 是否在 Edge/Chrome/Firefox 登录了 mihoyo.com")
        print("  2) Edge/Chrome 是否用【管理员身份】运行了本脚本")
        print("  3) 实在不行就用 README 里的开发者工具手动法")
        sys.exit(1)

    cookie_str = "; ".join(f"{k}={v}" for k, v in cookies.items())
    have = [k for k in KEY_FIELDS if k in cookies]

    print(f"\n✅ 从 [{name}] 读到 {len(cookies)} 个 cookie")
    if have:
        print(f"   关键字段命中: {', '.join(have)}")
    else:
        print("   ⚠️ 没命中关键字段，可能未登录或登录态已过期，建议重新登录米游社")

    print("\n========== 复制下面这一整行 → 粘贴到 GitHub 的 COOKIE Secret ==========\n")
    print(cookie_str)
    print("\n========== 复制到上面这行结束 ==========")
    print("\n⚠️ 这串是账号钥匙，只填进 GitHub Secrets，别发给任何人。")


if __name__ == "__main__":
    main()
