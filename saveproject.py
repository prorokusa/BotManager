import os
import json
import subprocess

def save_project_structure(root_dir, exclude_dirs):
    project_structure = {}

    def traverse_directory(directory, structure):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                if item in exclude_dirs:
                    structure[item] = None
                else:
                    structure[item] = {}
                    traverse_directory(item_path, structure[item])
            elif os.path.isfile(item_path):
                try:
                    with open(item_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()
                    structure[item] = {
                        "path": item_path,
                        "content": file_content,
                        "description": f"Файл {item} содержит код для {item_path.split('/')[-2] if '/' in item_path else 'корневой директории'}."
                    }
                except UnicodeDecodeError:
                    print(f"Файл {item_path} не может быть прочитан как текст. Пропускаем.")

    traverse_directory(root_dir, project_structure)
    return project_structure

def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def create_requirements_txt():
    subprocess.run(["pip", "freeze", ">", "requirements.txt"], shell=True)

if __name__ == "__main__":
    root_directory = "."  # Текущая директория проекта
    exclude_directories = [".idea", ".venv", ".git","BotForClone", "CloneBots"]
    output_json_file = "project_structure.json"

    project_structure = save_project_structure(root_directory, exclude_directories)
    save_to_json(project_structure, output_json_file)
    create_requirements_txt()
    print(f"Структура проекта сохранена в {output_json_file}")
    print("Файл requirements.txt создан.")