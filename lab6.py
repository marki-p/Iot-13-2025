import os
import yaml
import logging

#print(os.getcwd())

class FileNotFound(Exception): pass
class FileCorrupted(Exception): pass

def logged(exception_cls, mode):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_cls as e:
                msg = f"Помилка: {e}"
                if mode == "console":
                    logging.basicConfig(level=logging.ERROR, force=True)
                    logging.error(msg)
                elif mode == "file":
                    logging.basicConfig(filename="log.txt", level=logging.ERROR, force=True)
                    logging.error(msg)
                else:
                    raise FileCorrupted("Невірний режим логування")
                raise e 
        return wrapper
    return decorator

class FileManager:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            raise FileNotFound(f"Файл {self.path} не знайдено!")

    @logged(FileCorrupted, mode="console")
    def read_file(self):
        try:
            with open(self.path, "r") as f:
                return yaml.safe_load(f) or []
        except Exception:
            raise FileCorrupted("Не вдалося прочитати файл")

    @logged(FileCorrupted, mode="file")
    def write_file(self, data):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, allow_unicode=True)
        except yaml.YAMLError as e:
            raise FileCorrupted("Не вдалося записати у файл")
        except Exception:
            raise FileCorrupted("Не вдалося записати у файл")

    @logged(FileCorrupted, mode="console")
    def append_file(self, new_data):
        try:
            data = self.read_file()
            if isinstance(data, list):
                data.append(new_data)
            else:
                data = [data, new_data]
            self.write_file(data)
        except Exception:
             raise FileCorrupted("Не вдалося дописати у файл")

if __name__ == "__main__":
    with open("data.yaml", "w") as f: f.write("- apple\n- banana\n")

    try:
        manager = FileManager("data.yaml")
        
        print(manager.read_file())
        
        manager.append_file("orange")
        print(manager.read_file())

        manager.write_file(["new", "list"])
        print(manager.read_file())

        manager.write_file({"error": lambda x: x})
        print(manager.read_file())
        
    except Exception as e:
        print(f"Помилка: {e}")
