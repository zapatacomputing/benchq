from typing import Any

import juliapkg

# juliapkg.json is undesirable because you have to put it in the same directory as
# the script that calls it. So we have to check whether the dependencies are already
# installed and if not, install them. When adding a new dependency, you have to
# manually add it to the dependency_dict below as well as the juliapkg.add() call.
required_julia_version = "1.9"
dependency_dict: Any = {
    "julia": "^" + required_julia_version,
    "packages": {
        "JSON": {"uuid": "682c06a0-de6a-54ab-a142-c8b1cf79cde6", "version": "0.21"},
        "Jabalizer": {
            "uuid": "5ba14d91-d028-496b-b148-c0fbc366f709",
            "version": "0.4.4",
        },
        "TimerOutputs": {
            "uuid": "a759f4b9-e2f1-59dc-863e-4aeb61b1ea8f",
            "version": "0.5.23",
        },
        "StatsBase": {
            "uuid": "2913bbd2-ae8a-5f71-8c99-4fb6c76f3a91",
            "version": "0.34.0",
        },
    },
}
curr_deps = juliapkg.deps.load_cur_deps()
if curr_deps != dependency_dict:
    if "julia" not in curr_deps or curr_deps["julia"] != dependency_dict["julia"]:
        print(
            "No suitable Julia installation detected. "
            "Automatically installing Julia " + required_julia_version + "."
        )
    juliapkg.require_julia(required_julia_version)
    print("Installing required Julia dependencies...")
    for pkg_name, pkg_data in dependency_dict["packages"].items():
        juliapkg.add(
            pkg_name,
            pkg_data["uuid"],
            version=pkg_data["version"],
        )


juliapkg.resolve()


# Put this import second because it can install julia automatically and we don't
# want to install julia twice if the julia version that juliacall finds is different
# from the one that juliapkg requires.
from juliacall import Main as jl  # noqa: E402
