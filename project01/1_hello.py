import os

def main():
    target_directory = "test"
    file_path = os.path.join(target_directory, "hello.txt")
    content = "Hello Linux"

    os.makedirs(target_directory, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"file creation complete: {file_path}")

if __name__ == "__main__":
    main()
