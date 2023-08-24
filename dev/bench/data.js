window.BENCHMARK_DATA = {
  "lastUpdate": 1692882881676,
  "repoUrl": "https://github.com/zapatacomputing/benchq",
  "entries": {
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
      },
      {
        "commit": {
          "author": {
            "email": "bdas23@uri.edu",
            "name": "Bhargav Das",
            "username": "bdas4018"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "9ce15fd0188e37aef62703a9d074ea2b85aa0373",
          "message": "DTA2-224: Compression Gadget (#121)\n\n* Methods for ADD^L and ADD_dagger\r\n\r\n* style fixes done\r\n\r\n* ADD_L and ADD_dagger\r\n\r\n* Tests for compression gadget\r\n\r\n* Fixed \"forward\" and \"backward\"issue\r\n\r\n* Fixed \"forward\" and \"backward\" issue and edited the Docstring\r\n\r\n* isort src test fix\r\n\r\n* isort test fix\r\n\r\n* forward/backward issue fixed",
          "timestamp": "2023-08-07T11:26:55-04:00",
          "tree_id": "5b6c883ee6d79cbc9916bf7f9b3437ad7f9ca071",
          "url": "https://github.com/zapatacomputing/benchq/commit/9ce15fd0188e37aef62703a9d074ea2b85aa0373"
        },
        "date": 1691422575813,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[vlasov]",
            "value": 100.97754748046248,
            "unit": "iter/sec",
            "range": "stddev: 0.00034028739605438757",
            "extra": "mean: 9.90319160002855 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[jw-2]",
            "value": 2.689516769584101,
            "unit": "iter/sec",
            "range": "stddev: 0.08508663629150645",
            "extra": "mean: 371.8140043999938 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[many single qubit gates]",
            "value": 1.8656538303660417,
            "unit": "iter/sec",
            "range": "stddev: 0.11438800112733183",
            "extra": "mean: 536.0051172000112 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[GHZ state]",
            "value": 524.9879244275697,
            "unit": "iter/sec",
            "range": "stddev: 0.017815445845117003",
            "extra": "mean: 1.9048057173702964 msec\nrounds: 1019"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[Fully connected state]",
            "value": 18.123430493296762,
            "unit": "iter/sec",
            "range": "stddev: 0.06921497217853699",
            "extra": "mean: 55.17719177778543 msec\nrounds: 36"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[CNOT chain]",
            "value": 46.68657519898053,
            "unit": "iter/sec",
            "range": "stddev: 0.005344729418523702",
            "extra": "mean: 21.419433653849094 msec\nrounds: 52"
          },
          {
            "name": "benchmarks/test_graph_sim_mini_performance.py::test_graph_sim_mini[rotation chain]",
            "value": 370.3827060555261,
            "unit": "iter/sec",
            "range": "stddev: 0.016458605582277974",
            "extra": "mean: 2.69991007585026 msec\nrounds: 646"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-fast]",
            "value": 5682.659980420271,
            "unit": "iter/sec",
            "range": "stddev: 0.000048665366846929206",
            "extra": "mean: 175.97392830919355 usec\nrounds: 2441"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-optimized]",
            "value": 3176.430822595431,
            "unit": "iter/sec",
            "range": "stddev: 0.00006153592539558546",
            "extra": "mean: 314.8187559718079 usec\nrounds: 1172"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-fast]",
            "value": 2735.2199219793006,
            "unit": "iter/sec",
            "range": "stddev: 0.00007473028580674055",
            "extra": "mean: 365.6013148940379 usec\nrounds: 2585"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-optimized]",
            "value": 2253.6730105750553,
            "unit": "iter/sec",
            "range": "stddev: 0.00007446956384774841",
            "extra": "mean: 443.7200939566811 usec\nrounds: 1373"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-fast]",
            "value": 5241.154123292897,
            "unit": "iter/sec",
            "range": "stddev: 0.00009436872705246741",
            "extra": "mean: 190.79767098543613 usec\nrounds: 4477"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-optimized]",
            "value": 2726.4139837377943,
            "unit": "iter/sec",
            "range": "stddev: 0.000059406155823202364",
            "extra": "mean: 366.78215632867455 usec\nrounds: 2322"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-fast]",
            "value": 4494.511318196851,
            "unit": "iter/sec",
            "range": "stddev: 0.00004552261418781938",
            "extra": "mean: 222.49359923765618 usec\nrounds: 4197"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-optimized]",
            "value": 2883.5728546031837,
            "unit": "iter/sec",
            "range": "stddev: 0.00007833355658310965",
            "extra": "mean: 346.7920009038969 usec\nrounds: 2212"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-fast]",
            "value": 742.5787783740619,
            "unit": "iter/sec",
            "range": "stddev: 0.00019236625378821898",
            "extra": "mean: 1.3466584679265725 msec\nrounds: 686"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-optimized]",
            "value": 306.16440773616205,
            "unit": "iter/sec",
            "range": "stddev: 0.000804595644864005",
            "extra": "mean: 3.266218981475314 msec\nrounds: 216"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-fast]",
            "value": 34.90959416168455,
            "unit": "iter/sec",
            "range": "stddev: 0.002197932493903778",
            "extra": "mean: 28.645420378377306 msec\nrounds: 37"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-optimized]",
            "value": 25.720102756445993,
            "unit": "iter/sec",
            "range": "stddev: 0.05186565578021446",
            "extra": "mean: 38.88009349999113 msec\nrounds: 30"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-fast]",
            "value": 733.0017812781599,
            "unit": "iter/sec",
            "range": "stddev: 0.00023369306212515885",
            "extra": "mean: 1.364253164919008 msec\nrounds: 667"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-optimized]",
            "value": 255.58250996492623,
            "unit": "iter/sec",
            "range": "stddev: 0.00025075465421585597",
            "extra": "mean: 3.9126307983172657 msec\nrounds: 238"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-fast]",
            "value": 527.3278413301534,
            "unit": "iter/sec",
            "range": "stddev: 0.00024902718226023894",
            "extra": "mean: 1.896353504638706 msec\nrounds: 539"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-optimized]",
            "value": 262.45095752514175,
            "unit": "iter/sec",
            "range": "stddev: 0.0008067127981113966",
            "extra": "mean: 3.8102356700459135 msec\nrounds: 197"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-fast]",
            "value": 74.19587225924755,
            "unit": "iter/sec",
            "range": "stddev: 0.0009699589395222398",
            "extra": "mean: 13.47783872000188 msec\nrounds: 75"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-optimized]",
            "value": 11.723845649785362,
            "unit": "iter/sec",
            "range": "stddev: 0.027756087119493743",
            "extra": "mean: 85.2962440714415 msec\nrounds: 14"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-fast]",
            "value": 0.29968668513478186,
            "unit": "iter/sec",
            "range": "stddev: 0.3190918300143658",
            "extra": "mean: 3.336818249200019 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-optimized]",
            "value": 0.3115957906913509,
            "unit": "iter/sec",
            "range": "stddev: 0.020265575157492038",
            "extra": "mean: 3.2092859719999978 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-fast]",
            "value": 72.05177695040263,
            "unit": "iter/sec",
            "range": "stddev: 0.001489095682311345",
            "extra": "mean: 13.87890822856954 msec\nrounds: 70"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-optimized]",
            "value": 8.615051227922876,
            "unit": "iter/sec",
            "range": "stddev: 0.0041075577699330075",
            "extra": "mean: 116.07592033333782 msec\nrounds: 9"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-fast]",
            "value": 22.96062053906472,
            "unit": "iter/sec",
            "range": "stddev: 0.1828989930543078",
            "extra": "mean: 43.552829867930654 msec\nrounds: 53"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-optimized]",
            "value": 11.46137633898707,
            "unit": "iter/sec",
            "range": "stddev: 0.02068679462742341",
            "extra": "mean: 87.24955628569627 msec\nrounds: 14"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-fast]",
            "value": 5643.490330649984,
            "unit": "iter/sec",
            "range": "stddev: 0.00004611114263440605",
            "extra": "mean: 177.19530670035292 usec\nrounds: 3642"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-optimized]",
            "value": 3183.051250741406,
            "unit": "iter/sec",
            "range": "stddev: 0.00005050383458130349",
            "extra": "mean: 314.16396445614157 usec\nrounds: 2504"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-fast]",
            "value": 2718.7995616515823,
            "unit": "iter/sec",
            "range": "stddev: 0.00006272520176790756",
            "extra": "mean: 367.8093869459551 usec\nrounds: 2344"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-optimized]",
            "value": 2267.226094922334,
            "unit": "iter/sec",
            "range": "stddev: 0.00007249620846793789",
            "extra": "mean: 441.067612197828 usec\nrounds: 1738"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-fast]",
            "value": 5143.078577917691,
            "unit": "iter/sec",
            "range": "stddev: 0.0000768177210193084",
            "extra": "mean: 194.4360726459824 usec\nrounds: 4281"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-optimized]",
            "value": 2676.911218950841,
            "unit": "iter/sec",
            "range": "stddev: 0.00006229211308108632",
            "extra": "mean: 373.56487317197207 usec\nrounds: 1640"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-fast]",
            "value": 4391.421085839183,
            "unit": "iter/sec",
            "range": "stddev: 0.00005968095233312257",
            "extra": "mean: 227.7167186778455 usec\nrounds: 3480"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-optimized]",
            "value": 2892.3043139456913,
            "unit": "iter/sec",
            "range": "stddev: 0.00008928055982353685",
            "extra": "mean: 345.7450846988492 usec\nrounds: 2255"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-fast]",
            "value": 719.1440532508602,
            "unit": "iter/sec",
            "range": "stddev: 0.00029150362364900633",
            "extra": "mean: 1.3905419859617032 msec\nrounds: 641"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-optimized]",
            "value": 319.909341355059,
            "unit": "iter/sec",
            "range": "stddev: 0.0005842103383390051",
            "extra": "mean: 3.1258855892242488 msec\nrounds: 297"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-fast]",
            "value": 37.03486345875059,
            "unit": "iter/sec",
            "range": "stddev: 0.001402090354571334",
            "extra": "mean: 27.00158463156748 msec\nrounds: 38"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-optimized]",
            "value": 27.49069146859627,
            "unit": "iter/sec",
            "range": "stddev: 0.04963839892390219",
            "extra": "mean: 36.37594933333491 msec\nrounds: 36"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-fast]",
            "value": 727.6594954981867,
            "unit": "iter/sec",
            "range": "stddev: 0.00030220305851147205",
            "extra": "mean: 1.3742691549917276 msec\nrounds: 671"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-optimized]",
            "value": 256.0994854303982,
            "unit": "iter/sec",
            "range": "stddev: 0.0005059302906493058",
            "extra": "mean: 3.904732562501678 msec\nrounds: 256"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-fast]",
            "value": 532.1937190454315,
            "unit": "iter/sec",
            "range": "stddev: 0.0001933188418537872",
            "extra": "mean: 1.8790150357160331 msec\nrounds: 560"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-optimized]",
            "value": 272.2784466457392,
            "unit": "iter/sec",
            "range": "stddev: 0.000542765367468124",
            "extra": "mean: 3.6727108308396414 msec\nrounds: 201"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-fast]",
            "value": 76.76327931524798,
            "unit": "iter/sec",
            "range": "stddev: 0.0011944297335267223",
            "extra": "mean: 13.027062013508372 msec\nrounds: 74"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-optimized]",
            "value": 13.577049992426808,
            "unit": "iter/sec",
            "range": "stddev: 0.01866984836889213",
            "extra": "mean: 73.65370242856832 msec\nrounds: 14"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-fast]",
            "value": 0.30037992878235803,
            "unit": "iter/sec",
            "range": "stddev: 0.3544033923761136",
            "extra": "mean: 3.329117241799986 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-optimized]",
            "value": 0.31064214437159426,
            "unit": "iter/sec",
            "range": "stddev: 0.030832625142983978",
            "extra": "mean: 3.219138221000003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-fast]",
            "value": 78.59038046829444,
            "unit": "iter/sec",
            "range": "stddev: 0.00042007853242760477",
            "extra": "mean: 12.724203573533126 msec\nrounds: 68"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-optimized]",
            "value": 8.854660486470134,
            "unit": "iter/sec",
            "range": "stddev: 0.003011836460862767",
            "extra": "mean: 112.93487780000078 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-fast]",
            "value": 23.402213027938128,
            "unit": "iter/sec",
            "range": "stddev: 0.17586688621030871",
            "extra": "mean: 42.73100149999386 msec\nrounds: 54"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-optimized]",
            "value": 12.184282813228283,
            "unit": "iter/sec",
            "range": "stddev: 0.020955102492546996",
            "extra": "mean: 82.07294720000391 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-fast]",
            "value": 1173.4917962867137,
            "unit": "iter/sec",
            "range": "stddev: 0.00023941073252147096",
            "extra": "mean: 852.1576402700942 usec\nrounds: 1187"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-optimized]",
            "value": 947.0040189898267,
            "unit": "iter/sec",
            "range": "stddev: 0.00024170650142320407",
            "extra": "mean: 1.055961727666905 msec\nrounds: 694"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-fast]",
            "value": 17.32639300020057,
            "unit": "iter/sec",
            "range": "stddev: 0.0027751811852497273",
            "extra": "mean: 57.71541716665575 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-optimized]",
            "value": 16.957861953370447,
            "unit": "iter/sec",
            "range": "stddev: 0.0009610446735127577",
            "extra": "mean: 58.96969811110213 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-fast]",
            "value": 365.52273808297116,
            "unit": "iter/sec",
            "range": "stddev: 0.015554441744575124",
            "extra": "mean: 2.7358079151098034 msec\nrounds: 483"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-optimized]",
            "value": 248.9030911961063,
            "unit": "iter/sec",
            "range": "stddev: 0.0008060920764404908",
            "extra": "mean: 4.017627885593908 msec\nrounds: 236"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-fast]",
            "value": 16.906143414656597,
            "unit": "iter/sec",
            "range": "stddev: 0.0010825755418158779",
            "extra": "mean: 59.1500956470688 msec\nrounds: 17"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-optimized]",
            "value": 15.707849410368864,
            "unit": "iter/sec",
            "range": "stddev: 0.0024436371224578857",
            "extra": "mean: 63.662438687494216 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-fast]",
            "value": 10234.93505979743,
            "unit": "iter/sec",
            "range": "stddev: 0.00002689249712047475",
            "extra": "mean: 97.70457693747126 usec\nrounds: 5134"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-optimized]",
            "value": 3282.952672904283,
            "unit": "iter/sec",
            "range": "stddev: 0.0001235239491869657",
            "extra": "mean: 304.6038428313206 usec\nrounds: 2316"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-fast]",
            "value": 1047.033831625077,
            "unit": "iter/sec",
            "range": "stddev: 0.00016927500576609713",
            "extra": "mean: 955.0789762427477 usec\nrounds: 926"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-optimized]",
            "value": 256.18552340731407,
            "unit": "iter/sec",
            "range": "stddev: 0.0009335082018942429",
            "extra": "mean: 3.9034211875043447 msec\nrounds: 240"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-fast]",
            "value": 5913.310657697596,
            "unit": "iter/sec",
            "range": "stddev: 0.00009804444498891934",
            "extra": "mean: 169.110005864187 usec\nrounds: 4946"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-optimized]",
            "value": 3016.423960807766,
            "unit": "iter/sec",
            "range": "stddev: 0.0001237272648388959",
            "extra": "mean: 331.5183850125003 usec\nrounds: 2322"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-fast]",
            "value": 264.1991193024908,
            "unit": "iter/sec",
            "range": "stddev: 0.00044492638236345384",
            "extra": "mean: 3.785023972222501 msec\nrounds: 252"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-optimized]",
            "value": 199.27192276636956,
            "unit": "iter/sec",
            "range": "stddev: 0.0008506969711131886",
            "extra": "mean: 5.018268434998845 msec\nrounds: 200"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "athena.caesura@zapatacomputing.com",
            "name": "Athena Caesura",
            "username": "AthenaCaesura"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "b4ece0d85878bac7fec343ecb214d787a402de95",
          "message": "Dta2 209 ruby slippers compiler (#112)\n\n* feat: add ruby slippers\r\n\r\n* fix: description -> implementation\r\n\r\n* feat: add CCZ gate\r\n\r\n* fix: final changes\r\n\r\n* fix: remove unused line\r\n\r\n* fix: size of example 2\r\n\r\n* fix: little things\r\n\r\n* feat: add flag\r\n\r\n* fix: allow more memory for molecule generation\r\n\r\n* fix: respond to PR comments\r\n\r\n* fix: style in ruby slippers\r\n\r\n* feat: automatically allocate adj memory\r\n\r\n* fix: use faster defaults",
          "timestamp": "2023-08-08T16:50:13-04:00",
          "tree_id": "6047186da7fe751436264d7cd8fa2d4614f6f15a",
          "url": "https://github.com/zapatacomputing/benchq/commit/b4ece0d85878bac7fec343ecb214d787a402de95"
        },
        "date": 1691528245247,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[vlasov]",
            "value": 137.6126012959013,
            "unit": "iter/sec",
            "range": "stddev: 0.00014472387183374642",
            "extra": "mean: 7.266776375004724 msec\nrounds: 8"
          },
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[jw-2]",
            "value": 3.8756993877830026,
            "unit": "iter/sec",
            "range": "stddev: 0.05526337561185261",
            "extra": "mean: 258.0179471999827 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[many single qubit gates]",
            "value": 1.3498616356592343,
            "unit": "iter/sec",
            "range": "stddev: 0.088918917360835",
            "extra": "mean: 740.8166685999845 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[GHZ state]",
            "value": 540.4108416577028,
            "unit": "iter/sec",
            "range": "stddev: 0.008824959492430982",
            "extra": "mean: 1.8504440009614052 msec\nrounds: 1040"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[Fully connected state]",
            "value": 12.155656268261499,
            "unit": "iter/sec",
            "range": "stddev: 0.052800512691977906",
            "extra": "mean: 82.26622881818457 msec\nrounds: 11"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[CNOT chain]",
            "value": 53.86515240997452,
            "unit": "iter/sec",
            "range": "stddev: 0.00684154133818779",
            "extra": "mean: 18.56487831666887 msec\nrounds: 60"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[rotation chain]",
            "value": 190.0198657294392,
            "unit": "iter/sec",
            "range": "stddev: 0.01295555162936378",
            "extra": "mean: 5.2626076550535785 msec\nrounds: 287"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-fast]",
            "value": 7336.8408703667565,
            "unit": "iter/sec",
            "range": "stddev: 0.000011487077592868835",
            "extra": "mean: 136.2984447487426 usec\nrounds: 4009"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-optimized]",
            "value": 4387.658515712525,
            "unit": "iter/sec",
            "range": "stddev: 0.00001697966498039945",
            "extra": "mean: 227.91199370209125 usec\nrounds: 1588"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-fast]",
            "value": 3668.631212327307,
            "unit": "iter/sec",
            "range": "stddev: 0.000013957237130128693",
            "extra": "mean: 272.5812277450531 usec\nrounds: 3078"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-optimized]",
            "value": 3106.5209914389507,
            "unit": "iter/sec",
            "range": "stddev: 0.000015225564525881068",
            "extra": "mean: 321.90350644847786 usec\nrounds: 2326"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-fast]",
            "value": 6842.788481109862,
            "unit": "iter/sec",
            "range": "stddev: 0.000012548634213625238",
            "extra": "mean: 146.13925342871414 usec\nrounds: 5031"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-optimized]",
            "value": 3690.8692241128583,
            "unit": "iter/sec",
            "range": "stddev: 0.00001705230045569596",
            "extra": "mean: 270.9388870965379 usec\nrounds: 2542"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-fast]",
            "value": 5801.623787445713,
            "unit": "iter/sec",
            "range": "stddev: 0.000012689709027432684",
            "extra": "mean: 172.3655370697987 usec\nrounds: 4532"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-optimized]",
            "value": 4004.858684177237,
            "unit": "iter/sec",
            "range": "stddev: 0.000014270291778042039",
            "extra": "mean: 249.6967006478635 usec\nrounds: 2776"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-fast]",
            "value": 1002.1494151413333,
            "unit": "iter/sec",
            "range": "stddev: 0.00005562402701155798",
            "extra": "mean: 997.8551949351482 usec\nrounds: 908"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-optimized]",
            "value": 413.59337003564826,
            "unit": "iter/sec",
            "range": "stddev: 0.00037886033172297457",
            "extra": "mean: 2.4178337286059697 msec\nrounds: 409"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-fast]",
            "value": 50.87548865184274,
            "unit": "iter/sec",
            "range": "stddev: 0.00014911782642729036",
            "extra": "mean: 19.655830862742572 msec\nrounds: 51"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-optimized]",
            "value": 43.03123740798434,
            "unit": "iter/sec",
            "range": "stddev: 0.022356347016980884",
            "extra": "mean: 23.2389319999999 msec\nrounds: 49"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-fast]",
            "value": 992.6967435939711,
            "unit": "iter/sec",
            "range": "stddev: 0.0000055665019098171005",
            "extra": "mean: 1.0073569863638197 msec\nrounds: 880"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-optimized]",
            "value": 327.8338244234161,
            "unit": "iter/sec",
            "range": "stddev: 0.00006723733185334878",
            "extra": "mean: 3.0503258831170603 msec\nrounds: 308"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-fast]",
            "value": 719.999841362368,
            "unit": "iter/sec",
            "range": "stddev: 0.0000831021045490553",
            "extra": "mean: 1.3888891949029072 msec\nrounds: 667"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-optimized]",
            "value": 352.2247821328045,
            "unit": "iter/sec",
            "range": "stddev: 0.0003957081960493009",
            "extra": "mean: 2.83909608501924 msec\nrounds: 247"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-fast]",
            "value": 88.24484868824837,
            "unit": "iter/sec",
            "range": "stddev: 0.01610670487359669",
            "extra": "mean: 11.332106234697083 msec\nrounds: 98"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-optimized]",
            "value": 15.485326937231997,
            "unit": "iter/sec",
            "range": "stddev: 0.023139007418196172",
            "extra": "mean: 64.5772610454649 msec\nrounds: 22"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-fast]",
            "value": 0.4688990806160964,
            "unit": "iter/sec",
            "range": "stddev: 0.01683030339479415",
            "extra": "mean: 2.1326550666000004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-optimized]",
            "value": 0.46693426360514834,
            "unit": "iter/sec",
            "range": "stddev: 0.01491381857063742",
            "extra": "mean: 2.1416290855999933 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-fast]",
            "value": 51.846963243924236,
            "unit": "iter/sec",
            "range": "stddev: 0.09538026499228897",
            "extra": "mean: 19.287532720003355 msec\nrounds: 100"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-optimized]",
            "value": 11.858343700649497,
            "unit": "iter/sec",
            "range": "stddev: 0.0017268862295519698",
            "extra": "mean: 84.32880891664733 msec\nrounds: 12"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-fast]",
            "value": 55.61643040514834,
            "unit": "iter/sec",
            "range": "stddev: 0.026253885986158444",
            "extra": "mean: 17.980298136994985 msec\nrounds: 73"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-optimized]",
            "value": 15.230374314430195,
            "unit": "iter/sec",
            "range": "stddev: 0.017470864398087448",
            "extra": "mean: 65.65826809998612 msec\nrounds: 20"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-fast]",
            "value": 7319.234864437409,
            "unit": "iter/sec",
            "range": "stddev: 0.000010787431528466095",
            "extra": "mean: 136.62630295671823 usec\nrounds: 4905"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-optimized]",
            "value": 4394.473805841522,
            "unit": "iter/sec",
            "range": "stddev: 0.00001655859765409812",
            "extra": "mean: 227.5585301409037 usec\nrounds: 2820"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-fast]",
            "value": 3667.673102416935,
            "unit": "iter/sec",
            "range": "stddev: 0.00001362115568742297",
            "extra": "mean: 272.6524344116211 usec\nrounds: 3034"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-optimized]",
            "value": 3102.0078174978908,
            "unit": "iter/sec",
            "range": "stddev: 0.000014833769864097067",
            "extra": "mean: 322.371850373546 usec\nrounds: 2279"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-fast]",
            "value": 6857.874980718705,
            "unit": "iter/sec",
            "range": "stddev: 0.000012510706606323302",
            "extra": "mean: 145.81776465910437 usec\nrounds: 4963"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-optimized]",
            "value": 3709.1273296025865,
            "unit": "iter/sec",
            "range": "stddev: 0.000017000071029712527",
            "extra": "mean: 269.6051958149263 usec\nrounds: 2007"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-fast]",
            "value": 5799.602294916572,
            "unit": "iter/sec",
            "range": "stddev: 0.00001243222879838262",
            "extra": "mean: 172.42561630070966 usec\nrounds: 4613"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-optimized]",
            "value": 4013.390855887327,
            "unit": "iter/sec",
            "range": "stddev: 0.000014037271745669827",
            "extra": "mean: 249.1658639559312 usec\nrounds: 2830"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-fast]",
            "value": 1001.8857439065544,
            "unit": "iter/sec",
            "range": "stddev: 0.00005523929691632009",
            "extra": "mean: 998.1178054303862 usec\nrounds: 884"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-optimized]",
            "value": 419.06274159622933,
            "unit": "iter/sec",
            "range": "stddev: 0.00038640413722816695",
            "extra": "mean: 2.386277520618879 msec\nrounds: 388"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-fast]",
            "value": 51.13086551320336,
            "unit": "iter/sec",
            "range": "stddev: 0.00023654575744972223",
            "extra": "mean: 19.557658372549415 msec\nrounds: 51"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-optimized]",
            "value": 50.327923277965276,
            "unit": "iter/sec",
            "range": "stddev: 0.0001349274137270827",
            "extra": "mean: 19.869685352938518 msec\nrounds: 51"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-fast]",
            "value": 975.6840329846801,
            "unit": "iter/sec",
            "range": "stddev: 0.00027595937451333727",
            "extra": "mean: 1.0249219687862838 msec\nrounds: 897"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-optimized]",
            "value": 275.60051611013057,
            "unit": "iter/sec",
            "range": "stddev: 0.01029811981535618",
            "extra": "mean: 3.6284402297722758 msec\nrounds: 309"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-fast]",
            "value": 722.5600973360235,
            "unit": "iter/sec",
            "range": "stddev: 0.00008291372412102693",
            "extra": "mean: 1.3839679269404135 msec\nrounds: 657"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-optimized]",
            "value": 359.3757890113975,
            "unit": "iter/sec",
            "range": "stddev: 0.00040433082103366174",
            "extra": "mean: 2.7826025864204373 msec\nrounds: 324"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-fast]",
            "value": 103.10677981523978,
            "unit": "iter/sec",
            "range": "stddev: 0.00013451467192011877",
            "extra": "mean: 9.698683265949445 msec\nrounds: 94"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-optimized]",
            "value": 16.062978548343047,
            "unit": "iter/sec",
            "range": "stddev: 0.015686795975743205",
            "extra": "mean: 62.25495458332375 msec\nrounds: 12"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-fast]",
            "value": 0.4601474388042213,
            "unit": "iter/sec",
            "range": "stddev: 0.10562027786911053",
            "extra": "mean: 2.1732164859999785 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-optimized]",
            "value": 0.47202951845279645,
            "unit": "iter/sec",
            "range": "stddev: 0.00985968652938196",
            "extra": "mean: 2.1185115779999704 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-fast]",
            "value": 50.86341047737188,
            "unit": "iter/sec",
            "range": "stddev: 0.09776734100854198",
            "extra": "mean: 19.660498393926616 msec\nrounds: 99"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-optimized]",
            "value": 11.806235937729513,
            "unit": "iter/sec",
            "range": "stddev: 0.0009906928639613244",
            "extra": "mean: 84.70100083332 msec\nrounds: 12"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-fast]",
            "value": 63.84499506412769,
            "unit": "iter/sec",
            "range": "stddev: 0.01775029187431349",
            "extra": "mean: 15.662934878381183 msec\nrounds: 74"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-optimized]",
            "value": 14.090839627189336,
            "unit": "iter/sec",
            "range": "stddev: 0.017400259666454948",
            "extra": "mean: 70.96809178570344 msec\nrounds: 14"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-fast]",
            "value": 1648.2519399326122,
            "unit": "iter/sec",
            "range": "stddev: 0.000023454959697629867",
            "extra": "mean: 606.7033660162925 usec\nrounds: 1489"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-optimized]",
            "value": 1290.1667994176382,
            "unit": "iter/sec",
            "range": "stddev: 0.000029348095672669037",
            "extra": "mean: 775.0935773974225 usec\nrounds: 1053"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-fast]",
            "value": 21.399581690392907,
            "unit": "iter/sec",
            "range": "stddev: 0.0330705611295668",
            "extra": "mean: 46.72988540000006 msec\nrounds: 25"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-optimized]",
            "value": 24.404885905403873,
            "unit": "iter/sec",
            "range": "stddev: 0.00020278904020045664",
            "extra": "mean: 40.975401560003775 msec\nrounds: 25"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-fast]",
            "value": 672.2927528510606,
            "unit": "iter/sec",
            "range": "stddev: 0.00009364686986194695",
            "extra": "mean: 1.4874472404457697 msec\nrounds: 628"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-optimized]",
            "value": 333.3576680716135,
            "unit": "iter/sec",
            "range": "stddev: 0.00046143070574386106",
            "extra": "mean: 2.999781003343158 msec\nrounds: 299"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-fast]",
            "value": 23.88479436945104,
            "unit": "iter/sec",
            "range": "stddev: 0.0002808277413622835",
            "extra": "mean: 41.867641166675185 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-optimized]",
            "value": 22.341110170177913,
            "unit": "iter/sec",
            "range": "stddev: 0.0005841869687460295",
            "extra": "mean: 44.76053304346767 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-fast]",
            "value": 13457.499650749729,
            "unit": "iter/sec",
            "range": "stddev: 0.000008663696113694079",
            "extra": "mean: 74.30800861616883 usec\nrounds: 6964"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-optimized]",
            "value": 4730.300283708998,
            "unit": "iter/sec",
            "range": "stddev: 0.000009850366739029746",
            "extra": "mean: 211.40306957762655 usec\nrounds: 3090"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-fast]",
            "value": 1420.8317294344747,
            "unit": "iter/sec",
            "range": "stddev: 0.000038933614986479745",
            "extra": "mean: 703.8131112105895 usec\nrounds: 1142"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-optimized]",
            "value": 341.4856813566024,
            "unit": "iter/sec",
            "range": "stddev: 0.0006053674695582725",
            "extra": "mean: 2.9283804697970117 msec\nrounds: 298"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-fast]",
            "value": 7765.694492533184,
            "unit": "iter/sec",
            "range": "stddev: 0.000012352057104996792",
            "extra": "mean: 128.77148347279345 usec\nrounds: 5597"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-optimized]",
            "value": 4278.723194158289,
            "unit": "iter/sec",
            "range": "stddev: 0.0000165549996778053",
            "extra": "mean: 233.71458134176407 usec\nrounds: 2637"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-fast]",
            "value": 366.5601731895329,
            "unit": "iter/sec",
            "range": "stddev: 0.00012420008476152767",
            "extra": "mean: 2.7280650576377314 msec\nrounds: 347"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-optimized]",
            "value": 264.7633111435418,
            "unit": "iter/sec",
            "range": "stddev: 0.00032750343704578534",
            "extra": "mean: 3.7769583545427436 msec\nrounds: 220"
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
          "id": "6df1fa61a3c87fe2764a16a9479100fdb601c39e",
          "message": "Feat: add new field to graph data resource info - ratio between graph and measure  (#118)",
          "timestamp": "2023-08-09T18:13:22+02:00",
          "tree_id": "e5b894ff8c3b5b42febe8a697f8d74beb9bc1e7d",
          "url": "https://github.com/zapatacomputing/benchq/commit/6df1fa61a3c87fe2764a16a9479100fdb601c39e"
        },
        "date": 1691598055061,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[vlasov]",
            "value": 133.35926599510188,
            "unit": "iter/sec",
            "range": "stddev: 0.00018449443236047037",
            "extra": "mean: 7.49854157143253 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[jw-2]",
            "value": 3.7156094549328342,
            "unit": "iter/sec",
            "range": "stddev: 0.06527743918662855",
            "extra": "mean: 269.1348517999927 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[many single qubit gates]",
            "value": 1.283070516093103,
            "unit": "iter/sec",
            "range": "stddev: 0.09828777079064273",
            "extra": "mean: 779.3803906000107 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[GHZ state]",
            "value": 475.0161350698302,
            "unit": "iter/sec",
            "range": "stddev: 0.010758285203520984",
            "extra": "mean: 2.10519164754897 msec\nrounds: 959"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[Fully connected state]",
            "value": 12.808010232062001,
            "unit": "iter/sec",
            "range": "stddev: 0.032800164779894905",
            "extra": "mean: 78.0761400000074 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[CNOT chain]",
            "value": 52.8360004432812,
            "unit": "iter/sec",
            "range": "stddev: 0.007213514830114752",
            "extra": "mean: 18.926489355936162 msec\nrounds: 59"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[rotation chain]",
            "value": 171.6283712613553,
            "unit": "iter/sec",
            "range": "stddev: 0.015332359663324932",
            "extra": "mean: 5.826542503728606 msec\nrounds: 268"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-fast]",
            "value": 7335.823360511226,
            "unit": "iter/sec",
            "range": "stddev: 0.000017991654744710022",
            "extra": "mean: 136.3173499218922 usec\nrounds: 3878"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-optimized]",
            "value": 4282.0001451990365,
            "unit": "iter/sec",
            "range": "stddev: 0.00001917293759640437",
            "extra": "mean: 233.535723047837 usec\nrounds: 1549"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-fast]",
            "value": 3500.7212029863927,
            "unit": "iter/sec",
            "range": "stddev: 0.000015819615105097125",
            "extra": "mean: 285.6554241300109 usec\nrounds: 2992"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-optimized]",
            "value": 2965.6914770227772,
            "unit": "iter/sec",
            "range": "stddev: 0.000017556789501934",
            "extra": "mean: 337.18949113475827 usec\nrounds: 2256"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-fast]",
            "value": 6845.022954118127,
            "unit": "iter/sec",
            "range": "stddev: 0.00001365499229759707",
            "extra": "mean: 146.09154807850229 usec\nrounds: 5023"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-optimized]",
            "value": 3621.944089149494,
            "unit": "iter/sec",
            "range": "stddev: 0.00001832758534702415",
            "extra": "mean: 276.0948196289856 usec\nrounds: 2700"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-fast]",
            "value": 5701.372056479016,
            "unit": "iter/sec",
            "range": "stddev: 0.000014215425902276763",
            "extra": "mean: 175.39637653775011 usec\nrounds: 4552"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-optimized]",
            "value": 3870.8161672829597,
            "unit": "iter/sec",
            "range": "stddev: 0.00001664849926685811",
            "extra": "mean: 258.3434492322919 usec\nrounds: 2019"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-fast]",
            "value": 953.3259031195245,
            "unit": "iter/sec",
            "range": "stddev: 0.000059229994235068215",
            "extra": "mean: 1.0489592244664139 msec\nrounds: 842"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-optimized]",
            "value": 394.0222963392961,
            "unit": "iter/sec",
            "range": "stddev: 0.0004244896307943956",
            "extra": "mean: 2.5379274454532164 msec\nrounds: 330"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-fast]",
            "value": 45.88862784133929,
            "unit": "iter/sec",
            "range": "stddev: 0.00015587908261338306",
            "extra": "mean: 21.79189152174079 msec\nrounds: 46"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-optimized]",
            "value": 44.88420661696008,
            "unit": "iter/sec",
            "range": "stddev: 0.0002165886707766819",
            "extra": "mean: 22.279551659093755 msec\nrounds: 44"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-fast]",
            "value": 782.1213644273556,
            "unit": "iter/sec",
            "range": "stddev: 0.006430747421935126",
            "extra": "mean: 1.278573947065323 msec\nrounds: 869"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-optimized]",
            "value": 315.742192832868,
            "unit": "iter/sec",
            "range": "stddev: 0.0000634047167431645",
            "extra": "mean: 3.1671408595345083 msec\nrounds: 299"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-fast]",
            "value": 674.7508251938882,
            "unit": "iter/sec",
            "range": "stddev: 0.00009459957296101699",
            "extra": "mean: 1.4820285691575883 msec\nrounds: 629"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-optimized]",
            "value": 341.0329512467949,
            "unit": "iter/sec",
            "range": "stddev: 0.00040981234589632337",
            "extra": "mean: 2.932267971010025 msec\nrounds: 276"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-fast]",
            "value": 81.27795464030342,
            "unit": "iter/sec",
            "range": "stddev: 0.018762475326742394",
            "extra": "mean: 12.30345921505422 msec\nrounds: 93"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-optimized]",
            "value": 15.323103887966395,
            "unit": "iter/sec",
            "range": "stddev: 0.013973798830952785",
            "extra": "mean: 65.26092933333985 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-fast]",
            "value": 0.40888032263314966,
            "unit": "iter/sec",
            "range": "stddev: 0.016310232302356592",
            "extra": "mean: 2.445703411599993 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-optimized]",
            "value": 0.40636538452764537,
            "unit": "iter/sec",
            "range": "stddev: 0.013626705165594735",
            "extra": "mean: 2.4608395254000017 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-fast]",
            "value": 40.53392266437819,
            "unit": "iter/sec",
            "range": "stddev: 0.13678811562432955",
            "extra": "mean: 24.67069393406661 msec\nrounds: 91"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-optimized]",
            "value": 10.191586520679051,
            "unit": "iter/sec",
            "range": "stddev: 0.005627678417654388",
            "extra": "mean: 98.120150181816 msec\nrounds: 11"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-fast]",
            "value": 58.19234593028174,
            "unit": "iter/sec",
            "range": "stddev: 0.021867050670287425",
            "extra": "mean: 17.18439055882136 msec\nrounds: 68"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-optimized]",
            "value": 13.464712482674297,
            "unit": "iter/sec",
            "range": "stddev: 0.017014374586939888",
            "extra": "mean: 74.26820300000827 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-fast]",
            "value": 7351.276459678839,
            "unit": "iter/sec",
            "range": "stddev: 0.00001207177959454758",
            "extra": "mean: 136.03079757439673 usec\nrounds: 4782"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-optimized]",
            "value": 4291.338930898217,
            "unit": "iter/sec",
            "range": "stddev: 0.000018883863596367678",
            "extra": "mean: 233.02750402674224 usec\nrounds: 2484"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-fast]",
            "value": 3491.5314924357367,
            "unit": "iter/sec",
            "range": "stddev: 0.00001583742894159071",
            "extra": "mean: 286.4072691787143 usec\nrounds: 2972"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-optimized]",
            "value": 2955.0128563274143,
            "unit": "iter/sec",
            "range": "stddev: 0.000017865142779672267",
            "extra": "mean: 338.4080031525928 usec\nrounds: 2220"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-fast]",
            "value": 6839.752307706575,
            "unit": "iter/sec",
            "range": "stddev: 0.000013646519517893319",
            "extra": "mean: 146.20412480043566 usec\nrounds: 5008"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-optimized]",
            "value": 3624.677177362172,
            "unit": "iter/sec",
            "range": "stddev: 0.00001859620721473181",
            "extra": "mean: 275.88663791784666 usec\nrounds: 2574"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-fast]",
            "value": 4687.433906461576,
            "unit": "iter/sec",
            "range": "stddev: 0.002607365688424795",
            "extra": "mean: 213.33634136611738 usec\nrounds: 4523"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-optimized]",
            "value": 3921.5991033347545,
            "unit": "iter/sec",
            "range": "stddev: 0.000015000869412588784",
            "extra": "mean: 254.99801832105794 usec\nrounds: 2620"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-fast]",
            "value": 954.0637486046834,
            "unit": "iter/sec",
            "range": "stddev: 0.000059064857581394694",
            "extra": "mean: 1.0481479895473425 msec\nrounds: 861"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-optimized]",
            "value": 398.5026467117451,
            "unit": "iter/sec",
            "range": "stddev: 0.0003785406981772856",
            "extra": "mean: 2.5093936219784885 msec\nrounds: 455"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-fast]",
            "value": 46.011657814229224,
            "unit": "iter/sec",
            "range": "stddev: 0.0001304507005905161",
            "extra": "mean: 21.733622466668596 msec\nrounds: 45"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-optimized]",
            "value": 45.5237987583182,
            "unit": "iter/sec",
            "range": "stddev: 0.00016038717375014525",
            "extra": "mean: 21.966532391308363 msec\nrounds: 46"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-fast]",
            "value": 944.4794319044383,
            "unit": "iter/sec",
            "range": "stddev: 0.000007237297397106936",
            "extra": "mean: 1.0587843061691777 msec\nrounds: 859"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-optimized]",
            "value": 313.41352285447937,
            "unit": "iter/sec",
            "range": "stddev: 0.00006169408005255177",
            "extra": "mean: 3.1906727919468514 msec\nrounds: 298"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-fast]",
            "value": 675.5850443647703,
            "unit": "iter/sec",
            "range": "stddev: 0.00009129714973273506",
            "extra": "mean: 1.4801985454551707 msec\nrounds: 638"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-optimized]",
            "value": 344.3754544575404,
            "unit": "iter/sec",
            "range": "stddev: 0.0004257468032718634",
            "extra": "mean: 2.9038074202332402 msec\nrounds: 257"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-fast]",
            "value": 79.74717654208688,
            "unit": "iter/sec",
            "range": "stddev: 0.021228657451431456",
            "extra": "mean: 12.539628904256519 msec\nrounds: 94"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-optimized]",
            "value": 15.209471742332289,
            "unit": "iter/sec",
            "range": "stddev: 0.013496429391383489",
            "extra": "mean: 65.74850309999363 msec\nrounds: 20"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-fast]",
            "value": 0.40695821141320454,
            "unit": "iter/sec",
            "range": "stddev: 0.004537607984291488",
            "extra": "mean: 2.4572547547999988 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-optimized]",
            "value": 0.40710129319592697,
            "unit": "iter/sec",
            "range": "stddev: 0.009348666113354224",
            "extra": "mean: 2.456391116199984 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-fast]",
            "value": 39.486530744501195,
            "unit": "iter/sec",
            "range": "stddev: 0.14275815485270874",
            "extra": "mean: 25.32509139560856 msec\nrounds: 91"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-optimized]",
            "value": 8.502520637171134,
            "unit": "iter/sec",
            "range": "stddev: 0.054763737737119775",
            "extra": "mean: 117.61218145454677 msec\nrounds: 11"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-fast]",
            "value": 57.159241443319274,
            "unit": "iter/sec",
            "range": "stddev: 0.022498772004288136",
            "extra": "mean: 17.49498374627012 msec\nrounds: 67"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-optimized]",
            "value": 11.955867747750426,
            "unit": "iter/sec",
            "range": "stddev: 0.018146993800085262",
            "extra": "mean: 83.64093858332922 msec\nrounds: 12"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-fast]",
            "value": 1551.519933796173,
            "unit": "iter/sec",
            "range": "stddev: 0.000028225937651302334",
            "extra": "mean: 644.5292633483963 usec\nrounds: 1386"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-optimized]",
            "value": 1219.6075173275437,
            "unit": "iter/sec",
            "range": "stddev: 0.000032861157202188125",
            "extra": "mean: 819.9359103584757 usec\nrounds: 1004"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-fast]",
            "value": 22.34721972239587,
            "unit": "iter/sec",
            "range": "stddev: 0.0002577655360551989",
            "extra": "mean: 44.7482958695673 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-optimized]",
            "value": 21.923136708717987,
            "unit": "iter/sec",
            "range": "stddev: 0.0003819155172231461",
            "extra": "mean: 45.613910695650524 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-fast]",
            "value": 634.1886979286325,
            "unit": "iter/sec",
            "range": "stddev: 0.00009985553272958274",
            "extra": "mean: 1.5768177567121098 msec\nrounds: 596"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-optimized]",
            "value": 315.58161340978455,
            "unit": "iter/sec",
            "range": "stddev: 0.0004691926800355087",
            "extra": "mean: 3.1687524161982603 msec\nrounds: 358"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-fast]",
            "value": 21.577491717277116,
            "unit": "iter/sec",
            "range": "stddev: 0.0002524987743099746",
            "extra": "mean: 46.34458968181641 msec\nrounds: 22"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-optimized]",
            "value": 20.374574620721777,
            "unit": "iter/sec",
            "range": "stddev: 0.0009648532151899908",
            "extra": "mean: 49.080779285716176 msec\nrounds: 21"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-fast]",
            "value": 13953.109126701593,
            "unit": "iter/sec",
            "range": "stddev: 0.000008982644038033324",
            "extra": "mean: 71.66861456607788 usec\nrounds: 7236"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-optimized]",
            "value": 4706.683511916666,
            "unit": "iter/sec",
            "range": "stddev: 0.000010861151850411302",
            "extra": "mean: 212.46382882302143 usec\nrounds: 3067"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-fast]",
            "value": 1362.7258510305226,
            "unit": "iter/sec",
            "range": "stddev: 0.00004215031651401995",
            "extra": "mean: 733.8233139437243 usec\nrounds: 1169"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-optimized]",
            "value": 323.9522225375146,
            "unit": "iter/sec",
            "range": "stddev: 0.0006623962284954495",
            "extra": "mean: 3.08687494769139 msec\nrounds: 325"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-fast]",
            "value": 7869.017832589585,
            "unit": "iter/sec",
            "range": "stddev: 0.000013295981461903865",
            "extra": "mean: 127.08066257754479 usec\nrounds: 5625"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-optimized]",
            "value": 4157.140136921016,
            "unit": "iter/sec",
            "range": "stddev: 0.000019227703679436024",
            "extra": "mean: 240.54998558231176 usec\nrounds: 2497"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-fast]",
            "value": 265.7282718075938,
            "unit": "iter/sec",
            "range": "stddev: 0.015315606509320309",
            "extra": "mean: 3.7632427787889697 msec\nrounds: 330"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-optimized]",
            "value": 250.6292867227848,
            "unit": "iter/sec",
            "range": "stddev: 0.0003397027438429362",
            "extra": "mean: 3.9899566929146504 msec\nrounds: 254"
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
          "id": "6e0dcb2510b7647f68a37558f2dede3823ac48bc",
          "message": "* Implementations of PREP_int and PREP_int_prime (#119)\n\n* Added basic tests for 'get_prep_int()'\r\n\r\n* Tests split\r\n\r\n* Adressed @max-radin comments from ZQS1336: Inverse of Block Encoding\r\n\r\nCo-authored-by: Olga Okrut <olgaokrut@Olgas-MacBook-Pro-2.local>",
          "timestamp": "2023-08-10T09:25:39-07:00",
          "tree_id": "01e92f5e4812bf1972672626c298ef7906ed509e",
          "url": "https://github.com/zapatacomputing/benchq/commit/6e0dcb2510b7647f68a37558f2dede3823ac48bc"
        },
        "date": 1691685177001,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[vlasov]",
            "value": 131.31486379763996,
            "unit": "iter/sec",
            "range": "stddev: 0.0001678123245144798",
            "extra": "mean: 7.615284142860089 msec\nrounds: 7"
          },
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[jw-2]",
            "value": 3.814244265917525,
            "unit": "iter/sec",
            "range": "stddev: 0.0592016689936283",
            "extra": "mean: 262.1751336000102 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[many single qubit gates]",
            "value": 1.3196815476140817,
            "unit": "iter/sec",
            "range": "stddev: 0.11493543709428582",
            "extra": "mean: 757.7585681999949 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[GHZ state]",
            "value": 530.3968756253203,
            "unit": "iter/sec",
            "range": "stddev: 0.008971333702702424",
            "extra": "mean: 1.8853806384531082 msec\nrounds: 957"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[Fully connected state]",
            "value": 9.883543184886895,
            "unit": "iter/sec",
            "range": "stddev: 0.05975737536003188",
            "extra": "mean: 101.17829014286274 msec\nrounds: 21"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[CNOT chain]",
            "value": 53.34876437601472,
            "unit": "iter/sec",
            "range": "stddev: 0.005874165447301965",
            "extra": "mean: 18.744576593222728 msec\nrounds: 59"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[rotation chain]",
            "value": 176.64310263499266,
            "unit": "iter/sec",
            "range": "stddev: 0.01550981458789736",
            "extra": "mean: 5.661132447760244 msec\nrounds: 268"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-fast]",
            "value": 7373.076028196571,
            "unit": "iter/sec",
            "range": "stddev: 0.000011317914071223488",
            "extra": "mean: 135.62860279423927 usec\nrounds: 3721"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-optimized]",
            "value": 4391.724001577733,
            "unit": "iter/sec",
            "range": "stddev: 0.00001753346921345045",
            "extra": "mean: 227.7010120947374 usec\nrounds: 1571"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-fast]",
            "value": 3665.2286053676316,
            "unit": "iter/sec",
            "range": "stddev: 0.000014550095373639661",
            "extra": "mean: 272.83427793167556 usec\nrounds: 2882"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-optimized]",
            "value": 3112.2860039839843,
            "unit": "iter/sec",
            "range": "stddev: 0.00001696462678426114",
            "extra": "mean: 321.30723163614044 usec\nrounds: 1865"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-fast]",
            "value": 6890.8135588898185,
            "unit": "iter/sec",
            "range": "stddev: 0.000012709655139410998",
            "extra": "mean: 145.1207453886055 usec\nrounds: 4988"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-optimized]",
            "value": 3699.6892303754403,
            "unit": "iter/sec",
            "range": "stddev: 0.000017429937839748215",
            "extra": "mean: 270.2929726609824 usec\nrounds: 2597"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-fast]",
            "value": 5839.082002945239,
            "unit": "iter/sec",
            "range": "stddev: 0.00001278952186097035",
            "extra": "mean: 171.259797258473 usec\nrounds: 4523"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-optimized]",
            "value": 4008.3410431951847,
            "unit": "iter/sec",
            "range": "stddev: 0.000015014199679198129",
            "extra": "mean: 249.4797696163264 usec\nrounds: 2791"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-fast]",
            "value": 1005.0445098893609,
            "unit": "iter/sec",
            "range": "stddev: 0.00006031675307624763",
            "extra": "mean: 994.9808094669198 usec\nrounds: 845"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-optimized]",
            "value": 357.79228279521425,
            "unit": "iter/sec",
            "range": "stddev: 0.00755692097389791",
            "extra": "mean: 2.794917744417532 msec\nrounds: 403"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-fast]",
            "value": 48.84942906002911,
            "unit": "iter/sec",
            "range": "stddev: 0.0001968341377097695",
            "extra": "mean: 20.47106832653336 msec\nrounds: 49"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-optimized]",
            "value": 47.65524436028058,
            "unit": "iter/sec",
            "range": "stddev: 0.0002197489711288661",
            "extra": "mean: 20.984049361699935 msec\nrounds: 47"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-fast]",
            "value": 999.8709736154382,
            "unit": "iter/sec",
            "range": "stddev: 0.000006535831238860327",
            "extra": "mean: 1.000129043034518 msec\nrounds: 883"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-optimized]",
            "value": 324.01424214901897,
            "unit": "iter/sec",
            "range": "stddev: 0.00007799719083928049",
            "extra": "mean: 3.0862840885249883 msec\nrounds: 305"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-fast]",
            "value": 716.1999766734986,
            "unit": "iter/sec",
            "range": "stddev: 0.00009355508904910455",
            "extra": "mean: 1.3962580739595307 msec\nrounds: 649"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-optimized]",
            "value": 355.31586190661903,
            "unit": "iter/sec",
            "range": "stddev: 0.00040081278148474547",
            "extra": "mean: 2.8143972932534354 msec\nrounds: 341"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-fast]",
            "value": 80.9875546476887,
            "unit": "iter/sec",
            "range": "stddev: 0.02251760335768177",
            "extra": "mean: 12.347576172045084 msec\nrounds: 93"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-optimized]",
            "value": 18.389936085415307,
            "unit": "iter/sec",
            "range": "stddev: 0.011182046959795609",
            "extra": "mean: 54.37756799998234 msec\nrounds: 14"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-fast]",
            "value": 0.4567734290669163,
            "unit": "iter/sec",
            "range": "stddev: 0.006936511215928454",
            "extra": "mean: 2.1892692007999925 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-optimized]",
            "value": 0.4577380770972829,
            "unit": "iter/sec",
            "range": "stddev: 0.011913186113165773",
            "extra": "mean: 2.1846554831999923 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-fast]",
            "value": 44.09097315635565,
            "unit": "iter/sec",
            "range": "stddev: 0.1272253070935901",
            "extra": "mean: 22.680379415845383 msec\nrounds: 101"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-optimized]",
            "value": 11.676693321589648,
            "unit": "iter/sec",
            "range": "stddev: 0.0027249810296187536",
            "extra": "mean: 85.64068375000033 msec\nrounds: 12"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-fast]",
            "value": 60.076840133848506,
            "unit": "iter/sec",
            "range": "stddev: 0.022730498245333845",
            "extra": "mean: 16.64534948529325 msec\nrounds: 68"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-optimized]",
            "value": 15.588114586387304,
            "unit": "iter/sec",
            "range": "stddev: 0.014432583532503419",
            "extra": "mean: 64.1514401538512 msec\nrounds: 13"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-fast]",
            "value": 7440.743634594266,
            "unit": "iter/sec",
            "range": "stddev: 0.000011130805914518014",
            "extra": "mean: 134.39516923425472 usec\nrounds: 4414"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-optimized]",
            "value": 4415.246218591704,
            "unit": "iter/sec",
            "range": "stddev: 0.000016692681084046202",
            "extra": "mean: 226.48793532492104 usec\nrounds: 2845"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-fast]",
            "value": 3680.1225220837837,
            "unit": "iter/sec",
            "range": "stddev: 0.00001412654717046309",
            "extra": "mean: 271.7300834412908 usec\nrounds: 2325"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-optimized]",
            "value": 3110.4436586193547,
            "unit": "iter/sec",
            "range": "stddev: 0.000016267103996788393",
            "extra": "mean: 321.4975449656189 usec\nrounds: 2235"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-fast]",
            "value": 6888.646562970358,
            "unit": "iter/sec",
            "range": "stddev: 0.00001289937772483966",
            "extra": "mean: 145.16639674554645 usec\nrounds: 4978"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-optimized]",
            "value": 3696.8029247841896,
            "unit": "iter/sec",
            "range": "stddev: 0.00001779758636566066",
            "extra": "mean: 270.50400585213174 usec\nrounds: 2563"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-fast]",
            "value": 5813.655521958881,
            "unit": "iter/sec",
            "range": "stddev: 0.000052252939486563734",
            "extra": "mean: 172.0088154901643 usec\nrounds: 4493"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-optimized]",
            "value": 4026.1956476375676,
            "unit": "iter/sec",
            "range": "stddev: 0.000015013402261064736",
            "extra": "mean: 248.37342432347157 usec\nrounds: 2623"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-fast]",
            "value": 1000.2414443490962,
            "unit": "iter/sec",
            "range": "stddev: 0.00006449460643368312",
            "extra": "mean: 999.7586139322058 usec\nrounds: 847"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-optimized]",
            "value": 415.2738009717642,
            "unit": "iter/sec",
            "range": "stddev: 0.00038539854564408613",
            "extra": "mean: 2.408049815952616 msec\nrounds: 326"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-fast]",
            "value": 49.10524860024509,
            "unit": "iter/sec",
            "range": "stddev: 0.00019796861777961764",
            "extra": "mean: 20.364421900004572 msec\nrounds: 50"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-optimized]",
            "value": 48.4230880552516,
            "unit": "iter/sec",
            "range": "stddev: 0.00020489139280192539",
            "extra": "mean: 20.65130581632841 msec\nrounds: 49"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-fast]",
            "value": 997.2200347966938,
            "unit": "iter/sec",
            "range": "stddev: 0.000006630846148520935",
            "extra": "mean: 1.0027877149538746 msec\nrounds: 856"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-optimized]",
            "value": 325.0459140061367,
            "unit": "iter/sec",
            "range": "stddev: 0.00006992896170603898",
            "extra": "mean: 3.076488449509076 msec\nrounds: 307"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-fast]",
            "value": 716.2922562178314,
            "unit": "iter/sec",
            "range": "stddev: 0.00009398728144759047",
            "extra": "mean: 1.3960781947863057 msec\nrounds: 652"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-optimized]",
            "value": 359.36310320958046,
            "unit": "iter/sec",
            "range": "stddev: 0.0003797577601110923",
            "extra": "mean: 2.7827008144929124 msec\nrounds: 345"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-fast]",
            "value": 82.82414812530992,
            "unit": "iter/sec",
            "range": "stddev: 0.021255031117340933",
            "extra": "mean: 12.073773442100924 msec\nrounds: 95"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-optimized]",
            "value": 18.180852971354778,
            "unit": "iter/sec",
            "range": "stddev: 0.010316374684627911",
            "extra": "mean: 55.002919916660176 msec\nrounds: 12"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-fast]",
            "value": 0.4639031371956692,
            "unit": "iter/sec",
            "range": "stddev: 0.01199517877911671",
            "extra": "mean: 2.1556224130000032 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-optimized]",
            "value": 0.46006188064533915,
            "unit": "iter/sec",
            "range": "stddev: 0.015591956543341418",
            "extra": "mean: 2.1736206412000003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-fast]",
            "value": 57.69608436500785,
            "unit": "iter/sec",
            "range": "stddev: 0.0746219998768",
            "extra": "mean: 17.332198727276037 msec\nrounds: 99"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-optimized]",
            "value": 11.567607683198663,
            "unit": "iter/sec",
            "range": "stddev: 0.001512942436040344",
            "extra": "mean: 86.44829833332324 msec\nrounds: 12"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-fast]",
            "value": 57.74724670542358,
            "unit": "iter/sec",
            "range": "stddev: 0.027354283495073715",
            "extra": "mean: 17.31684291549229 msec\nrounds: 71"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-optimized]",
            "value": 15.180878087696081,
            "unit": "iter/sec",
            "range": "stddev: 0.019895907790333484",
            "extra": "mean: 65.87234244443924 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-fast]",
            "value": 1643.9501534848068,
            "unit": "iter/sec",
            "range": "stddev: 0.000027287154831811954",
            "extra": "mean: 608.290949625342 usec\nrounds: 1469"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-optimized]",
            "value": 1286.062896612378,
            "unit": "iter/sec",
            "range": "stddev: 0.00003274079517429353",
            "extra": "mean: 777.5669468686974 usec\nrounds: 1054"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-fast]",
            "value": 24.00365197322002,
            "unit": "iter/sec",
            "range": "stddev: 0.00036809173961239723",
            "extra": "mean: 41.660327399999915 msec\nrounds: 25"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-optimized]",
            "value": 23.83327764290961,
            "unit": "iter/sec",
            "range": "stddev: 0.0003862903076314727",
            "extra": "mean: 41.958139999997 msec\nrounds: 25"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-fast]",
            "value": 534.2057668792529,
            "unit": "iter/sec",
            "range": "stddev: 0.009533814821803368",
            "extra": "mean: 1.871937859903394 msec\nrounds: 621"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-optimized]",
            "value": 326.40765608739247,
            "unit": "iter/sec",
            "range": "stddev: 0.0004437506349531683",
            "extra": "mean: 3.0636536286767115 msec\nrounds: 272"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-fast]",
            "value": 23.52109535106441,
            "unit": "iter/sec",
            "range": "stddev: 0.0003550074234514545",
            "extra": "mean: 42.51502683333778 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-optimized]",
            "value": 22.334719769186353,
            "unit": "iter/sec",
            "range": "stddev: 0.0006299647135393653",
            "extra": "mean: 44.77333990908763 msec\nrounds: 22"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-fast]",
            "value": 13758.392364288371,
            "unit": "iter/sec",
            "range": "stddev: 0.000008954714101531618",
            "extra": "mean: 72.68291043913132 usec\nrounds: 6878"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-optimized]",
            "value": 4734.809366082379,
            "unit": "iter/sec",
            "range": "stddev: 0.000010717557190845557",
            "extra": "mean: 211.20174492419076 usec\nrounds: 3054"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-fast]",
            "value": 1430.7934725762905,
            "unit": "iter/sec",
            "range": "stddev: 0.00004031702010645472",
            "extra": "mean: 698.9128893629892 usec\nrounds: 1175"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-optimized]",
            "value": 338.30820119752394,
            "unit": "iter/sec",
            "range": "stddev: 0.0006225027435234349",
            "extra": "mean: 2.955884594166672 msec\nrounds: 377"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-fast]",
            "value": 7857.743102603924,
            "unit": "iter/sec",
            "range": "stddev: 0.000012009591539621385",
            "extra": "mean: 127.26300503112871 usec\nrounds: 5565"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-optimized]",
            "value": 4173.5275988305475,
            "unit": "iter/sec",
            "range": "stddev: 0.000022084415414334253",
            "extra": "mean: 239.60545996633812 usec\nrounds: 2935"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-fast]",
            "value": 368.5741770875672,
            "unit": "iter/sec",
            "range": "stddev: 0.0001274777092093129",
            "extra": "mean: 2.7131580619724653 msec\nrounds: 355"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-optimized]",
            "value": 263.10804985748615,
            "unit": "iter/sec",
            "range": "stddev: 0.0003437070904794373",
            "extra": "mean: 3.800719896413869 msec\nrounds: 251"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "monika.kodrycka@zapatacomputing.com",
            "name": "Monika Kodrycka",
            "username": "mkodrycka"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "f58ebf0c6a4db5939ec2b7d636d60486da4679c9",
          "message": "Dta2 223: Fix the bottleneck of truncating space with FNO (#114)\n\n* Add the _truncate_with_fno() method\r\n* Remove the get_occupied_and_active_indicies_with_FNO() method\r\n* Refractor tests\r\n* Add density fitting for the MP2 calculation",
          "timestamp": "2023-08-11T18:25:36-04:00",
          "tree_id": "1f874e02d8a12f5ad3ebd3b5fb0eceab5f5fca15",
          "url": "https://github.com/zapatacomputing/benchq/commit/f58ebf0c6a4db5939ec2b7d636d60486da4679c9"
        },
        "date": 1691793232006,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[vlasov]",
            "value": 121.0008195586424,
            "unit": "iter/sec",
            "range": "stddev: 0.0011748084597916102",
            "extra": "mean: 8.264406833338475 msec\nrounds: 6"
          },
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[jw-2]",
            "value": 2.942985705674269,
            "unit": "iter/sec",
            "range": "stddev: 0.10223885075235262",
            "extra": "mean: 339.79098099998737 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[many single qubit gates]",
            "value": 1.0335661881333293,
            "unit": "iter/sec",
            "range": "stddev: 0.12992019175388597",
            "extra": "mean: 967.5239104000184 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[GHZ state]",
            "value": 388.65124829894745,
            "unit": "iter/sec",
            "range": "stddev: 0.011974814325819016",
            "extra": "mean: 2.573000870000572 msec\nrounds: 700"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[Fully connected state]",
            "value": 10.799625807652486,
            "unit": "iter/sec",
            "range": "stddev: 0.0323924694623359",
            "extra": "mean: 92.5958008000066 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[CNOT chain]",
            "value": 49.75317068334073,
            "unit": "iter/sec",
            "range": "stddev: 0.008134165060612961",
            "extra": "mean: 20.099221542373748 msec\nrounds: 59"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[rotation chain]",
            "value": 127.49152044909088,
            "unit": "iter/sec",
            "range": "stddev: 0.025122939976528362",
            "extra": "mean: 7.843658907490352 msec\nrounds: 227"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-fast]",
            "value": 5685.211388257483,
            "unit": "iter/sec",
            "range": "stddev: 0.00016969517573560031",
            "extra": "mean: 175.8949547708023 usec\nrounds: 3825"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-optimized]",
            "value": 3037.0475273754064,
            "unit": "iter/sec",
            "range": "stddev: 0.00021247824129813723",
            "extra": "mean: 329.2671553494563 usec\nrounds: 1178"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-fast]",
            "value": 2211.5719306537467,
            "unit": "iter/sec",
            "range": "stddev: 0.000443835898024973",
            "extra": "mean: 452.16707000997127 usec\nrounds: 2114"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-optimized]",
            "value": 2352.676066362543,
            "unit": "iter/sec",
            "range": "stddev: 0.0002562107904248674",
            "extra": "mean: 425.04789090922037 usec\nrounds: 2255"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-fast]",
            "value": 6436.309357805546,
            "unit": "iter/sec",
            "range": "stddev: 0.00006269767926911344",
            "extra": "mean: 155.36854187831472 usec\nrounds: 5516"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-optimized]",
            "value": 2925.732604877827,
            "unit": "iter/sec",
            "range": "stddev: 0.00015108790764441153",
            "extra": "mean: 341.79473487521875 usec\nrounds: 2810"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-fast]",
            "value": 4851.428445218563,
            "unit": "iter/sec",
            "range": "stddev: 0.00009347057620596532",
            "extra": "mean: 206.12485813030446 usec\nrounds: 3905"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-optimized]",
            "value": 3262.1088856915785,
            "unit": "iter/sec",
            "range": "stddev: 0.00009470659822623722",
            "extra": "mean: 306.55015974060484 usec\nrounds: 2310"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-fast]",
            "value": 862.1915753912464,
            "unit": "iter/sec",
            "range": "stddev: 0.0003320449737323069",
            "extra": "mean: 1.1598350396154342 msec\nrounds: 934"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-optimized]",
            "value": 363.2919283938556,
            "unit": "iter/sec",
            "range": "stddev: 0.0006770897835010405",
            "extra": "mean: 2.7526072611111534 msec\nrounds: 360"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-fast]",
            "value": 44.73304952075239,
            "unit": "iter/sec",
            "range": "stddev: 0.0018045862027316528",
            "extra": "mean: 22.35483631707433 msec\nrounds: 41"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-optimized]",
            "value": 43.75219043724705,
            "unit": "iter/sec",
            "range": "stddev: 0.0016438941580769475",
            "extra": "mean: 22.855998522731824 msec\nrounds: 44"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-fast]",
            "value": 898.704169389884,
            "unit": "iter/sec",
            "range": "stddev: 0.0003426438184245106",
            "extra": "mean: 1.112713208706803 msec\nrounds: 781"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-optimized]",
            "value": 313.739149617168,
            "unit": "iter/sec",
            "range": "stddev: 0.0005162889762609919",
            "extra": "mean: 3.1873612241896616 msec\nrounds: 339"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-fast]",
            "value": 669.9518742813208,
            "unit": "iter/sec",
            "range": "stddev: 0.000310020324879561",
            "extra": "mean: 1.4926445292398542 msec\nrounds: 684"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-optimized]",
            "value": 315.1783258622734,
            "unit": "iter/sec",
            "range": "stddev: 0.0007886931037813229",
            "extra": "mean: 3.172807004619283 msec\nrounds: 433"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-fast]",
            "value": 67.01861745292842,
            "unit": "iter/sec",
            "range": "stddev: 0.032717953998995825",
            "extra": "mean: 14.921226936714499 msec\nrounds: 79"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-optimized]",
            "value": 15.06313857634083,
            "unit": "iter/sec",
            "range": "stddev: 0.019437382407432726",
            "extra": "mean: 66.3872270000003 msec\nrounds: 17"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-fast]",
            "value": 0.3598571962796704,
            "unit": "iter/sec",
            "range": "stddev: 0.07407447013447065",
            "extra": "mean: 2.7788800956000044 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-optimized]",
            "value": 0.3215802806310229,
            "unit": "iter/sec",
            "range": "stddev: 0.47527903327154297",
            "extra": "mean: 3.1096434086000047 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-fast]",
            "value": 90.9053166855975,
            "unit": "iter/sec",
            "range": "stddev: 0.0015158686503153923",
            "extra": "mean: 11.00045670000327 msec\nrounds: 80"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-optimized]",
            "value": 10.160446496190335,
            "unit": "iter/sec",
            "range": "stddev: 0.002574406796531877",
            "extra": "mean: 98.42087159997845 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-fast]",
            "value": 63.295242525919036,
            "unit": "iter/sec",
            "range": "stddev: 0.0017681653036250044",
            "extra": "mean: 15.798975722235456 msec\nrounds: 54"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-optimized]",
            "value": 10.867148269118227,
            "unit": "iter/sec",
            "range": "stddev: 0.05603699601207933",
            "extra": "mean: 92.02046160000918 msec\nrounds: 15"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-fast]",
            "value": 6643.770923873251,
            "unit": "iter/sec",
            "range": "stddev: 0.00006534419020872643",
            "extra": "mean: 150.51692953570563 usec\nrounds: 4669"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-optimized]",
            "value": 3453.356745706694,
            "unit": "iter/sec",
            "range": "stddev: 0.00010281887755067659",
            "extra": "mean: 289.5733263709945 usec\nrounds: 3064"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-fast]",
            "value": 3200.5677006984943,
            "unit": "iter/sec",
            "range": "stddev: 0.00012407208198878284",
            "extra": "mean: 312.4445703122478 usec\nrounds: 2944"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-optimized]",
            "value": 2642.1755788127543,
            "unit": "iter/sec",
            "range": "stddev: 0.0002034628705256886",
            "extra": "mean: 378.47598320825597 usec\nrounds: 2382"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-fast]",
            "value": 6128.395173700455,
            "unit": "iter/sec",
            "range": "stddev: 0.00008361312267843362",
            "extra": "mean: 163.17485600331787 usec\nrounds: 5021"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-optimized]",
            "value": 3028.162229927648,
            "unit": "iter/sec",
            "range": "stddev: 0.0001139023881421473",
            "extra": "mean: 330.2332979775304 usec\nrounds: 2470"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-fast]",
            "value": 5077.160897141817,
            "unit": "iter/sec",
            "range": "stddev: 0.00012288339916249294",
            "extra": "mean: 196.9604706762295 usec\nrounds: 5286"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-optimized]",
            "value": 3453.8029521858402,
            "unit": "iter/sec",
            "range": "stddev: 0.00009333470529720756",
            "extra": "mean: 289.5359155817273 usec\nrounds: 2689"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-fast]",
            "value": 965.4566700092356,
            "unit": "iter/sec",
            "range": "stddev: 0.00018744567900923884",
            "extra": "mean: 1.0357792649466433 msec\nrounds: 853"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-optimized]",
            "value": 398.51165960058046,
            "unit": "iter/sec",
            "range": "stddev: 0.0006381900042590274",
            "extra": "mean: 2.5093368685932003 msec\nrounds: 312"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-fast]",
            "value": 46.44769427606591,
            "unit": "iter/sec",
            "range": "stddev: 0.0016595237669440929",
            "extra": "mean: 21.52959400000381 msec\nrounds: 42"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-optimized]",
            "value": 41.66002602898156,
            "unit": "iter/sec",
            "range": "stddev: 0.0029595423971735335",
            "extra": "mean: 24.003825617015497 msec\nrounds: 47"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-fast]",
            "value": 821.016227028248,
            "unit": "iter/sec",
            "range": "stddev: 0.00019760562735803285",
            "extra": "mean: 1.2180027228202324 msec\nrounds: 837"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-optimized]",
            "value": 292.6818057526311,
            "unit": "iter/sec",
            "range": "stddev: 0.0006227942479168357",
            "extra": "mean: 3.416679753729483 msec\nrounds: 268"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-fast]",
            "value": 612.9898960163778,
            "unit": "iter/sec",
            "range": "stddev: 0.00027914021343121995",
            "extra": "mean: 1.6313482595694893 msec\nrounds: 601"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-optimized]",
            "value": 308.77913635626237,
            "unit": "iter/sec",
            "range": "stddev: 0.0006368014749729335",
            "extra": "mean: 3.2385607777794374 msec\nrounds: 360"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-fast]",
            "value": 74.95354256461725,
            "unit": "iter/sec",
            "range": "stddev: 0.026225486654844674",
            "extra": "mean: 13.341597552082382 msec\nrounds: 96"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-optimized]",
            "value": 12.336617103471882,
            "unit": "iter/sec",
            "range": "stddev: 0.024777792420355688",
            "extra": "mean: 81.05949885715192 msec\nrounds: 14"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-fast]",
            "value": 0.35696011253511645,
            "unit": "iter/sec",
            "range": "stddev: 0.09983211480477405",
            "extra": "mean: 2.8014334512000234 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-optimized]",
            "value": 0.3375133357551975,
            "unit": "iter/sec",
            "range": "stddev: 0.483795925685715",
            "extra": "mean: 2.962845891000029 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-fast]",
            "value": 52.592636063742866,
            "unit": "iter/sec",
            "range": "stddev: 0.0749830970238255",
            "extra": "mean: 19.014068790695124 msec\nrounds: 86"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-optimized]",
            "value": 10.268117314335038,
            "unit": "iter/sec",
            "range": "stddev: 0.008746866655362744",
            "extra": "mean: 97.38883666667182 msec\nrounds: 12"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-fast]",
            "value": 48.76278375647953,
            "unit": "iter/sec",
            "range": "stddev: 0.030247875259288386",
            "extra": "mean: 20.507442827587166 msec\nrounds: 58"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-optimized]",
            "value": 14.25011282170194,
            "unit": "iter/sec",
            "range": "stddev: 0.01435377166690092",
            "extra": "mean: 70.1748830000187 msec\nrounds: 11"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-fast]",
            "value": 1437.2932266466478,
            "unit": "iter/sec",
            "range": "stddev: 0.00016963781311969233",
            "extra": "mean: 695.7522525400765 usec\nrounds: 1378"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-optimized]",
            "value": 1119.2196580951447,
            "unit": "iter/sec",
            "range": "stddev: 0.00030377816941773087",
            "extra": "mean: 893.479660375113 usec\nrounds: 689"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-fast]",
            "value": 22.13177979529881,
            "unit": "iter/sec",
            "range": "stddev: 0.004385043300135329",
            "extra": "mean: 45.18389434782005 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-optimized]",
            "value": 22.354246721286803,
            "unit": "iter/sec",
            "range": "stddev: 0.0026516856930058714",
            "extra": "mean: 44.73422935999679 msec\nrounds: 25"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-fast]",
            "value": 642.3854223018247,
            "unit": "iter/sec",
            "range": "stddev: 0.00029220377146567264",
            "extra": "mean: 1.5566978410200443 msec\nrounds: 629"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-optimized]",
            "value": 299.7293809149282,
            "unit": "iter/sec",
            "range": "stddev: 0.0007858684118045834",
            "extra": "mean: 3.336342926901213 msec\nrounds: 342"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-fast]",
            "value": 21.034010248756108,
            "unit": "iter/sec",
            "range": "stddev: 0.004903726927440948",
            "extra": "mean: 47.54205157141335 msec\nrounds: 21"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-optimized]",
            "value": 18.014114797523153,
            "unit": "iter/sec",
            "range": "stddev: 0.0030472132494576954",
            "extra": "mean: 55.512025499998195 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-fast]",
            "value": 11570.677267244891,
            "unit": "iter/sec",
            "range": "stddev: 0.00006770048169708369",
            "extra": "mean: 86.42536447117682 usec\nrounds: 7622"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-optimized]",
            "value": 4205.363103868694,
            "unit": "iter/sec",
            "range": "stddev: 0.00005267544118654734",
            "extra": "mean: 237.79159499450998 usec\nrounds: 2837"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-fast]",
            "value": 1299.9328563448896,
            "unit": "iter/sec",
            "range": "stddev: 0.00021190929169789696",
            "extra": "mean: 769.2705012563252 usec\nrounds: 1195"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-optimized]",
            "value": 315.66397240619415,
            "unit": "iter/sec",
            "range": "stddev: 0.0008917080955877756",
            "extra": "mean: 3.1679256659458344 msec\nrounds: 461"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-fast]",
            "value": 6971.467503198791,
            "unit": "iter/sec",
            "range": "stddev: 0.00009652724449736966",
            "extra": "mean: 143.4418219035174 usec\nrounds: 5935"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-optimized]",
            "value": 3702.7379052210763,
            "unit": "iter/sec",
            "range": "stddev: 0.0000930319619772293",
            "extra": "mean: 270.0704250738195 usec\nrounds: 2042"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-fast]",
            "value": 241.01971812053304,
            "unit": "iter/sec",
            "range": "stddev: 0.019742235473446938",
            "extra": "mean: 4.149038127660177 msec\nrounds: 329"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-optimized]",
            "value": 210.564276393962,
            "unit": "iter/sec",
            "range": "stddev: 0.0009176899022296833",
            "extra": "mean: 4.749143668268866 msec\nrounds: 208"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "1ethanhansen@protonmail.com",
            "name": "Ethan Hansen",
            "username": "1ethanhansen"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "8b0dfe9decaaa875d368f851e4c3deed0050e864",
          "message": "feat: user accessible mlflow for scf tooling (#123)\n\n* feat: add callback function that logs to mlflow\r\n\r\n* feat: log params and add example\r\n\r\n* fix: must expose _flatten_dict to use elsewhere\r\n\r\n* fix: correct kwargs\r\n\r\n* debugging\r\n\r\n* make it a scf callback function factory instead\r\n\r\nallows for parallelization\r\n\r\n* fix function name\r\n\r\n* no log_params anymore\r\n\r\n* clean up clean up everybody everywhere\r\n\r\n* more docs\r\n\r\n* type hints\r\n\r\n* oops\r\n\r\n* try to refactor\r\n\r\n* refactor ChemAppInstance\r\n\r\n* rm icecream\r\n\r\n* still testin\r\n\r\n* tests almost working\r\n\r\n* finish tests\r\n\r\n* change example\r\n\r\n* updating docstrings\r\n\r\n* style\r\n\r\n* style\r\n\r\n* style\r\n\r\n* style\r\n\r\n* typing style fixes\r\n\r\n* style\r\n\r\n* style\r\n\r\n* style\r\n\r\n* list of args duh\r\n\r\n* orq_workspace_id needed\r\n\r\n* use fixtures\r\n\r\n* clean up\r\n\r\nCo-Authored-By: Alexander Juda <6004040+alexjuda@users.noreply.github.com>\r\n\r\n* fix: correct python run command\r\n\r\nCo-authored-by: Max Radin <radin.max@gmail.com>\r\n\r\n* updating with review suggestions\r\n\r\nCo-Authored-By: Max Radin <radin.max@gmail.com>\r\n\r\n* split ChemAppData -> MolSpec and ActiveSpaceSpec\r\n\r\n* Update subclass names\r\n\r\n* style\r\n\r\n* move methods out to functions\r\n\r\n* cant change frozen dataclass\r\n\r\n---------\r\n\r\nCo-authored-by: Alexander Juda <6004040+alexjuda@users.noreply.github.com>\r\nCo-authored-by: Max Radin <radin.max@gmail.com>",
          "timestamp": "2023-08-14T15:23:49-07:00",
          "tree_id": "451edffa39a0b3fe77c03c1683a6a2b3d053d753",
          "url": "https://github.com/zapatacomputing/benchq/commit/8b0dfe9decaaa875d368f851e4c3deed0050e864"
        },
        "date": 1692052265381,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[vlasov]",
            "value": 140.61006398585167,
            "unit": "iter/sec",
            "range": "stddev: 0.0001736585161497937",
            "extra": "mean: 7.11186647422777 msec\nrounds: 97"
          },
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[jw-2]",
            "value": 3.851715323094461,
            "unit": "iter/sec",
            "range": "stddev: 0.05731711063709959",
            "extra": "mean: 259.6245870000075 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[many single qubit gates]",
            "value": 1.4003359145956766,
            "unit": "iter/sec",
            "range": "stddev: 0.054062005642922135",
            "extra": "mean: 714.1143704000001 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[GHZ state]",
            "value": 525.7384061630602,
            "unit": "iter/sec",
            "range": "stddev: 0.009429096501846548",
            "extra": "mean: 1.902086642857599 msec\nrounds: 1078"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[Fully connected state]",
            "value": 11.013922735919898,
            "unit": "iter/sec",
            "range": "stddev: 0.056420918399632175",
            "extra": "mean: 90.79417242856466 msec\nrounds: 21"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[CNOT chain]",
            "value": 54.01253045548844,
            "unit": "iter/sec",
            "range": "stddev: 0.006777580755746058",
            "extra": "mean: 18.514222377048174 msec\nrounds: 61"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[rotation chain]",
            "value": 180.23455265546852,
            "unit": "iter/sec",
            "range": "stddev: 0.01385674785080506",
            "extra": "mean: 5.548325697079698 msec\nrounds: 274"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-fast]",
            "value": 7373.228729739607,
            "unit": "iter/sec",
            "range": "stddev: 0.000012542760004425464",
            "extra": "mean: 135.6257938895266 usec\nrounds: 3993"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-optimized]",
            "value": 4416.149981069545,
            "unit": "iter/sec",
            "range": "stddev: 0.00001708197461685606",
            "extra": "mean: 226.44158470311066 usec\nrounds: 1582"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-fast]",
            "value": 3689.6307693025005,
            "unit": "iter/sec",
            "range": "stddev: 0.000014026953270147295",
            "extra": "mean: 271.02982995478516 usec\nrounds: 2417"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-optimized]",
            "value": 3127.8522788176197,
            "unit": "iter/sec",
            "range": "stddev: 0.000015299026009297652",
            "extra": "mean: 319.70819298986095 usec\nrounds: 2368"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-fast]",
            "value": 6927.104571544257,
            "unit": "iter/sec",
            "range": "stddev: 0.000012442513183631724",
            "extra": "mean: 144.36045965119166 usec\nrounds: 5217"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-optimized]",
            "value": 3732.2891059499934,
            "unit": "iter/sec",
            "range": "stddev: 0.00001660681034932295",
            "extra": "mean: 267.93208446950314 usec\nrounds: 2640"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-fast]",
            "value": 5884.765443506933,
            "unit": "iter/sec",
            "range": "stddev: 0.000012483300799526497",
            "extra": "mean: 169.93030726541002 usec\nrounds: 4693"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-optimized]",
            "value": 4051.7364824444485,
            "unit": "iter/sec",
            "range": "stddev: 0.000014180936506739106",
            "extra": "mean: 246.8077586814558 usec\nrounds: 2851"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-fast]",
            "value": 1019.3339019633818,
            "unit": "iter/sec",
            "range": "stddev: 0.000051929028425578254",
            "extra": "mean: 981.0328078697845 usec\nrounds: 864"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-optimized]",
            "value": 418.1047472773435,
            "unit": "iter/sec",
            "range": "stddev: 0.0004287404096457404",
            "extra": "mean: 2.391745146430172 msec\nrounds: 280"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-fast]",
            "value": 44.98530308952622,
            "unit": "iter/sec",
            "range": "stddev: 0.020150764761548236",
            "extra": "mean: 22.22948232692527 msec\nrounds: 52"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-optimized]",
            "value": 50.46348594352133,
            "unit": "iter/sec",
            "range": "stddev: 0.0001125729339996787",
            "extra": "mean: 19.81630839215505 msec\nrounds: 51"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-fast]",
            "value": 1002.6791837929495,
            "unit": "iter/sec",
            "range": "stddev: 0.0000050601111147260855",
            "extra": "mean: 997.3279750529829 usec\nrounds: 922"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-optimized]",
            "value": 329.910633999493,
            "unit": "iter/sec",
            "range": "stddev: 0.00007649227532331566",
            "extra": "mean: 3.0311238770240334 msec\nrounds: 309"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-fast]",
            "value": 728.1672277139312,
            "unit": "iter/sec",
            "range": "stddev: 0.00008174555964060842",
            "extra": "mean: 1.3733109125763368 msec\nrounds: 652"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-optimized]",
            "value": 362.45878144887155,
            "unit": "iter/sec",
            "range": "stddev: 0.0003701508574761349",
            "extra": "mean: 2.7589343980097776 msec\nrounds: 402"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-fast]",
            "value": 87.73921754933633,
            "unit": "iter/sec",
            "range": "stddev: 0.017562872705011095",
            "extra": "mean: 11.397411874999838 msec\nrounds: 96"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-optimized]",
            "value": 16.131308754940672,
            "unit": "iter/sec",
            "range": "stddev: 0.014322538432935766",
            "extra": "mean: 61.99125038095384 msec\nrounds: 21"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-fast]",
            "value": 0.47475581782424187,
            "unit": "iter/sec",
            "range": "stddev: 0.006837650020654214",
            "extra": "mean: 2.1063459623999963 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-optimized]",
            "value": 0.4761760676015213,
            "unit": "iter/sec",
            "range": "stddev: 0.004680514922736253",
            "extra": "mean: 2.100063543800002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-fast]",
            "value": 54.42046708780855,
            "unit": "iter/sec",
            "range": "stddev: 0.0881827221790813",
            "extra": "mean: 18.375439490191795 msec\nrounds: 102"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-optimized]",
            "value": 10.427901472275286,
            "unit": "iter/sec",
            "range": "stddev: 0.04347714574327028",
            "extra": "mean: 95.89657158333391 msec\nrounds: 12"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-fast]",
            "value": 64.50729401294265,
            "unit": "iter/sec",
            "range": "stddev: 0.01731276853756242",
            "extra": "mean: 15.502122904106958 msec\nrounds: 73"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-optimized]",
            "value": 14.94165553642521,
            "unit": "iter/sec",
            "range": "stddev: 0.01779916105587122",
            "extra": "mean: 66.92698794736437 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-fast]",
            "value": 7412.884408636157,
            "unit": "iter/sec",
            "range": "stddev: 0.000010938032468904363",
            "extra": "mean: 134.9002554032787 usec\nrounds: 5090"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-optimized]",
            "value": 4417.492880553869,
            "unit": "iter/sec",
            "range": "stddev: 0.000016618307191589937",
            "extra": "mean: 226.3727474020556 usec\nrounds: 2791"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-fast]",
            "value": 3687.70567225759,
            "unit": "iter/sec",
            "range": "stddev: 0.00001394564602602021",
            "extra": "mean: 271.17131595478077 usec\nrounds: 3184"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-optimized]",
            "value": 3123.7548852023547,
            "unit": "iter/sec",
            "range": "stddev: 0.000014861381365113985",
            "extra": "mean: 320.127550576114 usec\nrounds: 2343"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-fast]",
            "value": 6959.308640638626,
            "unit": "iter/sec",
            "range": "stddev: 0.000012244594298218471",
            "extra": "mean: 143.69243435483477 usec\nrounds: 5187"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-optimized]",
            "value": 3737.0546088530245,
            "unit": "iter/sec",
            "range": "stddev: 0.000016342166436668955",
            "extra": "mean: 267.59041669635104 usec\nrounds: 2791"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-fast]",
            "value": 5885.057319547636,
            "unit": "iter/sec",
            "range": "stddev: 0.000012310987575047746",
            "extra": "mean: 169.9218793805846 usec\nrounds: 4709"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-optimized]",
            "value": 3951.2973489809624,
            "unit": "iter/sec",
            "range": "stddev: 0.00001777548787549412",
            "extra": "mean: 253.08143419221523 usec\nrounds: 2872"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-fast]",
            "value": 1015.1128035580728,
            "unit": "iter/sec",
            "range": "stddev: 0.00005414288943914329",
            "extra": "mean: 985.1121929453545 usec\nrounds: 907"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-optimized]",
            "value": 413.25111838124815,
            "unit": "iter/sec",
            "range": "stddev: 0.0003755166523633434",
            "extra": "mean: 2.4198361614049935 msec\nrounds: 285"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-fast]",
            "value": 51.53641731498969,
            "unit": "iter/sec",
            "range": "stddev: 0.00008993996947494738",
            "extra": "mean: 19.403754705881422 msec\nrounds: 51"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-optimized]",
            "value": 50.69700534249892,
            "unit": "iter/sec",
            "range": "stddev: 0.00007306036820268034",
            "extra": "mean: 19.725030960787493 msec\nrounds: 51"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-fast]",
            "value": 997.7833945196187,
            "unit": "iter/sec",
            "range": "stddev: 0.000013070968097899893",
            "extra": "mean: 1.0022215297353676 msec\nrounds: 908"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-optimized]",
            "value": 328.5812938135844,
            "unit": "iter/sec",
            "range": "stddev: 0.00008206215381278207",
            "extra": "mean: 3.043386884243431 msec\nrounds: 311"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-fast]",
            "value": 600.1159613260777,
            "unit": "iter/sec",
            "range": "stddev: 0.007470626175036726",
            "extra": "mean: 1.6663446141147413 msec\nrounds: 666"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-optimized]",
            "value": 358.1433901212051,
            "unit": "iter/sec",
            "range": "stddev: 0.00040816873173758967",
            "extra": "mean: 2.792177735463927 msec\nrounds: 344"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-fast]",
            "value": 104.91695403415423,
            "unit": "iter/sec",
            "range": "stddev: 0.00011339842789971311",
            "extra": "mean: 9.5313480000045 msec\nrounds: 99"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-optimized]",
            "value": 13.766114339030034,
            "unit": "iter/sec",
            "range": "stddev: 0.044333059815775906",
            "extra": "mean: 72.64213963157162 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-fast]",
            "value": 0.47552635042844343,
            "unit": "iter/sec",
            "range": "stddev: 0.010376915814689061",
            "extra": "mean: 2.1029328849999844 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-optimized]",
            "value": 0.4750774739598075,
            "unit": "iter/sec",
            "range": "stddev: 0.010131679685259042",
            "extra": "mean: 2.10491983899999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-fast]",
            "value": 54.0864465902968,
            "unit": "iter/sec",
            "range": "stddev: 0.08917206215606747",
            "extra": "mean: 18.48892029411675 msec\nrounds: 102"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-optimized]",
            "value": 11.590840257529194,
            "unit": "iter/sec",
            "range": "stddev: 0.010073844390961118",
            "extra": "mean: 86.27502215384416 msec\nrounds: 13"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-fast]",
            "value": 63.743006665381,
            "unit": "iter/sec",
            "range": "stddev: 0.019513697298394677",
            "extra": "mean: 15.687995472970098 msec\nrounds: 74"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-optimized]",
            "value": 16.650437335967116,
            "unit": "iter/sec",
            "range": "stddev: 0.017740616708394743",
            "extra": "mean: 60.058482538465796 msec\nrounds: 13"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-fast]",
            "value": 1665.507964509646,
            "unit": "iter/sec",
            "range": "stddev: 0.000023250079611424362",
            "extra": "mean: 600.4174229778703 usec\nrounds: 1532"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-optimized]",
            "value": 1100.8289979197054,
            "unit": "iter/sec",
            "range": "stddev: 0.004711922837760724",
            "extra": "mean: 908.4063027861301 usec\nrounds: 1113"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-fast]",
            "value": 25.315560255991606,
            "unit": "iter/sec",
            "range": "stddev: 0.00018034102391331852",
            "extra": "mean: 39.50139716000649 msec\nrounds: 25"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-optimized]",
            "value": 25.006888941031225,
            "unit": "iter/sec",
            "range": "stddev: 0.00018858820322154325",
            "extra": "mean: 39.98898073079387 msec\nrounds: 26"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-fast]",
            "value": 682.3976856245854,
            "unit": "iter/sec",
            "range": "stddev: 0.00009093774326606745",
            "extra": "mean: 1.4654211482043924 msec\nrounds: 641"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-optimized]",
            "value": 334.2484808395018,
            "unit": "iter/sec",
            "range": "stddev: 0.00041075662234618644",
            "extra": "mean: 2.9917862228973786 msec\nrounds: 332"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-fast]",
            "value": 24.26994067156645,
            "unit": "iter/sec",
            "range": "stddev: 0.00020677892578761296",
            "extra": "mean: 41.20323216000088 msec\nrounds: 25"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-optimized]",
            "value": 22.673604703132433,
            "unit": "iter/sec",
            "range": "stddev: 0.0008526939240565466",
            "extra": "mean: 44.10414722727554 msec\nrounds: 22"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-fast]",
            "value": 13717.265306980771,
            "unit": "iter/sec",
            "range": "stddev: 0.000008828394763860743",
            "extra": "mean: 72.90082808933468 usec\nrounds: 7469"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-optimized]",
            "value": 4764.3405036706035,
            "unit": "iter/sec",
            "range": "stddev: 0.00001024230364073075",
            "extra": "mean: 209.89263870404884 usec\nrounds: 3147"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-fast]",
            "value": 1445.9632793999276,
            "unit": "iter/sec",
            "range": "stddev: 0.000036307933695571254",
            "extra": "mean: 691.5804946409139 usec\nrounds: 1213"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-optimized]",
            "value": 348.44697000251614,
            "unit": "iter/sec",
            "range": "stddev: 0.0005699230550357907",
            "extra": "mean: 2.8698771580443907 msec\nrounds: 348"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-fast]",
            "value": 7913.678415528377,
            "unit": "iter/sec",
            "range": "stddev: 0.0000115219975975006",
            "extra": "mean: 126.36348705271877 usec\nrounds: 5831"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-optimized]",
            "value": 4322.146783315961,
            "unit": "iter/sec",
            "range": "stddev: 0.000016840004626535508",
            "extra": "mean: 231.366506075205 usec\nrounds: 3045"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-fast]",
            "value": 372.2252986066189,
            "unit": "iter/sec",
            "range": "stddev: 0.00010251270671063413",
            "extra": "mean: 2.6865449601179203 msec\nrounds: 351"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-optimized]",
            "value": 269.4443596851146,
            "unit": "iter/sec",
            "range": "stddev: 0.0002889269287046116",
            "extra": "mean: 3.711341373664853 msec\nrounds: 281"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "1ethanhansen@protonmail.com",
            "name": "Ethan Hansen",
            "username": "1ethanhansen"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "c20da266bdda40d27cb9b1a09a89b7a505e0f592",
          "message": "feat: ability to optimize ruby slippers hyperparams (#124)\n\n* time and return i\r\n\r\n* return proportion\r\n\r\n* add needed cost functions\r\n\r\n* tune them params\r\n\r\n* testing and error fixing\r\n\r\n* add estimate prop feature and test for it\r\n\r\n* tests\r\n\r\n* skip slow\r\n\r\n* add docstrings\r\n\r\n* style\r\n\r\n* address code review\r\n\r\nCo-Authored-By: Athena Caesura <mathmeetsmusic@gmail.com>\r\n\r\n* rename iteration_prop\r\n\r\n---------\r\n\r\nCo-authored-by: Athena Caesura <mathmeetsmusic@gmail.com>",
          "timestamp": "2023-08-18T08:52:29-07:00",
          "tree_id": "56c1f80925f7efd8d792e89726347febd47d6a8b",
          "url": "https://github.com/zapatacomputing/benchq/commit/c20da266bdda40d27cb9b1a09a89b7a505e0f592"
        },
        "date": 1692374483751,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[vlasov]",
            "value": 109.5039703114487,
            "unit": "iter/sec",
            "range": "stddev: 0.0010094322059133294",
            "extra": "mean: 9.13208897500084 msec\nrounds: 80"
          },
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[jw-2]",
            "value": 3.0439611882236854,
            "unit": "iter/sec",
            "range": "stddev: 0.07763052473728627",
            "extra": "mean: 328.5193004000007 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[many single qubit gates]",
            "value": 0.9975376250572918,
            "unit": "iter/sec",
            "range": "stddev: 0.07954487818723095",
            "extra": "mean: 1.0024684532000152 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[GHZ state]",
            "value": 375.4028310102441,
            "unit": "iter/sec",
            "range": "stddev: 0.013728858459845122",
            "extra": "mean: 2.6638051644653467 msec\nrounds: 833"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[Fully connected state]",
            "value": 7.704208599467224,
            "unit": "iter/sec",
            "range": "stddev: 0.08288179391300712",
            "extra": "mean: 129.79918535294513 msec\nrounds: 17"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[CNOT chain]",
            "value": 41.78093032053394,
            "unit": "iter/sec",
            "range": "stddev: 0.009776874079727667",
            "extra": "mean: 23.9343641304352 msec\nrounds: 46"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[rotation chain]",
            "value": 129.76276785198544,
            "unit": "iter/sec",
            "range": "stddev: 0.021701846033295256",
            "extra": "mean: 7.706370760684258 msec\nrounds: 234"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-fast]",
            "value": 5753.6660315340405,
            "unit": "iter/sec",
            "range": "stddev: 0.00006382242405644145",
            "extra": "mean: 173.80223226709953 usec\nrounds: 3440"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-optimized]",
            "value": 3322.0276514070397,
            "unit": "iter/sec",
            "range": "stddev: 0.00016132068938149062",
            "extra": "mean: 301.0209742162897 usec\nrounds: 1435"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-fast]",
            "value": 2646.264694207382,
            "unit": "iter/sec",
            "range": "stddev: 0.0001959500806750708",
            "extra": "mean: 377.8911467885201 usec\nrounds: 2616"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-optimized]",
            "value": 2281.5551215062014,
            "unit": "iter/sec",
            "range": "stddev: 0.0001977449763716959",
            "extra": "mean: 438.2975412576645 usec\nrounds: 1018"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-fast]",
            "value": 5449.613638598453,
            "unit": "iter/sec",
            "range": "stddev: 0.00010579160498977112",
            "extra": "mean: 183.49924716079192 usec\nrounds: 4402"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-optimized]",
            "value": 2811.0195171557893,
            "unit": "iter/sec",
            "range": "stddev: 0.00011064246185257061",
            "extra": "mean: 355.7428164041378 usec\nrounds: 1841"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-fast]",
            "value": 4471.108997259468,
            "unit": "iter/sec",
            "range": "stddev: 0.00008544144553181158",
            "extra": "mean: 223.6581574309511 usec\nrounds: 3970"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-optimized]",
            "value": 2991.7798210374694,
            "unit": "iter/sec",
            "range": "stddev: 0.00015003236435344767",
            "extra": "mean: 334.2491960699256 usec\nrounds: 2392"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-fast]",
            "value": 731.8694004607879,
            "unit": "iter/sec",
            "range": "stddev: 0.00029616024537158065",
            "extra": "mean: 1.3663639979624727 msec\nrounds: 491"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-optimized]",
            "value": 315.90375362830656,
            "unit": "iter/sec",
            "range": "stddev: 0.0007841432098094988",
            "extra": "mean: 3.1655211073452567 msec\nrounds: 354"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-fast]",
            "value": 34.99701468126527,
            "unit": "iter/sec",
            "range": "stddev: 0.0015132522453145298",
            "extra": "mean: 28.57386577419484 msec\nrounds: 31"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-optimized]",
            "value": 33.97998406567894,
            "unit": "iter/sec",
            "range": "stddev: 0.0014706297142685577",
            "extra": "mean: 29.42908972726793 msec\nrounds: 33"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-fast]",
            "value": 739.1756453676624,
            "unit": "iter/sec",
            "range": "stddev: 0.00025345266807532654",
            "extra": "mean: 1.352858425824629 msec\nrounds: 728"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-optimized]",
            "value": 250.50179902262664,
            "unit": "iter/sec",
            "range": "stddev: 0.0003219082255516882",
            "extra": "mean: 3.991987298700696 msec\nrounds: 231"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-fast]",
            "value": 511.90247376986935,
            "unit": "iter/sec",
            "range": "stddev: 0.0004423529655353679",
            "extra": "mean: 1.953497103922103 msec\nrounds: 510"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-optimized]",
            "value": 244.14348978188747,
            "unit": "iter/sec",
            "range": "stddev: 0.0009275182233492373",
            "extra": "mean: 4.0959519374994535 msec\nrounds: 128"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-fast]",
            "value": 56.579997049985764,
            "unit": "iter/sec",
            "range": "stddev: 0.03074264592549824",
            "extra": "mean: 17.674090705882275 msec\nrounds: 68"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-optimized]",
            "value": 11.147871050747469,
            "unit": "iter/sec",
            "range": "stddev: 0.023446018987247803",
            "extra": "mean: 89.70322633333201 msec\nrounds: 9"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-fast]",
            "value": 0.3144559543011102,
            "unit": "iter/sec",
            "range": "stddev: 0.028675669508992176",
            "extra": "mean: 3.1800956106000173 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-optimized]",
            "value": 0.31630004495041114,
            "unit": "iter/sec",
            "range": "stddev: 0.02392385505540973",
            "extra": "mean: 3.161555036000004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-fast]",
            "value": 30.329638586871116,
            "unit": "iter/sec",
            "range": "stddev: 0.17663333291928873",
            "extra": "mean: 32.97104899999939 msec\nrounds: 77"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-optimized]",
            "value": 7.970131171843057,
            "unit": "iter/sec",
            "range": "stddev: 0.0030888675933688258",
            "extra": "mean: 125.46844944444679 msec\nrounds: 9"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-fast]",
            "value": 43.2376974850618,
            "unit": "iter/sec",
            "range": "stddev: 0.03208865773085492",
            "extra": "mean: 23.12796606122447 msec\nrounds: 49"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-optimized]",
            "value": 10.565389603019188,
            "unit": "iter/sec",
            "range": "stddev: 0.023939152831500183",
            "extra": "mean: 94.64866300001259 msec\nrounds: 11"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-fast]",
            "value": 5948.230354308004,
            "unit": "iter/sec",
            "range": "stddev: 0.00004327617863608006",
            "extra": "mean: 168.11722822330682 usec\nrounds: 2296"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-optimized]",
            "value": 3424.5512422965357,
            "unit": "iter/sec",
            "range": "stddev: 0.00009435006799523981",
            "extra": "mean: 292.0090631581237 usec\nrounds: 1995"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-fast]",
            "value": 2770.795474638504,
            "unit": "iter/sec",
            "range": "stddev: 0.00007139121547523162",
            "extra": "mean: 360.9071868180622 usec\nrounds: 1836"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-optimized]",
            "value": 2278.860139078695,
            "unit": "iter/sec",
            "range": "stddev: 0.00018537654842834287",
            "extra": "mean: 438.81587239675156 usec\nrounds: 1967"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-fast]",
            "value": 5182.059881907605,
            "unit": "iter/sec",
            "range": "stddev: 0.00013864597575683559",
            "extra": "mean: 192.97345511026452 usec\nrounds: 4333"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-optimized]",
            "value": 2868.4819893524655,
            "unit": "iter/sec",
            "range": "stddev: 0.00011252938650924894",
            "extra": "mean: 348.6164472051439 usec\nrounds: 2254"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-fast]",
            "value": 4468.458034187359,
            "unit": "iter/sec",
            "range": "stddev: 0.00006326688489641359",
            "extra": "mean: 223.79084515266385 usec\nrounds: 3920"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-optimized]",
            "value": 3070.7475662847073,
            "unit": "iter/sec",
            "range": "stddev: 0.00006687171606061486",
            "extra": "mean: 325.65360011337515 usec\nrounds: 1778"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-fast]",
            "value": 722.376811827428,
            "unit": "iter/sec",
            "range": "stddev: 0.00037358543643376",
            "extra": "mean: 1.3843190750686702 msec\nrounds: 706"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-optimized]",
            "value": 317.94905566928935,
            "unit": "iter/sec",
            "range": "stddev: 0.0005307856194120323",
            "extra": "mean: 3.145157949580882 msec\nrounds: 357"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-fast]",
            "value": 35.491967966687014,
            "unit": "iter/sec",
            "range": "stddev: 0.0012918376227500751",
            "extra": "mean: 28.175388891892563 msec\nrounds: 37"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-optimized]",
            "value": 34.884425538379304,
            "unit": "iter/sec",
            "range": "stddev: 0.0010826690054981352",
            "extra": "mean: 28.666087647045114 msec\nrounds: 34"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-fast]",
            "value": 539.445237600475,
            "unit": "iter/sec",
            "range": "stddev: 0.011829963336234364",
            "extra": "mean: 1.8537562857133274 msec\nrounds: 532"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-optimized]",
            "value": 245.79888630393043,
            "unit": "iter/sec",
            "range": "stddev: 0.0006120580442728331",
            "extra": "mean: 4.068366683986922 msec\nrounds: 231"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-fast]",
            "value": 535.4611787470948,
            "unit": "iter/sec",
            "range": "stddev: 0.0002693448686752355",
            "extra": "mean: 1.867549020714932 msec\nrounds: 531"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-optimized]",
            "value": 262.7517451926598,
            "unit": "iter/sec",
            "range": "stddev: 0.0008691417898489746",
            "extra": "mean: 3.8058738649547736 msec\nrounds: 311"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-fast]",
            "value": 76.43138557108205,
            "unit": "iter/sec",
            "range": "stddev: 0.0008106246662385334",
            "extra": "mean: 13.083630402983978 msec\nrounds: 67"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-optimized]",
            "value": 11.876609695724182,
            "unit": "iter/sec",
            "range": "stddev: 0.015164440363123354",
            "extra": "mean: 84.19911284615338 msec\nrounds: 13"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-fast]",
            "value": 0.3171560611732007,
            "unit": "iter/sec",
            "range": "stddev: 0.058402962176739785",
            "extra": "mean: 3.153021879200014 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-optimized]",
            "value": 0.3189556464154072,
            "unit": "iter/sec",
            "range": "stddev: 0.015201146839067568",
            "extra": "mean: 3.1352321591999726 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-fast]",
            "value": 38.66826629068965,
            "unit": "iter/sec",
            "range": "stddev: 0.10756183866897455",
            "extra": "mean: 25.860999106669926 msec\nrounds: 75"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-optimized]",
            "value": 8.003388450591624,
            "unit": "iter/sec",
            "range": "stddev: 0.008687962064172649",
            "extra": "mean: 124.94707787500658 msec\nrounds: 8"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-fast]",
            "value": 53.41871867330703,
            "unit": "iter/sec",
            "range": "stddev: 0.0015094520697581893",
            "extra": "mean: 18.720029698123277 msec\nrounds: 53"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-optimized]",
            "value": 8.97366308770508,
            "unit": "iter/sec",
            "range": "stddev: 0.07336300527050582",
            "extra": "mean: 111.43721245453393 msec\nrounds: 11"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-fast]",
            "value": 1191.415654464438,
            "unit": "iter/sec",
            "range": "stddev: 0.00022594146768003842",
            "extra": "mean: 839.3376369135568 usec\nrounds: 1154"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-optimized]",
            "value": 950.4892095146009,
            "unit": "iter/sec",
            "range": "stddev: 0.000212843105026063",
            "extra": "mean: 1.0520897975377157 msec\nrounds: 731"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-fast]",
            "value": 17.189924583567848,
            "unit": "iter/sec",
            "range": "stddev: 0.0025649519069285693",
            "extra": "mean: 58.17361182351653 msec\nrounds: 17"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-optimized]",
            "value": 16.921708128999764,
            "unit": "iter/sec",
            "range": "stddev: 0.0019830136613408216",
            "extra": "mean: 59.09568894444166 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-fast]",
            "value": 486.65100426186063,
            "unit": "iter/sec",
            "range": "stddev: 0.00029507130365518086",
            "extra": "mean: 2.054860652176756 msec\nrounds: 460"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-optimized]",
            "value": 250.74415083836715,
            "unit": "iter/sec",
            "range": "stddev: 0.000742738547518144",
            "extra": "mean: 3.9881289220764824 msec\nrounds: 231"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-fast]",
            "value": 16.758467084877065,
            "unit": "iter/sec",
            "range": "stddev: 0.002485802239964959",
            "extra": "mean: 59.671328823529784 msec\nrounds: 17"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-optimized]",
            "value": 16.13379383963799,
            "unit": "iter/sec",
            "range": "stddev: 0.0014051846087379959",
            "extra": "mean: 61.981701882366316 msec\nrounds: 17"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-fast]",
            "value": 11009.371027571016,
            "unit": "iter/sec",
            "range": "stddev: 0.00003392149846836522",
            "extra": "mean: 90.83171032165937 usec\nrounds: 6162"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-optimized]",
            "value": 3763.4953717576054,
            "unit": "iter/sec",
            "range": "stddev: 0.00008374162256645253",
            "extra": "mean: 265.71043703263166 usec\nrounds: 2668"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-fast]",
            "value": 1072.2358079493633,
            "unit": "iter/sec",
            "range": "stddev: 0.00015965964282942176",
            "extra": "mean: 932.6306700318904 usec\nrounds: 991"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-optimized]",
            "value": 260.08347561187117,
            "unit": "iter/sec",
            "range": "stddev: 0.001106910795282912",
            "extra": "mean: 3.844919396156963 msec\nrounds: 260"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-fast]",
            "value": 6213.778050161307,
            "unit": "iter/sec",
            "range": "stddev: 0.000056338771229341486",
            "extra": "mean: 160.9326873163808 usec\nrounds: 4746"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-optimized]",
            "value": 3251.589117320219,
            "unit": "iter/sec",
            "range": "stddev: 0.00010955557352062852",
            "extra": "mean: 307.5419322427014 usec\nrounds: 2627"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-fast]",
            "value": 262.0580659224273,
            "unit": "iter/sec",
            "range": "stddev: 0.0006189393868836899",
            "extra": "mean: 3.8159481811027844 msec\nrounds: 254"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-optimized]",
            "value": 200.08604608326593,
            "unit": "iter/sec",
            "range": "stddev: 0.0005069299530627098",
            "extra": "mean: 4.997849773011405 msec\nrounds: 163"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "Henriamaa@gmail.com",
            "name": "Amara Katabarwa",
            "username": "akataba"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "fad541f3f6f3c47b5f878d850581fbccb144709e",
          "message": "DTA2-218-Look-into-what-LANL-magnetization-instances-entail (#122)\n\n* adding lanl code for magnetization simulations\r\n\r\n* finished adding lanl hamiltonians\r\n\r\n* removing flatten_graph method\r\n\r\n* adding changes from black, isort and flake\r\n\r\n---------\r\n\r\nCo-authored-by: Max Radin <radin.max@gmail.com>",
          "timestamp": "2023-08-21T14:59:27-04:00",
          "tree_id": "18eacf8b0599cf4c39c7ccb127586b1c4cf829e9",
          "url": "https://github.com/zapatacomputing/benchq/commit/fad541f3f6f3c47b5f878d850581fbccb144709e"
        },
        "date": 1692644914993,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[vlasov]",
            "value": 99.63907190252023,
            "unit": "iter/sec",
            "range": "stddev: 0.0016417717453407687",
            "extra": "mean: 10.036223550720432 msec\nrounds: 69"
          },
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[jw-2]",
            "value": 2.722553383935702,
            "unit": "iter/sec",
            "range": "stddev: 0.09790919626030961",
            "extra": "mean: 367.3022559999936 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[many single qubit gates]",
            "value": 0.9624126852029397,
            "unit": "iter/sec",
            "range": "stddev: 0.12194593793691509",
            "extra": "mean: 1.039055298600033 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[GHZ state]",
            "value": 346.5944321586021,
            "unit": "iter/sec",
            "range": "stddev: 0.01577401494202616",
            "extra": "mean: 2.8852165736534356 msec\nrounds: 835"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[Fully connected state]",
            "value": 8.035009936384606,
            "unit": "iter/sec",
            "range": "stddev: 0.07793035143356129",
            "extra": "mean: 124.45535324999923 msec\nrounds: 8"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[CNOT chain]",
            "value": 42.3717119274407,
            "unit": "iter/sec",
            "range": "stddev: 0.009192050461147974",
            "extra": "mean: 23.600651342868723 msec\nrounds: 35"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[rotation chain]",
            "value": 135.70313220916697,
            "unit": "iter/sec",
            "range": "stddev: 0.020649107826248677",
            "extra": "mean: 7.369026666670029 msec\nrounds: 174"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-fast]",
            "value": 5506.093033683034,
            "unit": "iter/sec",
            "range": "stddev: 0.00006418498338530122",
            "extra": "mean: 181.61698211101572 usec\nrounds: 2795"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-optimized]",
            "value": 3193.3426248151923,
            "unit": "iter/sec",
            "range": "stddev: 0.00009667523834392376",
            "extra": "mean: 313.1514896738877 usec\nrounds: 1501"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-fast]",
            "value": 2700.8293189291126,
            "unit": "iter/sec",
            "range": "stddev: 0.0001961867151154114",
            "extra": "mean: 370.2566441319969 usec\nrounds: 1849"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-optimized]",
            "value": 2286.213357652582,
            "unit": "iter/sec",
            "range": "stddev: 0.0001317465155479741",
            "extra": "mean: 437.40449536467196 usec\nrounds: 1510"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-fast]",
            "value": 4882.332478920735,
            "unit": "iter/sec",
            "range": "stddev: 0.00028280589510870175",
            "extra": "mean: 204.82013552281782 usec\nrounds: 2649"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-optimized]",
            "value": 2890.016156891817,
            "unit": "iter/sec",
            "range": "stddev: 0.00013168311479358513",
            "extra": "mean: 346.0188267858993 usec\nrounds: 1680"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-fast]",
            "value": 4999.2865960333575,
            "unit": "iter/sec",
            "range": "stddev: 0.00004704314604696386",
            "extra": "mean: 200.0285402308085 usec\nrounds: 2610"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-optimized]",
            "value": 3169.3675030240042,
            "unit": "iter/sec",
            "range": "stddev: 0.0000726051348624892",
            "extra": "mean: 315.52036772190826 usec\nrounds: 2491"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-fast]",
            "value": 806.7363988683925,
            "unit": "iter/sec",
            "range": "stddev: 0.0002547295534781253",
            "extra": "mean: 1.2395622676783866 msec\nrounds: 792"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-optimized]",
            "value": 337.87652026944306,
            "unit": "iter/sec",
            "range": "stddev: 0.0007017703929578983",
            "extra": "mean: 2.959661118809143 msec\nrounds: 303"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-fast]",
            "value": 40.565182618818014,
            "unit": "iter/sec",
            "range": "stddev: 0.0021017883194416075",
            "extra": "mean: 24.651682439021098 msec\nrounds: 41"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-optimized]",
            "value": 40.68945369998781,
            "unit": "iter/sec",
            "range": "stddev: 0.0009153811364664555",
            "extra": "mean: 24.576392874999442 msec\nrounds: 40"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-fast]",
            "value": 618.9340251200188,
            "unit": "iter/sec",
            "range": "stddev: 0.010938223314883623",
            "extra": "mean: 1.6156810894442066 msec\nrounds: 682"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-optimized]",
            "value": 279.549124633216,
            "unit": "iter/sec",
            "range": "stddev: 0.0004425641194910465",
            "extra": "mean: 3.577188808271375 msec\nrounds: 266"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-fast]",
            "value": 556.9497497789504,
            "unit": "iter/sec",
            "range": "stddev: 0.00033432255502492306",
            "extra": "mean: 1.795494118449453 msec\nrounds: 515"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-optimized]",
            "value": 278.89229508623424,
            "unit": "iter/sec",
            "range": "stddev: 0.0006559485314457994",
            "extra": "mean: 3.5856135777820515 msec\nrounds: 270"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-fast]",
            "value": 84.51522837476831,
            "unit": "iter/sec",
            "range": "stddev: 0.0007004276588424536",
            "extra": "mean: 11.832187159995252 msec\nrounds: 75"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-optimized]",
            "value": 13.184334230009249,
            "unit": "iter/sec",
            "range": "stddev: 0.020681229701643284",
            "extra": "mean: 75.84759173685622 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-fast]",
            "value": 0.30220150017778497,
            "unit": "iter/sec",
            "range": "stddev: 0.29449010373702533",
            "extra": "mean: 3.3090504163999865 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-optimized]",
            "value": 0.3177584473934264,
            "unit": "iter/sec",
            "range": "stddev: 0.04419497934186342",
            "extra": "mean: 3.1470445811999754 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-fast]",
            "value": 34.54144245804473,
            "unit": "iter/sec",
            "range": "stddev: 0.15151696627026526",
            "extra": "mean: 28.95073074075108 msec\nrounds: 81"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-optimized]",
            "value": 9.048598813525714,
            "unit": "iter/sec",
            "range": "stddev: 0.005217205550567431",
            "extra": "mean: 110.51434819999031 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-fast]",
            "value": 57.33770902616831,
            "unit": "iter/sec",
            "range": "stddev: 0.0018297611562368614",
            "extra": "mean: 17.44052940000813 msec\nrounds: 40"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-optimized]",
            "value": 10.534173704866616,
            "unit": "iter/sec",
            "range": "stddev: 0.0660119525706739",
            "extra": "mean: 94.92913521428038 msec\nrounds: 14"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-fast]",
            "value": 5799.323240257722,
            "unit": "iter/sec",
            "range": "stddev: 0.00004720544936996989",
            "extra": "mean: 172.43391316045353 usec\nrounds: 4491"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-optimized]",
            "value": 3095.239501045489,
            "unit": "iter/sec",
            "range": "stddev: 0.0001969040286130164",
            "extra": "mean: 323.0767763406441 usec\nrounds: 2705"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-fast]",
            "value": 2789.932208696316,
            "unit": "iter/sec",
            "range": "stddev: 0.00011487591152122304",
            "extra": "mean: 358.4316482253458 usec\nrounds: 2422"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-optimized]",
            "value": 2145.0193871405622,
            "unit": "iter/sec",
            "range": "stddev: 0.0001222222524787951",
            "extra": "mean: 466.1962525816884 usec\nrounds: 1548"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-fast]",
            "value": 5100.489591423559,
            "unit": "iter/sec",
            "range": "stddev: 0.00007119946508579959",
            "extra": "mean: 196.05960997969558 usec\nrounds: 4269"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-optimized]",
            "value": 2701.391607799664,
            "unit": "iter/sec",
            "range": "stddev: 0.00007133491958927333",
            "extra": "mean: 370.17957600546464 usec\nrounds: 2092"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-fast]",
            "value": 4356.934738977528,
            "unit": "iter/sec",
            "range": "stddev: 0.00011157072382280819",
            "extra": "mean: 229.51915966376788 usec\nrounds: 4165"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-optimized]",
            "value": 2831.765628172684,
            "unit": "iter/sec",
            "range": "stddev: 0.00011145797393464585",
            "extra": "mean: 353.13656965505726 usec\nrounds: 2333"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-fast]",
            "value": 781.9545843678515,
            "unit": "iter/sec",
            "range": "stddev: 0.0001763156584082237",
            "extra": "mean: 1.2788466491419332 msec\nrounds: 818"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-optimized]",
            "value": 320.73010665803827,
            "unit": "iter/sec",
            "range": "stddev: 0.0008073048882604269",
            "extra": "mean: 3.117886282706219 msec\nrounds: 237"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-fast]",
            "value": 38.45657372585148,
            "unit": "iter/sec",
            "range": "stddev: 0.0019102386321967093",
            "extra": "mean: 26.00335659460413 msec\nrounds: 37"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-optimized]",
            "value": 37.78892064308121,
            "unit": "iter/sec",
            "range": "stddev: 0.0019626551464373377",
            "extra": "mean: 26.462782820527327 msec\nrounds: 39"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-fast]",
            "value": 812.0526043002297,
            "unit": "iter/sec",
            "range": "stddev: 0.0001554445118020697",
            "extra": "mean: 1.2314473159798929 msec\nrounds: 826"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-optimized]",
            "value": 269.73514558531184,
            "unit": "iter/sec",
            "range": "stddev: 0.00048469315115640306",
            "extra": "mean: 3.707340390626701 msec\nrounds: 256"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-fast]",
            "value": 556.668712802415,
            "unit": "iter/sec",
            "range": "stddev: 0.00027609232012621414",
            "extra": "mean: 1.7964005826117657 msec\nrounds: 575"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-optimized]",
            "value": 286.74748716288326,
            "unit": "iter/sec",
            "range": "stddev: 0.0006331224753641463",
            "extra": "mean: 3.4873888866267997 msec\nrounds: 344"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-fast]",
            "value": 64.78256739726234,
            "unit": "iter/sec",
            "range": "stddev: 0.03348799352625626",
            "extra": "mean: 15.436251451223885 msec\nrounds: 82"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-optimized]",
            "value": 12.820712303624887,
            "unit": "iter/sec",
            "range": "stddev: 0.030029735464870286",
            "extra": "mean: 77.99878636362999 msec\nrounds: 11"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-fast]",
            "value": 0.3470721028122691,
            "unit": "iter/sec",
            "range": "stddev: 0.010032020993664284",
            "extra": "mean: 2.8812456889999565 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-optimized]",
            "value": 0.33540995272511615,
            "unit": "iter/sec",
            "range": "stddev: 0.06848654817077358",
            "extra": "mean: 2.9814261379999834 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-fast]",
            "value": 33.87052328692438,
            "unit": "iter/sec",
            "range": "stddev: 0.1668906776450478",
            "extra": "mean: 29.524196940472045 msec\nrounds: 84"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-optimized]",
            "value": 9.218375788244154,
            "unit": "iter/sec",
            "range": "stddev: 0.009053845961726942",
            "extra": "mean: 108.47897970000986 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-fast]",
            "value": 47.38564112737005,
            "unit": "iter/sec",
            "range": "stddev: 0.03246534197538752",
            "extra": "mean: 21.103439274189704 msec\nrounds: 62"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-optimized]",
            "value": 11.217875311083104,
            "unit": "iter/sec",
            "range": "stddev: 0.06799249601580694",
            "extra": "mean: 89.14344047058661 msec\nrounds: 17"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-fast]",
            "value": 1277.9990989936332,
            "unit": "iter/sec",
            "range": "stddev: 0.00019877837415989186",
            "extra": "mean: 782.4731651121311 usec\nrounds: 1393"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-optimized]",
            "value": 968.930605213677,
            "unit": "iter/sec",
            "range": "stddev: 0.00029854842369287163",
            "extra": "mean: 1.0320656552895975 msec\nrounds: 879"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-fast]",
            "value": 19.52654497801688,
            "unit": "iter/sec",
            "range": "stddev: 0.0023819826400978553",
            "extra": "mean: 51.21233690475232 msec\nrounds: 21"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-optimized]",
            "value": 17.65676588503643,
            "unit": "iter/sec",
            "range": "stddev: 0.006132120344674459",
            "extra": "mean: 56.635513350011024 msec\nrounds: 20"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-fast]",
            "value": 519.5763849517149,
            "unit": "iter/sec",
            "range": "stddev: 0.0005251198181221926",
            "extra": "mean: 1.9246448240578364 msec\nrounds: 557"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-optimized]",
            "value": 272.4028138481877,
            "unit": "iter/sec",
            "range": "stddev: 0.0005652612799655825",
            "extra": "mean: 3.6710340318191728 msec\nrounds: 220"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-fast]",
            "value": 18.455435627054474,
            "unit": "iter/sec",
            "range": "stddev: 0.0031624674216363135",
            "extra": "mean: 54.18457847367551 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-optimized]",
            "value": 17.11598564252691,
            "unit": "iter/sec",
            "range": "stddev: 0.004666200912644705",
            "extra": "mean: 58.42491463158096 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-fast]",
            "value": 11231.112171487905,
            "unit": "iter/sec",
            "range": "stddev: 0.00003663581300562736",
            "extra": "mean: 89.03837703078692 usec\nrounds: 5233"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-optimized]",
            "value": 3612.668950647998,
            "unit": "iter/sec",
            "range": "stddev: 0.00010374838146468476",
            "extra": "mean: 276.80366334718593 usec\nrounds: 3214"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-fast]",
            "value": 1190.8043527349696,
            "unit": "iter/sec",
            "range": "stddev: 0.00035753219005376253",
            "extra": "mean: 839.7685125211868 usec\nrounds: 1118"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-optimized]",
            "value": 285.8209851906139,
            "unit": "iter/sec",
            "range": "stddev: 0.000910270813587795",
            "extra": "mean: 3.498693419355127 msec\nrounds: 248"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-fast]",
            "value": 6804.260120801316,
            "unit": "iter/sec",
            "range": "stddev: 0.00005780200314206995",
            "extra": "mean: 146.96675057188043 usec\nrounds: 3051"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-optimized]",
            "value": 3162.461231031422,
            "unit": "iter/sec",
            "range": "stddev: 0.00022450089311108033",
            "extra": "mean: 316.2094099961044 usec\nrounds: 2461"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-fast]",
            "value": 286.5216557618546,
            "unit": "iter/sec",
            "range": "stddev: 0.00037823882887076963",
            "extra": "mean: 3.490137586078869 msec\nrounds: 273"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-optimized]",
            "value": 208.7389695359851,
            "unit": "iter/sec",
            "range": "stddev: 0.0007505357860770682",
            "extra": "mean: 4.790672303417725 msec\nrounds: 234"
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
          "id": "35bf74203db6da8bb1c3ac4638f6e2cc354ed008",
          "message": "ZQS-1338: Block encoding exp(A)\n\n* Constructs Matrix Exponentiation Circuit (#125)\r\n\r\n* Basic tests\r\n\r\nCo-authored-by: Olga Okrut <olgaokrut@Olgas-MacBook-Pro-2.local>",
          "timestamp": "2023-08-22T22:49:33-04:00",
          "tree_id": "977172506787f21db5bc235bba9ee87133f19eca",
          "url": "https://github.com/zapatacomputing/benchq/commit/35bf74203db6da8bb1c3ac4638f6e2cc354ed008"
        },
        "date": 1692759396445,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[vlasov]",
            "value": 141.67158516579985,
            "unit": "iter/sec",
            "range": "stddev: 0.00007723101876533585",
            "extra": "mean: 7.0585784639148965 msec\nrounds: 97"
          },
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[jw-2]",
            "value": 3.8780561620743357,
            "unit": "iter/sec",
            "range": "stddev: 0.05783858532111957",
            "extra": "mean: 257.8611444000103 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[many single qubit gates]",
            "value": 1.3736657197147275,
            "unit": "iter/sec",
            "range": "stddev: 0.06311126257395443",
            "extra": "mean: 727.9791477999993 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[GHZ state]",
            "value": 528.3999581705782,
            "unit": "iter/sec",
            "range": "stddev: 0.009232143190509235",
            "extra": "mean: 1.8925058273323705 msec\nrounds: 1083"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[Fully connected state]",
            "value": 11.079060508688993,
            "unit": "iter/sec",
            "range": "stddev: 0.05098612631117986",
            "extra": "mean: 90.26036090476521 msec\nrounds: 21"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[CNOT chain]",
            "value": 53.91700887282512,
            "unit": "iter/sec",
            "range": "stddev: 0.006892740612152839",
            "extra": "mean: 18.547022932201514 msec\nrounds: 59"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[rotation chain]",
            "value": 171.35163838100036,
            "unit": "iter/sec",
            "range": "stddev: 0.0158481442129103",
            "extra": "mean: 5.835952369340642 msec\nrounds: 287"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-fast]",
            "value": 7419.173416061526,
            "unit": "iter/sec",
            "range": "stddev: 0.000015732503316710742",
            "extra": "mean: 134.78590456386053 usec\nrounds: 3856"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-optimized]",
            "value": 4424.312264366914,
            "unit": "iter/sec",
            "range": "stddev: 0.000016514109309253826",
            "extra": "mean: 226.0238292974767 usec\nrounds: 1693"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-fast]",
            "value": 3680.383216113096,
            "unit": "iter/sec",
            "range": "stddev: 0.000013402109795895774",
            "extra": "mean: 271.7108358776057 usec\nrounds: 3144"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-optimized]",
            "value": 3110.6382041213906,
            "unit": "iter/sec",
            "range": "stddev: 0.000015416220743800242",
            "extra": "mean: 321.4774378695233 usec\nrounds: 2366"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-fast]",
            "value": 6933.812292673669,
            "unit": "iter/sec",
            "range": "stddev: 0.00001230934697888491",
            "extra": "mean: 144.2208063602485 usec\nrounds: 5314"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-optimized]",
            "value": 3723.884738130226,
            "unit": "iter/sec",
            "range": "stddev: 0.000016362901007456697",
            "extra": "mean: 268.5367755238587 usec\nrounds: 2958"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-fast]",
            "value": 5854.294049282761,
            "unit": "iter/sec",
            "range": "stddev: 0.000012493368119028936",
            "extra": "mean: 170.81478852646887 usec\nrounds: 4724"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-optimized]",
            "value": 4025.320641475896,
            "unit": "iter/sec",
            "range": "stddev: 0.000014577069473065478",
            "extra": "mean: 248.4274146253718 usec\nrounds: 2858"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-fast]",
            "value": 1021.0216637319559,
            "unit": "iter/sec",
            "range": "stddev: 0.000052452959866661135",
            "extra": "mean: 979.4111481874742 usec\nrounds: 911"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-optimized]",
            "value": 426.94131290443585,
            "unit": "iter/sec",
            "range": "stddev: 0.00036411700358807836",
            "extra": "mean: 2.342242293670546 msec\nrounds: 395"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-fast]",
            "value": 51.01103388478336,
            "unit": "iter/sec",
            "range": "stddev: 0.00013667816706492287",
            "extra": "mean: 19.603601884616985 msec\nrounds: 52"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-optimized]",
            "value": 49.635170506143524,
            "unit": "iter/sec",
            "range": "stddev: 0.00023970071314044524",
            "extra": "mean: 20.14700442856797 msec\nrounds: 49"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-fast]",
            "value": 1003.826679878811,
            "unit": "iter/sec",
            "range": "stddev: 0.0000054628963504908365",
            "extra": "mean: 996.1879077777919 usec\nrounds: 900"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-optimized]",
            "value": 329.08120942209075,
            "unit": "iter/sec",
            "range": "stddev: 0.00006679266371078565",
            "extra": "mean: 3.0387635980678738 msec\nrounds: 311"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-fast]",
            "value": 725.2194537715073,
            "unit": "iter/sec",
            "range": "stddev: 0.0000841057405306622",
            "extra": "mean: 1.3788929610195853 msec\nrounds: 667"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-optimized]",
            "value": 308.1038724906674,
            "unit": "iter/sec",
            "range": "stddev: 0.009497143176502295",
            "extra": "mean: 3.245658653739545 msec\nrounds: 361"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-fast]",
            "value": 105.23740740890705,
            "unit": "iter/sec",
            "range": "stddev: 0.00011270508678347988",
            "extra": "mean: 9.502324549999912 msec\nrounds: 100"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-optimized]",
            "value": 13.834969186142297,
            "unit": "iter/sec",
            "range": "stddev: 0.02113698918074736",
            "extra": "mean: 72.28060912500212 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-fast]",
            "value": 0.4615552076987104,
            "unit": "iter/sec",
            "range": "stddev: 0.14924285338649057",
            "extra": "mean: 2.1665880555999935 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-optimized]",
            "value": 0.4734807652512936,
            "unit": "iter/sec",
            "range": "stddev: 0.008805079246326881",
            "extra": "mean: 2.112018213600004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-fast]",
            "value": 59.07933728248872,
            "unit": "iter/sec",
            "range": "stddev: 0.0748152778789974",
            "extra": "mean: 16.926391628573715 msec\nrounds: 105"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-optimized]",
            "value": 11.941801644384219,
            "unit": "iter/sec",
            "range": "stddev: 0.0016068491149837838",
            "extra": "mean: 83.73945823076558 msec\nrounds: 13"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-fast]",
            "value": 63.6055242869325,
            "unit": "iter/sec",
            "range": "stddev: 0.019999854413696498",
            "extra": "mean: 15.721904837838842 msec\nrounds: 74"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-optimized]",
            "value": 16.24149319631229,
            "unit": "iter/sec",
            "range": "stddev: 0.01089580089090376",
            "extra": "mean: 61.570693526322735 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-fast]",
            "value": 7400.004492999865,
            "unit": "iter/sec",
            "range": "stddev: 0.000011075205062328229",
            "extra": "mean: 135.1350530862466 usec\nrounds: 4973"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-optimized]",
            "value": 4399.300740978427,
            "unit": "iter/sec",
            "range": "stddev: 0.000017226697184108775",
            "extra": "mean: 227.3088517648364 usec\nrounds: 2975"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-fast]",
            "value": 3685.9858448637683,
            "unit": "iter/sec",
            "range": "stddev: 0.00001429759313705407",
            "extra": "mean: 271.2978405474477 usec\nrounds: 3142"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-optimized]",
            "value": 3121.3157357437467,
            "unit": "iter/sec",
            "range": "stddev: 0.000015166772976984874",
            "extra": "mean: 320.37771397122697 usec\nrounds: 2276"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-fast]",
            "value": 6908.719851225855,
            "unit": "iter/sec",
            "range": "stddev: 0.000012833437460116651",
            "extra": "mean: 144.74461572248643 usec\nrounds: 5228"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-optimized]",
            "value": 3706.469429737535,
            "unit": "iter/sec",
            "range": "stddev: 0.00001693213604903044",
            "extra": "mean: 269.7985290197882 usec\nrounds: 2550"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-fast]",
            "value": 5870.848330901955,
            "unit": "iter/sec",
            "range": "stddev: 0.000012628152701462655",
            "extra": "mean: 170.33313477651487 usec\nrounds: 4667"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-optimized]",
            "value": 4034.69397652957,
            "unit": "iter/sec",
            "range": "stddev: 0.000014409332986939162",
            "extra": "mean: 247.85027211906336 usec\nrounds: 2690"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-fast]",
            "value": 1007.2117100014023,
            "unit": "iter/sec",
            "range": "stddev: 0.00006018948224438396",
            "extra": "mean: 992.839926373183 usec\nrounds: 910"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-optimized]",
            "value": 353.24741414217414,
            "unit": "iter/sec",
            "range": "stddev: 0.00859079220875239",
            "extra": "mean: 2.8308770566046455 msec\nrounds: 371"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-fast]",
            "value": 51.22997108404218,
            "unit": "iter/sec",
            "range": "stddev: 0.00009733561587230097",
            "extra": "mean: 19.5198236274526 msec\nrounds: 51"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-optimized]",
            "value": 50.8538965517806,
            "unit": "iter/sec",
            "range": "stddev: 0.00012881118797778934",
            "extra": "mean: 19.664176549023676 msec\nrounds: 51"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-fast]",
            "value": 1004.1074696893577,
            "unit": "iter/sec",
            "range": "stddev: 0.000006963984745220225",
            "extra": "mean: 995.9093326029848 usec\nrounds: 914"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-optimized]",
            "value": 325.9150396417743,
            "unit": "iter/sec",
            "range": "stddev: 0.00013420415645722325",
            "extra": "mean: 3.0682843022498694 msec\nrounds: 311"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-fast]",
            "value": 722.8156662650972,
            "unit": "iter/sec",
            "range": "stddev: 0.00008562589215465478",
            "extra": "mean: 1.3834785916679948 msec\nrounds: 600"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-optimized]",
            "value": 363.91902254160686,
            "unit": "iter/sec",
            "range": "stddev: 0.00035951796922445645",
            "extra": "mean: 2.747864052326833 msec\nrounds: 344"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-fast]",
            "value": 87.17698516681462,
            "unit": "iter/sec",
            "range": "stddev: 0.019156851218305734",
            "extra": "mean: 11.470917445544638 msec\nrounds: 101"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-optimized]",
            "value": 16.786257811420214,
            "unit": "iter/sec",
            "range": "stddev: 0.018278552936053162",
            "extra": "mean: 59.57253911110961 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-fast]",
            "value": 0.47190452901210145,
            "unit": "iter/sec",
            "range": "stddev: 0.005247197610184383",
            "extra": "mean: 2.119072690600001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-optimized]",
            "value": 0.4714201858359446,
            "unit": "iter/sec",
            "range": "stddev: 0.007763078626670433",
            "extra": "mean: 2.12124985319997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-fast]",
            "value": 53.46185419129807,
            "unit": "iter/sec",
            "range": "stddev: 0.09213544490304545",
            "extra": "mean: 18.704925504861535 msec\nrounds: 103"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-optimized]",
            "value": 10.17012297801808,
            "unit": "iter/sec",
            "range": "stddev: 0.05029436777910655",
            "extra": "mean: 98.3272279166556 msec\nrounds: 12"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-fast]",
            "value": 63.312801122004394,
            "unit": "iter/sec",
            "range": "stddev: 0.019519069615765064",
            "extra": "mean: 15.794594178087149 msec\nrounds: 73"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-optimized]",
            "value": 16.1186923379115,
            "unit": "iter/sec",
            "range": "stddev: 0.016366910051482757",
            "extra": "mean: 62.03977215000123 msec\nrounds: 20"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-fast]",
            "value": 1661.126578054912,
            "unit": "iter/sec",
            "range": "stddev: 0.000023594033804884705",
            "extra": "mean: 602.0010836085382 usec\nrounds: 1519"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-optimized]",
            "value": 1288.6061855029297,
            "unit": "iter/sec",
            "range": "stddev: 0.00003304773541760689",
            "extra": "mean: 776.0322829815615 usec\nrounds: 1046"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-fast]",
            "value": 24.98115707353071,
            "unit": "iter/sec",
            "range": "stddev: 0.0002299578351961633",
            "extra": "mean: 40.03017142306712 msec\nrounds: 26"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-optimized]",
            "value": 24.723285247941003,
            "unit": "iter/sec",
            "range": "stddev: 0.0001707007704726525",
            "extra": "mean: 40.44769900000574 msec\nrounds: 25"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-fast]",
            "value": 680.4514404911633,
            "unit": "iter/sec",
            "range": "stddev: 0.000092889136837009",
            "extra": "mean: 1.469612584372193 msec\nrounds: 640"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-optimized]",
            "value": 339.69405822161997,
            "unit": "iter/sec",
            "range": "stddev: 0.000399414076714561",
            "extra": "mean: 2.9438254093558194 msec\nrounds: 342"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-fast]",
            "value": 23.927640207896623,
            "unit": "iter/sec",
            "range": "stddev: 0.00022336723285811948",
            "extra": "mean: 41.792671208336664 msec\nrounds: 24"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-optimized]",
            "value": 18.301344086435897,
            "unit": "iter/sec",
            "range": "stddev: 0.050244139673304766",
            "extra": "mean: 54.64079552174277 msec\nrounds: 23"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-fast]",
            "value": 13681.420261882382,
            "unit": "iter/sec",
            "range": "stddev: 0.000008752550144659471",
            "extra": "mean: 73.09182678834055 usec\nrounds: 7257"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-optimized]",
            "value": 4748.030458372123,
            "unit": "iter/sec",
            "range": "stddev: 0.000009474150178419672",
            "extra": "mean: 210.6136447032931 usec\nrounds: 3172"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-fast]",
            "value": 1444.3672488529226,
            "unit": "iter/sec",
            "range": "stddev: 0.00003825297502919621",
            "extra": "mean: 692.3446933556359 usec\nrounds: 1174"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-optimized]",
            "value": 339.6324868089761,
            "unit": "iter/sec",
            "range": "stddev: 0.0005976961030833425",
            "extra": "mean: 2.9443590906026693 msec\nrounds: 298"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-fast]",
            "value": 7883.415581135365,
            "unit": "iter/sec",
            "range": "stddev: 0.000011800986042321038",
            "extra": "mean: 126.8485708647597 usec\nrounds: 5828"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-optimized]",
            "value": 4290.253013501174,
            "unit": "iter/sec",
            "range": "stddev: 0.000017393534696121958",
            "extra": "mean: 233.08648624056875 usec\nrounds: 3089"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-fast]",
            "value": 372.2201872933501,
            "unit": "iter/sec",
            "range": "stddev: 0.00010554151954191852",
            "extra": "mean: 2.6865818516497897 msec\nrounds: 364"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-optimized]",
            "value": 268.75386247632525,
            "unit": "iter/sec",
            "range": "stddev: 0.00030192977151748086",
            "extra": "mean: 3.7208767560990528 msec\nrounds: 287"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "radin.max@gmail.com",
            "name": "Max Radin",
            "username": "max-radin"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "5c06364836d323adbdf829a17a85292f9c462c87",
          "message": "Increasing maximum data qubit code distance (#128)",
          "timestamp": "2023-08-24T09:05:58-04:00",
          "tree_id": "0864bb8027e9cd0d08dd0e9701851ec7cc280a64",
          "url": "https://github.com/zapatacomputing/benchq/commit/5c06364836d323adbdf829a17a85292f9c462c87"
        },
        "date": 1692882880968,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[vlasov]",
            "value": 120.79278922734285,
            "unit": "iter/sec",
            "range": "stddev: 0.00018528922695258018",
            "extra": "mean: 8.27863986249966 msec\nrounds: 80"
          },
          {
            "name": "benchmarks/test_get_qsp_program.py::test_get_qsp_program[jw-2]",
            "value": 3.21067329929787,
            "unit": "iter/sec",
            "range": "stddev: 0.08148211191701828",
            "extra": "mean: 311.461150599996 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[many single qubit gates]",
            "value": 1.1179021285531436,
            "unit": "iter/sec",
            "range": "stddev: 0.11426993493040395",
            "extra": "mean: 894.5326915999885 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[GHZ state]",
            "value": 453.67056683916246,
            "unit": "iter/sec",
            "range": "stddev: 0.011294305020366168",
            "extra": "mean: 2.20424262249864 msec\nrounds: 800"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[Fully connected state]",
            "value": 11.381111802147771,
            "unit": "iter/sec",
            "range": "stddev: 0.040140435276068906",
            "extra": "mean: 87.8648779999935 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[CNOT chain]",
            "value": 38.19441344937698,
            "unit": "iter/sec",
            "range": "stddev: 0.02706147305974364",
            "extra": "mean: 26.181839428569933 msec\nrounds: 49"
          },
          {
            "name": "benchmarks/test_ruby_slippers_performance.py::test_ruby_slippers[rotation chain]",
            "value": 147.04972287503207,
            "unit": "iter/sec",
            "range": "stddev: 0.0191117343681512",
            "extra": "mean: 6.800420840301987 msec\nrounds: 263"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-fast]",
            "value": 6195.602656440385,
            "unit": "iter/sec",
            "range": "stddev: 0.00001689010877510352",
            "extra": "mean: 161.40479876650755 usec\nrounds: 3404"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-path_graph-optimized]",
            "value": 3649.9544111400987,
            "unit": "iter/sec",
            "range": "stddev: 0.000024046764536714563",
            "extra": "mean: 273.97602472728977 usec\nrounds: 1375"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-fast]",
            "value": 2930.9932446055395,
            "unit": "iter/sec",
            "range": "stddev: 0.000019818444695769597",
            "extra": "mean: 341.1812708338679 usec\nrounds: 1920"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-complete_graph-optimized]",
            "value": 2483.066378770811,
            "unit": "iter/sec",
            "range": "stddev: 0.00002263486063507501",
            "extra": "mean: 402.7278563914303 usec\nrounds: 1901"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-fast]",
            "value": 5777.026152170991,
            "unit": "iter/sec",
            "range": "stddev: 0.000016362974039061525",
            "extra": "mean: 173.0994414183503 usec\nrounds: 4259"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-star_graph-optimized]",
            "value": 3053.9531489979386,
            "unit": "iter/sec",
            "range": "stddev: 0.000021852169742501532",
            "extra": "mean: 327.44444698770815 usec\nrounds: 1660"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-fast]",
            "value": 4835.062533980647,
            "unit": "iter/sec",
            "range": "stddev: 0.000017051248706188354",
            "extra": "mean: 206.82255771709998 usec\nrounds: 3751"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[10-wheel_graph-optimized]",
            "value": 3239.469873109653,
            "unit": "iter/sec",
            "range": "stddev: 0.000021710472622127975",
            "extra": "mean: 308.69248339083134 usec\nrounds: 2288"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-fast]",
            "value": 793.2524588481649,
            "unit": "iter/sec",
            "range": "stddev: 0.00008572800780469915",
            "extra": "mean: 1.2606327138929276 msec\nrounds: 727"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-path_graph-optimized]",
            "value": 338.73482038745306,
            "unit": "iter/sec",
            "range": "stddev: 0.00045316349794426695",
            "extra": "mean: 2.952161808627102 msec\nrounds: 371"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-fast]",
            "value": 37.958578384600024,
            "unit": "iter/sec",
            "range": "stddev: 0.0002394418313391247",
            "extra": "mean: 26.344506105257743 msec\nrounds: 38"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-complete_graph-optimized]",
            "value": 36.88214366315892,
            "unit": "iter/sec",
            "range": "stddev: 0.00022313777305433012",
            "extra": "mean: 27.113391486484733 msec\nrounds: 37"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-fast]",
            "value": 796.2522121488288,
            "unit": "iter/sec",
            "range": "stddev: 0.000023572893961183475",
            "extra": "mean: 1.2558834810660324 msec\nrounds: 713"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-star_graph-optimized]",
            "value": 264.8582566486949,
            "unit": "iter/sec",
            "range": "stddev: 0.00017374655506940677",
            "extra": "mean: 3.775604403099236 msec\nrounds: 258"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-fast]",
            "value": 561.0869623421526,
            "unit": "iter/sec",
            "range": "stddev: 0.00012497481531109145",
            "extra": "mean: 1.7822549214576064 msec\nrounds: 522"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[100-wheel_graph-optimized]",
            "value": 287.21939531517955,
            "unit": "iter/sec",
            "range": "stddev: 0.0004467528507694507",
            "extra": "mean: 3.4816590255078426 msec\nrounds: 196"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-fast]",
            "value": 63.340514775337375,
            "unit": "iter/sec",
            "range": "stddev: 0.028672672858942008",
            "extra": "mean: 15.787683499998417 msec\nrounds: 76"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-path_graph-optimized]",
            "value": 14.069663559582656,
            "unit": "iter/sec",
            "range": "stddev: 0.02087193319710415",
            "extra": "mean: 71.0749049375039 msec\nrounds: 16"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-fast]",
            "value": 0.3433508083093756,
            "unit": "iter/sec",
            "range": "stddev: 0.027013294344198625",
            "extra": "mean: 2.9124731202000023 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-complete_graph-optimized]",
            "value": 0.34235368389933385,
            "unit": "iter/sec",
            "range": "stddev: 0.008196830777602407",
            "extra": "mean: 2.9209558624000125 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-fast]",
            "value": 30.774373523635155,
            "unit": "iter/sec",
            "range": "stddev: 0.1721095920914066",
            "extra": "mean: 32.49456887341625 msec\nrounds: 79"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-star_graph-optimized]",
            "value": 8.09088343729281,
            "unit": "iter/sec",
            "range": "stddev: 0.003412492537273385",
            "extra": "mean: 123.5958974999889 msec\nrounds: 8"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-fast]",
            "value": 42.966552932170785,
            "unit": "iter/sec",
            "range": "stddev: 0.03362608759674606",
            "extra": "mean: 23.273917309090436 msec\nrounds: 55"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing[1000-wheel_graph-optimized]",
            "value": 10.492776772471307,
            "unit": "iter/sec",
            "range": "stddev: 0.02665289308476522",
            "extra": "mean: 95.30365714284373 msec\nrounds: 14"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-fast]",
            "value": 5677.952617372719,
            "unit": "iter/sec",
            "range": "stddev: 0.00011465155732127898",
            "extra": "mean: 176.1198212433686 usec\nrounds: 4039"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-path_graph-optimized]",
            "value": 3598.1641567838547,
            "unit": "iter/sec",
            "range": "stddev: 0.000039916831195007546",
            "extra": "mean: 277.91950462144274 usec\nrounds: 1407"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-fast]",
            "value": 2917.538729053407,
            "unit": "iter/sec",
            "range": "stddev: 0.000019867595642446947",
            "extra": "mean: 342.75466167485945 usec\nrounds: 2471"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-complete_graph-optimized]",
            "value": 2474.725563906621,
            "unit": "iter/sec",
            "range": "stddev: 0.00002383167522105706",
            "extra": "mean: 404.08521032990507 usec\nrounds: 1878"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-fast]",
            "value": 5749.760993565912,
            "unit": "iter/sec",
            "range": "stddev: 0.000017081385147549773",
            "extra": "mean: 173.92027270681658 usec\nrounds: 4558"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-star_graph-optimized]",
            "value": 3030.1477818246362,
            "unit": "iter/sec",
            "range": "stddev: 0.00002363270405359096",
            "extra": "mean: 330.01690742549835 usec\nrounds: 2020"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-fast]",
            "value": 4817.196831155174,
            "unit": "iter/sec",
            "range": "stddev: 0.000016448889839578286",
            "extra": "mean: 207.58960761837872 usec\nrounds: 3833"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[10-wheel_graph-optimized]",
            "value": 3269.209091216607,
            "unit": "iter/sec",
            "range": "stddev: 0.000019667289956472603",
            "extra": "mean: 305.8843812366431 usec\nrounds: 1844"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-fast]",
            "value": 795.8217703717634,
            "unit": "iter/sec",
            "range": "stddev: 0.00008105455432761777",
            "extra": "mean: 1.2565627596903461 msec\nrounds: 774"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-path_graph-optimized]",
            "value": 328.3287405185945,
            "unit": "iter/sec",
            "range": "stddev: 0.0004897165786237364",
            "extra": "mean: 3.0457278836464403 msec\nrounds: 318"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-fast]",
            "value": 37.690066330444466,
            "unit": "iter/sec",
            "range": "stddev: 0.00015878609996170564",
            "extra": "mean: 26.532189973681255 msec\nrounds: 38"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-complete_graph-optimized]",
            "value": 29.305867975248976,
            "unit": "iter/sec",
            "range": "stddev: 0.04393761732666364",
            "extra": "mean: 34.12285897297346 msec\nrounds: 37"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-fast]",
            "value": 791.465824988729,
            "unit": "iter/sec",
            "range": "stddev: 0.000011070923627888978",
            "extra": "mean: 1.2634784325832902 msec\nrounds: 712"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-star_graph-optimized]",
            "value": 264.79881115931346,
            "unit": "iter/sec",
            "range": "stddev: 0.00007897376237719483",
            "extra": "mean: 3.7764519999992006 msec\nrounds: 251"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-fast]",
            "value": 563.845980339176,
            "unit": "iter/sec",
            "range": "stddev: 0.00012299499973090193",
            "extra": "mean: 1.7735339700363915 msec\nrounds: 534"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[100-wheel_graph-optimized]",
            "value": 287.1388338576795,
            "unit": "iter/sec",
            "range": "stddev: 0.0004530151237977213",
            "extra": "mean: 3.4826358614232253 msec\nrounds: 267"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-fast]",
            "value": 81.02877877320473,
            "unit": "iter/sec",
            "range": "stddev: 0.0001276463023001787",
            "extra": "mean: 12.341294230768888 msec\nrounds: 78"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-path_graph-optimized]",
            "value": 14.430544049720169,
            "unit": "iter/sec",
            "range": "stddev: 0.012037113024572653",
            "extra": "mean: 69.2974566000089 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-fast]",
            "value": 0.3448039270455218,
            "unit": "iter/sec",
            "range": "stddev: 0.007956184588534728",
            "extra": "mean: 2.9001989871999854 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-complete_graph-optimized]",
            "value": 0.34387010794637457,
            "unit": "iter/sec",
            "range": "stddev: 0.010707242940697467",
            "extra": "mean: 2.908074813400026 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-fast]",
            "value": 30.365537095231797,
            "unit": "iter/sec",
            "range": "stddev: 0.17730652529504973",
            "extra": "mean: 32.93207022368218 msec\nrounds: 76"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-star_graph-optimized]",
            "value": 8.684560404400232,
            "unit": "iter/sec",
            "range": "stddev: 0.0005336906254090481",
            "extra": "mean: 115.14687600000191 msec\nrounds: 9"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-fast]",
            "value": 45.61699867060391,
            "unit": "iter/sec",
            "range": "stddev: 0.03214223421777122",
            "extra": "mean: 21.921652654548947 msec\nrounds: 55"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_with_pre_mapping_optimizer[1000-wheel_graph-optimized]",
            "value": 11.238410317364867,
            "unit": "iter/sec",
            "range": "stddev: 0.014372131420664258",
            "extra": "mean: 88.98055612499434 msec\nrounds: 8"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-fast]",
            "value": 1290.461354764306,
            "unit": "iter/sec",
            "range": "stddev: 0.00009353462415647995",
            "extra": "mean: 774.916657758142 usec\nrounds: 1160"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-10-optimized]",
            "value": 1022.6993429795265,
            "unit": "iter/sec",
            "range": "stddev: 0.000039384105455680397",
            "extra": "mean: 977.8044807251031 usec\nrounds: 882"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-fast]",
            "value": 18.617529516394413,
            "unit": "iter/sec",
            "range": "stddev: 0.00038047108294416825",
            "extra": "mean: 53.71281936840277 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[10-100-optimized]",
            "value": 18.23664066489191,
            "unit": "iter/sec",
            "range": "stddev: 0.00020038988047980442",
            "extra": "mean: 54.83466052632929 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-fast]",
            "value": 528.8474599062675,
            "unit": "iter/sec",
            "range": "stddev: 0.0001294991982745368",
            "extra": "mean: 1.8909044210541146 msec\nrounds: 494"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-10-optimized]",
            "value": 266.7488731382087,
            "unit": "iter/sec",
            "range": "stddev: 0.0005256864265629048",
            "extra": "mean: 3.7488443277579546 msec\nrounds: 299"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-fast]",
            "value": 17.88167136572041,
            "unit": "iter/sec",
            "range": "stddev: 0.00025047042888220024",
            "extra": "mean: 55.92318411113536 msec\nrounds: 18"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_barbell_graph[100-100-optimized]",
            "value": 16.907307613443614,
            "unit": "iter/sec",
            "range": "stddev: 0.0010977734477602722",
            "extra": "mean: 59.146022705878 msec\nrounds: 17"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-fast]",
            "value": 11798.376623957314,
            "unit": "iter/sec",
            "range": "stddev: 0.000011189628376769102",
            "extra": "mean: 84.75742315001538 usec\nrounds: 5797"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-10-optimized]",
            "value": 3963.1449870156034,
            "unit": "iter/sec",
            "range": "stddev: 0.000013409766859661031",
            "extra": "mean: 252.32485898857755 usec\nrounds: 2553"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-fast]",
            "value": 1130.2844068540003,
            "unit": "iter/sec",
            "range": "stddev: 0.00005670433181346081",
            "extra": "mean: 884.7330759727722 usec\nrounds: 1053"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.01-100-optimized]",
            "value": 272.1377493797466,
            "unit": "iter/sec",
            "range": "stddev: 0.0008410493819891572",
            "extra": "mean: 3.6746096499996383 msec\nrounds: 220"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-fast]",
            "value": 6647.770773140364,
            "unit": "iter/sec",
            "range": "stddev: 0.000016123494591010313",
            "extra": "mean: 150.42636608957656 usec\nrounds: 4630"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-10-optimized]",
            "value": 3503.415973094675,
            "unit": "iter/sec",
            "range": "stddev: 0.000023429429681962437",
            "extra": "mean: 285.4357026626985 usec\nrounds: 2704"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-fast]",
            "value": 284.86790718488993,
            "unit": "iter/sec",
            "range": "stddev: 0.0001734265547162072",
            "extra": "mean: 3.510398942029516 msec\nrounds: 276"
          },
          {
            "name": "benchmarks/test_substrate_scheduler_performance.py::TestSubstrateScheduler::test_substrate_scheduler_timing_erdos_renyi[0.1-100-optimized]",
            "value": 208.17127549538975,
            "unit": "iter/sec",
            "range": "stddev: 0.00040974400039429996",
            "extra": "mean: 4.803736719296541 msec\nrounds: 171"
          }
        ]
      }
    ]
  }
}