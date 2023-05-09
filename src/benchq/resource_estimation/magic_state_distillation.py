def get_specs_for_t_state_widget(
    widget_name: str = "(15-to-1)_7,3,3", hardwdare_type: str = "ions"
):
    widget_lookup_table = {
        "ions": [
            {
                "widget_choice": "(15-to-1)_7,3,3",
                "p_out": 4.4e-8,
                "space": (30, 27),
                "qubits": 810,
                "time": 18.1,
            },
            {
                "widget_choice": "(15-to-1)_9,3,3",
                "p_out": 9.3e-10,
                "space": (38, 30),
                "qubits": 1150,
                "time": 18.1,
            },
            {
                "widget_choice": "(15-to-1)_11,5,5",
                "p_out": 1.9e-11,
                "space": (47, 44),
                "qubits": 2070,
                "time": 30,
            },
            {
                "widget_choice": "(15-to-1)^4_9,3,3 x (20-to-4)_15,7,9",
                "p_out": 2.4e-15,
                "space": (221, 96),
                "qubits": 16400,
                "time": 90.3,
            },
            {
                "widget_choice": "(15-to-1)^4_9,3,3 x (15-to-1)_25,9,9",
                "p_out": 6.3e-25,
                "space": (193, 96),
                "qubits": 18600,
                "time": 67.8,
            },
        ],
        "sc": [
            {
                "widget_choice": "(15-to-1)_17,7,7",
                "p_out": 4.5e-8,
                "space": (72, 64),
                "qubits": 4620,
                "time": 42.6,
            },
            {
                "widget_choice": "(15-to-1)^6_15,5,5 x (20-to-4)_23,11,13",
                "p_out": 1.4e-10,
                "space": (387, 155),
                "qubits": 43300,
                "time": 130,
            },
            {
                "widget_choice": "(15-to-1)^4_13,5,5 x (20-to-4)_27,13,15",
                "p_out": 2.6e-11,
                "space": (382, 142),
                "qubits": 46800,
                "time": 157,
            },
            {
                "widget_choice": "(15-to-1)^6_11,5,5 x (15-to-1)_25,11,11",
                "p_out": 2.7e-12,
                "space": (279, 117),
                "qubits": 30700,
                "time": 82.5,
            },
            {
                "widget_choice": "(15-to-1)^6_13,5,5 x (15-to-1)_29,11,13",
                "p_out": 3.3e-14,
                "space": (292, 138),
                "qubits": 39100,
                "time": 97.5,
            },
            {
                "widget_choice": "(15-to-1)^6_17,7,7 x (15-to-1)_41,17,17",
                "p_out": 4.5e-20,
                "space": (426, 181),
                "qubits": 73400,
                "time": 128,
            },
        ],
    }

    for widget_dict in widget_lookup_table[hardwdare_type]:
        if widget_dict.get("widget_choice") == widget_name:
            widget_specs = widget_dict
            break

    return widget_specs
