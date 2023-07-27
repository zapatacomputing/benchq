window.BENCHMARK_DATA = {
  "lastUpdate": 1690462251912,
  "repoUrl": "https://github.com/zapatacomputing/benchq",
  "entries": {
    "My Project Go Benchmark": [
      {
        "commit": {
          "author": {
            "email": "Sebastian.Morawiec@zapatacomputing.com",
            "name": "Sebastian Morawiec",
            "username": "SebastianMorawiec"
          },
          "committer": {
            "email": "Sebastian.Morawiec@zapatacomputing.com",
            "name": "Sebastian Morawiec",
            "username": "SebastianMorawiec"
          },
          "distinct": true,
          "id": "143fb98e87f0d24d18b47b806b1e5db662544a28",
          "message": "again fix whitespaces....",
          "timestamp": "2023-07-27T14:33:27+02:00",
          "tree_id": "4e21db545399fb9eacf89f39b4772765213c391e",
          "url": "https://github.com/zapatacomputing/benchq/commit/143fb98e87f0d24d18b47b806b1e5db662544a28"
        },
        "date": 1690461586942,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[many single qubit gates]",
            "value": 2.1794608202497034,
            "unit": "iter/sec",
            "range": "stddev: 0.11988177141252593",
            "extra": "mean: 458.82907860001296 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[GHZ state]",
            "value": 658.1863424124368,
            "unit": "iter/sec",
            "range": "stddev: 0.014532573595540221",
            "extra": "mean: 1.5193265729804126 msec\nrounds: 1473"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[Fully connected state]",
            "value": 20.11014211324937,
            "unit": "iter/sec",
            "range": "stddev: 0.07278925630070979",
            "extra": "mean: 49.72615282221997 msec\nrounds: 45"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[CNOT chain]",
            "value": 51.326442513190905,
            "unit": "iter/sec",
            "range": "stddev: 0.00046857811152982984",
            "extra": "mean: 19.483134833336635 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[rotation chain]",
            "value": 400.288587984024,
            "unit": "iter/sec",
            "range": "stddev: 0.015092426095073892",
            "extra": "mean: 2.498197625458938 msec\nrounds: 817"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "Sebastian.Morawiec@zapatacomputing.com",
            "name": "Sebastian Morawiec",
            "username": "SebastianMorawiec"
          },
          "committer": {
            "email": "Sebastian.Morawiec@zapatacomputing.com",
            "name": "Sebastian Morawiec",
            "username": "SebastianMorawiec"
          },
          "distinct": true,
          "id": "942e70fb0462b07011938c9efdb71bc52a16c0f0",
          "message": "test commit to rerun",
          "timestamp": "2023-07-27T14:44:51+02:00",
          "tree_id": "4e21db545399fb9eacf89f39b4772765213c391e",
          "url": "https://github.com/zapatacomputing/benchq/commit/942e70fb0462b07011938c9efdb71bc52a16c0f0"
        },
        "date": 1690462250773,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[many single qubit gates]",
            "value": 2.2981093504472727,
            "unit": "iter/sec",
            "range": "stddev: 0.11286635838412079",
            "extra": "mean: 435.14030339999863 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[GHZ state]",
            "value": 668.3160268765939,
            "unit": "iter/sec",
            "range": "stddev: 0.013976170214408062",
            "extra": "mean: 1.496298098182003 msec\nrounds: 1375"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[Fully connected state]",
            "value": 20.694479340989695,
            "unit": "iter/sec",
            "range": "stddev: 0.059579824085618883",
            "extra": "mean: 48.32206616666568 msec\nrounds: 48"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[CNOT chain]",
            "value": 43.26110131794519,
            "unit": "iter/sec",
            "range": "stddev: 0.022038890299159317",
            "extra": "mean: 23.115454057689206 msec\nrounds: 52"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[rotation chain]",
            "value": 437.2717353769061,
            "unit": "iter/sec",
            "range": "stddev: 0.01346795796880035",
            "extra": "mean: 2.2869074744519 msec\nrounds: 822"
          }
        ]
      }
    ]
  }
}