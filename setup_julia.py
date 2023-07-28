import juliapkg

if __name__ == "__main__":
    juliapkg.require_julia("1.8.5")
    juliapkg.add("Jabalizer", "5ba14d91-d028-496b-b148-c0fbc366f709", version="0.4.4")
    juliapkg.add("StatsBase", "2913bbd2-ae8a-5f71-8c99-4fb6c76f3a91", version="0.34.0")
    juliapkg.resolve()
