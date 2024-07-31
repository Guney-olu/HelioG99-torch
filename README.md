# Running and training LLM using tinyops in HelioG99 Chip

**using ADB and Termux to make connection with our TAB with the chip(8-cores)**

````sh
https://github.com/Guney-olu/llama-in-cpp
```

We clocked 14toks/sec (which is pretty slower compared to the bechmarks)

## Running Tinyops 
*SETUP*
```sh
 git clone https://github.com/Guney-olu/tinyOPS.git
 python3 -m pip install tinygrad
 python3 -m LDFLAGS=-llog pip install sentencepiece
 pkg python-numpy
```

**We are able to load models issue is predicting the tokens (Solvable)**
