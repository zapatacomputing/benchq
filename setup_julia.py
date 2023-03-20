import juliapkg


if __name__ == "__main__":
    juliapkg.require_julia("1.8")
    juliapkg.add("Jabalizer", "5ba14d91-d028-496b-b148-c0fbc366f709", version="0.4.3")
    juliapkg.add("JSON", "682c06a0-de6a-54ab-a142-c8b1cf79cde6", version="0.21.3")

    juliapkg.resolve()
