Feedback For IEEE Presentation:

Comments from first round of feedback:

- Put open source on the opening slide!!
- Acknowledge DARPA on opening slide (logo) UTS, Rigetti, IONQ, UTD
- Citations?? Probably at the end.... Cite Dan Litinski, Simon, Madhav, Darcy, MIT PyLiQTR Team
- Add your algorithms!!
- FIX OUTPUT NOT APPEARING ON SECOND CODE SLIDE!!!!!
- White text might be hard to read??!!

- Trying to figure out how to arrange qubits in your computers (ELU configuration)

- Taking this to heart:
  - Motivation: more precise resource estimates
  - Solution: GSC
  - What can this become: Compilers, Architectures, You get involved too!
    - For hardware providers: Access to well vetted application instances (WE NEED A PHOTONICS ARCHITECTURE MODEL!)
    - For algorithm developers: Access to well vetted hardware instances

- magic state distillation factory! NOT DISTILLATION WIDGET!
- Say `pip install benchq`
- Use iceream for output



Comments from second round of feedback:

ADD INTRODUCTORY CONTEXT! WHY ARE WE DOING THIS???
- People usually just count T gates
- We are compiling the full circuit
- Maybe do the footprint analysis first to compare it to the graph state compilation case.
Be more specific that the people are coming from the DARPA QB program.
- Put DARPA logo on the first slide
Put error budgeting in the slides???
Don't talk so much about the different ways people can contribute
- Just say "we need your help!"
Pre-run the second piece of code
Use detailed ion trap architecture model
Emphasize how modularity facilities collaboration


Final Feedback:
Give the google folks more credit for the assumptions they make and the progress they have made
Talk about how benchq can help contributors
MOAR WHITESPACE!
Tell a story about benchq:
- Footprint analysis is great! (coarse grained, we did it too!)
- IonQ and Rigetti wanted a tool to help design their architectures, but they need a fine-grained tool!
- BenchQ is a tool that can help them do that!
Emphasize that IonQ made this model! You can too!
Decoder people too!
Spend more time let the audience see the ResourceInfo model.



Preparation:
Hide tabs
run first cell
Make sure footprint analysis is first!!
Delete other outputs




people to see:
[x] Nicole
[x] Kevin Obenland
[x] Sitong and Naphann
[x] Rutuja
[ ] Yuval
[ ] Josh Mutus
[ ] Litinski
[ ] Cassandra


Oak Ridge talk: What does it take to make quantum computing reliable?

Resources define performance (You should talk about this! We are doing this!!!)
Sam Jaques:
    Space and time tradeoff! We can do this! (not optimally)
    We do routing too!



Consider adding "total power consumption" to the ResourceInfo object


New node to patch optimizer tools:
Book embedding (1 page)
2 Layer crossing


Ophilia at Riverlane: ophelia.crawford@riverlane.com
