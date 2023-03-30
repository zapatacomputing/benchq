import juliapkg

if __name__ == "__main__":
    juliapkg.require_julia("1.8")
    juliapkg.add("Jabalizer", "5ba14d91-d028-496b-b148-c0fbc366f709", version="0.4.4")
    juliapkg.resolve()
