window.BENCHMARK_DATA = {
  "lastUpdate": 1690800113021,
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
      }
    ]
  }
}