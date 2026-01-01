#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để refactor các file JSON trong thư mục Data/
Theo yêu cầu: tách nghĩa thành các phần tử riêng, đảm bảo định dạng đúng
"""

import json
import os
import re
import sys
from pathlib import Path

# Đặt encoding cho stdout để tránh lỗi Unicode trên Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def split_meanings(meanings_list):
    """
    Tách các nghĩa được nối bằng dấu chấm phẩy thành các phần tử riêng
    Chỉ tách theo dấu chấm phẩy (;), không tách theo dấu phẩy (,) vì dấu phẩy có thể là phần của câu
    """
    result = []
    for meaning in meanings_list:
        if isinstance(meaning, str):
            # Loại bỏ phần "LT:..." vì đây là thông tin về lượng từ, đã có trong classifiers
            meaning = re.sub(r'\s*,\s*LT:[^;]*', '', meaning)  # Loại bỏ ", LT:..."
            meaning = re.sub(r'\s*LT:[^;]*', '', meaning)  # Loại bỏ "LT:..." ở đầu
            # Loại bỏ dấu phẩy thừa ở cuối
            meaning = re.sub(r',\s*$', '', meaning)
            meaning = meaning.strip()
            
            if not meaning:
                continue
            
            # Chỉ tách theo dấu chấm phẩy (;)
            # Dấu phẩy (,) thường là phần của câu tiếng Việt, không phải dấu phân cách nghĩa
            parts = meaning.split(';')
            for part in parts:
                part = part.strip()
                if part:
                    result.append(part)
        else:
            result.append(meaning)
    return result


def clean_meaning(meaning):
    """
    Làm sạch nghĩa: loại bỏ khoảng trắng thừa, đảm bảo định dạng đúng
    """
    if not isinstance(meaning, str):
        return meaning
    # Loại bỏ khoảng trắng đầu cuối
    meaning = meaning.strip()
    # Xử lý các trường hợp đặc biệt
    # Nếu có "LT:" (lượng từ), giữ nguyên
    return meaning


def refactor_entry(entry, level):
    """
    Refactor một entry theo định dạng yêu cầu
    """
    # Đảm bảo có đầy đủ các trường bắt buộc
    refactored = {
        "simplified": entry.get("simplified", ""),
        "radical": entry.get("radical", ""),
        "frequency": entry.get("frequency", 0),
        "pos": entry.get("pos", []),
        "forms": [],
        "level": level
    }
    
    # Xử lý forms
    forms = entry.get("forms", [])
    if not forms:
        # Nếu không có forms, tạo một form mặc định từ các trường ở cấp cao nhất
        form = {
            "traditional": entry.get("traditional", entry.get("simplified", "")),
            "transcriptions": entry.get("transcriptions", {
                "pinyin": "",
                "numeric": "",
                "wadegiles": "",
                "bopomofo": "",
                "romatzyh": ""
            }),
            "meanings": [],
            "classifiers": entry.get("classifiers", []),
            "han_viet": entry.get("han_viet", "")
        }
        forms = [form]
    
    for form in forms:
        refactored_form = {
            "traditional": form.get("traditional", refactored["simplified"]),
            "transcriptions": {
                "pinyin": form.get("transcriptions", {}).get("pinyin", ""),
                "numeric": form.get("transcriptions", {}).get("numeric", ""),
                "wadegiles": form.get("transcriptions", {}).get("wadegiles", ""),
                "bopomofo": form.get("transcriptions", {}).get("bopomofo", ""),
                "romatzyh": form.get("transcriptions", {}).get("romatzyh", "")
            },
            "meanings": [],
            "classifiers": form.get("classifiers", []),
            "han_viet": form.get("han_viet", "")
        }
        
        # Xử lý meanings: tách các nghĩa được nối bằng dấu chấm phẩy
        meanings = form.get("meanings", [])
        if meanings:
            split_meanings_list = split_meanings(meanings)
            refactored_form["meanings"] = [clean_meaning(m) for m in split_meanings_list if m]
        else:
            # Nếu không có meanings trong form, thử lấy từ cấp entry
            meanings = entry.get("meanings", [])
            if meanings:
                split_meanings_list = split_meanings(meanings)
                refactored_form["meanings"] = [clean_meaning(m) for m in split_meanings_list if m]
        
        refactored["forms"].append(refactored_form)
    
    return refactored


def refactor_json_file(input_path, output_path, level):
    """
    Refactor một file JSON
    """
    print(f"Đang xử lý file: {input_path}")
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Lỗi khi đọc file {input_path}: {e}")
        return False
    
    if not isinstance(data, list):
        print(f"File {input_path} không phải là mảng JSON")
        return False
    
    # Refactor từng entry
    refactored_data = []
    for i, entry in enumerate(data):
        try:
            # Sử dụng level từ entry nếu có, nếu không dùng level từ tham số
            entry_level = entry.get("level", level)
            refactored_entry = refactor_entry(entry, entry_level)
            refactored_data.append(refactored_entry)
        except Exception as e:
            print(f"Lỗi khi xử lý entry {i} trong file {input_path}: {e}")
            continue
    
    # Ghi file mới
    try:
        # Tạo thư mục output nếu chưa có
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(refactored_data, f, ensure_ascii=False, indent=2)
        
        print(f"Đã refactor thành công: {output_path} ({len(refactored_data)} entries)")
        return True
    except Exception as e:
        print(f"Lỗi khi ghi file {output_path}: {e}")
        return False


def main():
    """
    Hàm chính: refactor tất cả các file JSON trong thư mục Data/
    """
    # Đường dẫn thư mục Data
    data_dir = Path(__file__).parent.parent / "Data"
    output_dir = Path(__file__).parent.parent / "Data" / "refactored"
    
    # Tạo thư mục output
    output_dir.mkdir(exist_ok=True)
    
    # Danh sách các file cần xử lý
    files_to_process = [
        ("1.json", 1),
        ("2.json", 2),
        ("3.json", 3),
        ("4.json", 4),
        ("5.json", 5),
        ("6.json", 6),
        ("7.json", 7),
        ("others.json", 0)  # others.json có level 0 hoặc không có level
    ]
    
    print("=" * 60)
    print("BẮT ĐẦU REFACTOR CÁC FILE JSON")
    print("=" * 60)
    
    success_count = 0
    for filename, level in files_to_process:
        input_path = data_dir / filename
        output_path = output_dir / filename
        
        if not input_path.exists():
            print(f"File không tồn tại: {input_path}")
            continue
        
        if refactor_json_file(input_path, output_path, level):
            success_count += 1
    
    print("=" * 60)
    print(f"HOÀN THÀNH: Đã refactor {success_count}/{len(files_to_process)} file")
    print(f"Kết quả được lưu trong thư mục: {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()

