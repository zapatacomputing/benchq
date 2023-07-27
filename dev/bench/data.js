window.BENCHMARK_DATA = {
  "lastUpdate": 1690467503294,
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
          "id": "fb02338e1a4429ba32cae0dd6a7b615876fb8b06",
          "message": "change ref to sub workflow, reduce permissions",
          "timestamp": "2023-07-27T16:13:24+02:00",
          "tree_id": "abda40092767503d0cd8f698169c365bcd078c9c",
          "url": "https://github.com/zapatacomputing/benchq/commit/fb02338e1a4429ba32cae0dd6a7b615876fb8b06"
        },
        "date": 1690467502754,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[many single qubit gates]",
            "value": 2.813128228499203,
            "unit": "iter/sec",
            "range": "stddev: 0.0852747423699998",
            "extra": "mean: 355.47615280000855 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[GHZ state]",
            "value": 936.3502825456305,
            "unit": "iter/sec",
            "range": "stddev: 0.009462950462756114",
            "extra": "mean: 1.0679763958433661 msec\nrounds: 1877"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[Fully connected state]",
            "value": 25.207556075846746,
            "unit": "iter/sec",
            "range": "stddev: 0.0464576551959406",
            "extra": "mean: 39.67064466666704 msec\nrounds: 54"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[CNOT chain]",
            "value": 58.76605270379395,
            "unit": "iter/sec",
            "range": "stddev: 0.0037013902630292717",
            "extra": "mean: 17.016627014926932 msec\nrounds: 67"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[rotation chain]",
            "value": 547.955413210515,
            "unit": "iter/sec",
            "range": "stddev: 0.010063235257844536",
            "extra": "mean: 1.8249660025090717 msec\nrounds: 1196"
          }
        ]
      }
    ]
  }
}