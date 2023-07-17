# from typing import Optional


# class SubroutineModel:
#     def __init__(self, name: str, requirements: Optional[dict] = None, **kwargs):
#         self.name = name
#         self.requirements = requirements or {}
#         # Initialize the subroutine_profile with the subroutines in the kwargs
#         self.subroutine_profile = [
#             (value, None)
#             for attr, value in kwargs.items()
#             if isinstance(value, SubroutineModel)
#         ]

#     def set_requirements(self, *args, **kwargs):
#         """
#         Sets the requirements using the passed arguments. The arguments passed to this method will be automatically
#         converted to a dictionary and stored in the 'requirements' attribute.
#         """

#         # Check for positional arguments
#         if args:
#             raise TypeError(
#                 "The set_requirements method expects keyword arguments of the form argument=value."
#             )

#         self.requirements = kwargs

#     def populate_subroutine_profile(self):
#         # Should decide how to treat this!
#         pass
#         # raise NotImplementedError("This method should be implemented in child classes.")

#     def run_profile(self, requirements=None):
#         self.populate_subroutine_profile()
#         # if requirements is not None:
#         #     self.requirements.update(requirements)
#         for child, _ in self.subroutine_profile:
#             child.run_profile()

#     def print_profile(self, level=0):
#         requirements_str = ", ".join(f"{k}: {v}" for k, v in self.requirements.items())
#         print_str = f"Task: {self.name}, Requirements: {requirements_str}, Subroutine: {type(self)}"
#         print("  " * level + print_str)
#         for child, count in self.subroutine_profile:
#             print("  " * level + f"Count: {count}")
#             child.print_profile(level + 1)

#     def count_subroutines(self):
#         counts = {self.name: 1}
#         for child, count in self.subroutine_profile:
#             child_counts = child.count_subroutines()
#             for name, child_count in child_counts.items():
#                 if name in counts:
#                     counts[name] += child_count * (count if count is not None else 1)
#                 else:
#                     counts[name] = child_count * (count if count is not None else 1)
#         return counts


from typing import Optional


class SubroutineModel:
    def __init__(self, task_name: str, requirements: Optional[dict] = None, **kwargs):
        self.task_name = task_name
        self.requirements = requirements or {}
        self.number_of_times_called = None
        for attr, value in kwargs.items():
            if isinstance(value, SubroutineModel):
                setattr(self, attr, value)

    def set_requirements(self, *args, **kwargs):
        if args:
            raise TypeError(
                "The set_requirements method expects keyword arguments of the form argument=value."
            )
        self.requirements = kwargs

    def populate_requirements_for_subroutines(self):
        pass

    def run_profile(self, requirements=None):
        self.populate_requirements_for_subroutines()
        for attr in dir(self):
            child = getattr(self, attr)
            if isinstance(child, SubroutineModel):
                child.run_profile()

    def print_profile(self, level=0):
        # Format the requirements string to be more readable
        requirements_str = "\n".join(
            "  " * (level + 2) + f"{k}: {v}" for k, v in self.requirements.items()
        )
        print_str = (
            f"{'  ' * level}Subroutine: {type(self).__name__} (Task: {self.task_name})"
        )
        print(print_str)
        if (
            requirements_str.strip()
        ):  # only print "Requirements:" if there are requirements
            print("  " * (level + 1) + "Requirements:")
            print(requirements_str)
        if self.number_of_times_called is not None:
            print("  " * (level + 1) + f"Count: {self.number_of_times_called}")
        # Recurse for child subroutines
        for attr in dir(self):
            child = getattr(self, attr)
            if isinstance(child, SubroutineModel):
                child.print_profile(level + 1)

    def count_subroutines(self):
        counts = {self.task_name: 1}
        for attr in dir(self):
            child = getattr(self, attr)
            if isinstance(child, SubroutineModel):
                child_counts = child.count_subroutines()
                for name, child_count in child_counts.items():
                    if name in counts:
                        counts[name] += child_count * (
                            child.number_of_times_called
                            if child.number_of_times_called is not None
                            else 1
                        )
                    else:
                        counts[name] = child_count * (
                            child.number_of_times_called
                            if child.number_of_times_called is not None
                            else 1
                        )
        return counts
