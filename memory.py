import pickle

def save_memory(memory, filename="memory.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(memory, f)

def load_memory(filename="memory.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []
