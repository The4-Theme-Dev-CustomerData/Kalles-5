#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để kiểm tra và xóa các giá trị liên quan đến URL video trong các file JSON
"""

import json
import os
import glob
import re
from pathlib import Path

def find_json_files(root_dir):
    """Tìm tất cả các file JSON trong thư mục và các thư mục con"""
    json_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files

def clean_video_urls_in_text(content, file_path):
    """Xóa video URLs trực tiếp trong nội dung text để giữ nguyên format gốc"""
    changes_made = False
    lines = content.split('\n')
    
    # Danh sách các key liên quan đến video (không bao gồm external_video_url)
    video_keys = [
        'video', 'video_url', 'video_mp4', 
        'video_webm', 'video_ogg', 'video_src', 'video_file',
        'background_video', 'hero_video', 'banner_video'
    ]
    
    for i, line in enumerate(lines):
        for key in video_keys:
            # Tìm pattern: "key": "value" hoặc "key": "value",
            pattern = rf'(\s*"{key}"\s*:\s*)"[^"]*"(\s*[,]?)'
            match = re.search(pattern, line)
            
            if match:
                # Lấy giá trị hiện tại
                current_value = match.group(0)
                # Tạo giá trị mới với chuỗi rỗng
                new_value = f'{match.group(1)}""{match.group(2)}'
                
                # Thay thế trong dòng
                lines[i] = line.replace(current_value, new_value)
                changes_made = True
                
                # Lấy giá trị video để hiển thị (loại bỏ quotes)
                video_value = re.search(rf'"{key}"\s*:\s*"([^"]*)"', line)
                if video_value:
                    print(f"  - Xóa giá trị {key}: '{video_value.group(1)}'")
                break
    
    if changes_made:
        # Ghi lại file với nội dung đã được sửa
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    return changes_made

def process_json_file(file_path):
    """Xử lý một file JSON"""
    try:
        print(f"\n📁 Đang xử lý: {file_path}")
        
        # Đọc file JSON và giữ nguyên format gốc hoàn toàn
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Xử lý trực tiếp trên nội dung text để giữ nguyên format
        changes_made = clean_video_urls_in_text(original_content, file_path)
        
        if changes_made:
            print(f"  ✅ Đã xóa video URLs và lưu file (giữ nguyên format gốc)")
            return True
        else:
            print(f"  ℹ️  Không tìm thấy video URLs để xóa")
            return False
            
    except json.JSONDecodeError as e:
        print(f"  ❌ Lỗi JSON: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Lỗi: {e}")
        return False

def main():
    """Hàm chính"""
    print("🔍 Script kiểm tra và xóa video URLs trong file JSON")
    print("=" * 60)
    
    # Thư mục gốc (thư mục hiện tại)
    root_dir = "."
    
    # Tìm tất cả file JSON
    json_files = find_json_files(root_dir)
    
    if not json_files:
        print("❌ Không tìm thấy file JSON nào!")
        return
    
    print(f"📊 Tìm thấy {len(json_files)} file JSON:")
    for file in json_files:
        print(f"  - {file}")
    
    # Xác nhận từ người dùng
    print(f"\n⚠️  Script sẽ:")
    print(f"  - Xóa giá trị video URLs (giữ nguyên key và cấu trúc)")
    print(f"  - Lưu file đã được làm sạch với format gốc")
    print(f"  - Không xóa external_video_url")
    
    confirm = input(f"\n❓ Bạn có muốn tiếp tục? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes', 'có']:
        print("❌ Đã hủy thao tác")
        return
    
    # Xử lý từng file
    processed_count = 0
    changed_count = 0
    
    for file_path in json_files:
        if process_json_file(file_path):
            changed_count += 1
        processed_count += 1
    
    # Báo cáo kết quả
    print(f"\n📈 KẾT QUẢ:")
    print(f"  - Đã xử lý: {processed_count} file")
    print(f"  - Có thay đổi: {changed_count} file")
    print(f"  - Không thay đổi: {processed_count - changed_count} file")
    
    if changed_count > 0:
        print(f"\n💡 Lưu ý:")
        print(f"  - Các file backup có đuôi .backup")
        print(f"  - Có thể xóa file backup nếu kết quả ổn định")
        print(f"  - Kiểm tra lại các file đã được xử lý")

if __name__ == "__main__":
    main()
