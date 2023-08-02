window.BENCHMARK_DATA = {
  "lastUpdate": 1691013924457,
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
          "id": "aba307b8b5910bb062a59db697ceeb07ce810850",
          "message": "lauch all the tests",
          "timestamp": "2023-07-27T17:17:49+02:00",
          "tree_id": "b6d7bde3faeeb7931e7a62d04c84bf5bc905b506",
          "url": "https://github.com/zapatacomputing/benchq/commit/aba307b8b5910bb062a59db697ceeb07ce810850"
        },
        "date": 1690471497563,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[vlasov]",
            "value": 137.61817380117148,
            "unit": "iter/sec",
            "range": "stddev: 0.00012168329829401611",
            "extra": "mean: 7.266482124990148 msec\nrounds: 8"
          },
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[jw-2]",
            "value": 3.8985870864658305,
            "unit": "iter/sec",
            "range": "stddev: 0.05327592099891528",
            "extra": "mean: 256.5031837999868 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[many single qubit gates]",
            "value": 2.9775711351615426,
            "unit": "iter/sec",
            "range": "stddev: 0.12504018557916938",
            "extra": "mean: 335.8442013999934 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[GHZ state]",
            "value": 841.4666493023861,
            "unit": "iter/sec",
            "range": "stddev: 0.010816179402543745",
            "extra": "mean: 1.1884012287700827 msec\nrounds: 1731"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[Fully connected state]",
            "value": 26.651856917879456,
            "unit": "iter/sec",
            "range": "stddev: 0.05435051527220104",
            "extra": "mean: 37.52083778181879 msec\nrounds: 55"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[CNOT chain]",
            "value": 57.3233423912226,
            "unit": "iter/sec",
            "range": "stddev: 0.00787438103671222",
            "extra": "mean: 17.444900424248825 msec\nrounds: 66"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[rotation chain]",
            "value": 586.8797978740228,
            "unit": "iter/sec",
            "range": "stddev: 0.01101003510846709",
            "extra": "mean: 1.7039264319925627 msec\nrounds: 1044"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-fast]",
            "value": 6947.514136181576,
            "unit": "iter/sec",
            "range": "stddev: 0.000012038373329925678",
            "extra": "mean: 143.936374996656 usec\nrounds: 8"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-optimized]",
            "value": 4369.098900814838,
            "unit": "iter/sec",
            "range": "stddev: 0.00001737596531489411",
            "extra": "mean: 228.88014730302845 usec\nrounds: 1446"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-fast]",
            "value": 3690.8332544199507,
            "unit": "iter/sec",
            "range": "stddev: 0.000013477560312165927",
            "extra": "mean: 270.941527581191 usec\nrounds: 3118"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-optimized]",
            "value": 3131.262691450344,
            "unit": "iter/sec",
            "range": "stddev: 0.00001469687073609175",
            "extra": "mean: 319.3599830287053 usec\nrounds: 2357"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-fast]",
            "value": 6927.638188462186,
            "unit": "iter/sec",
            "range": "stddev: 0.000012304195849182003",
            "extra": "mean: 144.34933996199106 usec\nrounds: 5280"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-optimized]",
            "value": 3708.5034681501947,
            "unit": "iter/sec",
            "range": "stddev: 0.000016698339647852973",
            "extra": "mean: 269.6505500367783 usec\nrounds: 2658"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-fast]",
            "value": 5862.7070335940225,
            "unit": "iter/sec",
            "range": "stddev: 0.0000123325033818761",
            "extra": "mean: 170.56966931314813 usec\nrounds: 4660"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-optimized]",
            "value": 4027.997115222479,
            "unit": "iter/sec",
            "range": "stddev: 0.000014365219818881155",
            "extra": "mean: 248.26234264687818 usec\nrounds: 2863"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-fast]",
            "value": 1012.8384880366242,
            "unit": "iter/sec",
            "range": "stddev: 0.00005583821560060745",
            "extra": "mean: 987.3242494353553 usec\nrounds: 882"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-optimized]",
            "value": 415.0531526803948,
            "unit": "iter/sec",
            "range": "stddev: 0.0003816566556379981",
            "extra": "mean: 2.409329970250905 msec\nrounds: 437"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-fast]",
            "value": 51.380640165083435,
            "unit": "iter/sec",
            "range": "stddev: 0.00008393803159479092",
            "extra": "mean: 19.462583509801547 msec\nrounds: 51"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-optimized]",
            "value": 50.36372399432317,
            "unit": "iter/sec",
            "range": "stddev: 0.0000852401088277066",
            "extra": "mean: 19.85556111999813 msec\nrounds: 50"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-fast]",
            "value": 1005.4605158677355,
            "unit": "iter/sec",
            "range": "stddev: 0.000005268069786274503",
            "extra": "mean: 994.5691394325684 usec\nrounds: 918"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-optimized]",
            "value": 326.6941513873056,
            "unit": "iter/sec",
            "range": "stddev: 0.0000738790597928051",
            "extra": "mean: 3.0609669495260423 msec\nrounds: 317"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-fast]",
            "value": 729.3836227838821,
            "unit": "iter/sec",
            "range": "stddev: 0.00008196416369222791",
            "extra": "mean: 1.3710206381975514 msec\nrounds: 644"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-optimized]",
            "value": 358.44645688526793,
            "unit": "iter/sec",
            "range": "stddev: 0.00038597082715560054",
            "extra": "mean: 2.7898169469703573 msec\nrounds: 396"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-fast]",
            "value": 85.86207888406885,
            "unit": "iter/sec",
            "range": "stddev: 0.02055002833057002",
            "extra": "mean: 11.646584999999849 msec\nrounds: 98"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-optimized]",
            "value": 15.910051762920263,
            "unit": "iter/sec",
            "range": "stddev: 0.012698145384524866",
            "extra": "mean: 62.85334673332652 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-fast]",
            "value": 0.4784712451753009,
            "unit": "iter/sec",
            "range": "stddev: 0.007869383399441226",
            "extra": "mean: 2.0899897539999985 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-optimized]",
            "value": 0.47763059283677906,
            "unit": "iter/sec",
            "range": "stddev: 0.009777945743088566",
            "extra": "mean: 2.0936682343999906 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-fast]",
            "value": 55.470700584761744,
            "unit": "iter/sec",
            "range": "stddev: 0.08609802888355751",
            "extra": "mean: 18.027535067309177 msec\nrounds: 104"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-optimized]",
            "value": 11.855932974285249,
            "unit": "iter/sec",
            "range": "stddev: 0.0014663892402020826",
            "extra": "mean: 84.34595591666512 msec\nrounds: 12"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-fast]",
            "value": 63.86585943241936,
            "unit": "iter/sec",
            "range": "stddev: 0.0203047746196384",
            "extra": "mean: 15.65781794666312 msec\nrounds: 75"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-optimized]",
            "value": 13.707042538406942,
            "unit": "iter/sec",
            "range": "stddev: 0.03659365745844604",
            "extra": "mean: 72.95519782608203 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-fast]",
            "value": 7403.048975269851,
            "unit": "iter/sec",
            "range": "stddev: 0.000010698898018998222",
            "extra": "mean: 135.07947919033572 usec\nrounds: 5286"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-optimized]",
            "value": 4415.883098080081,
            "unit": "iter/sec",
            "range": "stddev: 0.000016429278671738122",
            "extra": "mean: 226.45527016663453 usec\nrounds: 3124"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-fast]",
            "value": 3700.5606425914593,
            "unit": "iter/sec",
            "range": "stddev: 0.00001329108908948879",
            "extra": "mean: 270.229323765307 usec\nrounds: 2369"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-optimized]",
            "value": 3142.313259479897,
            "unit": "iter/sec",
            "range": "stddev: 0.000014065503620751434",
            "extra": "mean: 318.2368902855713 usec\nrounds: 2306"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-fast]",
            "value": 6918.312681166747,
            "unit": "iter/sec",
            "range": "stddev: 0.000012140315902552029",
            "extra": "mean: 144.54391498121097 usec\nrounds: 5587"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-optimized]",
            "value": 3719.8851524087067,
            "unit": "iter/sec",
            "range": "stddev: 0.000016080564458908513",
            "extra": "mean: 268.82550375311405 usec\nrounds: 2664"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-fast]",
            "value": 5857.053184828965,
            "unit": "iter/sec",
            "range": "stddev: 0.000012264473317400839",
            "extra": "mean: 170.73432124369577 usec\nrounds: 4632"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-optimized]",
            "value": 4041.5126449833388,
            "unit": "iter/sec",
            "range": "stddev: 0.000013776765724582687",
            "extra": "mean: 247.43210966846362 usec\nrounds: 2234"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-fast]",
            "value": 1004.9016033458358,
            "unit": "iter/sec",
            "range": "stddev: 0.00006070326264203495",
            "extra": "mean: 995.1223051794167 usec\nrounds: 888"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-optimized]",
            "value": 424.1296040225007,
            "unit": "iter/sec",
            "range": "stddev: 0.0003427249767577753",
            "extra": "mean: 2.357769866842279 msec\nrounds: 383"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-fast]",
            "value": 51.755288105708885,
            "unit": "iter/sec",
            "range": "stddev: 0.00007383458211820357",
            "extra": "mean: 19.32169709803421 msec\nrounds: 51"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-optimized]",
            "value": 51.13926882962759,
            "unit": "iter/sec",
            "range": "stddev: 0.00010037711646782947",
            "extra": "mean: 19.554444615380362 msec\nrounds: 52"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-fast]",
            "value": 1005.2383243742242,
            "unit": "iter/sec",
            "range": "stddev: 0.000004908660640121118",
            "extra": "mean: 994.7889726772154 usec\nrounds: 915"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-optimized]",
            "value": 328.7970848461915,
            "unit": "iter/sec",
            "range": "stddev: 0.0000779959348147209",
            "extra": "mean: 3.0413894954932204 msec\nrounds: 333"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-fast]",
            "value": 727.7717176469242,
            "unit": "iter/sec",
            "range": "stddev: 0.0000833805734615206",
            "extra": "mean: 1.3740572431603426 msec\nrounds: 658"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-optimized]",
            "value": 360.92053139949064,
            "unit": "iter/sec",
            "range": "stddev: 0.00039112491880655007",
            "extra": "mean: 2.7706930279705646 msec\nrounds: 286"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-fast]",
            "value": 86.8655743714335,
            "unit": "iter/sec",
            "range": "stddev: 0.020076161543252945",
            "extra": "mean: 11.512040382350351 msec\nrounds: 102"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-optimized]",
            "value": 18.14409815695898,
            "unit": "iter/sec",
            "range": "stddev: 0.012001184118431088",
            "extra": "mean: 55.11434028571216 msec\nrounds: 14"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-fast]",
            "value": 0.4795800582005082,
            "unit": "iter/sec",
            "range": "stddev: 0.00491038002373218",
            "extra": "mean: 2.0851575933999924 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-optimized]",
            "value": 0.4782602597418002,
            "unit": "iter/sec",
            "range": "stddev: 0.010164461548364503",
            "extra": "mean: 2.090911756999992 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-fast]",
            "value": 53.30028439793336,
            "unit": "iter/sec",
            "range": "stddev: 0.09252177433199846",
            "extra": "mean: 18.76162597058813 msec\nrounds: 102"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-optimized]",
            "value": 12.04746758945844,
            "unit": "iter/sec",
            "range": "stddev: 0.00046577230553646807",
            "extra": "mean: 83.00499607693504 msec\nrounds: 13"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-fast]",
            "value": 62.420462813258425,
            "unit": "iter/sec",
            "range": "stddev: 0.021664313744827864",
            "extra": "mean: 16.02038746479135 msec\nrounds: 71"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-optimized]",
            "value": 18.072933475368174,
            "unit": "iter/sec",
            "range": "stddev: 0.007430251340635164",
            "extra": "mean: 55.331360642859245 msec\nrounds: 14"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-fast]",
            "value": 1659.6127289967433,
            "unit": "iter/sec",
            "range": "stddev: 0.000024018715050086565",
            "extra": "mean: 602.550210978746 usec\nrounds: 1512"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-optimized]",
            "value": 1295.8353690484867,
            "unit": "iter/sec",
            "range": "stddev: 0.00003036351494403936",
            "extra": "mean: 771.7029677421799 usec\nrounds: 1147"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-fast]",
            "value": 25.28709781883952,
            "unit": "iter/sec",
            "range": "stddev: 0.0002008035061820593",
            "extra": "mean: 39.5458588076871 msec\nrounds: 26"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-optimized]",
            "value": 20.656204919618883,
            "unit": "iter/sec",
            "range": "stddev: 0.04127688196588866",
            "extra": "mean: 48.41160338461874 msec\nrounds: 26"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-fast]",
            "value": 683.1033103057825,
            "unit": "iter/sec",
            "range": "stddev: 0.0000864820049945354",
            "extra": "mean: 1.4639074132906233 msec\nrounds: 617"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-optimized]",
            "value": 344.6794031804408,
            "unit": "iter/sec",
            "range": "stddev: 0.0003530719011568727",
            "extra": "mean: 2.901246755021497 msec\nrounds: 249"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-fast]",
            "value": 24.45342745557461,
            "unit": "iter/sec",
            "range": "stddev: 0.0005711383716050922",
            "extra": "mean: 40.89406288000873 msec\nrounds: 25"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-optimized]",
            "value": 23.13668107522203,
            "unit": "iter/sec",
            "range": "stddev: 0.0005581315166785382",
            "extra": "mean: 43.22141091666509 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-fast]",
            "value": 13598.709191542674,
            "unit": "iter/sec",
            "range": "stddev: 0.000008579140183779661",
            "extra": "mean: 73.53639127910179 usec\nrounds: 8577"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-optimized]",
            "value": 4757.147148615942,
            "unit": "iter/sec",
            "range": "stddev: 0.000009482438004250166",
            "extra": "mean: 210.21002057734182 usec\nrounds: 3256"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-fast]",
            "value": 1445.4028969126475,
            "unit": "iter/sec",
            "range": "stddev: 0.00003613439618449059",
            "extra": "mean: 691.8486202954073 usec\nrounds: 1222"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-optimized]",
            "value": 344.1902661570059,
            "unit": "iter/sec",
            "range": "stddev: 0.0005648583327220683",
            "extra": "mean: 2.9053697862095835 msec\nrounds: 290"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-fast]",
            "value": 7873.635813071656,
            "unit": "iter/sec",
            "range": "stddev: 0.000012044314113390663",
            "extra": "mean: 127.0061282666668 usec\nrounds: 5855"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-optimized]",
            "value": 4295.77413150624,
            "unit": "iter/sec",
            "range": "stddev: 0.000017299019719672677",
            "extra": "mean: 232.78691322845856 usec\nrounds: 3054"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-fast]",
            "value": 373.562617860251,
            "unit": "iter/sec",
            "range": "stddev: 0.00011117129555032969",
            "extra": "mean: 2.676927380282194 msec\nrounds: 355"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-optimized]",
            "value": 268.503056211947,
            "unit": "iter/sec",
            "range": "stddev: 0.0003104694626746444",
            "extra": "mean: 3.724352393257806 msec\nrounds: 267"
          }
        ]
      }
    ],
    "Benchq Benchmarking": [
      {
        "commit": {
          "author": {
            "name": "Sebastian Morawiec",
            "username": "SebastianMorawiec",
            "email": "Sebastian.Morawiec@zapatacomputing.com"
          },
          "committer": {
            "name": "Sebastian Morawiec",
            "username": "SebastianMorawiec",
            "email": "Sebastian.Morawiec@zapatacomputing.com"
          },
          "id": "4aa32d409abe2c6fcd86910c9709fb94f6e3044d",
          "message": "fix ref",
          "timestamp": "2023-07-31T10:34:16Z",
          "url": "https://github.com/zapatacomputing/benchq/commit/4aa32d409abe2c6fcd86910c9709fb94f6e3044d"
        },
        "date": 1690800112485,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[vlasov]",
            "value": 134.01370944930844,
            "unit": "iter/sec",
            "range": "stddev: 0.00017747382672251338",
            "extra": "mean: 7.4619231428576835 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[jw-2]",
            "value": 3.7367233313879997,
            "unit": "iter/sec",
            "range": "stddev: 0.07044931599268081",
            "extra": "mean: 267.6141398000027 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[many single qubit gates]",
            "value": 2.4137585830383728,
            "unit": "iter/sec",
            "range": "stddev: 0.1616294672429198",
            "extra": "mean: 414.29163919998473 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[GHZ state]",
            "value": 729.5528443710822,
            "unit": "iter/sec",
            "range": "stddev: 0.013081862222648899",
            "extra": "mean: 1.3707026265685516 msec\nrounds: 1754"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[Fully connected state]",
            "value": 23.05335077815371,
            "unit": "iter/sec",
            "range": "stddev: 0.0743539212597972",
            "extra": "mean: 43.37764213207741 msec\nrounds: 53"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[CNOT chain]",
            "value": 55.46827289401139,
            "unit": "iter/sec",
            "range": "stddev: 0.008380598010538361",
            "extra": "mean: 18.028324081962978 msec\nrounds: 61"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[rotation chain]",
            "value": 468.0215021364041,
            "unit": "iter/sec",
            "range": "stddev: 0.013775047868635225",
            "extra": "mean: 2.1366539687498194 msec\nrounds: 928"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-fast]",
            "value": 7325.3028618495455,
            "unit": "iter/sec",
            "range": "stddev: 0.000013025861526078274",
            "extra": "mean: 136.51312701458912 usec\nrounds: 3661"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-optimized]",
            "value": 4287.336551222566,
            "unit": "iter/sec",
            "range": "stddev: 0.000018751666299766714",
            "extra": "mean: 233.2450434092566 usec\nrounds: 1267"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-fast]",
            "value": 3512.1001429411926,
            "unit": "iter/sec",
            "range": "stddev: 0.00001610154047625989",
            "extra": "mean: 284.7299220695212 usec\nrounds: 2823"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-optimized]",
            "value": 2971.3552821631674,
            "unit": "iter/sec",
            "range": "stddev: 0.0000181151145766669",
            "extra": "mean: 336.54676234879355 usec\nrounds: 2146"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-fast]",
            "value": 6853.807280089172,
            "unit": "iter/sec",
            "range": "stddev: 0.000013334707009132444",
            "extra": "mean: 145.9043067792518 usec\nrounds: 4971"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-optimized]",
            "value": 3630.3915137211407,
            "unit": "iter/sec",
            "range": "stddev: 0.000017074872339344257",
            "extra": "mean: 275.45238474155724 usec\nrounds: 2451"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-fast]",
            "value": 5742.962260051711,
            "unit": "iter/sec",
            "range": "stddev: 0.000013529308902938163",
            "extra": "mean: 174.1261660303851 usec\nrounds: 4457"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-optimized]",
            "value": 3871.602215012523,
            "unit": "iter/sec",
            "range": "stddev: 0.00001653842028251215",
            "extra": "mean: 258.29099800656184 usec\nrounds: 2507"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-fast]",
            "value": 951.2487677518425,
            "unit": "iter/sec",
            "range": "stddev: 0.00006826962183893965",
            "extra": "mean: 1.0512497192121204 msec\nrounds: 812"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-optimized]",
            "value": 396.04805871995444,
            "unit": "iter/sec",
            "range": "stddev: 0.00038060443481528826",
            "extra": "mean: 2.5249460967743307 msec\nrounds: 434"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-fast]",
            "value": 46.72995873692269,
            "unit": "iter/sec",
            "range": "stddev: 0.00008183491501668768",
            "extra": "mean: 21.39954810638151 msec\nrounds: 47"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-optimized]",
            "value": 45.805221084230155,
            "unit": "iter/sec",
            "range": "stddev: 0.00013754912794098736",
            "extra": "mean: 21.8315723913028 msec\nrounds: 46"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-fast]",
            "value": 947.0313584063928,
            "unit": "iter/sec",
            "range": "stddev: 0.00001365732253362193",
            "extra": "mean: 1.0559312435891666 msec\nrounds: 858"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-optimized]",
            "value": 313.09105919841807,
            "unit": "iter/sec",
            "range": "stddev: 0.00006602514958453999",
            "extra": "mean: 3.193958979730114 msec\nrounds: 296"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-fast]",
            "value": 678.4978623501488,
            "unit": "iter/sec",
            "range": "stddev: 0.00009476159086152947",
            "extra": "mean: 1.4738439949335247 msec\nrounds: 592"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-optimized]",
            "value": 279.4700210613472,
            "unit": "iter/sec",
            "range": "stddev: 0.01193228619030424",
            "extra": "mean: 3.578201326218412 msec\nrounds: 328"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-fast]",
            "value": 98.3980698930198,
            "unit": "iter/sec",
            "range": "stddev: 0.00006463353795061819",
            "extra": "mean: 10.162800968425689 msec\nrounds: 95"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-optimized]",
            "value": 13.090729793611153,
            "unit": "iter/sec",
            "range": "stddev: 0.05052209528406693",
            "extra": "mean: 76.38993514999015 msec\nrounds: 20"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-fast]",
            "value": 0.4077669361160626,
            "unit": "iter/sec",
            "range": "stddev: 0.014153723868170575",
            "extra": "mean: 2.452381278199982 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-optimized]",
            "value": 0.4108473016161154,
            "unit": "iter/sec",
            "range": "stddev: 0.013564550382081974",
            "extra": "mean: 2.4339943235999955 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-fast]",
            "value": 40.077347276377935,
            "unit": "iter/sec",
            "range": "stddev: 0.14432387863783777",
            "extra": "mean: 24.95175124999882 msec\nrounds: 96"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-optimized]",
            "value": 9.647978167501893,
            "unit": "iter/sec",
            "range": "stddev: 0.017876892844268508",
            "extra": "mean: 103.64865909091557 msec\nrounds: 11"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-fast]",
            "value": 58.4159495073594,
            "unit": "iter/sec",
            "range": "stddev: 0.02290857015619984",
            "extra": "mean: 17.118612441179568 msec\nrounds: 68"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-optimized]",
            "value": 12.312681067087283,
            "unit": "iter/sec",
            "range": "stddev: 0.04999922318239524",
            "extra": "mean: 81.21707973684747 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-fast]",
            "value": 7348.182497669038,
            "unit": "iter/sec",
            "range": "stddev: 0.000012115107399741144",
            "extra": "mean: 136.08807352256372 usec\nrounds: 4706"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-optimized]",
            "value": 4269.014276581186,
            "unit": "iter/sec",
            "range": "stddev: 0.00001917762100833426",
            "extra": "mean: 234.24611285227277 usec\nrounds: 2552"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-fast]",
            "value": 3501.0554634191903,
            "unit": "iter/sec",
            "range": "stddev: 0.000016622893710811683",
            "extra": "mean: 285.6281514099131 usec\nrounds: 2305"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-optimized]",
            "value": 2943.136713455937,
            "unit": "iter/sec",
            "range": "stddev: 0.000019056804049447613",
            "extra": "mean: 339.77354685157115 usec\nrounds: 2017"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-fast]",
            "value": 6795.228083241441,
            "unit": "iter/sec",
            "range": "stddev: 0.000013896436901874026",
            "extra": "mean: 147.16209489218247 usec\nrounds: 4953"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-optimized]",
            "value": 3598.3359246153454,
            "unit": "iter/sec",
            "range": "stddev: 0.000018535063930621493",
            "extra": "mean: 277.90623803609935 usec\nrounds: 2424"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-fast]",
            "value": 5709.611185001609,
            "unit": "iter/sec",
            "range": "stddev: 0.000014045974509274216",
            "extra": "mean: 175.14327466410802 usec\nrounds: 3051"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-optimized]",
            "value": 3868.4606742749575,
            "unit": "iter/sec",
            "range": "stddev: 0.000016413913144315964",
            "extra": "mean: 258.5007537106278 usec\nrounds: 2627"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-fast]",
            "value": 958.2126176318375,
            "unit": "iter/sec",
            "range": "stddev: 0.000059345101161706055",
            "extra": "mean: 1.0436097183435524 msec\nrounds: 845"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-optimized]",
            "value": 395.10774628946865,
            "unit": "iter/sec",
            "range": "stddev: 0.0003871325709161564",
            "extra": "mean: 2.530955187265217 msec\nrounds: 267"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-fast]",
            "value": 46.66278887394901,
            "unit": "iter/sec",
            "range": "stddev: 0.0000804403312102637",
            "extra": "mean: 21.430352195650308 msec\nrounds: 46"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-optimized]",
            "value": 46.16151114154487,
            "unit": "iter/sec",
            "range": "stddev: 0.00009023215610405114",
            "extra": "mean: 21.663068978259915 msec\nrounds: 46"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-fast]",
            "value": 951.0319674318954,
            "unit": "iter/sec",
            "range": "stddev: 0.000006359747185653959",
            "extra": "mean: 1.051489365494553 msec\nrounds: 881"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-optimized]",
            "value": 313.03713989782585,
            "unit": "iter/sec",
            "range": "stddev: 0.00005953833328428117",
            "extra": "mean: 3.1945091254232527 msec\nrounds: 295"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-fast]",
            "value": 680.0684271857385,
            "unit": "iter/sec",
            "range": "stddev: 0.00009171418901270857",
            "extra": "mean: 1.4704402675157313 msec\nrounds: 628"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-optimized]",
            "value": 341.6616284348032,
            "unit": "iter/sec",
            "range": "stddev: 0.0003999815247508755",
            "extra": "mean: 2.92687242808369 msec\nrounds: 292"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-fast]",
            "value": 97.21831566613146,
            "unit": "iter/sec",
            "range": "stddev: 0.0000980588754983617",
            "extra": "mean: 10.286127600011241 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-optimized]",
            "value": 14.306704566320942,
            "unit": "iter/sec",
            "range": "stddev: 0.01603170974456551",
            "extra": "mean: 69.89729852631997 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-fast]",
            "value": 0.40473214183369866,
            "unit": "iter/sec",
            "range": "stddev: 0.008606055218807035",
            "extra": "mean: 2.470769915799997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-optimized]",
            "value": 0.4091558226553072,
            "unit": "iter/sec",
            "range": "stddev: 0.004370697972787479",
            "extra": "mean: 2.4440566273999935 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-fast]",
            "value": 38.67395524066531,
            "unit": "iter/sec",
            "range": "stddev: 0.1505501584338218",
            "extra": "mean: 25.857194946238888 msec\nrounds: 93"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-optimized]",
            "value": 10.467515826505474,
            "unit": "iter/sec",
            "range": "stddev: 0.00045201543049266826",
            "extra": "mean: 95.53365063636545 msec\nrounds: 11"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-fast]",
            "value": 49.624214940188104,
            "unit": "iter/sec",
            "range": "stddev: 0.03315350742459337",
            "extra": "mean: 20.151452294112794 msec\nrounds: 68"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-optimized]",
            "value": 12.826966832958966,
            "unit": "iter/sec",
            "range": "stddev: 0.017820373165205107",
            "extra": "mean: 77.96075354545192 msec\nrounds: 11"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-fast]",
            "value": 1549.4539043182506,
            "unit": "iter/sec",
            "range": "stddev: 0.000028732265853463327",
            "extra": "mean: 645.3886735275248 usec\nrounds: 1409"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-optimized]",
            "value": 1190.1551899006924,
            "unit": "iter/sec",
            "range": "stddev: 0.000031233226389020876",
            "extra": "mean: 840.2265590955756 usec\nrounds: 973"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-fast]",
            "value": 22.915778258889837,
            "unit": "iter/sec",
            "range": "stddev: 0.00018820067019899837",
            "extra": "mean: 43.63805534782851 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-optimized]",
            "value": 22.35127031554763,
            "unit": "iter/sec",
            "range": "stddev: 0.00047991143035359924",
            "extra": "mean: 44.740186391303055 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-fast]",
            "value": 635.7276424584473,
            "unit": "iter/sec",
            "range": "stddev: 0.00009925502658179312",
            "extra": "mean: 1.5730006581637077 msec\nrounds: 588"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-optimized]",
            "value": 321.2241866792171,
            "unit": "iter/sec",
            "range": "stddev: 0.0003924166034447323",
            "extra": "mean: 3.1130906123162703 msec\nrounds: 276"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-fast]",
            "value": 22.221702189500085,
            "unit": "iter/sec",
            "range": "stddev: 0.00016854072544490294",
            "extra": "mean: 45.001053090906204 msec\nrounds: 22"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-optimized]",
            "value": 20.729064104994503,
            "unit": "iter/sec",
            "range": "stddev: 0.0007543838390053481",
            "extra": "mean: 48.241444714286835 msec\nrounds: 21"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-fast]",
            "value": 13890.67650133941,
            "unit": "iter/sec",
            "range": "stddev: 0.000009119822067814243",
            "extra": "mean: 71.99073420963873 usec\nrounds: 8518"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-optimized]",
            "value": 4677.480791831089,
            "unit": "iter/sec",
            "range": "stddev: 0.000010353617827369337",
            "extra": "mean: 213.79029535437834 usec\nrounds: 2949"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-fast]",
            "value": 1360.040630829385,
            "unit": "iter/sec",
            "range": "stddev: 0.000041913595733423946",
            "extra": "mean: 735.2721509431497 usec\nrounds: 1166"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-optimized]",
            "value": 333.8939262248177,
            "unit": "iter/sec",
            "range": "stddev: 0.0005544453551983531",
            "extra": "mean: 2.9949631348690047 msec\nrounds: 304"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-fast]",
            "value": 7840.76983306053,
            "unit": "iter/sec",
            "range": "stddev: 0.000012822598992196455",
            "extra": "mean: 127.53849702149269 usec\nrounds: 5708"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-optimized]",
            "value": 4141.864633315433,
            "unit": "iter/sec",
            "range": "stddev: 0.000018724001355611775",
            "extra": "mean: 241.43715174958078 usec\nrounds: 2715"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-fast]",
            "value": 341.19471689341526,
            "unit": "iter/sec",
            "range": "stddev: 0.0001863387357091381",
            "extra": "mean: 2.9308777378062008 msec\nrounds: 328"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-optimized]",
            "value": 196.91746365102776,
            "unit": "iter/sec",
            "range": "stddev: 0.017693086922683534",
            "extra": "mean: 5.078269755556954 msec\nrounds: 270"
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
          "id": "a4a888347daeab37dca9e2d6a0f2ddaf10e54fa4",
          "message": "change trigger",
          "timestamp": "2023-07-31T15:28:15+02:00",
          "tree_id": "2987bdc78bacb29e66cc432b32b12fae60d2f806",
          "url": "https://github.com/zapatacomputing/benchq/commit/a4a888347daeab37dca9e2d6a0f2ddaf10e54fa4"
        },
        "date": 1690810531865,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[vlasov]",
            "value": 132.68948100524847,
            "unit": "iter/sec",
            "range": "stddev: 0.00017789006603251633",
            "extra": "mean: 7.536392428578763 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[jw-2]",
            "value": 3.6965752772269442,
            "unit": "iter/sec",
            "range": "stddev: 0.06789655055914297",
            "extra": "mean: 270.52066439998725 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[many single qubit gates]",
            "value": 2.7999820492030225,
            "unit": "iter/sec",
            "range": "stddev: 0.06115730333697681",
            "extra": "mean: 357.14514680000775 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[GHZ state]",
            "value": 754.6180278792388,
            "unit": "iter/sec",
            "range": "stddev: 0.01230621135774425",
            "extra": "mean: 1.3251737475850889 msec\nrounds: 1553"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[Fully connected state]",
            "value": 22.681770770122473,
            "unit": "iter/sec",
            "range": "stddev: 0.06723578456398072",
            "extra": "mean: 44.08826851020153 msec\nrounds: 49"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[CNOT chain]",
            "value": 55.06454799012374,
            "unit": "iter/sec",
            "range": "stddev: 0.010382644302140968",
            "extra": "mean: 18.160505016391994 msec\nrounds: 61"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[rotation chain]",
            "value": 480.1615459638455,
            "unit": "iter/sec",
            "range": "stddev: 0.013321945330533859",
            "extra": "mean: 2.0826324148733404 msec\nrounds: 1022"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-fast]",
            "value": 7312.456990369309,
            "unit": "iter/sec",
            "range": "stddev: 0.000013243467295506565",
            "extra": "mean: 136.75294108628952 usec\nrounds: 3904"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-optimized]",
            "value": 4277.856215134446,
            "unit": "iter/sec",
            "range": "stddev: 0.00001959424338544167",
            "extra": "mean: 233.76194750588914 usec\nrounds: 1524"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-fast]",
            "value": 3494.6532007264186,
            "unit": "iter/sec",
            "range": "stddev: 0.000016161707656923897",
            "extra": "mean: 286.1514269261781 usec\nrounds: 3038"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-optimized]",
            "value": 2959.798823546726,
            "unit": "iter/sec",
            "range": "stddev: 0.000018387882418032028",
            "extra": "mean: 337.8608005532283 usec\nrounds: 2171"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-fast]",
            "value": 6841.33095032949,
            "unit": "iter/sec",
            "range": "stddev: 0.000013861917586127648",
            "extra": "mean: 146.1703880809681 usec\nrounds: 5084"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-optimized]",
            "value": 3621.1373396064487,
            "unit": "iter/sec",
            "range": "stddev: 0.00001798454601835834",
            "extra": "mean: 276.1563305159483 usec\nrounds: 2366"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-fast]",
            "value": 5719.892111883913,
            "unit": "iter/sec",
            "range": "stddev: 0.000014173021313518084",
            "extra": "mean: 174.82847236267858 usec\nrounds: 4577"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-optimized]",
            "value": 3846.763850640106,
            "unit": "iter/sec",
            "range": "stddev: 0.000017459819311241335",
            "extra": "mean: 259.95877023581755 usec\nrounds: 2681"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-fast]",
            "value": 960.4406189480455,
            "unit": "iter/sec",
            "range": "stddev: 0.00005910252745974907",
            "extra": "mean: 1.0411887838472338 msec\nrounds: 879"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-optimized]",
            "value": 399.96703415348486,
            "unit": "iter/sec",
            "range": "stddev: 0.0003836720695343871",
            "extra": "mean: 2.500206053522542 msec\nrounds: 355"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-fast]",
            "value": 46.21280279388218,
            "unit": "iter/sec",
            "range": "stddev: 0.00014110801792000804",
            "extra": "mean: 21.639025108695282 msec\nrounds: 46"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-optimized]",
            "value": 45.462655624938925,
            "unit": "iter/sec",
            "range": "stddev: 0.00020773732356255944",
            "extra": "mean: 21.996075377775366 msec\nrounds: 45"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-fast]",
            "value": 954.2068614201169,
            "unit": "iter/sec",
            "range": "stddev: 0.000006152324132399626",
            "extra": "mean: 1.047990787355826 msec\nrounds: 870"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-optimized]",
            "value": 314.03709831095443,
            "unit": "iter/sec",
            "range": "stddev: 0.00007564718456059603",
            "extra": "mean: 3.1843371543632597 msec\nrounds: 298"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-fast]",
            "value": 680.5474026253249,
            "unit": "iter/sec",
            "range": "stddev: 0.00009402008487111846",
            "extra": "mean: 1.469405358307641 msec\nrounds: 614"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-optimized]",
            "value": 340.8518578722612,
            "unit": "iter/sec",
            "range": "stddev: 0.0004376984036081084",
            "extra": "mean: 2.9338258745086954 msec\nrounds: 255"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-fast]",
            "value": 78.64423037186289,
            "unit": "iter/sec",
            "range": "stddev: 0.023532843267557217",
            "extra": "mean: 12.71549095555492 msec\nrounds: 90"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-optimized]",
            "value": 15.467447120134759,
            "unit": "iter/sec",
            "range": "stddev: 0.01773277682182735",
            "extra": "mean: 64.65191005555464 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-fast]",
            "value": 0.41079776013458,
            "unit": "iter/sec",
            "range": "stddev: 0.018494290499570073",
            "extra": "mean: 2.434287858999994 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-optimized]",
            "value": 0.41218172137515485,
            "unit": "iter/sec",
            "range": "stddev: 0.010484714050251313",
            "extra": "mean: 2.4261143766000033 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-fast]",
            "value": 41.115508158024824,
            "unit": "iter/sec",
            "range": "stddev: 0.1387975400903065",
            "extra": "mean: 24.3217229896944 msec\nrounds: 97"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-optimized]",
            "value": 10.548462260754539,
            "unit": "iter/sec",
            "range": "stddev: 0.0005011499805671301",
            "extra": "mean: 94.80054772727313 msec\nrounds: 11"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-fast]",
            "value": 68.55679298894788,
            "unit": "iter/sec",
            "range": "stddev: 0.00017913402875641645",
            "extra": "mean: 14.586446599992087 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-optimized]",
            "value": 14.128085919218405,
            "unit": "iter/sec",
            "range": "stddev: 0.01416763232980665",
            "extra": "mean: 70.78099650000728 msec\nrounds: 14"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-fast]",
            "value": 7363.817464593233,
            "unit": "iter/sec",
            "range": "stddev: 0.000012008547353769662",
            "extra": "mean: 135.79912929784155 usec\nrounds: 4857"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-optimized]",
            "value": 4338.086162060479,
            "unit": "iter/sec",
            "range": "stddev: 0.000018316844131025583",
            "extra": "mean: 230.51639885479494 usec\nrounds: 2793"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-fast]",
            "value": 3520.7001345537933,
            "unit": "iter/sec",
            "range": "stddev: 0.000015598212318826104",
            "extra": "mean: 284.03441411710514 usec\nrounds: 2876"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-optimized]",
            "value": 2975.674423672196,
            "unit": "iter/sec",
            "range": "stddev: 0.000018134645694477435",
            "extra": "mean: 336.05827036881544 usec\nrounds: 2197"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-fast]",
            "value": 6852.160357664762,
            "unit": "iter/sec",
            "range": "stddev: 0.0000135360454344633",
            "extra": "mean: 145.93937500038354 usec\nrounds: 4912"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-optimized]",
            "value": 3631.5622206767084,
            "unit": "iter/sec",
            "range": "stddev: 0.00001772957060338016",
            "extra": "mean: 275.3635871378955 usec\nrounds: 2519"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-fast]",
            "value": 5741.254560070247,
            "unit": "iter/sec",
            "range": "stddev: 0.000013932934920485372",
            "extra": "mean: 174.1779587609445 usec\nrounds: 4583"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-optimized]",
            "value": 3885.3778915187336,
            "unit": "iter/sec",
            "range": "stddev: 0.00001644981130767653",
            "extra": "mean: 257.3752226734156 usec\nrounds: 2708"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-fast]",
            "value": 961.3925486378192,
            "unit": "iter/sec",
            "range": "stddev: 0.000059232269130334336",
            "extra": "mean: 1.0401578433459704 msec\nrounds: 849"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-optimized]",
            "value": 396.3197245643002,
            "unit": "iter/sec",
            "range": "stddev: 0.0004014720981647107",
            "extra": "mean: 2.5232153183881127 msec\nrounds: 446"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-fast]",
            "value": 46.270876000958445,
            "unit": "iter/sec",
            "range": "stddev: 0.0001509783925150414",
            "extra": "mean: 21.6118666086911 msec\nrounds: 46"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-optimized]",
            "value": 45.77329118917125,
            "unit": "iter/sec",
            "range": "stddev: 0.00017430923758919725",
            "extra": "mean: 21.846801355559364 msec\nrounds: 45"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-fast]",
            "value": 951.5257579043185,
            "unit": "iter/sec",
            "range": "stddev: 0.000007531977366852584",
            "extra": "mean: 1.0509436993092476 msec\nrounds: 868"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-optimized]",
            "value": 313.60769213218964,
            "unit": "iter/sec",
            "range": "stddev: 0.00006909175220325288",
            "extra": "mean: 3.188697296297462 msec\nrounds: 297"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-fast]",
            "value": 679.773644963284,
            "unit": "iter/sec",
            "range": "stddev: 0.00009371742527528966",
            "extra": "mean: 1.4710779204363122 msec\nrounds: 641"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-optimized]",
            "value": 339.76727306804963,
            "unit": "iter/sec",
            "range": "stddev: 0.00041671731650155244",
            "extra": "mean: 2.9431910583092478 msec\nrounds: 343"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-fast]",
            "value": 79.10638008992987,
            "unit": "iter/sec",
            "range": "stddev: 0.024058188182447413",
            "extra": "mean: 12.641205410526661 msec\nrounds: 95"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-optimized]",
            "value": 15.333524705434181,
            "unit": "iter/sec",
            "range": "stddev: 0.014436990673893327",
            "extra": "mean: 65.21657734999451 msec\nrounds: 20"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-fast]",
            "value": 0.40949327821353587,
            "unit": "iter/sec",
            "range": "stddev: 0.011213960450284008",
            "extra": "mean: 2.44204252720001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-optimized]",
            "value": 0.3836787170238965,
            "unit": "iter/sec",
            "range": "stddev: 0.42368826807162774",
            "extra": "mean: 2.606347330799997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-fast]",
            "value": 58.58237409959846,
            "unit": "iter/sec",
            "range": "stddev: 0.06652277144307223",
            "extra": "mean: 17.06998078124755 msec\nrounds: 96"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-optimized]",
            "value": 10.561672762801269,
            "unit": "iter/sec",
            "range": "stddev: 0.00017736610503195222",
            "extra": "mean: 94.68197154545908 msec\nrounds: 11"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-fast]",
            "value": 57.06075020293064,
            "unit": "iter/sec",
            "range": "stddev: 0.02466838891250083",
            "extra": "mean: 17.525181432834366 msec\nrounds: 67"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-optimized]",
            "value": 14.167237456794924,
            "unit": "iter/sec",
            "range": "stddev: 0.015981939053833993",
            "extra": "mean: 70.58539133332431 msec\nrounds: 12"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-fast]",
            "value": 1555.975206625892,
            "unit": "iter/sec",
            "range": "stddev: 0.000028073751119479057",
            "extra": "mean: 642.683762402927 usec\nrounds: 1431"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-optimized]",
            "value": 1196.0402016982123,
            "unit": "iter/sec",
            "range": "stddev: 0.000031091713922305534",
            "extra": "mean: 836.0922973827618 usec\nrounds: 955"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-fast]",
            "value": 22.77235352638256,
            "unit": "iter/sec",
            "range": "stddev: 0.00026998594835397926",
            "extra": "mean: 43.91289634782217 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-optimized]",
            "value": 22.242372737416634,
            "unit": "iter/sec",
            "range": "stddev: 0.00029421634794883785",
            "extra": "mean: 44.959232173902784 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-fast]",
            "value": 638.4877678304942,
            "unit": "iter/sec",
            "range": "stddev: 0.00009798028898274466",
            "extra": "mean: 1.5662007173573291 msec\nrounds: 605"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-optimized]",
            "value": 320.4572973548608,
            "unit": "iter/sec",
            "range": "stddev: 0.0004055378717345153",
            "extra": "mean: 3.120540578274435 msec\nrounds: 313"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-fast]",
            "value": 22.07224353463571,
            "unit": "iter/sec",
            "range": "stddev: 0.0002407177381206679",
            "extra": "mean: 45.30577049998576 msec\nrounds: 22"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-optimized]",
            "value": 20.652616789809073,
            "unit": "iter/sec",
            "range": "stddev: 0.0007050362334982695",
            "extra": "mean: 48.420014285717286 msec\nrounds: 21"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-fast]",
            "value": 13957.251537067303,
            "unit": "iter/sec",
            "range": "stddev: 0.000009122889510676196",
            "extra": "mean: 71.64734384446868 usec\nrounds: 7326"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-optimized]",
            "value": 4710.38100281094,
            "unit": "iter/sec",
            "range": "stddev: 0.000011070697671073158",
            "extra": "mean: 212.2970518527579 usec\nrounds: 2970"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-fast]",
            "value": 1370.2560582545707,
            "unit": "iter/sec",
            "range": "stddev: 0.000041138148248244835",
            "extra": "mean: 729.7906066358122 usec\nrounds: 1266"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-optimized]",
            "value": 326.6235615535908,
            "unit": "iter/sec",
            "range": "stddev: 0.0006394454239552523",
            "extra": "mean: 3.0616284852307727 msec\nrounds: 237"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-fast]",
            "value": 7862.473064528709,
            "unit": "iter/sec",
            "range": "stddev: 0.000013249206050478474",
            "extra": "mean: 127.18644525619646 usec\nrounds: 5754"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-optimized]",
            "value": 4165.329230384614,
            "unit": "iter/sec",
            "range": "stddev: 0.000019488996713326975",
            "extra": "mean: 240.0770610652698 usec\nrounds: 2702"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-fast]",
            "value": 344.0244445616637,
            "unit": "iter/sec",
            "range": "stddev: 0.00012863228263193657",
            "extra": "mean: 2.906770189758297 msec\nrounds: 332"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-optimized]",
            "value": 249.86314443457627,
            "unit": "iter/sec",
            "range": "stddev: 0.0003179189208400699",
            "extra": "mean: 4.002190888387856 msec\nrounds: 224"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "108305907+SebastianMorawiec@users.noreply.github.com",
            "name": "SebastianMorawiec",
            "username": "SebastianMorawiec"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "c8e9c4b6d9fbed77d22f85267f1d43394a1d9f07",
          "message": "Change workflow trigger on performance tests (#113)",
          "timestamp": "2023-07-31T19:24:45+02:00",
          "tree_id": "ff2f3d4207d5db65c40a44bd9df65eed6ed361a8",
          "url": "https://github.com/zapatacomputing/benchq/commit/c8e9c4b6d9fbed77d22f85267f1d43394a1d9f07"
        },
        "date": 1690824692673,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[vlasov]",
            "value": 138.88158046010983,
            "unit": "iter/sec",
            "range": "stddev: 0.00011147679108472845",
            "extra": "mean: 7.2003788888853 msec\nrounds: 9"
          },
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[jw-2]",
            "value": 3.9720920053068274,
            "unit": "iter/sec",
            "range": "stddev: 0.047566848023132276",
            "extra": "mean: 251.7565047999824 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[many single qubit gates]",
            "value": 2.733848264115378,
            "unit": "iter/sec",
            "range": "stddev: 0.1316490460154444",
            "extra": "mean: 365.7847486000037 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[GHZ state]",
            "value": 896.6140262174474,
            "unit": "iter/sec",
            "range": "stddev: 0.010079338665302013",
            "extra": "mean: 1.1153071118223612 msec\nrounds: 1717"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[Fully connected state]",
            "value": 24.33024572920738,
            "unit": "iter/sec",
            "range": "stddev: 0.04873705334526494",
            "extra": "mean: 41.10110564150794 msec\nrounds: 53"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[CNOT chain]",
            "value": 58.40942240158682,
            "unit": "iter/sec",
            "range": "stddev: 0.0054597545141402875",
            "extra": "mean: 17.12052540298417 msec\nrounds: 67"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[rotation chain]",
            "value": 565.1171637730938,
            "unit": "iter/sec",
            "range": "stddev: 0.010011331262662529",
            "extra": "mean: 1.769544554837695 msec\nrounds: 1085"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-fast]",
            "value": 7366.707427114198,
            "unit": "iter/sec",
            "range": "stddev: 0.000011068895454955112",
            "extra": "mean: 135.74585524047825 usec\nrounds: 2929"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-optimized]",
            "value": 4385.9066637707065,
            "unit": "iter/sec",
            "range": "stddev: 0.00001701344081706192",
            "extra": "mean: 228.00302803075783 usec\nrounds: 1427"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-fast]",
            "value": 3683.064026950521,
            "unit": "iter/sec",
            "range": "stddev: 0.000014179831831144233",
            "extra": "mean: 271.51306430802765 usec\nrounds: 3250"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-optimized]",
            "value": 3118.100945374558,
            "unit": "iter/sec",
            "range": "stddev: 0.000015295241123857014",
            "extra": "mean: 320.70802630152707 usec\nrounds: 1863"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-fast]",
            "value": 6939.376620088217,
            "unit": "iter/sec",
            "range": "stddev: 0.000012229601174340336",
            "extra": "mean: 144.10516315041673 usec\nrounds: 5308"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-optimized]",
            "value": 3717.0920684807065,
            "unit": "iter/sec",
            "range": "stddev: 0.00001684065890685851",
            "extra": "mean: 269.0275036444636 usec\nrounds: 2744"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-fast]",
            "value": 5876.284790399751,
            "unit": "iter/sec",
            "range": "stddev: 0.000012658140701546151",
            "extra": "mean: 170.1755506529785 usec\nrounds: 4669"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-optimized]",
            "value": 4038.391720987684,
            "unit": "iter/sec",
            "range": "stddev: 0.000014570811566004406",
            "extra": "mean: 247.62332856492347 usec\nrounds: 2167"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-fast]",
            "value": 1006.3519315388403,
            "unit": "iter/sec",
            "range": "stddev: 0.000056543973778797436",
            "extra": "mean: 993.6881608314425 usec\nrounds: 914"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-optimized]",
            "value": 428.76811831586514,
            "unit": "iter/sec",
            "range": "stddev: 0.0003379099155436818",
            "extra": "mean: 2.3322629581878553 msec\nrounds: 287"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-fast]",
            "value": 51.72499176061783,
            "unit": "iter/sec",
            "range": "stddev: 0.00007956257506381385",
            "extra": "mean: 19.333014196077183 msec\nrounds: 51"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-optimized]",
            "value": 50.47340047100836,
            "unit": "iter/sec",
            "range": "stddev: 0.00012866980385294757",
            "extra": "mean: 19.812415860001238 msec\nrounds: 50"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-fast]",
            "value": 995.0921676148025,
            "unit": "iter/sec",
            "range": "stddev: 0.000005325180722218719",
            "extra": "mean: 1.004932038001024 msec\nrounds: 921"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-optimized]",
            "value": 329.90859709414514,
            "unit": "iter/sec",
            "range": "stddev: 0.00007043827576920484",
            "extra": "mean: 3.0311425916392007 msec\nrounds: 311"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-fast]",
            "value": 721.6849856432557,
            "unit": "iter/sec",
            "range": "stddev: 0.00008570997686389196",
            "extra": "mean: 1.385646119696775 msec\nrounds: 660"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-optimized]",
            "value": 363.4981041367543,
            "unit": "iter/sec",
            "range": "stddev: 0.0003848704416491874",
            "extra": "mean: 2.751045985163605 msec\nrounds: 337"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-fast]",
            "value": 88.46821771025083,
            "unit": "iter/sec",
            "range": "stddev: 0.0164648451098333",
            "extra": "mean: 11.303494360824338 msec\nrounds: 97"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-optimized]",
            "value": 16.256342153531676,
            "unit": "iter/sec",
            "range": "stddev: 0.01598346380289524",
            "extra": "mean: 61.514453285713536 msec\nrounds: 21"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-fast]",
            "value": 0.4794747160241166,
            "unit": "iter/sec",
            "range": "stddev: 0.006681694897169661",
            "extra": "mean: 2.0856157093999967 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-optimized]",
            "value": 0.48125802978842097,
            "unit": "iter/sec",
            "range": "stddev: 0.011276247961856953",
            "extra": "mean: 2.077887407800006 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-fast]",
            "value": 51.20449138786161,
            "unit": "iter/sec",
            "range": "stddev: 0.08751299292097564",
            "extra": "mean: 19.52953682178468 msec\nrounds: 101"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-optimized]",
            "value": 11.892124328282016,
            "unit": "iter/sec",
            "range": "stddev: 0.0029056602170190486",
            "extra": "mean: 84.0892655000071 msec\nrounds: 12"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-fast]",
            "value": 65.5864981313392,
            "unit": "iter/sec",
            "range": "stddev: 0.014866208077846662",
            "extra": "mean: 15.247040602739087 msec\nrounds: 73"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-optimized]",
            "value": 16.904875493049083,
            "unit": "iter/sec",
            "range": "stddev: 0.013305342675358439",
            "extra": "mean: 59.15453209999555 msec\nrounds: 20"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-fast]",
            "value": 7407.02807769688,
            "unit": "iter/sec",
            "range": "stddev: 0.000010905824455611572",
            "extra": "mean: 135.00691363801837 usec\nrounds: 5778"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-optimized]",
            "value": 4418.843399227531,
            "unit": "iter/sec",
            "range": "stddev: 0.00001669301491607887",
            "extra": "mean: 226.30356173627072 usec\nrounds: 3110"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-fast]",
            "value": 3692.5224447688233,
            "unit": "iter/sec",
            "range": "stddev: 0.00001412310700959158",
            "extra": "mean: 270.8175820073063 usec\nrounds: 3268"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-optimized]",
            "value": 3125.6821665870834,
            "unit": "iter/sec",
            "range": "stddev: 0.000015431184356578474",
            "extra": "mean: 319.9301613867845 usec\nrounds: 1989"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-fast]",
            "value": 6923.472072320111,
            "unit": "iter/sec",
            "range": "stddev: 0.000012647811617854478",
            "extra": "mean: 144.4362004431242 usec\nrounds: 5418"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-optimized]",
            "value": 3721.7742314548573,
            "unit": "iter/sec",
            "range": "stddev: 0.000016874744999669047",
            "extra": "mean: 268.68905468483933 usec\nrounds: 2615"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-fast]",
            "value": 5875.154979562339,
            "unit": "iter/sec",
            "range": "stddev: 0.000012776249195197562",
            "extra": "mean: 170.20827594823612 usec\nrounds: 4769"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-optimized]",
            "value": 4049.6678581387096,
            "unit": "iter/sec",
            "range": "stddev: 0.000014348378291044852",
            "extra": "mean: 246.93383137342417 usec\nrounds: 2977"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-fast]",
            "value": 1003.0011447172388,
            "unit": "iter/sec",
            "range": "stddev: 0.00005920835265388442",
            "extra": "mean: 997.0078352023368 usec\nrounds: 892"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-optimized]",
            "value": 399.0309533304011,
            "unit": "iter/sec",
            "range": "stddev: 0.00031160464454202353",
            "extra": "mean: 2.5060712499964666 msec\nrounds: 8"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-fast]",
            "value": 51.57968155925865,
            "unit": "iter/sec",
            "range": "stddev: 0.00010029510002607546",
            "extra": "mean: 19.387479134610867 msec\nrounds: 52"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-optimized]",
            "value": 50.76170319453018,
            "unit": "iter/sec",
            "range": "stddev: 0.0001161844871601598",
            "extra": "mean: 19.699890607842228 msec\nrounds: 51"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-fast]",
            "value": 996.3294673693032,
            "unit": "iter/sec",
            "range": "stddev: 0.000011926817043721536",
            "extra": "mean: 1.0036840550750632 msec\nrounds: 926"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-optimized]",
            "value": 326.51103846607606,
            "unit": "iter/sec",
            "range": "stddev: 0.00008994369416987035",
            "extra": "mean: 3.0626835916418744 msec\nrounds: 311"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-fast]",
            "value": 722.934852915042,
            "unit": "iter/sec",
            "range": "stddev: 0.00008278719404672443",
            "extra": "mean: 1.383250504478746 msec\nrounds: 670"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-optimized]",
            "value": 361.55872324442004,
            "unit": "iter/sec",
            "range": "stddev: 0.0003627577598541533",
            "extra": "mean: 2.76580244289662 msec\nrounds: 359"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-fast]",
            "value": 90.06812523319866,
            "unit": "iter/sec",
            "range": "stddev: 0.015714104415188807",
            "extra": "mean: 11.102706949998833 msec\nrounds: 100"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-optimized]",
            "value": 16.860645734504402,
            "unit": "iter/sec",
            "range": "stddev: 0.014076743739708212",
            "extra": "mean: 59.309709470590086 msec\nrounds: 17"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-fast]",
            "value": 0.4810762244735716,
            "unit": "iter/sec",
            "range": "stddev: 0.01366818721446438",
            "extra": "mean: 2.078672670000003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-optimized]",
            "value": 0.479071678739546,
            "unit": "iter/sec",
            "range": "stddev: 0.00885270489894573",
            "extra": "mean: 2.0873703129999965 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-fast]",
            "value": 103.50861710269103,
            "unit": "iter/sec",
            "range": "stddev: 0.00003816252994702591",
            "extra": "mean: 9.66103140000314 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-optimized]",
            "value": 11.778104203355115,
            "unit": "iter/sec",
            "range": "stddev: 0.002359670285673289",
            "extra": "mean: 84.90330725000206 msec\nrounds: 12"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-fast]",
            "value": 64.4383560084484,
            "unit": "iter/sec",
            "range": "stddev: 0.016376092458379017",
            "extra": "mean: 15.518707520547109 msec\nrounds: 73"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-optimized]",
            "value": 16.23367721207536,
            "unit": "iter/sec",
            "range": "stddev: 0.013210950101369244",
            "extra": "mean: 61.60033779999973 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-fast]",
            "value": 1658.59242214224,
            "unit": "iter/sec",
            "range": "stddev: 0.000023653444788322332",
            "extra": "mean: 602.9208783604587 usec\nrounds: 1562"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-optimized]",
            "value": 1283.1290170781685,
            "unit": "iter/sec",
            "range": "stddev: 0.000037211872962543154",
            "extra": "mean: 779.3448567448925 usec\nrounds: 1075"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-fast]",
            "value": 25.276757207644433,
            "unit": "iter/sec",
            "range": "stddev: 0.00021570598174722682",
            "extra": "mean: 39.56203684614934 msec\nrounds: 26"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-optimized]",
            "value": 25.027243731520866,
            "unit": "iter/sec",
            "range": "stddev: 0.00027591307756644895",
            "extra": "mean: 39.956457479995606 msec\nrounds: 25"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-fast]",
            "value": 576.8574051322164,
            "unit": "iter/sec",
            "range": "stddev: 0.006690757447675272",
            "extra": "mean: 1.7335306630427998 msec\nrounds: 644"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-optimized]",
            "value": 342.27692421080934,
            "unit": "iter/sec",
            "range": "stddev: 0.0003821017634997706",
            "extra": "mean: 2.9216109216410313 msec\nrounds: 268"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-fast]",
            "value": 24.461051586886303,
            "unit": "iter/sec",
            "range": "stddev: 0.00018985441019039553",
            "extra": "mean: 40.881316833332924 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-optimized]",
            "value": 23.0734875899238,
            "unit": "iter/sec",
            "range": "stddev: 0.0005818076800765707",
            "extra": "mean: 43.339785374998975 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-fast]",
            "value": 13703.591728082376,
            "unit": "iter/sec",
            "range": "stddev: 0.000008644054311307124",
            "extra": "mean: 72.9735692541634 usec\nrounds: 8606"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-optimized]",
            "value": 4776.138839836328,
            "unit": "iter/sec",
            "range": "stddev: 0.000009726336903863932",
            "extra": "mean: 209.37414793290824 usec\nrounds: 3265"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-fast]",
            "value": 1433.0028321786106,
            "unit": "iter/sec",
            "range": "stddev: 0.000038382829597708705",
            "extra": "mean: 697.8353270102673 usec\nrounds: 1318"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-optimized]",
            "value": 341.1917537433246,
            "unit": "iter/sec",
            "range": "stddev: 0.0006488033030054175",
            "extra": "mean: 2.930903191617845 msec\nrounds: 334"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-fast]",
            "value": 7858.277185280309,
            "unit": "iter/sec",
            "range": "stddev: 0.000011977685413984352",
            "extra": "mean: 127.25435568411163 usec\nrounds: 6025"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-optimized]",
            "value": 4279.420589548039,
            "unit": "iter/sec",
            "range": "stddev: 0.000018173964667919374",
            "extra": "mean: 233.67649406613074 usec\nrounds: 2949"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-fast]",
            "value": 370.56404848219836,
            "unit": "iter/sec",
            "range": "stddev: 0.00011375026823104691",
            "extra": "mean: 2.6985888245120444 msec\nrounds: 359"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-optimized]",
            "value": 267.82673838292556,
            "unit": "iter/sec",
            "range": "stddev: 0.000288017194976256",
            "extra": "mean: 3.7337571522461244 msec\nrounds: 289"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "46659064+olgOk@users.noreply.github.com",
            "name": "Olga Okrut",
            "username": "olgOk"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "f2a69be149a099213c9b22c86165ac31c00d9838",
          "message": "Description (#109)\n\n* Implementation of the QSP in qiskit (qsp.py).\r\n\r\n* Added the estimation of the parameters for quantum DE solver: number of grid points, matrix condition number, degree of approximating polynomial.\r\n\r\n* Construction of the inverse of block incoding (SEL_inv) using the QSP circuit construction.\r\n\r\nCo-authored-by: Olga Okrut <olgaokrut@Olgas-MacBook-Pro-2.local>",
          "timestamp": "2023-08-02T21:57:11Z",
          "tree_id": "68f089129f176bd7db931cd96392f1714a571b57",
          "url": "https://github.com/zapatacomputing/benchq/commit/f2a69be149a099213c9b22c86165ac31c00d9838"
        },
        "date": 1691013923327,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[vlasov]",
            "value": 114.67016293462895,
            "unit": "iter/sec",
            "range": "stddev: 0.00024065367387755688",
            "extra": "mean: 8.720664333319897 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[jw-2]",
            "value": 3.232416405322214,
            "unit": "iter/sec",
            "range": "stddev: 0.07182893490706774",
            "extra": "mean: 309.3660823999926 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[many single qubit gates]",
            "value": 2.3671817766575036,
            "unit": "iter/sec",
            "range": "stddev: 0.17290579185650207",
            "extra": "mean: 422.44326559999763 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[GHZ state]",
            "value": 676.5609822445481,
            "unit": "iter/sec",
            "range": "stddev: 0.014275103659487438",
            "extra": "mean: 1.4780633619787171 msec\nrounds: 1536"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[Fully connected state]",
            "value": 19.56195326767646,
            "unit": "iter/sec",
            "range": "stddev: 0.0765360696478821",
            "extra": "mean: 51.11963955319163 msec\nrounds: 47"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[CNOT chain]",
            "value": 47.13481467372101,
            "unit": "iter/sec",
            "range": "stddev: 0.009015308075809012",
            "extra": "mean: 21.215740571427943 msec\nrounds: 56"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[rotation chain]",
            "value": 456.1502764017421,
            "unit": "iter/sec",
            "range": "stddev: 0.013569099639985446",
            "extra": "mean: 2.1922599891604078 msec\nrounds: 738"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-fast]",
            "value": 6256.253942646086,
            "unit": "iter/sec",
            "range": "stddev: 0.00001849248430590932",
            "extra": "mean: 159.84005911004462 usec\nrounds: 3079"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-optimized]",
            "value": 3687.1833133687915,
            "unit": "iter/sec",
            "range": "stddev: 0.000024275691063878963",
            "extra": "mean: 271.2097324736347 usec\nrounds: 1241"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-fast]",
            "value": 2967.172923949152,
            "unit": "iter/sec",
            "range": "stddev: 0.000021521146290079225",
            "extra": "mean: 337.02113952598773 usec\nrounds: 2745"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-optimized]",
            "value": 2506.0357077009094,
            "unit": "iter/sec",
            "range": "stddev: 0.00002248368222707433",
            "extra": "mean: 399.0366126576151 usec\nrounds: 1580"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-fast]",
            "value": 5830.986560397377,
            "unit": "iter/sec",
            "range": "stddev: 0.00001721919775020188",
            "extra": "mean: 171.4975655735092 usec\nrounds: 4392"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-optimized]",
            "value": 3083.805203807573,
            "unit": "iter/sec",
            "range": "stddev: 0.000025141958493353736",
            "extra": "mean: 324.27469762529114 usec\nrounds: 2358"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-fast]",
            "value": 4860.312157263744,
            "unit": "iter/sec",
            "range": "stddev: 0.00001686750866474579",
            "extra": "mean: 205.74810169455853 usec\nrounds: 3894"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-optimized]",
            "value": 3301.1911899419138,
            "unit": "iter/sec",
            "range": "stddev: 0.000020093588358009287",
            "extra": "mean: 302.92095866692154 usec\nrounds: 2250"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-fast]",
            "value": 810.648903689061,
            "unit": "iter/sec",
            "range": "stddev: 0.00008231546515516845",
            "extra": "mean: 1.2335796612432945 msec\nrounds: 676"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-optimized]",
            "value": 341.3507741541434,
            "unit": "iter/sec",
            "range": "stddev: 0.00044820457035150583",
            "extra": "mean: 2.9295378118827147 msec\nrounds: 202"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-fast]",
            "value": 38.5718157010601,
            "unit": "iter/sec",
            "range": "stddev: 0.00025432484166420193",
            "extra": "mean: 25.92566571794846 msec\nrounds: 39"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-optimized]",
            "value": 30.821044888784137,
            "unit": "iter/sec",
            "range": "stddev: 0.03743846710767701",
            "extra": "mean: 32.44536334210729 msec\nrounds: 38"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-fast]",
            "value": 808.3148219649197,
            "unit": "iter/sec",
            "range": "stddev: 0.00004586398073507199",
            "extra": "mean: 1.2371417334264834 msec\nrounds: 724"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-optimized]",
            "value": 268.13323864012693,
            "unit": "iter/sec",
            "range": "stddev: 0.00011098609724390441",
            "extra": "mean: 3.7294891341022542 msec\nrounds: 261"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-fast]",
            "value": 569.186346292742,
            "unit": "iter/sec",
            "range": "stddev: 0.00011169963207858975",
            "extra": "mean: 1.7568938652749821 msec\nrounds: 527"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-optimized]",
            "value": 292.90301057936546,
            "unit": "iter/sec",
            "range": "stddev: 0.00043301227421597396",
            "extra": "mean: 3.4140994250007495 msec\nrounds: 320"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-fast]",
            "value": 81.73832248634423,
            "unit": "iter/sec",
            "range": "stddev: 0.00033694378798327415",
            "extra": "mean: 12.234163481481612 msec\nrounds: 81"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-optimized]",
            "value": 11.562437088864861,
            "unit": "iter/sec",
            "range": "stddev: 0.05405656546057302",
            "extra": "mean: 86.4869570588232 msec\nrounds: 17"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-fast]",
            "value": 0.3483225320521294,
            "unit": "iter/sec",
            "range": "stddev: 0.01749527466992678",
            "extra": "mean: 2.8709024194000223 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-optimized]",
            "value": 0.3493320437397221,
            "unit": "iter/sec",
            "range": "stddev: 0.014112876379696167",
            "extra": "mean: 2.8626059873999794 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-fast]",
            "value": 32.50170219439136,
            "unit": "iter/sec",
            "range": "stddev: 0.16719873899696208",
            "extra": "mean: 30.767619308645454 msec\nrounds: 81"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-optimized]",
            "value": 8.669225259427028,
            "unit": "iter/sec",
            "range": "stddev: 0.004294597030578868",
            "extra": "mean: 115.35056133333102 msec\nrounds: 9"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-fast]",
            "value": 57.19459603382146,
            "unit": "iter/sec",
            "range": "stddev: 0.001061341759287335",
            "extra": "mean: 17.484169298243838 msec\nrounds: 57"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-optimized]",
            "value": 11.199000518768127,
            "unit": "iter/sec",
            "range": "stddev: 0.026248875284516304",
            "extra": "mean: 89.29368280000745 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-fast]",
            "value": 6269.668139420028,
            "unit": "iter/sec",
            "range": "stddev: 0.000016521479723265357",
            "extra": "mean: 159.49807513934934 usec\nrounds: 4139"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-optimized]",
            "value": 3628.9248675473177,
            "unit": "iter/sec",
            "range": "stddev: 0.000025331676705717475",
            "extra": "mean: 275.56371005164135 usec\nrounds: 2497"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-fast]",
            "value": 2958.8429879491346,
            "unit": "iter/sec",
            "range": "stddev: 0.00002266723762340429",
            "extra": "mean: 337.9699443575851 usec\nrounds: 2552"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-optimized]",
            "value": 2493.6942284909815,
            "unit": "iter/sec",
            "range": "stddev: 0.00002444250243526477",
            "extra": "mean: 401.0114746927629 usec\nrounds: 1936"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-fast]",
            "value": 5759.40641301637,
            "unit": "iter/sec",
            "range": "stddev: 0.000017533798950379426",
            "extra": "mean: 173.62900415223012 usec\nrounds: 4335"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-optimized]",
            "value": 3057.1258188926745,
            "unit": "iter/sec",
            "range": "stddev: 0.000024165412670231513",
            "extra": "mean: 327.1046267772556 usec\nrounds: 1688"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-fast]",
            "value": 4857.076977384003,
            "unit": "iter/sec",
            "range": "stddev: 0.00001840542567661524",
            "extra": "mean: 205.88514546018064 usec\nrounds: 3843"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-optimized]",
            "value": 3283.6546956357283,
            "unit": "iter/sec",
            "range": "stddev: 0.00001986585920771363",
            "extra": "mean: 304.5387206301228 usec\nrounds: 2409"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-fast]",
            "value": 807.4542301784052,
            "unit": "iter/sec",
            "range": "stddev: 0.00007795277915333273",
            "extra": "mean: 1.238460289915197 msec\nrounds: 714"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-optimized]",
            "value": 338.5184378908317,
            "unit": "iter/sec",
            "range": "stddev: 0.0004796054517387197",
            "extra": "mean: 2.9540488436334105 msec\nrounds: 275"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-fast]",
            "value": 38.55616856951379,
            "unit": "iter/sec",
            "range": "stddev: 0.00017413657633604424",
            "extra": "mean: 25.936187051290567 msec\nrounds: 39"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-optimized]",
            "value": 38.80152940110681,
            "unit": "iter/sec",
            "range": "stddev: 0.0004358558305609228",
            "extra": "mean: 25.7721799999841 msec\nrounds: 39"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-fast]",
            "value": 800.974061177838,
            "unit": "iter/sec",
            "range": "stddev: 0.00002863182551080728",
            "extra": "mean: 1.2484798802716441 msec\nrounds: 735"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-optimized]",
            "value": 265.1498826783913,
            "unit": "iter/sec",
            "range": "stddev: 0.00007592112067722453",
            "extra": "mean: 3.771451791336192 msec\nrounds: 254"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-fast]",
            "value": 574.1600476923237,
            "unit": "iter/sec",
            "range": "stddev: 0.0001153356594743606",
            "extra": "mean: 1.7416746498110087 msec\nrounds: 534"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-optimized]",
            "value": 289.8310711436547,
            "unit": "iter/sec",
            "range": "stddev: 0.0004665927381775302",
            "extra": "mean: 3.450285699369859 msec\nrounds: 316"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-fast]",
            "value": 63.64789189555795,
            "unit": "iter/sec",
            "range": "stddev: 0.030048140990493712",
            "extra": "mean: 15.711439455700042 msec\nrounds: 79"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-optimized]",
            "value": 14.754426212990554,
            "unit": "iter/sec",
            "range": "stddev: 0.008822208605575975",
            "extra": "mean: 67.77627171428387 msec\nrounds: 14"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-fast]",
            "value": 0.3451192118933454,
            "unit": "iter/sec",
            "range": "stddev: 0.009139116247032345",
            "extra": "mean: 2.897549500399987 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-optimized]",
            "value": 0.34883167668590703,
            "unit": "iter/sec",
            "range": "stddev: 0.021012660341168807",
            "extra": "mean: 2.8667121332000307 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-fast]",
            "value": 32.90012137299979,
            "unit": "iter/sec",
            "range": "stddev: 0.16447425582744776",
            "extra": "mean: 30.395024646342858 msec\nrounds: 82"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-optimized]",
            "value": 8.930779014367625,
            "unit": "iter/sec",
            "range": "stddev: 0.0010359122014326433",
            "extra": "mean: 111.97231488890542 msec\nrounds: 9"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-fast]",
            "value": 47.78597867653066,
            "unit": "iter/sec",
            "range": "stddev: 0.03059018340202725",
            "extra": "mean: 20.926640568965357 msec\nrounds: 58"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-optimized]",
            "value": 11.958100702342048,
            "unit": "iter/sec",
            "range": "stddev: 0.02066548523972156",
            "extra": "mean: 83.6253201818367 msec\nrounds: 11"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-fast]",
            "value": 1322.2680539013181,
            "unit": "iter/sec",
            "range": "stddev: 0.000039836816434350996",
            "extra": "mean: 756.2763064943796 usec\nrounds: 1155"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-optimized]",
            "value": 1038.3799863034008,
            "unit": "iter/sec",
            "range": "stddev: 0.00004416424277948578",
            "extra": "mean: 963.0385920283072 usec\nrounds: 853"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-fast]",
            "value": 19.140318105557515,
            "unit": "iter/sec",
            "range": "stddev: 0.0006344271708418953",
            "extra": "mean: 52.245735650006964 msec\nrounds: 20"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-optimized]",
            "value": 18.66122459523266,
            "unit": "iter/sec",
            "range": "stddev: 0.0004360933340735435",
            "extra": "mean: 53.587051315778474 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-fast]",
            "value": 535.3111931994836,
            "unit": "iter/sec",
            "range": "stddev: 0.00011601071895927507",
            "extra": "mean: 1.868072277777592 msec\nrounds: 504"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-optimized]",
            "value": 271.4931978751413,
            "unit": "iter/sec",
            "range": "stddev: 0.0005081922306832825",
            "extra": "mean: 3.6833335340500732 msec\nrounds: 279"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-fast]",
            "value": 18.399962502814514,
            "unit": "iter/sec",
            "range": "stddev: 0.0005191942128943054",
            "extra": "mean: 54.34793684210155 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-optimized]",
            "value": 17.322219491052028,
            "unit": "iter/sec",
            "range": "stddev: 0.0009056012964646636",
            "extra": "mean: 57.72932276470462 msec\nrounds: 17"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-fast]",
            "value": 11967.42512083956,
            "unit": "iter/sec",
            "range": "stddev: 0.000011909290115964915",
            "extra": "mean: 83.56016351910512 usec\nrounds: 6250"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-optimized]",
            "value": 4004.40627120846,
            "unit": "iter/sec",
            "range": "stddev: 0.00001446900215815778",
            "extra": "mean: 249.7249110785698 usec\nrounds: 2654"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-fast]",
            "value": 1148.2711711241245,
            "unit": "iter/sec",
            "range": "stddev: 0.00005367110768071626",
            "extra": "mean: 870.8744285733733 usec\nrounds: 973"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-optimized]",
            "value": 278.18867469312966,
            "unit": "iter/sec",
            "range": "stddev: 0.0007922295724564811",
            "extra": "mean: 3.5946826415672795 msec\nrounds: 332"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-fast]",
            "value": 6706.079030402906,
            "unit": "iter/sec",
            "range": "stddev: 0.000016876355405346526",
            "extra": "mean: 149.11843350881585 usec\nrounds: 4948"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-optimized]",
            "value": 3538.358958641092,
            "unit": "iter/sec",
            "range": "stddev: 0.000022551075830748935",
            "extra": "mean: 282.6168887014364 usec\nrounds: 2372"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-fast]",
            "value": 290.0610461340669,
            "unit": "iter/sec",
            "range": "stddev: 0.00013800978696252222",
            "extra": "mean: 3.447550139282742 msec\nrounds: 280"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-optimized]",
            "value": 162.0529075518042,
            "unit": "iter/sec",
            "range": "stddev: 0.021801671614250433",
            "extra": "mean: 6.17082417777864 msec\nrounds: 225"
          }
        ]
      }
    ]
  }
}