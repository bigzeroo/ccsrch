import textract
import os
import zipfile
import tarfile
import gzip
import rarfile
import py7zr
import shutil

'''
写了个大概框架，有时间了把c版的ccsrch用python写完
'''


# Luhn算法验证函数
def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10 == 0

# Visa卡检测函数
def is_visa(card_number):
    return (len(card_number) == 13 or len(card_number) == 16) and card_number.startswith('4')

# MasterCard卡检测函数
def is_mastercard(card_number):
    return len(card_number) == 16 and card_number[:2] in ['51', '52', '53', '54', '55']

# American Express卡检测函数
def is_american_express(card_number):
    return len(card_number) == 15 and card_number[:2] in ['34', '37']

# Discover卡检测函数
def is_discover(card_number):
    return len(card_number) == 16 and card_number.startswith('6011')

# 函数：根据信用卡类型检测卡号
def detect_card_type(card_number):
    if is_visa(card_number):
        return "Visa"
    elif is_mastercard(card_number):
        return "MasterCard"
    elif is_american_express(card_number):
        return "American Express"
    elif is_discover(card_number):
        return "Discover"
    else:
        return None

# 函数：扫描文件内容并检测不同类型的信用卡号
def find_credit_cards_in_text(text):
    valid_cards = {
        "Visa": [],
        "MasterCard": [],
        "American Express": [],
        "Discover": []
    }

    current_digits = []
    for char in text:
        if char.isdigit():
            current_digits.append(char)
        else:
            if 13 <= len(current_digits) <= 19:
                card_number = ''.join(current_digits)
                if luhn_checksum(card_number):
                    card_type = detect_card_type(card_number)
                    if card_type:
                        valid_cards[card_type].append(card_number)
            current_digits = []  # 重置

    if 13 <= len(current_digits) <= 19:
        card_number = ''.join(current_digits)
        if luhn_checksum(card_number):
            card_type = detect_card_type(card_number)
            if card_type:
                valid_cards[card_type].append(card_number)

    return valid_cards

# 函数：从各种文件类型中提取文本
def extract_text_from_file(file_path):
    try:
        text = textract.process(file_path).decode('utf-8')
        return text
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return None

# 函数：扫描压缩文件并解压
def extract_and_scan_compressed_file(file_path, temp_dir):
    # 处理 zip 文件
    if file_path.endswith('.zip'):
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
        except Exception as e:
            print(f"Error extracting zip file {file_path}: {e}")
    
    # 处理 tar.gz 文件
    elif file_path.endswith('.tar.gz') or file_path.endswith('.tgz') or file_path.endswith('.tar'):
        try:
            with tarfile.open(file_path, 'r:*') as tar_ref:
                tar_ref.extractall(temp_dir)
        except Exception as e:
            print(f"Error extracting tar file {file_path}: {e}")

    # 处理 rar 文件
    elif file_path.endswith('.rar'):
        try:
            with rarfile.RarFile(file_path, 'r') as rar_ref:
                rar_ref.extractall(temp_dir)
        except Exception as e:
            print(f"Error extracting rar file {file_path}: {e}")

    # 处理 7z 文件
    elif file_path.endswith('.7z'):
        try:
            with py7zr.SevenZipFile(file_path, 'r') as seven_ref:
                seven_ref.extractall(temp_dir)
        except Exception as e:
            print(f"Error extracting 7z file {file_path}: {e}")
    
    # 处理 gzip 文件
    elif file_path.endswith('.gz'):
        try:
            with gzip.open(file_path, 'rb') as f_in:
                with open(os.path.join(temp_dir, os.path.basename(file_path).replace('.gz', '')), 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        except Exception as e:
            print(f"Error extracting gzip file {file_path}: {e}")

    # 扫描解压后的目录
    scan_directory_for_credit_cards(temp_dir)

# 运行扫描并输出结果
def scan_file_for_credit_cards(file_path):
    print(f"Scanning file: {file_path}")
    text = extract_text_from_file(file_path)
    
    if text is not None:
        valid_cards = find_credit_cards_in_text(text)
        for card_type, cards in valid_cards.items():
            if cards:
                print(f"Found valid {card_type} numbers in {file_path}:")
                for card in cards:
                    print(f"- {card}")
        if all(len(cards) == 0 for cards in valid_cards.values()):
            print(f"No valid credit card numbers found in {file_path}.")
    else:
        print(f"Unable to extract text from {file_path}")

# 扫描文件目录中所有支持的文件类型（递归扫描）
def scan_directory_for_credit_cards(directory):
    supported_extensions = ['.pdf', '.docx', '.xlsx', '.pptx', '.txt']  # 可支持更多格式
    compressed_extensions = ['.zip', '.tar.gz', '.tgz', '.rar', '.7z', '.gz']  # 压缩文件格式
    temp_dir = 'temp_extracted'  # 用于存放解压缩文件的临时目录

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            # 处理支持的文件类型
            if any(file.endswith(ext) for ext in supported_extensions):
                scan_file_for_credit_cards(file_path)
            
            # 处理压缩文件
            elif any(file.endswith(ext) for ext in compressed_extensions):
                extract_and_scan_compressed_file(file_path, temp_dir)

    # 删除临时目录
    shutil.rmtree(temp_dir)

# 示例：扫描指定目录
directory_to_scan = 'your_directory'  # 替换为要扫描的目录路径
scan_directory_for_credit_cards(directory_to_scan)
