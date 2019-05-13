
## Compiler Project for CSc 42000 Spring 2019
> Programming language is optional with no restrictions
> Standard Compiler Components:
>  - Lexer (Tokenizer) 
>  - Parser
>  - Semantic Analyzer 
>  - Code Generator (IR, probably going to use LLVM)

## Status:
* Current using Python for implementation
* ~~Libraries being used as a learning tool: rPLY, LLVM/lite~~ Not using rPLY for Lexer and Parser
* ~~rPLY for Lexer & Parser~~
* LLVM for generating machine code [?] Need to read up on LLVM after the other parts 
* Current language input: ~~Unknown because the professor hasn't told us yet. So thats cool. Will assume Pascal as input for now~~ Pascal is the input language.

Features:
- [x] Pascal Program
- [x] Variable 
- [x] Assignments**(Required)** **(Required)**
- [ ] Writeln (done for strings)
- [x] Addition/Subtraction
- [x] Multiplication/Division
- [ ] TypeChecking
- [x] Begin/End
- [x] Symbol Table 
- [ ] If/Else **(Required)**
- [ ] While **(Required)**
- [ ] And **(Required)**
- [x] Procedures (Kind of) **(Required)**
- [x] Declarations **(Required)**
- [ ] Repeat **(Required)**
- [ ] Goto **(Required)**
- [ ] Case **(Required)**
- [x] Tokenizer (Kind of done?)
- [x] Lexer ^
- [x] Parser ^
- [ ] Code Generator/Stack Machine: I have no idea how to approach this atm. Finishing some functions before I move on to this.

  
