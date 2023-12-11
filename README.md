## Instructions
- Dear all, Please extract [TSSB-Data-3M](https://drive.google.com/file/d/1NRGnKuzia01JCK4G1bDFKWolZOeNtSuU/view?usp=sharing) file to [```./data/```](https://github.com/SahandMoslemi/Collect-Commits/tree/main/data) path.
- Edit ```settings.py```. There are 3 parameters, take the second one and the third one from [Files-to-Process](##Files-to-Process) table. The first one should be your personal github token.
- Install the ```requirements.txt```.
- Then you should be able to run ```main.py```.

- After running for a while the program will create files named ```commits_<n>.json ```. If you had to stop the program, next time you run it, just change the value of the ```NEXT_INDEX_TO_OBSERVE``` variable to ```n+1```. It will continue running from where you left.

## Files-to-Process
| Member | FFI | LFI |
|---|---|---|
| Sahand  | 0 | 4 |
| Elcin  | 5 | 9 |
| Metehan | 10 | 14 |
| Nima | 15 | 19 |
| Huzaifa  | 20 | 24 |
