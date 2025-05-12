import os
import sys
import requests
from pathlib import Path
from typing import Optional, Dict, Any
import PyPDF2
import docx
import json

def read_pdf(file_path: str) -> str:
    """读取PDF文件内容"""
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return text

def read_txt(file_path: str) -> str:
    """读取TXT文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_docx(file_path: str) -> str:
    """读取Word文件内容"""
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def add_document_to_knowledge_base(content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """将文档添加到知识库"""
    url = "http://localhost:8000/add_document"
    payload = {
        "content": content,
        "metadata": metadata or {}
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print(f"错误: {response.text}")

def process_file(file_path: str) -> None:
    """处理单个文件并添加到知识库"""
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"文件不存在: {file_path}")
        return

    # 准备元数据
    metadata = {
        "filename": file_path.name,
        "file_type": file_path.suffix[1:],
        "file_size": os.path.getsize(file_path)
    }

    # 根据文件类型读取内容
    content = ""
    if file_path.suffix.lower() == '.pdf':
        content = read_pdf(str(file_path))
    elif file_path.suffix.lower() == '.txt':
        content = read_txt(str(file_path))
    elif file_path.suffix.lower() in ['.docx', '.doc']:
        content = read_docx(str(file_path))
    else:
        print(f"不支持的文件类型: {file_path.suffix}")
        return

    # 添加到知识库
    add_document_to_knowledge_base(content, metadata)

def main():
    if len(sys.argv) < 2:
        print("使用方法: python add_document.py <文件路径>")
        return

    file_path = sys.argv[1]
    process_file(file_path)

if __name__ == "__main__":
    main()
