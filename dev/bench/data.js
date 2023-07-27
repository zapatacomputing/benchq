window.BENCHMARK_DATA = {
  "lastUpdate": 1690471498085,
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
    ]
  }
}