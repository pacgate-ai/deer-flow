#!/usr/bin/env python3
"""Test PDF generation with weasyprint."""
from weasyprint import HTML
import os

html_content = "<h1>百宸尽调报告</h1><p>测试 PDF 生成 — PacGate-Law</p>"
HTML(string=html_content).write_pdf("/tmp/test.pdf")
size = os.path.getsize("/tmp/test.pdf")
print(f"PDF created successfully: {size} bytes")
print(f"Path: /tmp/test.pdf")