def get_cats_info(path: str) -> list[dict]:
    cats = []

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                try:
                    cat_id, name, age = line.split(",")
                    cats.append({
                        "id": cat_id,
                        "name": name,
                        "age": age
                    })
                except ValueError:
                    raise ValueError("Invalid cats file format. Expected: 'id,name,age'")

        return cats

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
